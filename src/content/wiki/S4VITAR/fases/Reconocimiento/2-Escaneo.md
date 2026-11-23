---
title: "2 Escaneo"
category: ["S4VITAR", "fases", "Reconocimiento", "2-Escaneo"]
---

NMAP OPTIMIZATIONS


Nmap data 
- If a port shows as filtered, it doesn't mean it can't be accessed
- The first scan should be done as quickly as possible
- To visualize nmap graphically, use **tcpdump -i (network interface) -w (filename.cap) -v** to create a file that can be opened with Wireshark or tshark. Run this in a separate terminal and let it listen, then close it after performing the scan.

**NMAP and its TCP nomenclature**

	-p : (specific port, e.g. -p22. For a range: -p-)
	--top-ports (number, e.g. 500): scans the top 500 most popular ports
	
	--open: scans only open ports
	
	-v: shows results in real time without waiting for the scan to finish
	
	-n: avoids DNS lookups for faster scanning
	
	-T(numbers 0-5): higher numbers are more aggressive/faster, lower are stealthier
	
	-sT: a **direct and noisy scan** that confirms a port is truly open by completing a TCP connection, but **leaves traces** on the scanned system. In the three-way handshake, closed ports return RST.
	
	-Pn: assumes the target machine is active
	
	-sU: UDP scan
	
	-sn: lists active network devices with a ping sweep (e.g. nmap -sn 192.168.111.0/24)
	
	-O: detects OS (rarely used)
	
	-sV: service/version detection on ports

Firewall/IDS evasion with nmap
--------
	When on a machine with netstat or ss, we can see active internal ports
	
		-S: The -S parameter lets nmap spoof a source IP different from the real scanning machine's IP.
		
	-f: packet fragmentation
	 - To view fragmented packets in Wireshark: ip.flags.mf == 1
	
	-mtu (multiple of 8, sets packet size)
	
	-D (IP): decoy mode - adds fake source IPs to mask the real scanner
	
	--source-port: specify source port in case firewall whitelists certain ports
	
	--data-length (number): manipulates packet size (e.g. adds 21 bytes to default 58-byte packet)
	
	--spoof-mac (vendor OUI): spoofs MAC address (can use Dell OUI or specific MAC)
	
	-sS: SYN scan that doesn't complete connections, avoiding logs
	
	--min-rate (number): minimum packets per minute (typically 5000)
	
	--max-rate

NMAP SCRIPTS
----

	locate .nse: shows available nmap scripts
	
	-sC: runs default script set (most common scripts)
	
	--script: runs specific scripts
			Common script categories:
				- **default**: Basic reconnaissance scripts
			     - **discovery**: Network/host discovery
			    - **safe**: Non-intrusive scripts
			    - **intrusive**: Easily detected but provides vulnerability info
			    - **vuln**: Focuses specifically on vulnerability detection

Other tools
---
**File descriptors** 
 -  PortScan.sh
		#!/bin/bash
		function ctrl_c(){
			echo -e "\n\n [!]Exiting..."
			exit 1 
		}
		
		#Ctrl+C
		trap ctrl_c SIGINT


		declare -a ports=($(seq 1 65535))


		function checkport(){
		
			(exec 3 <> /dev/tcp/$1/$2) 2>/dev/null

			if [$? -eq 0 ]; then 
				echo "[+] Host $1 - Port $2 (OPEN)"
			fi 
			exec3<&-
			exec3>&-
		}
		if[ $1 ] ; then 
		
		for port in ${ports [@]}; do 
		chechPort $1 $port &
		done
		
		else 
		echo -e "\n[!] Usage: $0<ip-addres>\n"
		fi   
		wait 


arp-scan -I (network interface) --localnet: lists devices on the local network

**Subdomain enumeration** 
----
https://phonebook.cz can passively list subdomains

SSL abuse
###### **CTFR** 

'git clone https://github.com/UnaPibaGeek/ctfr' 
cd ctfr
pip3 install -r requirments.txt
python3 ctfr.py -d [target domain]
![Pasted image 20251122150211](/VaultSite/wiki-images/Pasted%20image%2020251122150211.png)

### GOBUSTER subdomain listing

###### **!!!!!IMPORTANT !!!!!**

Clone the SecLists repository from GitHub to /usr/share
These are thousands of useful wordlists

For gobuster we typically use subdomains-top1million.txt

Basic gobuster syntax:
-u: target URL
-w: wordlist path
-t: number of concurrent threads

EXAMPLE:
[gobuster vhost -u https://tinder.com -w /usr/share/SecLists/Discovery/DNS/subdomains-top1million.txt -t 20 ]

**Web server fuzzing and file enumeration**

-b: blacklist status codes
-s: whitelist status codes
-x (php,html): file extensions to test
-dir: directory listing mode
example: gobuster dir -u https://miwifi.com -w /usr/share/SecLists/Discovery/Web-content/directory-list-2.3-medium.txt -t 200 -b 403,404

![Pasted image 20260125224328](/VaultSite/wiki-images/Pasted%20image%2020260125224328.png)

### WFUZZ
Tool for fuzzing - path discovery, parameter fuzzing, GET/POST requests, extensions. Can fuzz multiple parameters simultaneously.

**What is fuzzing**: A security testing technique that sends random, manipulated, or malicious data to an application

###### **WFUZZ syntax**
https://book.h4ck.cl/metodologia-y-fases-de-hacking-etico/recopilacion-activa-de-informacion/wfuzz
-c: colored output
-hc=[status code like 404]: filters specified codes
-sc: shows only specified codes
-w: wordlist
-u <http://example.com/FUZZ>: FUZZ marks injection point
-H "Host: FUZZ.tinder.com": example for subdomain fuzzing
-X: specifies HTTP method (GET, POST etc.)

**Web file fuzzing example**
wfuzz -c --hc=404,403 -t 200 -w /usr/share/SecLists/Discovery/Web-content/directory-list-2.3-medium.txt https://miwifi.com/FUZZ

![Pasted image 20251124182133](/VaultSite/wiki-images/Pasted%20image%2020251124182133.png)
Here we can add a second payload with -z and .FUZ2Z for file extension fuzzing

Example filtering by product ID range:
![Pasted image 20251124182415](/VaultSite/wiki-images/Pasted%20image%2020251124182415.png)

We can filter by:
-hl=(hide by line count, e.g. 600)
-sl=(show only results with X lines)
-hw=(hide by word count)
-sw
-hh=(hide by character count)
-sh

For passive discovery: https://phonebook.cz

**Web reconnaissance** 
----
Identifying CMS and web technologies

**WHATWEB**

whatweb (url): shows versions
![Pasted image 20251124163525](/VaultSite/wiki-images/Pasted%20image%2020251124163525.png)
Research any unknown versions for potential vulnerabilities

We also have WAPPALYZER which shows us the same thing but as a browser add-on  
![Pasted image 20251124164027](/VaultSite/wiki-images/Pasted%20image%2020251124164027.png)





