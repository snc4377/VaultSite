---
title: "LFI (Local File Inclusion)"
category: ["Networking & services configs", "Networking", "HACKING WIFI", "info de herramientas y conceptos", "LFI (Local File Inclusion)"]
---

# LFI (Local File Inclusion)

An **LFI (Local File Inclusion)** is a web security vulnerability that allows an attacker to include local files from the server in the web application. This occurs when the application allows users to provide file names or paths that are not properly validated. Attackers can use this vulnerability to access sensitive files, execute malicious code, or even take control of the system.

### **How does an LFI work?**

An LFI typically occurs in poorly configured web applications that accept user input to load files without properly validating that input. For example:

1. **Vulnerable code:**

    `<?php $file = $_GET['file']; include($file); ?>`
    
    In this example, the PHP script includes a file based on the `file` parameter provided in the URL.
    
2. **LFI attack:** An attacker could send a request like this:

    
    `http://victima.com/index.php?file=/etc/passwd`
    
    This may allow the attacker to include and read the contents of the `/etc/passwd` file, which contains information about system users.
    

---

### **Impact of an LFI**

Depending on the files the attacker can access, the consequences may vary:

- **Access to sensitive information:**
    
    - Server configuration files.
    - Databases or credentials stored in files.
    - Log files with critical information.
- **Privilege escalation:** In combination with other vulnerabilities, such as remote code execution (RCE), an attacker could completely compromise the server.
    

---

### **Example of a typical attack**

1. **Access to sensitive files:**
    
    
    `http://victima.com/index.php?file=../../../../etc/passwd`
    
    In this case, the attacker uses `../../` to navigate backward through directories and access `/etc/passwd`.
    
2. **Log exploration:** If the server stores sensitive information in logs, the attacker may attempt to include them:
    
    `http://victima.com/index.php?file=../../var/log/apache2/access.log`
    
3. **Execution of malicious code:** If the attacker can upload a malicious file to the server and then include it via LFI, they could execute malicious commands.
    

---

### **How to prevent LFI**

1. **Validate and sanitize user input:**  
    Never allow the user to provide file paths directly. Use a whitelist of allowed files.
    
2. **Configure the server correctly:**
    
    - Limit access to critical directories using file permissions and secure paths.
    - Disable dangerous functions like `allow_url_include` in PHP.
3. **Use secure methods for including files:**  
    For example, instead of using `include($file)`, use absolute paths or identify valid files by their identifier.
    
4. **Monitor logs and detect unusual behavior:**  
    Implement intrusion detection systems (IDS) or web application firewalls (WAF).


An **RFI (Remote File Inclusion)** is a web vulnerability similar to LFI, but it allows an attacker to include remote files on the server through manipulated input. It is more dangerous than LFI, as it facilitates the execution of arbitrary code hosted on another server controlled by the attacker.

### **How LFI and RFI are exploited**

- **LFI exploitation**: Involves searching for vulnerabilities that allow access to local server files. This can lead to the exposure of sensitive data or command execution if combined with other vulnerabilities.
- **RFI exploitation**: Seeks a vulnerability that allows the inclusion of external files. The attacker can use this to execute malicious scripts that give them control over the server.

### **Is LFI necessary to perform RFI?**

No. If a web application is vulnerable to **RFI**, an attacker can directly include a remote file and execute code without needing to perform LFI first. However, in some cases, LFI can be a preliminary step to finding entry points that could lead to **RFI**, especially if the goal is to find ways to execute malicious code from a server controlled by the attacker.

### **Attack sequence**

1. **LFI (if necessary)**: Access local files or expose system information.
2. **RFI**: Include and execute a remote file (such as a malicious PHP script) from an external server to take control of the compromised server.

### **How to protect against LFI and RFI?**

- **Validate inputs**: Do not allow the inclusion of file paths provided by the user without strict validation.
- **Disable remote file inclusion**: Configure the `php.ini` file to disable the `allow_url_include` option:

    
    `allow_url_include = Off`
    
- **Use absolute paths and avoid user input in `include` or `require` functions**.
- **Monitor and audit**: Use vulnerability scanning tools and perform periodic audits to detect potential insecure entry points.



# **How to use LFI**
### **URL and parameter review**:

- **Observe URL parameters**: If you find parameters that seem to indicate file loading (e.g., `page`, `file`, `include`), you might be facing a potential entry point for LFI.
- **Relative path testing**: Try modifying URL parameters to include relative paths that access files outside the application folder (e.g., `../../../../etc/passwd`). If you get errors or the contents of local files, it's a sign that the application might be vulnerable to LFI.

### 2. **Local file inclusion testing**:

- **File loading test**: If the application allows loading specific files via a URL parameter, try loading files like `../../../../etc/passwd`, `../../../../etc/shadow`, `../../../../var/log/apache2/access.log`, etc. If the application displays contents of critical files, this indicates LFI.
- **Error testing**: Some applications may display errors or debugging messages that confirm the existence of a vulnerability. Look for messages like `Warning: include(../../../../etc/passwd): failed to open stream: No such file or directory`.

### 3. **Application response verification**:

- **HTTP error review**: If the application responds with HTTP errors, such as `404 Not Found` or `500 Internal Server Error`, or displays file content when testing relative paths, this could indicate an LFI vulnerability.
- **Unexpected content**: If injecting relative paths displays contents of important files, the application might be vulnerable.

We would also try to view `.ssh` to obtain `id_rsa` or the most critical would be to perform log poisoning by viewing some system log like Apache, we would see the `access_log` and check the `user_agent` where we could inject PHP and when we view the log again, we should see `wdata`, `apache`, etc...

# **View PHP from LFI**

We would use a wrapper from the path in the URL. 