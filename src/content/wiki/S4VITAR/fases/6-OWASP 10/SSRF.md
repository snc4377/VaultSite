---
title: "SSRF"
category: ["S4VITAR", "fases", "6-OWASP 10", "SSRF"]
---

**Server-Side Request Forgery** (**SSRF**) is a security vulnerability in which an attacker can force a web server to make HTTP requests on their behalf.

In an SSRF attack, the attacker uses a user input, such as a URL or form field, to send an HTTP request to a web server. The attacker manipulates the request to target a vulnerable server or an internal network that the web server has access to.

The SSRF attack can allow the attacker to access confidential information, such as passwords, API keys, and other sensitive data, and may even enable the attacker (depending on the scenario) to execute commands on the web server or other servers on the internal network.

One of the key **differences** between **SSRF** and **CSRF** is that SSRF is executed on the web server rather than the user's browser. The attacker **does not need to trick a legitimate user** into clicking on a malicious link, as they can send the HTTP request directly to the web server from an external source.

To prevent SSRF attacks, it is important for web application developers to properly validate and filter user input and limit the web server's access to internal network resources. Additionally, web servers should be configured to restrict access to sensitive resources and block unauthorized users.


**LABORATORY** (configuring the server)
In the following image, we see our machine, which does have access to the server like any other user, but only to the production part (which is the finished product that we see and interact with). However, we do not have access to pre-production, which is not exposed on an internal port of the machine (it is not visible from the outside). This is a pre-release environment before it goes to market, where testing is usually done. Pre-production and production may be similar, but pre-production often has additional functionalities or elements that are not meant to be visible.

Initially, if we perform a scan and attempt to make a request to port 8089, it will not respond or allow access.
![Pasted image 20260126153930](/VaultSite/wiki-images/Pasted%20image%2020260126153930.png)
We have configured an Ubuntu machine with Docker (fully updated and with Apache2, PHP, Python3). We edited Apache's index.html to create a PHP utility that allows viewing the content of a web page entered by the user on the server.

utility.php

```php
<?php
	if(isset($_GET['URL'])){             #This line checks if a URL parameter is received via GET, then displays "Listing the content" + the URL + two line breaks.
		echo "\n[+] Listing the content " . $url  . ":\n\n";
		 include ($url);  #Include that URL
	}else{
		echo "\n[!] No URL provided \n\n";
	}

?>
```

If we save this and reload the web page:
![Pasted image 20260126153624](/VaultSite/wiki-images/Pasted%20image%2020260126153624.png)
![Pasted image 20260126153632](/VaultSite/wiki-images/Pasted%20image%2020260126153632.png)
We see that PHP is working, but it does not list Google's website because we need to edit Apache's php.ini.
![Pasted image 20260126153655](/VaultSite/wiki-images/Pasted%20image%2020260126153655.png)

We need to enable the `allow_url_include` directive.
![Pasted image 20260126153808](/VaultSite/wiki-images/Pasted%20image%2020260126153808.png)
![Pasted image 20260126153823](/VaultSite/wiki-images/Pasted%20image%2020260126153823.png)
And now we see it.

Next, we will create a login page. We take a default login page from the internet and make some edits to the HTML to indicate that this is the production part.
![Pasted image 20260126154603](/VaultSite/wiki-images/Pasted%20image%2020260126154603.png)

Now, we will copy the same setup but for pre-production and make a few changes. We will simulate a developer who has placed credentials in the HTML.
![Pasted image 20260126154914](/VaultSite/wiki-images/Pasted%20image%2020260126154914.png)
We start the service on port 4646 but with `--bind 127.0.0.1`, which means it can only be accessed through the server itself. If we try to access it from an external machine, it will not appear.
![Pasted image 20260126155006](/VaultSite/wiki-images/Pasted%20image%2020260126155006.png)
![Pasted image 20260126155142](/VaultSite/wiki-images/Pasted%20image%2020260126155142.png)
If we run an nmap scan with `--open`, we will not see the port.
![Pasted image 20260126155306](/VaultSite/wiki-images/Pasted%20image%2020260126155306.png)
It shows as closed, but it is active.
![Pasted image 20260126155315](/VaultSite/wiki-images/Pasted%20image%2020260126155315.png) 


**First SSRF Case**

