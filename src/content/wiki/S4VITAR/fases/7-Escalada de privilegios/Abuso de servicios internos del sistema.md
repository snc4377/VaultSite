---
title: "Abuso De Servicios Internos Del Sistema"
category: ["S4VITAR", "fases", "7-Escalada de privilegios", "Abuso de servicios internos del sistema"]
---

**Internal services** are essential components that operate in the background within an operating system, handling critical functions such as network management, printing, software updates, and system monitoring, among others.

However, if these services **are not properly configured** and remain active, they can represent a significant security gap. Attackers could exploit these services to gain unauthorized access to the system and carry out malicious activities.

A concrete example would be a misconfigured network service with elevated permissions. If an attacker manages to identify it and find a way to exploit it, they could use it to escalate privileges and gain administrator access.

In this class, we will analyze an illustrative case of how an attacker could first detect an active service on the system and then exploit it to increase their user privileges.

### Enumerating Timers (Systemd)

The first step is to check if there are any active **Systemd Timers**. These are like cron jobs but managed by systemd. We use the command `systemctl list-timers` or, even better, `watch` to see it in real-time and check how much time remains until execution.

We see there's an **`apt-update.timer`** that runs frequently (in the video, approximately every 30 seconds). This is interesting because if this timer calls the `apt` service to update the system, that process **runs as ROOT**.

### 2. Checking for Write Permissions

If the process runs as root, we can't modify it directly. BUT, if we can **edit the configuration used by that process**, then we've succeeded.

Let's check the permissions of the APT configuration directory at `/etc/apt/apt.conf.d/`.

Bingo! We see we have write permissions (`w`) in that directory as a regular user (or we're part of the group with permissions). This means we can create a new file there.

### 3. The Attack: APT Pre-Invoke

APT has a feature called **`Pre-Invoke`**. Essentially, you tell it: _"Hey, right before you start updating (which you'll do as root), run this command I specify."_

We'll create a malicious file (e.g., `00pwn`) inside that directory with our injection.

The goal: **Set SUID permissions on `/bin/bash`** so we can become root whenever we want.

```
echo 'APT::Update::Pre-Invoke {"chmod u+s /bin/bash";};' > /etc/apt/apt.conf.d/00pwn
```



Now we verify that the file has been created correctly with our malicious payload.

### 4. Wait and Escalate (Pwned)

Now we just have to wait for the **Timer** (which we saw in step 1) to execute again. We can leave a `watch` running on the bash to see when the permissions magically change.

Bash

```
watch -n 1 ls -l /bin/bash
```

When the timer triggers, we'll see the bash prompt change and the **`s`** (SUID) appears in red.

It's done. Since bash has SUID and the owner is root, if we execute it with `-p` (privileged), we maintain the owner's permissions.

Bash

```
bash -p
```