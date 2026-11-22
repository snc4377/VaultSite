**LCI -> RCE**  
**Log Poisoning** is an attack technique where an attacker **manipulates** **log files** to achieve a malicious outcome. This technique can be combined with an **LFI** vulnerability to achieve **remote command execution** on the server.

For this class, we'll attempt to poison the **'auth.log'** for **SSH** and **'access.log'** for **Apache**, starting by exploiting an LFI vulnerability to access these log files. Once we gain access, we'll manipulate them to inject malicious code.

For SSH logs, the attacker can inject PHP code into the **username** field during authentication. This causes the code to be logged in the SSH **'auth.log'** and executed when the log file is read, enabling remote command execution on the server.

For Apache's **'access.log'**, the attacker can inject PHP code into the **User-Agent** header of an HTTP request. This malicious code is logged in Apache's **'access.log'** and executed when the file is read, also enabling remote command execution.

Note that some systems do not use **'auth.log'** for SSH authentication events. Instead, they may log to files like **'btmp'**. For example:
- Debian/Ubuntu: SSH logs to **'auth.log'**  
- Red Hat/CentOS: SSH logs to **'btmp'** (though exceptions exist).

To prevent Log Poisoning, developers should:
- Restrict log file access  
- Store logs securely  
- Validate and filter user input before logging  

---

### Practice Setup  
We'll use Docker to spin up an Ubuntu instance with Apache (port 80) and SSH (port 22).  

Apache logs are in `/var/log`. Since we’re running Apache, we check its log directory:  
![[Pasted image 20260122131204.png]]  
The log folder is owned by `root:adm`. Users in the `adm` group can read logs. Verify group membership with `id`:  
![[Pasted image 20260122131615.png]]  
We belong to `adm`, so we can view logs (keep this in mind for LFI testing).  

From the attacker machine, we can modify the `User-Agent` header via `curl -H`:  
![[Pasted image 20260122131838.png]]  
![[Pasted image 20260122131856.png]]  

Since this is a PHP page, we attempt command injection via `User-Agent`:  
![[Pasted image 20260122131952.png]]  
![[Pasted image 20260122132013.png]]  

This works if `system()` is enabled. To check, we send a `phpinfo()` as the `User-Agent`:  
![[Pasted image 20260122132311.png]]  
![[Pasted image 20260122132330.png]]  

`phpinfo()` reveals system details. Filter for `disable_functions` to see blocked functions (e.g., `exec`, `system`, `passthru`):  
![[Pasted image 20260122132449.png]]  

Now, we inject `system()` with a command controlled via `cmd`:  
![[Pasted image 20260122132939.png]]  
The log doesn’t show the `User-Agent`:  
![[Pasted image 20260122133038.png]]  

Since `system()` executes OS commands, we append `&cmd=<COMMAND>` to the URL:  
![[Pasted image 20260122133304.png]]  
![[Pasted image 20260122133328.png]]  

---

### SSH Log Poisoning  
SSH logs typically use **'auth.log'**, but some systems use **'btmp'**.  

**'btmp'** is empty until a failed login occurs:  
![[Pasted image 20260122133557.png]]  

Inject PHP code via the SSH username during connection:  
![[Pasted image 20260122133800.png]]  
![[Pasted image 20260122133743.png]]  

The log records the attempt:  
![[Pasted image 20260122133831.png]]  

View the log and execute commands via `&cmd=`:  
![[Pasted image 20260122134038.png]]  

List processes with `ps -faux`:  
![[Pasted image 20260122134109.png]]  

**Note:** Log poisoning has many variants (e.g., via SMTP/mail).  

---

# HTB Log Poisoning  
As covered earlier, including any PHP file executes its code if the vulnerable function has `Execute` privileges. This attack involves:  
1. Writing PHP code to a controllable field that gets logged.  
2. Including the poisoned log to execute the code.  

PHP web apps must have read access to logs (varies by server).  

The following functions with `Execute` privileges are vulnerable:  

| **Function**          | **Read Content** | **Execute** | **Remote URL** |  
|-----------------------|:---------------:|:----------:|:-------------:|  
| **PHP**               |                 |            |               |  
| `include()`/`include_once()` | ✅ | ✅ | ✅ |  
| `require()`/`require_once()` | ✅ | ✅ | ❌ |  
| **NodeJS**            |                 |            |               |  
| `res.render()`        | ✅ | ✅ | ❌ |  
| **Java**              |                 |            |               |  
| `import`              | ✅ | ✅ | ✅ |  
| **.NET**              |                 |            |               |  
| `include`             | ✅ | ✅ | ✅ |  

---

## PHP Session Poisoning  
Most PHP web apps use `PHPSESSID` cookies to store user-specific backend data. Session files are stored in:  
- Linux: `/var/lib/php/sessions/`  
- Windows: `C:\Windows\Temp/`  

The session filename matches `sess_<PHPSESSID>`. For example, if `PHPSESSID=el4ukv0kqbvoirg7nkp4dncpk3`, the file is:  
`/var/lib/php/sessions/sess_el4ukv0kqbvoirg7nkp4dncpk3`  

### Attack Steps:  
1. Check if `PHPSESSID` is set:  
![imagen](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/rfi_cookies_storage.png)  

2. Include the session file via LFI (e.g., `?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd`):  
![Session file content](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/rfi_session_include.png)  

**Note:** The cookie value is session-specific—use your own `PHPSESSID`.  

