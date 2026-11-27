---
title: "Codify"
category: ["HTB", "Machines", "Codify"]
---

# Codify

- We perform an nmap scan of the virtual machine's IP (`nmap -sT ip_maquina`). For more detailed port information, we use the command (`nmap -sC -sV -v -oN nmap.log 10.10.11.239`)
![Pasted image 20240226181303](/VaultSite/wiki-images/Pasted%20image%2020240226181303.png)
- We add the domain name codify.htb with its IP to the /etc/hosts file using the nano command
- Access the page through a browser
![Pasted image 20240226180924](/VaultSite/wiki-images/Pasted%20image%2020240226180924.png)
- We can see there are 4 pages: one explaining what it is, a test page, a limitations page, and the important one - an about us page
- This gives us information like their use of the vm2 library which has vulnerabilities. After some research, we find an issue related to this library (https://github.com/advisories/GHSA-ch3r-j5x3-6q2m)
- We found this exploit code on GitHub but first we'll make some modifications, like changing the execSync section to include a `cat /etc/passwd`
![Pasted image 20240328180139](/VaultSite/wiki-images/Pasted%20image%2020240328180139.png)
- Now we modify the JavaScript code and replace the cat command with a reverse shell
![Pasted image 20240328181255](/VaultSite/wiki-images/Pasted%20image%2020240328181255.png)
- We open port 9001 with netcat to monitor traffic and connect
![Pasted image 20240328181236](/VaultSite/wiki-images/Pasted%20image%2020240328181236.png)
- We do a `cd /var/www/contact` and `ls` to see what's there
![Pasted image 20240328181603](/VaultSite/wiki-images/Pasted%20image%2020240328181603.png)
- We examine each file one by one and find an interesting database file called tickets.db
![Pasted image 20240328181723](/VaultSite/wiki-images/Pasted%20image%2020240328181723.png)
- Well well, we have user Joshua's hash here. Perfect, let's exit but first copy it
- We echo the hash
![Pasted image 20240328181903](/VaultSite/wiki-images/Pasted%20image%2020240328181903.png)
- Then use John with our password list and the hash file
![Pasted image 20240328182317](/VaultSite/wiki-images/Pasted%20image%2020240328182317.png)
- Now we have the user's password
![Pasted image 20240328182402](/VaultSite/wiki-images/Pasted%20image%2020240328182402.png)
- We log in via SSH: `ssh joshua@codify.htb`
![Pasted image 20240328182735](/VaultSite/wiki-images/Pasted%20image%2020240328182735.png)
- Privilege escalation
- First we run `sudo -l` to see available commands
![Pasted image 20240328183848](/VaultSite/wiki-images/Pasted%20image%2020240328183848.png)
- We `cat` the specified path and see the password comparison method - if the string after `==` isn't in quotes, bash uses pattern matching instead of treating it as a string. So if we use the wildcard "*", it will confirm the password
![Pasted image 20240328184107](/VaultSite/wiki-images/Pasted%20image%2020240328184107.png)
- Now we create a Python script for brute forcing, change permissions with chmod, and execute it
![Pasted image 20240328184216](/VaultSite/wiki-images/Pasted%20image%2020240328184216.png)
![Pasted image 20240328184526](/VaultSite/wiki-images/Pasted%20image%2020240328184526.png)
![Pasted image 20240328184659](/VaultSite/wiki-images/Pasted%20image%2020240328184659.png)
