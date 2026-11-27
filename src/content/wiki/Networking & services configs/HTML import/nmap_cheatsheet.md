---
title: "Nmap Cheatsheet"
category: ["Networking & services configs", "HTML import", "nmap_cheatsheet"]
---

# Nmap Cheatsheet: Main Flags and Practical Command Examples

## Flags & Options Practical Examples

Scanning  
`-sS` SYN scan (stealth) — sends SYN, does not complete the handshake. Faster and stealthier.  
`-sT` TCP connect scan — completes the handshake. Used without root.  
`-sU` UDP scan — detects UDP services (DNS, SNMP, DHCP…).  
`-sN` / `-sF` / `-sX` Null, FIN, and Xmas scan — evade some firewalls, ambiguous behavior on Windows.  
`-sA` ACK scan — does not detect open ports, but firewall rules.  
`-sV` Version detection of services on open ports.  
`-O` OS detection via TCP/IP fingerprinting.  
`-A` Aggressive mode: OS, versions, scripts, and traceroute all at once.  

Host/Ports  
`-p <ports>` Defines which ports to scan. E.g.: `-p 80,443` / `-p 1-1000` / `-p-`  
`-p-` Scans all 65535 ports.  
`--top-ports N` Scans the N most common ports based on usage frequency.  
`-sn` Ping scan — only discovers hosts without scanning ports.  
`-Pn` Skips host discovery — treats all hosts as active.  
`-PR` ARP ping — host discovery on local networks, very reliable.  
`--open` Shows only open ports in the result.  
`-iL <file>` Reads target list from a text file.  

Timing  
`-T0 … -T5` Scan speed. `T0=paranoid` (slow/stealthy), `T3=normal`, `T5=insane` (noisy).  
`--min-rate N` Forces a minimum of N packets per second sent.  
`--max-retries N` Limits retries per port (useful for speeding up).  
`--host-timeout` Abandons a host if it takes longer than X time. E.g.: `--host-timeout 30s`  

NSE Scripts  
`-sC` Runs default NSE scripts (equivalent to `--script=default`).  
`--script=<name>` Runs a specific script. E.g.: `--script=vuln` / `--script=smb-os-discovery`  
`--script-args` Passes arguments to scripts. E.g.: `--script-args user=admin`  
`--script-help` Shows help for a specific script.  

Evasion  
`-f` Fragments packets to evade IDS/IPS.  
`-D <decoys>` Decoy scan — mixes your IP with decoy IPs to confuse logs.  
`--spoof-mac` Spoofs the sender’s MAC address.  
`--data-length N` Adds N bytes of random padding to alter packet signature.  
`--source-port N` Forces the source port. Some firewalls trust ports like 53 or 80.  
`--scan-delay` Adds delay between probes to avoid triggering rate-limiting alerts.  

Output  
`-oN <file>` Saves the result in normal format (readable).  
`-oX <file>` Saves in XML — compatible with tools like Metasploit.  
`-oG <file>` Grepable format — easy to parse with grep/awk.  
`-oA <base>` Saves in all three formats at once (normal, XML, grepable).  
`-v` / `-vv` Verbosity — shows more real-time information during the scan.  
`--reason` Shows why a port is marked as open/closed/filtered.  

## Host Discovery / Local Network Recon

```bash
nmap -sn 192.168.1.0/24  
nmap -sn -PR 192.168.1.0/24  
nmap -sn --traceroute 192.168.1.0/24
```

Discovers active hosts without scanning ports. `-PR` uses ARP (more reliable on LAN). Ideal for the first step in an internal pentest.  

## Quick Port Scan Basics

```bash
nmap -sS -T4 --top-ports 1000 -Pn 10.10.10.5  
nmap -sS -p- --min-rate 5000 -Pn -n 10.10.10.5
```

The second command scans all ports at high speed. `-n` disables DNS resolution for greater speed. Widely used in CTFs and labs.  

## Version and OS Detection Basics

```bash
nmap -sV -O -sC 10.10.10.5  
nmap -A -p 22,80,443,8080 10.10.10.5
```

`-sV` fingerprints the service, `-O` the OS, `-sC` runs default scripts. `-A` groups everything. Essential after the initial port scan.  

## SMB Enumeration NSE

