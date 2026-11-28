---
title: "Codify"
category: ["Codify"]
---


- We perform an nmap scan of the virtual machine's IP (`nmap -sT ip_maquina`). For more detailed information about the ports, we use the command (`nmap -sC -sV -v -oN nmap.log 10.10.11.239`).
![Pasted image 20240226181303](/VaultSite/wiki-images/Pasted%20image%2020240226181303.png)
- We add the domain name `codify.htb` with its IP to the `/etc/hosts` file using the `nano` command.
- We access the page via a browser.
![Pasted image 20240226180924](/VaultSite/wiki-images/Pasted%20image%2020240226180924.png)
- We can see there are 4 pages: one explaining what it is, a testing page, a limitations page, and the important one, an "About Us" page.
- This page provides information such as the use of the `vm2` library, which has vulnerabilities. We search a bit and find an issue related to this library (https://github.com/advisories/GHSA-ch3r-j5x3-6q2m).
- We find this code on GitHub to create the exploit, but first, we make some modifications, such as changing the `execSync` section to include `cat /etc/passwd`.
![Pasted image 20240328180139](/VaultSite/wiki-images/Pasted%20image%2020240328180139.png)
- Now we modify the Java code and insert a reverse shell where we placed the `cat` command.
![Pasted image 20240328181255](/VaultSite/wiki-images/Pasted%20image%2020240328181255.png)
- We open port 9001 with netcat to monitor the traffic and connect.
![Pasted image 20240328181236](/VaultSite/wiki-images/Pasted%20image%2020240328181236.png)
- We navigate to `/var/www/contact` and run `ls` to see what's there.
![Pasted image 20240328181603](/VaultSite/wiki-images/Pasted%20image%2020240328181603.png)
- We examine each file one by one and find a very interesting database file named `tickets`.
![Pasted image 20240328181723](/VaultSite/wiki-images/Pasted%20image%2020240328181723.png)
- Well, well, what do we have here? The hash for the user `joshua`. Perfect, we exit but first copy it.
- We use `echo` with the hash.
![Pasted image 20240328181903](/VaultSite/wiki-images/Pasted%20image%2020240328181903.png)
- And with `john`, we use it (we specify the path to our password list and the file containing the hash).
![Pasted image 20240328182317](/VaultSite/wiki-images/Pasted%20image%2020240328182317.png)
- Now we have the user's password.
![Pasted image 20240328182402](/VaultSite/wiki-images/Pasted%20image%2020240328182402.png)
- We log in via SSH with `ssh joshua@codify.htb`.
![Pasted image 20240328182735](/VaultSite/wiki-images/Pasted%20image%2020240328182735.png)
- Privilege escalation
- We start by running `sudo -l` to see what we can do.
![Pasted image 20240328183848](/VaultSite/wiki-images/Pasted%20image%2020240328183848.png)
- We use `cat` on the specified path and observe the method used for passwords, which compares them. If the part after `==` is not enclosed in quotes, Bash uses pattern matching instead of treating it as a string. Therefore, if we use the wildcard `*`, it will confirm the password.
![Pasted image 20240328184107](/VaultSite/wiki-images/Pasted%20image%2020240328184107.png)
- Now we create a Python script to perform a brute force attack, change its permissions with `chmod`, and execute it.
![Pasted image 20240328184216](/VaultSite/wiki-images/Pasted%20image%2020240328184216.png)
![Pasted image 20240328184526](/VaultSite/wiki-images/Pasted%20image%2020240328184526.png)
![Pasted image 20240328184659](/VaultSite/wiki-images/Pasted%20image%2020240328184659.png)
