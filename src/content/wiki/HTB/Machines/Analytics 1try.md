---
title: "Analytics 1try"
category: ["HTB", "Machines", "Analytics 1try"]
---

# Analytics 1try

- We run nmap as usual  
- ![Pasted image 20240306203043](/VaultSite/wiki-images/Pasted%20image%2020240306203043.png)  
- Add the IP and domain name to /etc/hosts using `echo "ip_machine machine_name" | sudo tee -a /etc/hosts`  
![Pasted image 20240306203205](/VaultSite/wiki-images/Pasted%20image%2020240306203205.png)  
- We see there's a subpage for registration, so we add it to the /etc/hosts file.  
	- On Google, we search for possible exploits related to Metabase and find this Remote Code Execution (RCE) exploit [[CVE]].  
- The exploit tells us that the first step is to retrieve the setup token by navigating to [http://vulnerablehost.com/api/session/properties](http://vulnerablehost.com/api/session/properties), which will give us the setup token.  
- ![Pasted image 20240306204536](/VaultSite/wiki-images/Pasted%20image%2020240306204536.png)  
- Token:  
- ![Pasted image 20240306204551](/VaultSite/wiki-images/Pasted%20image%2020240306204551.png)  
- Now that we have the token, we searched for how to use it and found a section on GitHub that explains it: [GitHub](https://github.com/securezeron/CVE-2023-38646).  
- ![Pasted image 20240306204817](/VaultSite/wiki-images/Pasted%20image%2020240306204817.png)  
- This shows that the token we found earlier was already prepared.  
- ![Pasted image 20240306205651](/VaultSite/wiki-images/Pasted%20image%2020240306205651.png) 