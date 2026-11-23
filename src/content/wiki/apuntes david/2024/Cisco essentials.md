---
title: "Cisco Essentials"
category: ["apuntes david", "2024", "Cisco essentials"]
---

![Pasted image 20240710162024](/VaultSite/wiki-images/Pasted%20image%2020240710162024.png)
- **Confidentiality** is a set of rules that prevents sensitive information from being disclosed to unauthorized individuals, resources, and processes. Methods used to ensure confidentiality include **data encryption**, **authentication**, and **access control**.
  
- Integrity ensures that system information or processes are protected against intentional or accidental modifications. One way to ensure integrity is by using a **hash function** or **checksum**.
  
- **Availability** means that authorized users can access systems and data when and where needed, while those who do not meet the established conditions cannot. This can be achieved **by maintaining equipment**, **performing hardware repairs**, **keeping operating systems and software updated, and creating backups**.

![Pasted image 20240710162110](/VaultSite/wiki-images/Pasted%20image%2020240710162110.png)
- Processing refers to data used to perform an operation, such as updating a database record (data in process).
  
- Storage refers to data stored in memory or on a permanent storage device, such as a hard drive, solid-state drive, or USB drive (data at rest).
  
- Transmission refers to data traveling between information systems (data in transit).

![Pasted image 20240710162123](/VaultSite/wiki-images/Pasted%20image%2020240710162123.png)
- **Awareness**, training, and education are measures implemented by an organization to ensure users are informed about potential security threats and actions they can take to protect information systems.
  
- **Technology** refers to software (and hardware) solutions designed to protect information systems, such as firewalls, which continuously monitor the network for potential malicious incidents.
  
- **Policy and procedures** refer to administrative controls that provide a foundation for how an organization implements information assurance, such as incident response plans and best practice guidelines.

---

### Types of Malware

- **Spyware**: Monitors your online activity.
- **Adware**: Automatically delivers ads to the user.
- **Backdoor**: Gains unauthorized access by bypassing authentication procedures to access a system.
- **Ransomware**: Holds a system or its data hostage.
- **Scareware**: Pop-ups claiming your system is at risk and urging you to run a program.
- **Rootkit**: Modifies the operating system to create a backdoor, allowing attackers remote access to your computer.
- **Virus**: When executed, it replicates and attaches to other executable files, such as documents, inserting its own code.
- **Trojan**: Exploits user privileges and is most commonly found in image files, audio files, or games.
- **Worm**: A type of malware that self-replicates to spread from one computer to another. Unlike a virus, which requires a host program to run, worms can execute independently.

---

### Social Engineering

Common types:
- **Pretexting**: Deceiving someone by pretending to be someone else.
- **Tailgating**: Quickly following an authorized person into a secure area.
- **Quid pro quo**: The hacker offers something in exchange for information.

---

### Meltdown and Spectre

Google security researchers discovered Meltdown and Spectre, two hardware vulnerabilities affecting nearly all central processing units (CPUs) released since 1995, including desktops, laptops, servers, smartphones, smart devices, and cloud services.

Most software security vulnerabilities fall into several main categories.

**Select the headings to find out what they are.**

---

### Buffer Overflow

Buffers are memory areas allocated to an application. A vulnerability occurs when data is written beyond a buffer's boundaries. By altering data beyond these boundaries, the application can access memory allocated to other processes. This can crash the system, compromise data, or escalate privileges.

