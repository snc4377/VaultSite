---
title: "Enumeracion De Wordpress"
category: ["S4VITAR", "Preparacion Ejpt", "Enumeracion de Wordpress"]
---

Important for this exam  
When a website is using virtual hosting as shown here  
![Pasted image 20260401161425](/VaultSite/wiki-images/Pasted%20image%2020260401161425.png)  

The site will appear broken like this  
![Pasted image 20260401161333](/VaultSite/wiki-images/Pasted%20image%2020260401161333.png)  

We just need to edit /etc/hosts and add the domain name with its IP  
![Pasted image 20260401161458](/VaultSite/wiki-images/Pasted%20image%2020260401161458.png)  

Before using any tools, we'd go to wp-login and test some credentials, credential reuse, etc.  

**WPSCAN TOOL**  

With this tool we can perform multiple actions like:  

Brute-forcing specific users with a dictionary  
![Pasted image 20260401162538](/VaultSite/wiki-images/Pasted%20image%2020260401162538.png)  

We can also run a basic scan to enumerate versions and plugins  
![Pasted image 20260401162649](/VaultSite/wiki-images/Pasted%20image%2020260401162649.png)  
![Pasted image 20260401162659](/VaultSite/wiki-images/Pasted%20image%2020260401162659.png)  

With searchsploit we'd check the plugins for known vulnerabilities in their versions. We could also search Exploit DB for more comprehensive results.  

![Pasted image 20260401162840](/VaultSite/wiki-images/Pasted%20image%2020260401162840.png)  
Using -m downloads the exploit  

Following the script we found with wpscan, we'd then view /etc/passwd  
![Pasted image 20260401163052](/VaultSite/wiki-images/Pasted%20image%2020260401163052.png)  

Here we could attempt an LFI to RCE or try listing RSA keys for the user 'helios' we saw earlier  
![Pasted image 20260401163332](/VaultSite/wiki-images/Pasted%20image%2020260401163332.png)
