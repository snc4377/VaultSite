---
title: "SMB Relay"
category: ["Networking & services configs", "Networking", "HACKING WIFI", "info de herramientas y conceptos", "SMB Relay"]
---

Note title: SMB Relay

https://www.youtube.com/watch?v=Ekw4X_QrHJ0&ab_channel=s4vitar
The **SMB Relay** attack is a technique that exploits vulnerabilities in the SMB (Server Message Block) protocol to intercept and reuse NTLM credentials captured during communication between two machines on a network.

---

#### **Attack Phases:**

1. **Interception with Responder:**
    
    - The **Responder** tool is used without additional configuration to capture NTLM hashes sent by machine "A" (which believes it is communicating with a legitimate resource).
    - This intercepted NTLM hash can be cracked using dictionaries like **rockyou.txt**, revealing the original password.
2. **Authentication with captured credentials:**
    
    - Once the password is cracked, the attacker can use the credentials to connect via services like **RDP**, **SMB**, or others available on the target machine.
3. **Advanced use with pre-configuration:**
    
    - By configuring **Responder** and tools like **NTLMRelay.py** or **MultiRelay.py**, the attacker can perform "Pass-the-Hash" attacks, directly reusing the intercepted hash without needing to crack it.
    - This attack only succeeds if the password belongs to a privileged user on the target machine.
4. **Lateral escalation with Mimikatz:**
    
    - Even if the captured user is not a domain administrator, the attacker can move laterally across the network using tools like **Mimikatz**, accessing different machines until obtaining domain administrator credentials.

---

#### **Limitations and requirements:**

- **SMB signing disabled:**  
    This attack only works on networks where **SMB signing** is not enabled, as this signing protects the integrity of transmitted data.
    
- **Vulnerable protocols:**  
    Name resolution protocols like **LLMNR** (Link-Local Multicast Name Resolution) and **NBNS** (NetBIOS Name Service) are critical for facilitating the attack, as they can be manipulated to redirect traffic to the attacker.
    

---

#### **Attack impact:**

- Enables the capture and reuse of credentials without physical access.
- Facilitates lateral movement within the network to compromise additional systems.
- Can result in total domain control if privileged credentials are obtained.

---

#### **Protection measures:**

1. **Enable SMB signing:**  
    Configure servers and workstations to require SMB signing for all communications.
    
2. **Disable LLMNR and NBNS:**  
    Reduce the attack surface by disabling these protocols in network settings.
    
3. **Implement more secure authentication:**  
    Adopt **Kerberos** as the primary authentication protocol instead of NTLM.
    
4. **Monitoring and auditing:**  
    Detect unusual behavior, such as attempts to capture or relay credentials.