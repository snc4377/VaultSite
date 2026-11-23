---
title: "Resume"
category: ["PREP_CPTS", "Pen-testing", "AD ENUM & ATTACK", "4.9 DCSync", "Resume"]
---

# DCSync and Golden Tickets

## 🔑 Core Idea

> [!important] In one sentence: DCSync lets you impersonate a Domain Controller so another DC "replicates" its secrets to you. If among those secrets you obtain the `krbtgt` hash, you can forge **Golden Tickets**: completely fake yet valid Kerberos identities.

---

## 1. What is DCSync?

- It's not "dumping a stored file", it's **abusing the replication protocol between DCs** (MS-DRSR).
- Active Directory has multiple Domain Controllers that constantly synchronize with each other.
- DCSync = impersonating another DC by requesting "replicate your data to me" from a real DC.
- From the network, it looks like legitimate replication traffic → **very stealthy**, doesn't touch LSASS or NTDS.dit directly.

### Required Permissions

Not a normal account permission, but two _extended rights_ on the **domain** object (not a user):

- `Replicating Directory Changes`
- `Replicating Directory Changes All`

> [!note] By default, only Domain Admins, Enterprise Admins, and replication service accounts have these. Groups like `Exchange Windows Permissions` may gain them by abusing their DACL write capabilities.

### What Do You Get?

- NTLM hashes of any user or computer
- Kerberos keys (AES, etc.)
- Password history
- **The `krbtgt` account hash** ← the most valuable piece

### Tools

- `secretsdump.py` (Impacket) with DCSync option
- Mimikatz → `lsadump::dcsync`

### 🧪 Practical Example: Identify and Dump the `krbtgt` Hash

**Step 1 — Confirm You Have Replication Rights**

Using PowerView, check if your user (or a group you belong to) has the necessary extended rights on the domain object:


```powershell
PS C:\htb> Get-ObjectAcl -DistinguishedName "DC=inlanefreight,DC=local" -ResolveGUIDs |
  Where-Object {$_.ObjectType -match "Replicating Directory Changes"}
```

If your user has `ExtendedRight` over `DS-Replication-Get-Changes` and `DS-Replication-Get-Changes-All`, you can already perform DCSync.

**Step 2 — Execute DCSync targeting only `krbtgt`**

With `secretsdump.py` from Impacket, you can request a single object instead of dumping the entire NTDS (faster and more stealthy):

```bash
```

```bash
secretsdump.py -just-dc-user krbtgt INLANEFREIGHT.LOCAL/forend:Klmcargo2@172.16.5.5
```

Expected output (summarized):

```
[*] Using the DRSUAPI method to get NTDS.DIT secrets
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:1693c6cefffc62f23736af9bb...:::
```

Note title: Untitled

What comes after the colon (`1693c6ce...`) is the **NTLM hash of `krbtgt`**, the "secret ink" mentioned above.

With Mimikatz, the equivalent (executed from a host with a valid session and appropriate privileges) would be:

```
mimikatz # lsadump::dcsync /domain:inlanefreight.local /user:krbtgt
```

**Step 3 — Using It to Forge the Golden Ticket**

With the hash in hand, Mimikatz can generate the forged ticket by specifying the domain, SID, and the user you want to impersonate:

```
mimikatz # kerberos::golden /user:fakeadmin /domain:inlanefreight.local /sid:S-1-5-21-... /krbtgt:1693c6cefffc62f23736af9bb... /id:500 /ptt
```

`/ptt` injects the ticket directly into the current session, ready to use.

> [!note] Why `-just-dc-user`  
> Requesting only the `krbtgt` account instead of dumping the entire NTDS generates much less traffic and fewer audit events than a full DCSync, making it harder to detect.

---

## 2. What is the `krbtgt` account?

- Special account, **one per domain**, created automatically.
- No one logs in with it; it's not for humans.
- Its only function: **signing and encrypting Kerberos tickets**.

> [!tip] Festival wristband analogy  
> 
> - You authenticate → you get a wristband (TGT) that proves who you are  
> - You show the wristband at each "VIP area" without repeating your ID  
> - `krbtgt` is the machine that **manufactures and seals** those wristbands  
> - Its hash = the **secret ink** of the official seal  

---

## 3. What is a Golden Ticket?

- A **forged TGT** created by the attacker, sealed with the stolen `krbtgt` hash via DCSync.
- Since you have the secret ink, you can write whatever you want on the wristband:
    - "This user is Domain Admin" (even if they're not)  
    - Invent a user that doesn't even exist  
    - The system accepts it because the seal is valid  

### Why is it worse than stealing a normal hash?

|Stealing a normal user hash|Golden Ticket|
|---|---|
|Limited to their real permissions|Permissions you decide|
|If their password is reset, you lose access|Still works as long as `krbtgt` isn't rotated|
|Impersonating a specific person|Forging the system's own trust|
|Normal expiration|You can create tickets valid for up to 10 years|

---

## 4. Why it's so hard to remediate

> [!warning] Changing a password isn't enough  
> 
> - AD stores the **current and previous** `krbtgt` password for compatibility → it must be rotated **twice**  
> - Must wait for **full replication** to all DCs, otherwise it remains vulnerable  
> - Meanwhile, the attacker can keep generating valid tickets  
> - In many cases, you must assume **the entire domain's trust** is compromised  

---

## 5. Attack chain summarized

```
Conseguir cuenta con derechos de replicación (DCSync)
        ↓
Volcar hash de krbtgt (y otros)
        ↓
Forjar Golden Ticket (Mimikatz / Impacket)
        ↓
Autenticarse como cualquier identidad, con cualquier permiso
        ↓
Persistencia casi total sobre el dominio
```

Note title: Untitled

---

## 🔗 Related

- [[Exchange Windows Permissions]]
- [[PrivExchange]]
- [[Printer Bug]]
- [[ASREPRoasting]]
- [[GPO Abuse]]
