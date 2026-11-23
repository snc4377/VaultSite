---
title: "Abusando De Privilegios A Nivel De Sudoers"
category: ["S4VITAR", "fases", "7-Escalada de privilegios", "Abusando de privilegios a nivel de Sudoers"]
---


It is worth noting that for a user to have root permissions on a file using `sudo -l`, it must be explicitly configured in the sudoers file. For example, we can have two users with the same permissions, but one can execute nmap with admin privileges while the other cannot.

The **/etc/sudoers** file is a configuration file in Linux systems used to control user access to various actions they can perform on the system. This file contains a list of users and user groups that have permissions to perform administrative tasks on the system.

The **`sudo`** command allows users to execute commands as the superuser or as another user with special privileges. The sudoers file specifies which users can execute which commands with sudo and with what privileges.

Abusing sudoers-level privileges is a technique used by attackers to elevate their access level on a compromised system. If an attacker gains access to an account with sudo permissions in the sudoers file, they can execute commands with special privileges and perform malicious actions on the system.

The **`sudo -l`** command is used to list the sudo permissions of a particular user. When executed, it displays a list of commands the user is permitted to run and under what conditions.

To prevent abuse of sudoers-level privileges, it is recommended to maintain proper permissions in the sudoers file and limit the number of users with sudo permissions. Additionally, it is important to regularly monitor the sudoers file and look for unexpected or suspicious changes in its content.

The GTFOBins resource is used to detect commands that could potentially be exploited to elevate our user privileges:

- **GTFOBins**: [https://gtfobins.github.io/](https://gtfobins.github.io/)

In this example, we have two users: a normal user "s4vitar" and another with root permissions "manolito."

If we attempt to run `sudo -l` with the user s4vitar, we will see that we cannot execute that command on the hostname.  
![Pasted image 20260213171514](/VaultSite/wiki-images/Pasted%20image%2020260213171514.png)

Let's grant root privileges in awk to s4vitar from the root user.  
![Pasted image 20260213171612](/VaultSite/wiki-images/Pasted%20image%2020260213171612.png)

Now, with `sudo -l`, we can see that we can execute [[AWK]] without a password and as root.  
![Pasted image 20260213171835](/VaultSite/wiki-images/Pasted%20image%2020260213171835.png)

If we now go to [https://gtfobins.github.io/](https://gtfobins.github.io/) and search for awk, we will see various one-liners. We will choose the sudo one, which, as we read here, will give us a `/bin/sh` (interactive shell).  
![Pasted image 20260213172523](/VaultSite/wiki-images/Pasted%20image%2020260213172523.png)  
![Pasted image 20260213172617](/VaultSite/wiki-images/Pasted%20image%2020260213172617.png)  

And now we have a shell where we are root and can do whatever we want. 
