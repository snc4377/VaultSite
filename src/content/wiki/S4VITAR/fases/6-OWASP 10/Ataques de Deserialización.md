**Deserialization attacks** are a type of attack that exploits vulnerabilities in the **serialization** and **deserialization** processes of objects in applications that use object-oriented programming (**OOP**).

Serialization is the process of converting an [[object]] into a sequence of **bytes** that can be stored or transmitted over a network. Deserialization is the reverse process, where a byte sequence is converted back into an object. Deserialization attacks occur when an attacker can manipulate the data being deserialized, which can lead to **malicious code execution** on the server.

Deserialization attacks can occur in different types of applications, including web applications, mobile applications, and desktop applications. These attacks can be exploited in several ways, such as:

- Modifying the serialized object before it is sent to the application, which can cause errors during deserialization and allow an attacker to execute malicious code.
- Sending a malicious serialized object that exploits a vulnerability in the application to execute malicious code.
- Performing a **man-in-the-middle** attack to intercept and modify the serialized object before it reaches the application.

Deserialization attacks can be very dangerous, as they can allow an attacker to take full control of the server or the targeted application.

To prevent these attacks, it is crucial for applications to properly validate and authenticate all received data before deserializing it. It is also important to use secure serialization and deserialization libraries and to regularly update all application libraries and components to fix potential vulnerabilities.


