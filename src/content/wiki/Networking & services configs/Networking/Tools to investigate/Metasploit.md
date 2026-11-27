---
title: "Metasploit"
category: ["Networking & services configs", "Networking", "Tools to investigate", "Metasploit"]
---

Note title: Metasploit

Everything we've done before was done manually, and Metasploit does it all automatically.

**Metasploit** is a penetration testing platform (Penetration Testing Framework) used to conduct security testing on systems and applications. This platform is widely used by security researchers, pentesters, and security professionals to discover vulnerabilities and perform vulnerability exploitation testing. Metasploit is built on a set of security tools that include an exploit development framework, a vulnerability database engine, and a collection of vulnerability exploitation modules.

In practical terms, Metasploit is used to test the security of a system or application by performing penetration tests, with the goal of identifying and exploiting security vulnerabilities. To achieve this, Metasploit provides a vast array of exploits, payloads, and post-exploitation modules that security professionals can use to identify and exploit vulnerabilities. By using Metasploit, security professionals can simulate real attacks and discover vulnerabilities in systems and applications before malicious attackers can, allowing them to patch the vulnerabilities and improve their systems' security.

BASIC METASPLOIT GUIDES  
https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/metasploit

https://www.offsec.com/metasploit-unleashed/msfconsole/

**Example and practical Metasploit cases**

In this lab, we have a Windows 7 machine as the victim, and we will exploit a buffer overflow in SLMAIL.

To start Metasploit, we use `msfdb run` or, if not available, `msfconsole`.  
![Pasted image 20260313140429](/VaultSite/wiki-images/Pasted%20image%2020260313140429.png)  
Here we see it loading many things: exploits, auxiliary modules, etc. If we go to `/usr/share/metasploit-framework`, we can see where it pulls these resources from (here, by searching, we can find scripts, payloads, etc.).

A handy feature of Metasploit is the ability to create workspaces to switch between different tasks. This is very useful when working with multiple machines, as it helps with organization.  
![Pasted image 20260313141146](/VaultSite/wiki-images/Pasted%20image%2020260313141146.png)

Within Metasploit, we can use `SEARCH` to look for keywords—for example, to perform an ARP scan from Metasploit instead of the terminal.  
![Pasted image 20260313140901](/VaultSite/wiki-images/Pasted%20image%2020260313140901.png)  
Here we see an `auxiliary/scanner`.

We can also use filters like `platform` (in this filter, we specify the operating system, and it shows us all available related actions).  
![Pasted image 20260313141415](/VaultSite/wiki-images/Pasted%20image%2020260313141415.png)  
![Pasted image 20260313141419](/VaultSite/wiki-images/Pasted%20image%2020260313141419.png)  
![Pasted image 20260313141441](/VaultSite/wiki-images/Pasted%20image%2020260313141441.png)

And if we add the `type` filter, we can refine the results to show only the type we want.  
![Pasted image 20260313141531](/VaultSite/wiki-images/Pasted%20image%2020260313141531.png)  
Once we've chosen what to use, we enter the `USE` command followed by the path.  
![Pasted image 20260313141625](/VaultSite/wiki-images/Pasted%20image%2020260313141625.png)  
Running `show options` after selecting the resource will display the parameters required for the script to work.  
![Pasted image 20260313141710](/VaultSite/wiki-images/Pasted%20image%2020260313141710.png)  
There are also advanced options.  
![Pasted image 20260313141913](/VaultSite/wiki-images/Pasted%20image%2020260313141913.png)  
Using the `SET` command followed by the field name, we fill in the required fields.  
![Pasted image 20260313142022](/VaultSite/wiki-images/Pasted%20image%2020260313142022.png)  
To execute it, we simply run `run`.  
![Pasted image 20260313142040](/VaultSite/wiki-images/Pasted%20image%2020260313142040.png)  

After performing the ARP scan, if we use the `hosts` option, we can see the different devices it has detected.  
![Pasted image 20260313142155](/VaultSite/wiki-images/Pasted%20image%2020260313142155.png)  
We see that it doesn't provide additional information, but the advantage is that we can use multiple tools.  
Here, from the terminal, we would run an `nmap` scan with `-sS --min-rate 5000 -Pn -n -p- --open` and `-oX Allports` to save the results in an XML file.  
![Pasted image 20260313142443](/VaultSite/wiki-images/Pasted%20image%2020260313142443.png)  

We could then import that XML into Metasploit.  
![Pasted image 20260313142507](/VaultSite/wiki-images/Pasted%20image%2020260313142507.png)  
Now we see it has more information.  
![Pasted image 20260313142535](/VaultSite/wiki-images/Pasted%20image%2020260313142535.png)  
So, with `nmap`, we can perform scans to gather information and then import it into Metasploit.

After completing all this, we've identified an SLMAIL service.  

Let's see what Metasploit has for that.  
![Pasted image 20260313142819](/VaultSite/wiki-images/Pasted%20image%2020260313142819.png)  

We see a `check` section. If it says `YES`, it allows us to launch the exploit only to test if the machine is vulnerable, without leaving traces or executing the script.  

Let's configure the exploit.  
![Pasted image 20260313143009](/VaultSite/wiki-images/Pasted%20image%2020260313143009.png)  
Now we run `exploit` and see that we have access—it has already performed the buffer overflow.  
![Pasted image 20260313143316](/VaultSite/wiki-images/Pasted%20image%2020260313143316.png)  

Once inside the machine, we have many options beyond what we can do manually by searching through directories.  
![Pasted image 20260313144026](/VaultSite/wiki-images/Pasted%20image%2020260313144026.png)  

Another interesting feature in Windows systems is that `hashdump` will give us the hashes of the system users, which we can use for Pass-the-Hash—meaning we can crack them to see the password.  
But in Windows, the interesting part is that using the `psexec` tool with the `-hashes :NThash` parameter, we can get a remote command prompt.  
![Pasted image 20260313144506](/VaultSite/wiki-images/Pasted%20image%2020260313144506.png)  

We could also launch `mimikatz` to check for credentials in memory. We would do this by loading the `kiwi` module.  
![Pasted image 20260313144638](/VaultSite/wiki-images/Pasted%20image%2020260313144638.png)  
![Pasted image 20260313144705](/VaultSite/wiki-images/Pasted%20image%2020260313144705.png)  
And with `psexec`, we could log in with the password.  
![Pasted image 20260313144749](/VaultSite/wiki-images/Pasted%20image%2020260313144749.png)
