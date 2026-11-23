---
title: "Abuso De Permisos Incorrectamente Implementados"
category: ["S4VITAR", "fases", "7-Escalada de privilegios", "Abuso de permisos incorrectamente implementados"]
---

In Linux systems, files and directories have permissions that control access to them. Permissions are divided into three categories: owner, group, and others. Each category can have read, write, and execute permissions. A file's permissions can be modified by its owner or by the system superuser.

Abuse of incorrectly implemented permissions occurs when a critical file's permissions are misconfigured, allowing an unauthorized user to access or modify the file. This can enable an attacker to read sensitive information, modify important files, execute malicious commands, or even gain superuser access to the system.

Thus, an experienced attacker could exploit this flaw to escalate their privileges in the best-case scenario. One tool designed to perform this reconnaissance on the system is **lse**. Linux Smart Enumeration (LSE) is a security enumeration tool for Linux-based operating systems, designed to help system administrators and security auditors identify and assess vulnerabilities and weaknesses in system configuration.

LSE is designed to be easy to use and provides clear, readable output to facilitate the identification of security issues. The tool uses standard Linux commands and runs in the command line, meaning no additional software is required. Additionally, it enumerates a wide range of system information, including users, groups, services, open ports, scheduled tasks, file permissions, environment variables, and firewall configurations, among others.

- **Linux Smart Enumeration**: [https://github.com/diego-treitos/linux-smart-enumeration](https://github.com/diego-treitos/linux-smart-enumeration)


### 1. Write Abuse in /etc/passwd

We enumerate the system and find that the `/etc/passwd` file has write permissions for "others" (world-writable), which is a massive configuration blunder.  
![Pasted image 20260214130747](/VaultSite/wiki-images/Pasted%20image%2020260214130747.png)  
![Pasted image 20260214130649](/VaultSite/wiki-images/Pasted%20image%2020260214130649.png)  

If we try to read `/etc/shadow` (where the real hashes are stored), it won't let us. But since we can write to `passwd`, we can use a trick. In the `root` line, where there's usually an `x` (meaning "look for the password in shadow"), we can delete that `x` and place our own hashed password directly there.  
![Pasted image 20260214130642](/VaultSite/wiki-images/Pasted%20image%2020260214130642.png)  

First, we generate a hash for a password of our choice (e.g., "hola"):  

Bash

```
openssl passwd "hola"
# Nos devolverá algo tipo: $1$y7...
```
![Pasted image 20260214130705](/VaultSite/wiki-images/Pasted%20image%2020260214130705.png)

Now we edit `/etc/passwd` (with nano or vi), remove the `x` from the root user and paste the hash we just generated:
![Pasted image 20260214130727](/VaultSite/wiki-images/Pasted%20image%2020260214130727.png)
Once saved, the system will read the password from here instead of shadow. We simply run `su root`, enter "hola" and we're in.

---

### 2. Cron Job Abuse (Writable Directory)

Here we see that root is running a cron job every minute. It executes a script located in a directory we own (`/home/savitar`), but the script itself belongs to root, so we can't edit it directly.
![Pasted image 20260214130819](/VaultSite/wiki-images/Pasted%20image%2020260214130819.png)

But note: since the **directory** is ours, even though we can't edit the file, we can **delete it** and create a new one with the same name (Hijacking).

So we wipe out the original script:

Bash

```
rm script_de_root.sh
```

Note title: Untitled

![Pasted image 20260214130831](/VaultSite/wiki-images/Pasted%20image%2020260214130831.png)

And we create a new one with the same name, inserting whatever we want. In this case, we'll make it assign SUID permissions to `/bin/bash` so we can become root whenever we want:

Bash

```
#!/bin/bash
chmod u+s /bin/bash
```
Note title: Untitled

![Pasted image 20260214130849](/VaultSite/wiki-images/Pasted%20image%2020260214130849.png)

Important to give execution permissions so cron doesn't fail when trying to run it:

Bash

```
chmod +x script_de_root.sh
```

Now we start monitoring bash with a `watch` waiting for the minute to pass and root's cron to execute our malicious script:

Bash

```
watch -n 1 ls -l /bin/bash
```

Note title: Untitled

![Pasted image 20260214130901](/VaultSite/wiki-images/Pasted%20image%2020260214130901.png)
![Pasted image 20260214130907](/VaultSite/wiki-images/Pasted%20image%2020260214130907.png)
Once we see that the bash has the `s` (rwsr-xr-x), we're good. All that's left is to run it in privileged mode to become root:


```
bash -p
```



### Extra: Automated Tools

To avoid having to inspect this manually, S4vitar recommends using enumeration scripts. Besides the classic **LinPEAS**, in the video he uses **LSE (Linux Smart Enumeration)**.

We download it to `/tmp` (which is usually always writable):



```
cd /tmp
wget https://raw.githubusercontent.com/diego-treitos/linux-smart-enumeration/master/lse.sh
chmod +x lse.sh
```

Note title: Untitled

And we launch it. If we want to get straight to the point, we use verbosity level 1 to show us interesting things (like whether we can write to `/etc/passwd`):


```
./lse.sh -l1
```


Note title: Untitled

![Pasted image 20260214130928](/VaultSite/wiki-images/Pasted%20image%2020260214130928.png)
![Pasted image 20260214130935](/VaultSite/wiki-images/Pasted%20image%2020260214130935.png)
![Pasted image 20260214130941](/VaultSite/wiki-images/Pasted%20image%2020260214130941.png)