```bash
nmap -p 139,445 --script=smb-os-discovery 10.10.10.5  
nmap -p 139,445 --script=smb-enum-shares,smb-enum-users 10.10.10.5  
nmap -p 445 --script=smb-vuln-ms17-010 10.10.10.5  
nmap -p 445 --script=smb2-security-mode 10.10.10.5
```

Detects SMB version, available shares, users, and critical vulnerabilities like EternalBlue (MS17-010). Essential in Windows/AD environments.  

## HTTP / Web Enumeration NSE

```bash
nmap -p 80,443,8080 --script=http-title,http-headers 10.10.10.5  
nmap -p 80 --script=http-enum 10.10.10.5  
nmap -p 80 --script=http-methods 10.10.10.5  
nmap -p 80 --script=http-auth-finder 10.10.10.5  
nmap -p 80 --script=http-shellshock --script-args uri=/cgi-bin/test.sh 10.10.10.5
```

`http-enum` performs basic path fuzzing (similar to gobuster). `http-methods` detects dangerous verbs (PUT, DELETE). `http-shellshock` checks for CVE-2014-6271.  

## MySQL / MSSQL Enumeration NSE

```bash
nmap -p 3306 --script=mysql-info,mysql-empty-password 10.10.10.5  
nmap -p 3306 --script=mysql-enum 10.10.10.5  
nmap -p 1433 --script=ms-sql-info,ms-sql-empty-password 10.10.10.5  
nmap -p 1433 --script=ms-sql-config,ms-sql-dump-hashes 10.10.10.5
```

`mysql-empty-password` checks for users without passwords. `ms-sql-dump-hashes` attempts to extract MSSQL hashes if access is available. Credentials may be required in some cases.  

## FTP / SSH / RDP Enumeration NSE

```bash
nmap -p 21 --script=ftp-anon,ftp-bounce,ftp-syst 10.10.10.5  
nmap -p 22 --script=ssh-auth-methods,ssh-hostkey 10.10.10.5  
nmap -p 3389 --script=rdp-enum-encryption,rdp-vuln-ms12-020 10.10.10.5
```

`ftp-anon` detects if FTP accepts anonymous login. `ssh-auth-methods` lists allowed authentication methods. `rdp-vuln-ms12-020` checks for a critical DoS/RCE vulnerability.  

## General Vulnerability Scan Vulns

```bash
nmap -sV --script=vuln 10.10.10.5  
nmap -sV --script=exploit 10.10.10.5 --script-args=unsafe=1
```

The `vuln` category groups all CVE detection scripts. With `unsafe=1`, potentially intrusive scripts are enabled — use only in controlled environments.  

## UDP Scan (SNMP, DNS, NFS…) UDP

```bash
nmap -sU -p 53,67,68,161,500 10.10.10.5  
nmap -sU --top-ports 100 -T4 10.10.10.5  
nmap -sU -p 161 --script=snmp-info,snmp-sysdescr 10.10.10.5
```

UDP is slow — limit ports or use `--top-ports`. SNMP (161) often reveals critical network/system information. `snmp-info` dumps the entire MIB if the community string is "public".  

## Firewall / IDS Evasion Evasion

```bash
nmap -sS -f -T2 --data-length 200 -D RND:10 10.10.10.5  
nmap -sS --source-port 53 -Pn 10.10.10.5  
nmap -sS --scan-delay 500ms --max-retries 2 10.10.10.5
```

`-f` fragments packets, `-D RND:10` generates 10 random decoy IPs, `--source-port 53` mimics DNS traffic. Combining multiple techniques increases evasion chances.  

## Full Workflow (CTF/Pentest) Full Workflow

```bash
# 1. Discover ports quickly  
nmap -sS -p- --min-rate 5000 -Pn -n -oN ports.txt 10.10.10.5  

# 2. Deep dive into open ports  
nmap -sV -sC -O -p 22,80,445 -oA full_scan 10.10.10.5  

# 3. Specific scripts based on services found  
nmap -p 445 --script=smb-vuln-ms17-010 10.10.10.5  
nmap -p 80 --script=http-enum 10.10.10.5
```

Standard workflow in CTFs and real pentests: first speed to see what’s there, then depth, then targeted scripts. Always save output with `-oA` or `-oN`.