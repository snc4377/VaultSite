---
title: "Fawn"
category: ["fawn"]
---

Note title: Fawn

We run `nmap -sC -sV -v -oN nmap.log ip_machine` to check the FTP version  
![Pasted image 20240226202156](/VaultSite/wiki-images/Pasted%20image%2020240226202156.png)  
We also get the OS  
![Pasted image 20240226202306](/VaultSite/wiki-images/Pasted%20image%2020240226202306.png)  
We use `ftp -h` to get command information  
We connect using `ftp ip_machine`  
We enter the username `anonymous` with password `anonymous` (used in FTP when we don't have an account to log in) (if we accidentally exit FTP, just type `open` and the IP to reconnect, and `close` to exit properly)  
With `get flag.txt` we obtain the flag and it downloads to our machine (just do a normal `cat` and we have the flag)
