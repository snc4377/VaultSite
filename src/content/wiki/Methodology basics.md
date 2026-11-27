---
title: "Methodology Basics"
category: ["Methodology basics"]
---


# Methodology Basics

### Phase 0. Preparation and Scope

Before executing any technique, define the conditions of the audit.

- Define the scope: IPs, domains, applications, network ranges, and excluded elements.
    
- Establish engagement rules: allowed hours, prohibited techniques, emergency contacts, and incident procedures.
    
- Prepare the working environment: VPN if applicable, updated tools, evidence directories, and documentation templates.
    
- Verify authorizations and legal or contractual limitations.
    

### Phase 1. Reconnaissance and Passive OSINT

The goal is to gather information without directly interacting with the target.

- Domains and subdomains:
    
    - Tools: `whois`, `amass`, `subfinder`, `crt.sh`.
        
- Exposed infrastructure:
    
    - Tools: `Shodan`, `Censys`.
        
- Information leakage:
    
    - Tools: `theHarvester`, Google Dorks, `trufflehog`, `gitleaks`.
        
- Emails, employees, and organizational structure:
    
    - Tools: [Hunter.io](https://hunter.io/), LinkedIn, OSINT searches.
        

### Phase 2. Enumeration and Active Scanning

Here begins direct interaction with the target to discover hosts, ports, and services.

- Host discovery:
    
    - Tools: `arp-scan`, `netdiscover`, `nmap -sn`.
        
- Port and service scanning:
    
    - Tools: `nmap`, `masscan`, `rustscan`.
        
- Specific service enumeration:
    
    - SMB/NetBIOS: `enum4linux`, `smbclient`, Nmap NSE scripts.
        
    - SNMP: `snmpwalk`, `onesixtyone`.
        
    - DNS: `dig`, `dnsrecon`.
        
    - FTP/SSH: default credential testing and user enumeration.
        

### Phase 3. Web Discovery and Vulnerability Analysis

If a web server exists, this phase is critical for mapping the application.

- Fingerprinting:
    
    - Tools: `whatweb`, Wappalyzer.
        
- Directory and file enumeration:
    
    - Tools: `ffuf`, `feroxbuster`, `gobuster`, with dictionaries like SecLists.
        
- Endpoint and parameter enumeration:
    
    - Tools: `katana`, `hakrawler`, `arjun`.
        
- Vulnerability analysis:
    
    - Tools: `nikto`, `nuclei`, `WPScan` if WordPress.
        
    - Manual testing with Burp Suite or OWASP ZAP: SQL injection, XSS, LFI/RFI, file upload, access control.
        

### Phase 4. Exploitation and Initial Access

The goal is to leverage a vulnerability to gain access to the system.

- Public exploit search:
    
    - Tools: `searchsploit`, Exploit-DB searches, and public sources.
        
- Web exploitation:
    
    - SQL injection: `sqlmap`.
        
    - Command injection/RCE: manual testing and reverse shell generation.
        
    - File upload: attempt to upload a webshell if the application allows it.
        
- Network and credential exploitation:
    
    - Tools: Metasploit Framework, `hydra`, `medusa`.
        
- Binary vulnerabilities:
    
    - Analysis with Ghidra or IDA and payload generation with `msfvenom`.
        

### Phase 5. Post-Exploitation and Privilege Escalation

Once access is obtained, the goal is to consolidate and expand control.

- Stabilize the shell: `script`, Python PTY, or other techniques.
    
- Local enumeration:
    
    - Tools: LinPEAS, WinPEAS, `pspy`.
        
- Linux privilege escalation:
    
    - Check `sudo -l`, SUID permissions, cron jobs, capabilities, and exploitable binaries with GTFOBins.
        
- Windows privilege escalation:
    
    - Check privileges, vulnerable services, scheduled tasks, and use of LOLBAS/PowerUp.
        
- Lateral movement in networks or Active Directory:
    
    - Tools: BloodHound, CrackMapExec/NetExec, Impacket.
        

### Phase 6. Documentation and Reporting

The audit must be documented clearly and reproducibly.

- Record commands, tools, findings, and evidence.
    
- Classify vulnerabilities by severity, for example with CVSS.
    
- Draft concrete and actionable recommendations for each finding.
    
- Include an executive summary, methodology, technical details, and evidence appendices.
    

### Final Considerations

- Maintain a methodical approach and document each step.
    
- If one path doesn’t work, record what was attempted and move to the next.
    
- Use references like HackTricks, PayloadsAllTheThings, and GTFOBins for specific techniques.