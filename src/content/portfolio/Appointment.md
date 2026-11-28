---
title: "Appointment"
category: ["Appointment"]
---

Note title: Appointment

- The most common SQL vulnerability is SQL injection  
- `nmap -sV -T4 -Pn 10.129.12.149` (-sV: provides version information for services on scanned ports) (-T4 is scan speed - higher numbers are faster but more detectable) (-Pn tells nmap to assume the host is online and skip host detection)  
- We search for the IP in a web browser and find a page  
- Then we need to look for login credentials on this page https://pentestlab.blog/2012/12/24/sql-injection-authentication-bypass-cheat-sheet/ for example  
- We tried with username `admin'#` and password `admin` and obtained the flag  
![Pasted image 20240227213248](/VaultSite/wiki-images/Pasted%20image%2020240227213248.png)  
![Pasted image 20240227213159](/VaultSite/wiki-images/Pasted%20image%2020240227213159.png)