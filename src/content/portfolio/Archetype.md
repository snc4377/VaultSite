---
title: "Archetype"
category: ["Archetype"]
---


SMB MACHINE  
- Run `nmap -sC -sV ip`  
- To view devices on the SMB server, use `smbclient -L 10.129.6.125 -U root` which shows shared resources on the Samba server (`-L`) using the root user (`-U`)  
- Run `smbmap -H 10.129.6.125 -u ' ' -p ' '` to scan and display user permissions  
- ![Pasted image 20240306163810](/VaultSite/wiki-images/Pasted%20image%2020240306163810.png)  
- Execute `smbclient //10.129.6.125/backups` to access the backups user on the server, then `ls` to view files and `get` to download desired files  
- ![Pasted image 20240306164125](/VaultSite/wiki-images/Pasted%20image%2020240306164125.png)  
- Open with `cat`  
- ![Pasted image 20240306164216](/VaultSite/wiki-images/Pasted%20image%2020240306164216.png)  
- Search for a T-SQL shell and locate `xp_cmdshell` (a SQL Server procedure allowing system command execution from T-SQL)  
- Execute this command line using the python3-impacket package  
- ![Pasted image 20240306165743](/VaultSite/wiki-images/Pasted%20image%2020240306165743.png)  
- ![Pasted image 20240306165830](/VaultSite/wiki-images/Pasted%20image%2020240306165830.png)  
- Run `Invoke-PowerShellTcpOneLine.ps1` from a GitHub repository (establishes a TCP connection and executes a reverse shell)  
- ![Pasted image 20240306172517](/VaultSite/wiki-images/Pasted%20image%2020240306172517.png)  
- Execute `chmod +x`  
- Then `cat`  
- ![Pasted image 20240306172703](/VaultSite/wiki-images/Pasted%20image%2020240306172703.png)  
- Set up a new Python server in another tab while `nc` runs in a separate window  
- ![Pasted image 20240306174035](/VaultSite/wiki-images/Pasted%20image%2020240306174035.png)  
- ![Pasted image 20240306174044](/VaultSite/wiki-images/Pasted%20image%2020240306174044.png)  
- Verify that ufw is enabled and allows traffic  
- ![Pasted image 20240306174144](/VaultSite/wiki-images/Pasted%20image%2020240306174144.png) 