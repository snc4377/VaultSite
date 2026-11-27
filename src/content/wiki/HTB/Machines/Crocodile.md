---
title: "Crocodile"
category: ["HTB", "Machines", "Crocodile"]
---

# Crocodile

- `nmap -Sc` uses predefined script scans
- With `nmap -sC ip_machine`, we see that port 21 uses vsFTPd 3.0.3 and port 80 has Apache httpd 2.4.41
- Now we try to connect to the FTP server using `ftp ip_machine` and enter "anonymous" as the username
- To download files from the FTP server, use `get`, and the user with the most permissions is "admin"
- We log in as "anonymous"
- Using `get`, we download the two files containing usernames and passwords
- Now we run `gobuster dir -u http://10.129.1.15 -w common1.txt -x .php`, where `common1.txt` must be replaced with a file the command will use as a wordlist, and we obtain `login.php`
- Now we access the web page using its IP and append `/login.php` (e.g., `10.129.1.15/login.php`), and we use the previously provided usernames and passwords 