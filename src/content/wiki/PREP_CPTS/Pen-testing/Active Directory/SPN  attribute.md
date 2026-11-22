**Key Concept:** The Kerberoasting attack exploits legitimate Active Directory features to obtain service account passwords without raising suspicion.

### 1. What is an SPN (Service Principal Name)?

- It is a "unique identifier" that links a service (e.g., SQL, Backup, Web) with the **user account** responsible for running it.
    
- It is assigned **manually and statically** by an administrator (not temporary).
    
- Regular users who only _consume_ the service (e.g., reading a table) do **not** have an SPN.
    

### 2. Normal Accounts vs. Service Accounts

At the system level, both are "User" objects, but they are managed very differently:

- **Normal User ("Pepito"):** Changes passwords regularly, locks after multiple failed attempts (Account Lockout), usually has fewer privileges.
    
- **Service User ("sqldev"):** Has an SPN assigned. Its password is often set to **never expire** (to prevent service downtime). Administrators frequently grant them **excessive privileges** for convenience.
    

### 3. Why Do We Look for Accounts with SPNs? (The Appeal)

We search for the SPN attribute because it is the gateway to an **offline** attack. If we try to guess "Pepito's" password by sending attempts to the server (Online), we generate noise and lock the account. If we attack an account with an SPN, the server willingly provides the information we need.

### 4. The Attack: Kerberoasting (Step by Step)

1. **Reconnaissance:** An attacker with any valid domain user (even with minimal privileges) searches for accounts with the SPN attribute configured (e.g., using `Get-DomainUser -SPN`).
    
2. **Ticket Request:** The attacker pretends to be a normal user and requests a Kerberos access ticket (TGS) to connect to that service. Kerberos delivers the ticket without issue.
    
3. **The Design Flaw:** That ticket is encrypted with a derivative of the **service account password** (`sqldev`).
    
4. **Extraction and Cracking (Offline):** The attacker saves the ticket, disconnects from the victim's network, and takes it to their local machine. This is where brute force comes into play: leveraging powerful hardware, like an RTX 5060 Ti, they can use Hashcat or John the Ripper to test millions of passwords per second against that ticket, completely undetected by the domain's defenses.
    

**Conclusion:** Once the hash is cracked offline, you obtain the plaintext password of the `sqldev` account, which likely has high privileges and allows lateral movement or privilege escalation within the network.