**LABORATORY**
- **Machine Cereal 1**: [https://www.vulnhub.com/entry/cereal-1,703/](https://www.vulnhub.com/entry/cereal-1,703/)

Let's run an nmap scan to see which ports are open  
![Pasted image 20260128192149](/VaultSite/wiki-images/Pasted%20image%2020260128192149.png)  
![Pasted image 20260128192224](/VaultSite/wiki-images/Pasted%20image%2020260128192224.png)  
Let's perform a scan on specific ports  
![Pasted image 20260128192258](/VaultSite/wiki-images/Pasted%20image%2020260128192258.png)  
![Pasted image 20260128192323](/VaultSite/wiki-images/Pasted%20image%2020260128192323.png)  
Let's test the web services on port 80 and port 44441.

**Port 80**  
![Pasted image 20260128192355](/VaultSite/wiki-images/Pasted%20image%2020260128192355.png)  
Let's perform directory discovery with gobuster.  
Using the `Dir` command, we'll list directories and set 20 threads.  
![Pasted image 20260128192437](/VaultSite/wiki-images/Pasted%20image%2020260128192437.png)  
We see the `admin` directory, which is an authentication panel.  
![Pasted image 20260128192501](/VaultSite/wiki-images/Pasted%20image%2020260128192501.png)  
And in `blog`, we see this:  
![Pasted image 20260128192531](/VaultSite/wiki-images/Pasted%20image%2020260128192531.png)  
Using Wappalyzer, let's see what this web app is using.  
![Pasted image 20260128192604](/VaultSite/wiki-images/Pasted%20image%2020260128192604.png)  

If we press `Ctrl+U` and analyze the code, we can see that resources are being loaded from `https://cereal.ctf/blog/index.php/feed/`  
![Pasted image 20260128192715](/VaultSite/wiki-images/Pasted%20image%2020260128192715.png)  

If we try to ping `cereal.ctf`, we see no response, which is why the web page looks so bad—it's using virtual hosting.  
![Pasted image 20260128192813](/VaultSite/wiki-images/Pasted%20image%2020260128192813.png)  
So, let's add it to `/etc/hosts`.  
![Pasted image 20260128192926](/VaultSite/wiki-images/Pasted%20image%2020260128192926.png)  
![Pasted image 20260128192941](/VaultSite/wiki-images/Pasted%20image%2020260128192941.png)  

If we try to access port `44441`, we see a message:  
![Pasted image 20260128193114](/VaultSite/wiki-images/Pasted%20image%2020260128193114.png)  
Let's perform subdomain reconnaissance on this port. We do this because if multiple HTTP ports are running on the same machine, subdomains might not be listed on port 80 but could be on `44441`.  
![Pasted image 20260128193337](/VaultSite/wiki-images/Pasted%20image%2020260128193337.png)  
Let's add the domain to `/etc/hosts` again.  
![Pasted image 20260128193417](/VaultSite/wiki-images/Pasted%20image%2020260128193417.png)  
![Pasted image 20260128193437](/VaultSite/wiki-images/Pasted%20image%2020260128193437.png)  

We see this panel—let's try pinging `localhost`.  
![Pasted image 20260128193538](/VaultSite/wiki-images/Pasted%20image%2020260128193538.png)  
Based on the TTL, it's a Linux machine.  

Let's check if this ping panel actually works. We'll listen with `tcpdump -i ens33 icmp -n`.  
![Pasted image 20260128193705](/VaultSite/wiki-images/Pasted%20image%2020260128193705.png)  
![Pasted image 20260128193724](/VaultSite/wiki-images/Pasted%20image%2020260128193724.png)  

Let's test if we can concatenate other commands. We try adding a `whoami` after the ping, but it's sanitized.  
![Pasted image 20260128193851](/VaultSite/wiki-images/Pasted%20image%2020260128193851.png)  

Let's intercept with Burp Suite.  
![Pasted image 20260128193925](/VaultSite/wiki-images/Pasted%20image%2020260128193925.png)  
We see an object and then the IP.  
We notice in Burp that it's URL-encoded.  
![Pasted image 20260128194011](/VaultSite/wiki-images/Pasted%20image%2020260128194011.png)  
Once decoded, we see the object is 8 characters long (`pingTest`), a string with 9 characters (`s:9 "ipAddress"`), and another string (`s:14 "192.168.111.45"`).  

Here, we can see the serialized object being sent to the server, which deserializes and interprets it to execute functions or methods based on what we send.  

Let's press `Ctrl+U` on the web page.  
![Pasted image 20260128194603](/VaultSite/wiki-images/Pasted%20image%2020260128194603.png)  
We see it uses `php.js`. Let's inspect it.  
![Pasted image 20260128194737](/VaultSite/wiki-images/Pasted%20image%2020260128194737.png)  
But nothing interesting here.  

Let's perform reconnaissance on this new URL, `secure.cereal.ctf`, using a larger dictionary.  
![Pasted image 20260128194859](/VaultSite/wiki-images/Pasted%20image%2020260128194859.png)  

Let's check the `back_en` resource, but we don't have access.  
![Pasted image 20260128194935](/VaultSite/wiki-images/Pasted%20image%2020260128194935.png)  

Let's try enumerating files in this directory (we need to test enumerating all possible file types).  
![Pasted image 20260128195155](/VaultSite/wiki-images/Pasted%20image%2020260128195155.png)  
![Pasted image 20260128195209](/VaultSite/wiki-images/Pasted%20image%2020260128195209.png)  
Let's check the source code.  
![Pasted image 20260128195229](/VaultSite/wiki-images/Pasted%20image%2020260128195229.png)  

In the first part of the code, we see a function called `isValid` set to `false`, which blocks everything. The only way to set it to `true` is by providing an IP that passes validation.  
![Pasted image 20260128195730](/VaultSite/wiki-images/Pasted%20image%2020260128195730.png)  
And here, it executes the `ping` command.  
![Pasted image 20260128195747](/VaultSite/wiki-images/Pasted%20image%2020260128195747.png)  
Here, it checks if the serialized object contains anything. If not, it creates a new `pingTest` and pings `127.0.0.1` (defined above).  
![Pasted image 20260128195835](/VaultSite/wiki-images/Pasted%20image%2020260128195835.png)  
That's why, when we reload the page without entering anything in the ping test:  
![Pasted image 20260128200032](/VaultSite/wiki-images/Pasted%20image%2020260128200032.png)  

After analyzing the code, we see the target is here:  
![Pasted image 20260128200126](/VaultSite/wiki-images/Pasted%20image%2020260128200126.png)  
Because if we can input `ping 192.168.111.45; whoami`, the code will execute both the ping and the `whoami` command, as this part is not sanitized and trusts that the object cannot be manipulated.  

Let's create a serialized object with `ipAddress` set to `X` and send it with the `isValid` field set to `True`.  

To create a serialized object, we'll name it `serialize.php` and paste the first three lines of the code.  
![Pasted image 20260128200556](/VaultSite/wiki-images/Pasted%20image%2020260128200556.png)  
Where the IP is defined, we'll add a `;` and a reverse shell to our machine, and set `isValid` to `True`.  
![Pasted image 20260128200706](/VaultSite/wiki-images/Pasted%20image%2020260128200706.png)  

We'll create the serialized data by exploiting the `PingTest` class and URL-encode it, as we saw in Burp.  
This is our object:  
![Pasted image 20260128200924](/VaultSite/wiki-images/Pasted%20image%2020260128200924.png)  

![Pasted image 20260128201034](/VaultSite/wiki-images/Pasted%20image%2020260128201034.png)  
So, when the server processes the object and reaches the ping section, it will take whatever is in the `ipAddress` field—which contains our reverse shell. The server will execute `ping -c 3` to nothing (since we didn't specify a valid IP), but after the `;`, it will execute the shell.  

Let's take our URL-encoded object, send it via Burp, and listen on port `443`.  
![Pasted image 20260128201418](/VaultSite/wiki-images/Pasted%20image%2020260128201418.png)  
![Pasted image 20260128201513](/VaultSite/wiki-images/Pasted%20image%2020260128201513.png)  
![Pasted image 20260128201522](/VaultSite/wiki-images/Pasted%20image%2020260128201522.png)  
This is a PHP deserialization attack.  

There's another type, Node.js:  
https://opsecx.com/index.php/2017/02/08/exploiting-node-js-deserialization-bug-for-remote-code-execution/  

### 3. What is an IIFE?  

It's a function that is **created and executed immediately**.  

- **Its main purpose:** To create a privacy "bubble." Everything that happens inside the IIFE stays there and doesn't interfere with the rest of the program.