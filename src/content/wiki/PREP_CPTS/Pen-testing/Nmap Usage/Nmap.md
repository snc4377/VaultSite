---
title: "Nmap"
category: ["PREP_CPTS", "Pen-testing", "Nmap Usage", "Nmap"]
---



## **Most Used Commands and Parameters**

**BASIC SCANNING TECHNIQUES**:

- Scan a single target **– nmap [target]**
- Scan multiple targets **– nmap [target1,target2,etc]**
- Scan a target list **– nmap -iL [list.txt]**
- Scan a range of hosts **– nmap [range of IP addresses]**
- Scan an entire subnet **– nmap [IP address/cdir]**
- Scan random hosts **– nmap -iR [number]**
- Exclude targets from a scan **– nmap [targets] –exclude [targets]**
- Exclude targets using a list **– nmap [targets] –excludefile [list.txt]**
- Perform an aggressive scan **– nmap -A [target]**
- Scan an IPv6 target **– nmap -6 [target]**

**DISCOVERY OPTIONS:**

- Perform only a ping scan **– nmap -sP [target]**
- Skip ping **– nmap -PN [target]**
- TCP SYN Ping **– nmap -PS [target]**
- TCP ACK Ping **– nmap -PA [target]**
- UDP Ping **– nmap -PU [target]**
- SCTP Init Ping **– nmap -PY [target]**
- ICMP Echo Ping **– nmap -PE [target]**
- ICMP Timestamp Ping **– nmap -PP [target]**
- ICMP Address Mask Ping **– nmap -PM [target]**
- IP Protocol Ping **– nmap -PO [target]**
- ARP Ping **– nmap -PR [target]**
- Traceroute **– nmap -traceroute [target]**
- Force reverse DNS resolution **– nmap -R [target]**
- Disable reverse DNS resolution **– nmap -n [target]**
- Alternative DNS lookup **– nmap -system-dns [target]**
- Manually specify DNS servers **– nmap -dns-servers [servers] [target]**
- Create a host list **– nmap -SL [target]**

**ADVANCED SCANNING OPTIONS:**

- TCP SYN Scan **– nmap -sS [target]**
- TCP Connect Scan **– nmap -sT [target]**
- UDP Scan **– nmap -sU [target]**
- TCP Null Scan **– nmap -sN [target]**
- TCP Fin Scan **– nmap -sF [target]**
- Xmas Scan **– nmap -sX [target]**
- TCP ACK Scan **– nmap -sA [target]**
- Custom TCP Scan **– nmap -scanflags [flags] [target]**
- IP Protocol Scan **– nmap -sO [target]**
- Send Ethernet packets **– nmap -send-eth [target]**
- Send IP packets **– nmap -send-ip [target]**

**PORT SCANNING OPTIONS:**

- Perform a quick scan **– nmap -F [target]**
- Scan specific ports **– nmap -p [Ports] [target]**
- Scan ports by name **– nmap -p [port name] [target]**
- Scan protocol ports **– nmap -sU -sT -p U:[ports], T:[ports] [target]**
- Scan all ports **– nmap -p "*" [target]**
- Scan top ports **– nmap -top-ports [number] [target]**
- Perform sequential port scan **– nmap -r [target]**

**VERSION DETECTION:**

- OS detection **– nmap -O [target]**
- Submit TCP/IP Fingerprints **– www.nmap.org/submit/**
- Guess unknown OS **– nmap –osscan-guess [target]**
- Service version detection **– nmap -sV [target]**
- Troubleshoot version scans **– nmap -sV -version-trace [target]**
- Perform RPC scan **– nmap -sR [target]**

**TIMING OPTIONS:**

- Timing templates **– nmap -T [0-5] [target]**
- Adjust packet TTL **– nmap –ttl [time] [target]**
- Minimum parallel connections **– nmap –min-parallelism [number] [target]**
- Maximum parallel connections **– nmap –max-parallelism [number] [target]**
- Minimum host group size **– nmap –min-hostgroup [number] [targets]**
- Maximum host group size **– nmap –max-hostgroup [number] [targets]**
- Maximum RTT timeout **– nmap –initial-rtt-timeout [time] [target]**
- Initial RTT timeout **– nmap –max-rtt-timeout [TTL] [target]**
- Maximum retries **– nmap –max-retries [number] [target]**
- Host timeout **– nmap –host-timeout [time] [target]**
- Minimum scan delay **– nmap –scan-delay [time] [target]**
- Maximum scan delay **– nmap –max-scan-delay [time] [target]**
- Minimum packet rate **– nmap –min-rate [number] [target]**
- Maximum packet rate **– nmap –max-rate [number] [target]**
- Defeat RST rate limits **– nmap –defeat-rst-ratelimit [target]**

**FIREWALL EVASION:**

- Fragment packets **– nmap -f [target]**
- Specify a custom MTU **– nmap –mtu [MTU] [target]**
- Use decoys **– nmap -D RND:[number] [target]**
- Idle zombie scan **– nmap -sI [zombie] [target]**
- Manually specify source port **– nmap –source-port [port] [target]**
- Append random data **– nmap –data-length [size] [target]**
- Randomize target scan order **– nmap –randomize-hosts [target]**
- Spoof MAC Address **– nmap –spoof-mac [MAC|0|vendor] [target]**
- Send bad checksums **– nmap –badsum [target]**

**OUTPUT OPTIONS:**

- Save output to text file **– nmap -oN [scan.txt] [target]**
- Save output to XML file **– nmap -oX [scan.xml] [target]**
- Grepable output **– nmap -oG [scan.txt] [target]**
- Output all file types **– nmap -oA [path/filename] [target]**
- Periodically show statistics **– nmap –stats-every [time] [target]**
- 133t output **– nmap -oS [scan.txt] [target]**

**TROUBLESHOOTING AND DEBUGGING:**

- Help **– nmap -h**
- Show Nmap version **– nmap -V**
- Verbose output **– nmap -v [target]**
- Debug **– nmap -d [target]**
- Show port status **– nmap –reason [target]**
- Show only open ports **– nmap –open [target]**
- Packet trace **– nmap –packet-trace [target]**
- Display host interfaces **– nmap –iflist**
- Specify a network interface **– nmap -e [interface] [target]**

**NMAP SCRIPTING ENGINE:**

- Run individual scripts **– nmap –script [script.nse] [target]**
- Run multiple scripts **– nmap –script [expression] [target]**
- Script categories **– all, auth, default, discovery, external, intrusive, malware, safe, vuln**
- Run scripts by category **– nmap –script [category] [target]**
- Run scripts from multiple categories **– nmap –script [category1,category2, etc]**
- Troubleshoot scripts **– nmap –script [script] –script-trace [target]**
- Update script database **– nmap –script-updatedb**