The session file contains:  
- `page`: Controlled via `?language=` parameter.  
- `preference`: Automatically set (not user-controllable).  

We can poison the `page` field to inject PHP code.

Let's attempt to set a custom value for `page` (e.g., `language parameter`) and see if it changes in the session file. We can do this by simply visiting the page with `?language=session_poisoning` specified, as follows:

`http://<SERVER_IP>:<PORT>/index.php?language=session_poisoning`

Now, let's include the session file once more to see its contents:

`http://<SERVER_IP>:<PORT>/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd`

![Containers and cranes in a port with a PHP warning about an undefined variable.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/lfi_poisoned_sessid.png)

This time, the session file contains `session_poisoning` instead of `es.php`, confirming our ability to control the `page` value in the session file. Our next step is to perform the `poisoning` step by writing PHP code into the session file. We can write a basic PHP web shell by changing the `?language=` parameter to a URL-encoded web shell, as follows:

`http://<SERVER_IP>:<PORT>/index.php?language=%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%3B%3F%3E`

Finally, we can include the session file and use `&cmd=id` to execute a command:

`http://<SERVER_IP>:<PORT>/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd&cmd=id`

![Containers and cranes in a port with a PHP warning about an undefined variable.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/rfi_session_id.png)

Note: To execute another command, the session file must be poisoned with the web shell again, as it gets overwritten with `/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd` after our last inclusion. Ideally, we would use the poisoned web shell to write a permanent web shell in the web directory or send a reverse shell for easier interaction.

---

## Server Log Poisoning

Both `Apache` and `Nginx` maintain various log files, such as `access.log` and `error.log`. The `access.log` file contains information about all requests made to the server, including the `User-Agent` header for each request. Since we can control the `User-Agent` header in our requests, we can use it to poison the server logs as we did earlier.

Once poisoned, we need to include the logs through the LFI vulnerability, which requires read access to the logs. `Nginx` logs are readable by low-privileged users by default (e.g., `www-data`), while `Apache` logs are only readable by high-privileged users (e.g., `root`/`adm` groups). However, on older or misconfigured `Apache` servers, these logs may be readable by low-privileged users.

By default, `Apache` logs are located in `/var/log/apache2/` on Linux and `C:\xampp\apache\logs\` on Windows, while `Nginx` logs are in `/var/log/nginx/` on Linux and `C:\nginx\log\` on Windows. However, logs may be in a different location in some cases, so we can use an [LFI Wordlist](https://github.com/danielmiessler/SecLists/tree/master/Fuzzing/LFI) to fuzz and find their locations, as discussed in the next section.

So, let's try including the Apache access log from `/var/log/apache2/access.log` and see what we get:

`http://<SERVER_IP>:<PORT>/index.php?language=/var/log/apache2/access.log`

![Containers and cranes in a port with server log entries.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/rfi_access_log.png)

As we can see, we can read the log. The log contains the `remote IP address`, `requested page`, `response code`, and the `User-Agent` header. As mentioned earlier, the `User-Agent` header is controlled by us via HTTP request headers, so we should be able to poison this value.

**Tip:** Logs tend to be huge, and loading them in an LFI vulnerability may take time or even crash the server in the worst case. So, be careful and efficient with them in a production environment, and avoid unnecessary requests.

To do this, we'll use `Burp Suite` to intercept our previous LFI request and modify the `User-Agent` header to `Apache Log Poisoning`:![image](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/rfi_repeater_ua.png)

**Note:** Since all server requests are logged, we can poison any request to the web application, not necessarily the LFI one as we did earlier.

As expected, our custom User-Agent value is visible in the included log file. Now, we can poison the `User-Agent` header by setting it to a basic PHP web shell:![HTTP request and response showing Apache log poisoning with a PHP warning about an undefined variable.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/rfi_cmd_repeater.png)

We can also poison the log by sending a request via cURL, as follows:

`echo -n "User-Agent: <?php system(\$_GET['cmd']); ?>" > Poison snchh337@htb[/htb]$ curl -s "http://<SERVER_IP>:<PORT>/index.php" -H @Poison`

Since the log should now contain PHP code, the LFI vulnerability should execute this code, and we should achieve remote code execution (RCE). We can specify a command to execute with (`&cmd=id`):![HTTP request and response showing Apache log poisoning with PHP code execution using the system command.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/rfi_id_repeater.png)

We see that the command executed successfully. The exact same attack can be performed on `Nginx` logs as well.

**Tip:** The `User-Agent` header is also displayed in process files under Linux's `/proc/` directory. So, we can try including `/proc/self/environ` or `/proc/self/fd/N` (where N is a PID usually between 0-50) and perform the same attack on these files. This may be useful if we don't have read access to server logs; however, these files may also only be readable by privileged users.

Finally, there are other similar log poisoning techniques we can use on various system logs, depending on which logs we have read access to. The following are some service logs we might read:

- `/var/log/sshd.log`
- `/var/log/mail`
- `/var/log/vsftpd.log`

First, we should try reading these logs via LFI, and if we have access, we can attempt to poison them as we did earlier. For example, if `ssh` or `ftp` services are exposed to us and we can read their logs via LFI, we can try logging into them and setting the username as PHP code. When their logs are included, the PHP code would execute. The same applies to `mail` services, as we can send an email containing PHP code, and upon log inclusion, the PHP code would execute. We can generalize this technique to any log that records a parameter we control and can read via the LFI vulnerability.