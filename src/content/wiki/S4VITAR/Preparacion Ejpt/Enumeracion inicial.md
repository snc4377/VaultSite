Note title: Untitled

nmaIt's very important to create folders to keep everything organized by machines, and we'll use https://excalidraw.com/ to organize a diagram or draw.io

Step 1  
Use `ip a` to view our interfaces and see which networks we can reach from our machine

Step 2  
Reconnaissance with nmap. We'll scan the networks we identified with `ip a`. We'll use the `-sn` parameter to perform a ping scan to check connectivity

Step 3  
We'll perform a massive port scan for all IPs we see, or we can do them one by one if preferred.  
With `nmap -sS --min-rate 5000 -p- --open ips_to_scan -oN filename.txt`  
![Pasted image 20260401151421](/VaultSite/wiki-images/Pasted%20image%2020260401151421.png)  
IMPORTANT: Some exam machines may not be vulnerable and are just rabbit holes to waste time - they contain nothing  

Step 4  
Now that we have the file, we'll see which ports each machine has open and perform a customized nmap scan to detect service versions  
![Pasted image 20260401151914](/VaultSite/wiki-images/Pasted%20image%2020260401151914.png)  

We can use `grep` to extract only the ports from the file and separate them with commas. This helps us see all detected ports and include them in the version scan to avoid missing any (though we could also check manually and scan each host individually or scan all machines)  
![Pasted image 20260401152440](/VaultSite/wiki-images/Pasted%20image%2020260401152440.png)  
Add the `--open` flag to this nmap command because otherwise it will try all ports on all hosts even if the port isn't open on that host, which will clutter the output  

Save the output to a new file  
![Pasted image 20260401152644](/VaultSite/wiki-images/Pasted%20image%2020260401152644.png)  
For example, we see a machine where we can identify the hostname, so we add it to the diagram. It would also be good to add each machine's ports to the diagram.

