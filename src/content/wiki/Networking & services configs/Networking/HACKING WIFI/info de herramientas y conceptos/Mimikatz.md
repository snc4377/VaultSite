---
title: "Mimikatz"
category: ["Networking & services configs", "Networking", "HACKING WIFI", "info de herramientas y conceptos", "Mimikatz"]
---

# Mimikatz

It is an open-source tool used to extract credentials on Windows systems.

### Main functionalities of Mimikatz:

1. **Password extraction**: It can obtain plaintext passwords and password hashes from memory.
2. **Kerberos ticket retrieval**: Allows capturing and exporting Kerberos service tickets (TGT) for **Pass-the-Ticket** attacks.
3. **Credential injection**: It can inject credentials into the memory of other processes, facilitating lateral movement in a compromised network.
4. **Pass-the-Hash (PtH) attacks**: Uses password hashes instead of plaintext passwords to authenticate a user on other systems in the network.
5. **Decryption of stored passwords**: It can decrypt passwords found in Windows log files.

## Example
If we manage to dump the SAM of a Windows machine in an Active Directory environment, the hashes we obtain are from the local accounts of that machine. 