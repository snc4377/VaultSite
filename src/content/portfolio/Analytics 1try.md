---
title: "Analytics 1try"
category: ["Analytics 1try"]
---

Note title: Analytics 1try

- We run nmap as usual  
- ![Pasted image 20240306203043](/VaultSite/wiki-images/Pasted%20image%2020240306203043.png)
- We add the IP and domain name to /etc/hosts with `echo "machine_ip machine_name" | sudo tee -a /etc/hosts`  
![Pasted image 20240306203205](/VaultSite/wiki-images/Pasted%20image%2020240306203205.png)
- We see there's a subpage for registration, we add it to the /etc/hosts file  
	- On Google, we search for possible exploits related to Metabase and find this Remote Code Execution exploit [[CVE]]  
- The exploit tells us the first step is to retrieve the setup token by navigating to [http://vulnerablehost.com/api/session/properties](http://vulnerablehost.com/api/session/properties)  
- ![Pasted image 20240306204536](/VaultSite/wiki-images/Pasted%20image%2020240306204536.png)  
- Token  
- ![Pasted image 20240306204551](/VaultSite/wiki-images/Pasted%20image%2020240306204551.png)  
- Now that we have the token, we searched how to use it and found a section on GitHub explaining the process [GitHub](https://github.com/securezeron/CVE-2023-38646)  
- ![Pasted image 20240306204817](/VaultSite/wiki-images/Pasted%20image%2020240306204817.png)  
- This shows the token we found earlier was already preconfigured  
- ![Pasted image 20240306205651](/VaultSite/wiki-images/Pasted%20image%2020240306205651.png) 