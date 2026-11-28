---
title: "Crocodile"
category: ["Crocodile"]
---


- `nmap -Sc` uses predefined script scans
- With `nmap -sC machine_ip` we see port 21 uses vsFTPd 3.0.3 and port 80 has Apache httpd 2.4.41
- Now we try to connect to FTP with `ftp machine_ip` using "anonymous" as username  
- To download files from the FTP server use `get`, and the user with most permissions is "admin"  
- We access as anonymous  
- Using `get` we download the two available files containing usernames and passwords  
- Now we run `gobuster dir -u http://10.129.1.15 -w common1.txt -x .php` where common1.txt should be replaced with a file the command will use as a wordlist, and we'll obtain login.php  
- Now we access the web by entering its IP followed by login.php (10.129-1-15/login.php) and use the previously obtained usernames and passwords 