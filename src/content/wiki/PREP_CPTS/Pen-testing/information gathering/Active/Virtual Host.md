# Virtual Host (vHost) Enumeration

> [!info] Concept
> 
> **Virtual Hosting** allows a single web server (one IP) to host multiple websites. The server decides which site to show based on the **HTTP Host Header** sent by the client. If we access the IP directly, we see the default page. By fuzzing the Host header, we can discover hidden "vHosts".

---

## 1. Manual Identification with Curl

If you have a potential domain name from your initial recon, you can manually test it:

> [!shell] Testing a specific Host header
> 
> Bash
> 
> ```
> # Requesting the default IP
> curl -s http://10.129.129.104
> 
> # Requesting with a specific Host header
> curl -s http://10.129.129.104 -H "Host: dev.inlanefreight.htb"
> ```

---

## 2. Manual Fuzzing & Analysis (Bash)

When you have a wordlist and want to see which domains return different content.

### Step A: Execution

> [!shell] Loop for vHost Fuzzing
> 
> Bash
> 
> ```
> cat /usr/share/seclists/Discovery/DNS/namelist.txt | while read vhost; do 
>     echo "Testing: ${vhost}.inlanefreight.htb"
>     curl -s -I http://10.129.129.104 -H "Host: ${vhost}.inlanefreight.htb" | grep "Content-Length: "
> done > vhosts_results.txt
> ```

### Step B: Filtering Outliers

To find the valid vHosts, we look for `Content-Length` values that differ from the majority (the default page).

> [!shell] Analyzing results
> 
> Bash
> 
> ```
> # Sort and count occurrences of each Content-Length
> cat vhosts_results.txt | grep "Content-Length:" | sort | uniq -c
> ```
> 
> _If you see 3000 results with `Length: 612` and only 1 with `Length: 120`, the `120` is your target._

---

## 3. Automated Fuzzing with FFuf (Recommended)

`ffuf` is significantly faster and has built-in filtering.

> [!shell] FFuf vHost Enumeration
> 
> Bash
> 
> ```
> ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt \
>      -u http://10.129.129.104 \
>      -H "Host: FUZZ.inlanefreight.htb" \
>      -fs 612
> ```
> 
> - **`-fs 612`**: Filters out (hides) responses with size 612 (the default page size).*
>     

---

## 4. Automated Fuzzing with Gobuster

Useful if you prefer a tool that handles the pattern automatically.

> [!shell] Gobuster VHost mode
> 
> Bash
> 
> ```
> # Create a pattern file if needed
> echo "{GOBUSTER}.inlanefreight.htb" > pattern
> 
> # Run Gobuster
> gobuster vhost -u http://10.129.129.104 \
>                -w /usr/share/dirb/wordlists/common.txt \
>                -p pattern \
>                --exclude-length 301,612
> ```

---

## vHost Enumeration Cheatsheet

|**Tool**|**Command**|**Description**|
|---|---|---|
|**Curl**|`curl -H "Host: target.htb" http://<IP>`|Manual test for a single vHost.|
|**FFuf**|`ffuf -w <wordlist> -u http://<IP> -H "Host: FUZZ.target.htb" -fs <size>`|High-speed fuzzing with size filtering.|
|**Gobuster**|`gobuster vhost -u http://<IP> -w <wordlist> --exclude-length <size>`|Alternative tool for vHost discovery.|