We go to PRO, and in the URL parameter, we point to ourselves at localhost.
![Pasted image 20260126155555](/VaultSite/wiki-images/Pasted%20image%2020260126155555.png)

The point is that we can perform port enumeration, so if there is any internally open port, we will see it (since we have configured port 4646 to only be visible through the machine itself, but since it is the machine itself [172.17.0.2] making the request to itself [127.0.0.1]).

And how do we know which ports are open locally?

With wfuzz (or fuff), we launch in color format `-c` with 200 threads `-t 200` and a range payload from port 1 to 65535 `-z range,1-65535` and the URL with the parameter we want to fuzz.
![Pasted image 20260126160210](/VaultSite/wiki-images/Pasted%20image%2020260126160210.png)
Here, we edit the command. For example, we see that when running wfuzz, almost all ports return 3 lines and the same characters, which means it will always show the same thing for all those ports, and we are not interested in that. `--hl=3`
![Pasted image 20260126160438](/VaultSite/wiki-images/Pasted%20image%2020260126160438.png)
We see the production port that should be visible and the pre-production port that should not be visible.
![Pasted image 20260126160548](/VaultSite/wiki-images/Pasted%20image%2020260126160548.png)
![Pasted image 20260126160559](/VaultSite/wiki-images/Pasted%20image%2020260126160559.png)



**Second Scenario**
Here, we have our machine again, and we have access to the PRO port :80 of the server, which has two network interfaces: 172.17.0.2 and 10.10.0.2, which is an internal network. The pre-production environment is on another machine, 10.10.0.3, on port :8089. Externally, we only see port 80 of the machine 172.17.0.2. But since the machine 172.17.0.2 has a second network interface with the internal range, if we put `http://10.10.0.3:8089` in the web utility we created earlier, we would see it because they share the same subnet and can see each other. So now we will apply SSRF reconnaissance to internal networks.
![Pasted image 20260126160630](/VaultSite/wiki-images/Pasted%20image%2020260126160630.png)
Here, we see that from the attacking machine, we do not see the internal network 10.10.0.X, but we do see the IP 172.17.0.2.

![Pasted image 20260126162105](/VaultSite/wiki-images/Pasted%20image%2020260126162105.png)

On the PRO machine, we start the login and PHP for URLs again, and in the PRE environment, we create an index.html file in /tmp.
![Pasted image 20260126162527](/VaultSite/wiki-images/Pasted%20image%2020260126162527.png)
And we start the server in PRE on port 7878.
![Pasted image 20260126162537](/VaultSite/wiki-images/Pasted%20image%2020260126162537.png)

If we go to the attacking machine and use curl to make the web request, nothing will appear because we cannot see the machine.
![Pasted image 20260126162725](/VaultSite/wiki-images/Pasted%20image%2020260126162725.png)
But if we curl the production environment machine, it allows us because we are leveraging this machine, which internally has traceability with the PRE machine through this utility, allowing us to enumerate an internal subnet to see privileged information.
![Pasted image 20260126163019](/VaultSite/wiki-images/Pasted%20image%2020260126163019.png)

To discover this second internal network, which we normally should not know about, we would execute this script on our machine. It sends requests to the machine defined in **TARGET** with different IPs from a range defined in **base**. In this script, we only need to edit the **TARGET** parameter (with the URL of the victim we are SSRFing) and **BASE** (with the range we want to scan). Once we find something, we proceed to attack with wfuzz to discover ports.

Internal network SSRF scanner

```python
import requests 
import time 
TARGET = "https://victima.com/check?url=" 
def test(ip): 
	url = TARGET + f"http://{ip}" 
	try: 
		start = time.time() # Record the exact time before the request
		r = requests.get(url, timeout=5) # Send the request with a 5-second limit
		elapsed = time.time() - start  # Calculate how long it took
		return r.status_code, round(elapsed, 2) 
	except:
		return "timeout", 5 
	
def scan(): 
	base = "10.0.0." # The internal network segment we want to investigate    
	for i in range(1, 255): # Will try from .1 to .254
		ip = base + str(i) 
		code, t = test(ip) 
		print(f"{ip} -> {code} ({t}s)") 
		if code != "timeout": # If the server responded with something (anything), there is life
			print(f"[+] Possible host found: {ip}") 
scan()
```