![](https://skillsforall.com/content/i2cs/7.1/courses/content/m2/es-XL/assets/e3a11f600245ed0107323cc592db6b78a32fd24b.png)

---

### Unvalidated Input

Programs often require data input, but this input can contain malicious content designed to force the program to behave undesirably.

For example, consider a program that receives an image for processing. A malicious user could create an image file with invalid dimensions. These malicious dimensions could force the program to allocate buffers of incorrect and unforeseen sizes.

![](https://skillsforall.com/content/i2cs/7.1/courses/content/m2/es-XL/assets/f73c8e938c60bc30ef44706253c7ce4e22d6bb63.png)

---

### Race Conditions

This vulnerability describes a situation where the output of an event depends on ordered or timed outputs. A race condition becomes a vulnerability source when the required ordered or timed events do not occur in the correct order or at the right time.

![](https://skillsforall.com/content/i2cs/7.1/courses/content/m2/es-XL/assets/f09be8c7887ba369fe1e2c8d630a5048b1943e7a.png)

---

### Weak Security Practices

Systems and sensitive data can be protected using techniques like authentication, authorization, and encryption. Developers should adhere to using pre-existing, tested, and verified security techniques and libraries rather than attempting to create their own security algorithms. Doing so would likely introduce new vulnerabilities.

![](https://skillsforall.com/content/i2cs/7.1/courses/content/m2/es-XL/assets/c3d396dc995e72bf0cbea4b36f0208f3ea344292.png)

Your computing devices are the gateway to your online life, storing much of your personal data. Therefore, it's important to protect your devices' security.

**Select the headings for some important tips on how to do this.**

---

### Turn on the Firewall

You should use at least one type of firewall (either a software firewall or a hardware firewall on a router) to protect your device from unauthorized access. The firewall should be enabled and constantly updated to prevent hackers from accessing your personal or organizational data.

You can click [here](http://windows.microsoft.com/es-us/windows-10/turn-windows-firewall-on-or-off) to learn how to enable the firewall in Windows 10, or click [here](https://support.apple.com/es-us/HT201642) for Mac OS X devices.

---

### Install Antivirus and Anti-Spyware

Malicious software, such as viruses and spyware, is designed to gain unauthorized access to your device and data. Once installed, viruses can destroy data and slow down your device. They can even take over your computer and send unwanted emails from your account. Spyware can monitor your online activities, collect your personal information, or send unwanted pop-up ads to your web browser while you're online.

To prevent this, only download software from trusted websites. However, you should always use antivirus software to provide an additional layer of protection. This software, which usually includes anti-spyware, is designed to scan your computer and incoming emails for viruses and remove them. Keeping your software updated will protect your computer from recent malicious software.

---

### Manage Your Operating System or Web Browser

Hackers always try to exploit vulnerabilities that may exist in your operating system (such as Microsoft Windows or macOS) or web browser (such as Google Chrome or Apple Safari).

To protect your computer and data, set the security configuration on your computer or browser to a medium or high level. You should also update your computer's operating system, including web browsers, and regularly download and install software patches and security updates from vendors.

---

### Configure Password Protection

Have you ever needed to delete data or dispose of a hard drive? If so, did you take any precautions to protect the data and prevent it from falling into the wrong hands?

**Select the images to learn how to ensure your files are securely and permanently deleted.**

![](https://skillsforall.com/content/i2cs/7.1/courses/content/m3/es-XL/assets/0e266094040623560797646401c6900628013e39.png)touch_app

To erase data so it cannot be recovered, the data must be overwritten with ones and zeros multiple times using tools specifically designed for this purpose. Microsoft's SDelete program (for Vista and later) claims to completely remove confidential files. Shred for Linux and Secure Empty Trash for Mac OS X offer similar functionality.

Or physically destroy the disk.

**The Cloud**

When we talk about the cloud, we generally refer to three elements: data centers, cloud computing, and virtualization. Data centers are typically large facilities that provide massive amounts of power, cooling, and bandwidth. Only very large companies can afford their own data centers. Most smaller organizations lease services from a cloud provider.  
Cloud services include the following:

- SaaS - Software as a Service
- PaaS - Platform as a Service
- IaaS - Infrastructure as a Service  
    There are four main cloud models, as shown in the figure:
- Public Clouds - Cloud-based applications and services offered in a public cloud are available to the general public.
- Private Clouds - Applications and services offered in a private cloud are intended for a specific organization or entity, such as a government.
- Hybrid Clouds - A hybrid cloud consists of two or more clouds, where each remains a separate entity but is connected via a single architecture.
- Community Clouds - A community cloud is created for the exclusive use of a specific community. The differences between public and community clouds are the functional needs customized for the community.

Virtualization is the foundation of cloud computing. Without this foundation, large-scale cloud computing would not be possible. Virtualization means creating a virtual version instead of a physical version of something, such as a computer. An example would be running a "Linux computer" on your Windows PC.

**MAC Addressing**  
(A MAC address is also known as a hardware address, Ethernet address, or Burned-In Address (BIA).)

With `ipconfig /all`, we can see the MAC addresses, which are divided into two parts:  
The first bytes (e.g., 00-13-25) indicate the manufacturer of the network interface.  
The next three bytes are the network interface ID.  
To identify the manufacturer, you can use:  
https://www.wireshark.org/tools/oui-lookup.html

**Ethernet Frame**

When you send data over Ethernet (how many computers communicate on a network), that data is placed in a "packet" called an **Ethernet frame**. This packet has several parts or "fields," like sections of an envelope with important information to ensure the message reaches its destination correctly.

### Key Parts of an Ethernet Frame:

1. **Preamble and SFD (8 bytes):**  
   - Acts like a bell or alert, telling the destination computer that a packet is about to arrive. It doesn't count toward the packet size.
2. **Destination MAC Address (6 bytes):**  
   - The unique address of the computer you're sending the packet to. Like writing the recipient's name and address on an envelope.
3. **Source MAC Address (6 bytes):**  
   - Your unique address. Tells the recipient who sent the packet, like writing your return address on an envelope.
4. **Type/Length (2 bytes):**  
   - Indicates the type of data inside the packet or how much data there is. Like labeling an envelope as a bill, personal letter, etc.
5. **Data (46-1500 bytes):**  
   - Contains the actual data being sent, like the message inside the letter. It can be small or large, but not too large. If the packet is too small, padding bits are added to meet the minimum.
6. **FCS (4 bytes):**  
   - Acts like a security seal to check if the data arrived intact or was damaged in transit.

### Frame Size:

- **Minimum size:** 64 bytes (the smallest the packet can be).  
- **Maximum size:** 1518 bytes (the largest the packet can be without causing issues).  

If a frame is **smaller than 64 bytes**, it's considered defective (like a torn letter) and is discarded.  
If it's **larger than 1518 bytes** (excluding the preamble), it's also discarded because it's too big for most standard networks.

The MAC sublayer is responsible for data encapsulation and media access.

**Data Encapsulation**

IEEE 802.3 data encapsulation includes:

- **Ethernet Frame** – The internal structure of the Ethernet frame.  
- **Ethernet Addressing** – The Ethernet frame includes source and destination MAC addresses to deliver the frame from one Ethernet NIC to another on the same LAN.  
- **Ethernet Error Detection** – The Ethernet frame includes a Frame Check Sequence (FCS) trailer for error detection.

- **CSMA/CD:** Used in traditional wired Ethernet networks, especially with hubs or half-duplex connections.  
- **CSMA/CA:** Used in wireless (Wi-Fi) networks.  

To enable point-to-point communication across the network, network layer protocols perform four main tasks:

1. **End-Device Addressing:** Each device on the network is assigned a unique IP address for identification.  
2. **Encapsulation:** The network layer wraps transport layer data in a packet, adding information like source and destination IP addresses.  
3. **Routing:** Routers direct packets through the network to the destination device, choosing the best path. Packets may pass through multiple routers (hops) before reaching the destination.  
4. **Decapsulation:** When the packet arrives at the destination device, the IP address is verified. If it matches, the IP header is removed, and the data is passed to the transport layer for processing.

**IPv4**  
The header of an IPv4 packet is like a shipping label for data traveling across the network. Here are the key fields in simple terms:

1. **Version:** Indicates this is an IPv4 packet.  
2. **Differentiated Services (DS):** Defines the packet's priority and how it should be handled on the network.  
3. **Time to Live (TTL):** Prevents the packet from traveling forever. Each time it passes through a router, this number decreases. If it reaches 0, the packet is discarded.  
4. **Protocol:** Indicates the type of data the packet carries (e.g., TCP or UDP).  
5. **Header Checksum:** Ensures the packet header isn't corrupted.  
6. **Source IP Address:** Shows where the packet came from.  
7. **Destination IP Address:** Shows where the packet is going.  

The source and destination address fields are the most important because they indicate the starting point and final destination. Other fields help identify and reorder the packet if it fragments during transit.

**ARP Poisoning**  

In some cases, using ARP can lead to a potential security risk. An attacker can use ARP spoofing to perform an ARP poisoning attack. This is a technique where an attacker responds to an ARP request for an IPv4 address belonging to another device, such as the default gateway, as shown in the illustration. The attacker sends an ARP reply with their own MAC address. The receiver of the ARP reply adds the incorrect MAC address to the ARP table and sends these packets to the attacker.  
Enterprise-level switches include mitigation techniques known as "Dynamic ARP Inspection (DAI)."  
The **show ip arp** command is used on Cisco routers to view the ARP table.

### **3.3.2 TCP Services**

- **Reliable Delivery:** Uses ACKs and retransmissions to ensure reception. Protocols that use this: HTTP, TLS, FTP, DNS.  
- **Flow Control:** Allows multiple ACKs to manage congestion.  
- **Stateful Communication:** _Three-way handshake_ (SYN → SYN-ACK → ACK) before data transfer.

---

### **3.3.3 TCP Attacks**

- **SYN Flood**: Sends many SYN packets with spoofed IPs → half-open connections → denial of service.
    
- **TCP Reset (RST)**: Sends a fake RST packet → abruptly terminates connection.
    
- **Session Hijacking**: IP spoofing + sequence prediction + ACK → session control (send-only, no reception).





## 🧠 **Summary: What is an ACL?**

### 📌 **Definition**

- **ACL (Access Control List):**  
    A set of rules that tell the router whether to **allow or block** packets, based on the **packet header information** (e.g., IP address, protocol, port).
    

### ⚙️ **Operation**

- By default, a router **has no ACLs**.
    
- When an ACL is configured on an interface, the router **analyzes every packet** passing through that interface.
    
- For each packet, the router checks the ACL rules, which consist of **ACE (Access Control Entries)** or instructions.
    

### 📋 **ACE (Access Control Entries)**

- These are the **individual rules** within an ACL.
    
- They specify whether to **allow (permit)** or **deny (deny)** certain traffic.
    
- They are evaluated **in order**, top to bottom. The **first match** is applied, and the rest are ignored.
    

### 🛑 **Packet Filtering**

- When a packet enters an interface with an ACL, it is compared against each ACE one by one.
    
- If it **matches** a rule, the action is taken (allow or block).
    
- If it **matches none**, it is blocked by default (implicit "deny all" rule at the end).
    

### 📌 **Common Uses of ACLs**

- Network access control
    
- Security policy enforcement
    
- Traffic identification for redirection, QoS, NAT, etc.
### 🔢 **Numbered ACLs**

- **Standard ACL:**
    
    - Numbers: `1-99` and `1300-1999`
        
    - Filters **only by source IP**
        
    - Simpler, less specific
        
- **Extended ACLs:**
    
    - Numbers: `100-199` and `2000-2699`
        
    - Filters by:
        
        - **Source and destination IP**
            
        - Protocol (TCP, UDP, ICMP…)
            
        - Port (HTTP, FTP, etc.)
            
    - More detailed and specific
        

---

### 🏷️ **Named ACLs**

- Recommended method: allows giving a **descriptive name** to the ACL (e.g., `FTP-FILTER`).
    
- Created with:
    
    bash
    
    `R1(config)# ip access-list extended FTP-FILTER`
    
- Naming rules:
    
    - Use letters and numbers
        
    - No spaces or punctuation
        
    - Uppercase recommended
        
- Allows **easier ACL editing** (adding or removing rules)
    

---

### ⚙️ **ACL Operation**

- ACLs **control which packets enter or exit** the router's interfaces.
    
- Application types:
    
    - **Inbound:** Filters **before** routing → more efficient.
        
    - **Outbound:** Filters **after** routing → useful for traffic from multiple sources.
        
- ACLs **do not affect traffic generated by the router itself.**
    

---

### 🔄 **How an ACL Works in Practice (Step-by-Step)**

1. The router receives a packet on an interface with an ACL.
    
2. Checks the **source IP** (and more if extended).
    
3. Compares against each rule (**ACE**) from top to bottom.
    
4. If there's a match, **applies the action** (allow or deny).
    
5. If **no match**, the packet is **blocked by default** (implicit `deny all` rule).
    
6. **There must be at least one "permit" rule**, or everything will be blocked.
### 📌 What is a Wildcard Mask?

- A way to **tell the router which parts of an IP address to check** and which to ignore.
    
- Used in ACLs to define **which IPs are allowed or denied access.**
    
- In a wildcard mask:
    
    - `0` means **"must match exactly"**
        
    - `1` means **"can vary / is ignored"**
        

---

### ✅ **1. Match a Single Host**

- **Example IP:** `192.168.1.1`
    
- **Wildcard:** `0.0.0.0`
    
    - All bits must match exactly → only that host is allowed or denied.
        
- **Example ACE:**
    
    bash
    
    `access-list 10 permit 192.168.1.1 0.0.0.0`
    

---

### 🌐 **2. Match an IPv4 Subnet**

- **Example network:** `192.168.1.0/24` → includes IPs from `192.168.1.1` to `192.168.1.254`
    
- **Wildcard:** `0.0.0.255`
    
    - First three octets match (192.168.1), last can vary.
        
- **Example ACE:**
    
    bash
    
    `access-list 10 permit 192.168.1.0 0.0.0.255`
    

---

### 🧮 **3. Match a Specific IPv4 Range**

- This requires **manual calculation** to create a mask matching a non-subnet range.
    
- Example (simplified): allow addresses from `192.168.1.0` to `192.168.1.7`
    
    - This is a 3-bit subnet in the last octet → `192.168.1.0 0.0.0.7`
        
- **Example ACE:**
    
    bash
    
    `access-list 10 permit 192.168.1.0 0.0.0.7`

### 📌 10.2.1 Host Logs (HIDS)

- **What is a HIDS?**  
    An intrusion detection system installed directly on each host (computer). It not only detects attacks but can also **block them**, like a mini firewall inside the host.
    
- **Where are logs stored?**  
    On the host itself. But this is a problem if you have many computers, as checking each one individually is difficult.
    
- **Solution:**  
    Use **agents** to **send logs to a central server**, where they can be analyzed together. No need to check each host manually.
    
- **Useful Tools:**
    
    - **OSSEC** → Powerful, free HIDS
        
    - **Tripwire** → For Linux
        
    - **Event Viewer (Windows)** → View all local logs
        
- **Windows Log Types:**
    
    1. **Application** → Program activities
        
    2. **System** → Drivers, processes, hardware
        
    3. **Setup** → Installations and updates
        
    4. **Security** → Logins, file access
        
    5. **Command Line** → Detect if malware or users use the console
        
- **WARNING: Watch for lsass.exe!**  
    A system process (security), but malware often **impersonates it** (e.g., as `1sass.exe`). Only valid if located in the `System32` folder.
    

---

### 📌 10.2.2 Syslog

- **What is it?**  
    A **universal standard** for devices (routers, switches, servers, etc.) to send **logs to a central server**.
    
- **How it works:**
    
    - A **client-server protocol**.
        
    - Messages are sent as **plain text** (unless SSL is used).
        
    - Uses **UDP (port 514)** or **TCP (port 5000)**.
        
- **Syslog Message Format:**
    
    1. **PRI (Priority)** → Two numbers:
        
        - **Facility**: Type of system generating the message
            
        - **Severity**: From 0 (emergency) to 7 (debug)
            
    2. **HEADER** → Timestamp + hostname
        
    3. **MSG** → Message text (most important for analysts)
        
- **Useful Example:**  
    If a router sends a message with `Severity 3`, it's serious (error).
    

---

### 📌 10.2.3 Server Logs

- **What do servers log?**
    
    - Web, mail, DNS servers, etc., log access and errors.
        
    - **DNS is key**: Useful for detecting connections to malicious sites or data exfiltration.
        
- **Common Types:**
    
    - **Apache (web server)**
        
        txt
        
        `IP – user [date] "GET /file" response_code size`
        
    - **IIS (Microsoft)**  
        Longer logs, with date, method, URL, browser used, etc.
        

---

### 📌 10.2.4 SIEM and Log Collection

- **What is SIEM?**  
    **Security Information and Event Management**, a **central brain** that collects, analyzes, and correlates all network logs.
    
- **What does a SIEM do?**
    
    1. **Collects logs** from the entire network.
        
    2. **Normalizes** (formats everything uniformly).
        
    3. **Correlates related events**.
        
    4. **Groups** to avoid duplicates.
        
    5. **Generates real-time reports** and summaries.
        
    6. **Ensures compliance** with laws or audits (e.g., ISO, GDPR).
        
- **Popular Tools:**
    
    - **Splunk** → Commercial, widely used (nice dashboard)

Note title: Untitled

    - **Security Onion** → Free, based on ELK (Elasticsearch, Logstash, Kibana)
        
- **What is SOAR?**  
    Goes beyond SIEM: **automates responses** (like blocking IPs automatically). Examples:
    
    - **Cisco SecureX**
        
    - **Fortinet Security Fabric**
        
    - **Palo Alto Cortex XDR**
        

These modern tools **integrate multiple functions into a single dashboard**, improving efficiency and reducing human errors.

---

## ✅ Clear Conclusion

In cybersecurity, antivirus or firewalls alone aren't enough: you must **constantly monitor** what happens on the network and devices. That's what **logs** are for—they tell the full story of what occurred. But since there are so many, we need tools like **Syslog, SIEM, or SOAR** to **centralize, analyze, and react quickly** to threats.

Understanding how these technologies work **is key** to detecting attacks, performing forensic analysis, and keeping the network secure.