---
title: "Headless"
category: ["Headless"]
---



- We run an nmap scan
![Pasted image 20240409195907](/VaultSite/wiki-images/Pasted%20image%2020240409195907.png)
- Now we try to connect to the web page, but it doesn't allow us, so we try adding the port at the end of the IP
![Pasted image 20240409200038](/VaultSite/wiki-images/Pasted%20image%2020240409200038.png)
- Next, we run a dirsearch to find additional directories for more information
![Pasted image 20240409200157](/VaultSite/wiki-images/Pasted%20image%2020240409200157.png)
- We don't see anything interesting except a support directory, but on the web page, we try to implement a payload
![Pasted image 20240409200445](/VaultSite/wiki-images/Pasted%20image%2020240409200445.png)
![Pasted image 20240409200516](/VaultSite/wiki-images/Pasted%20image%2020240409200516.png)
- Now, with Burp Suite, we intercept it and place the payload at the end and in the User-Agent
![Pasted image 20240409203539](/VaultSite/wiki-images/Pasted%20image%2020240409203539.png)
- At the same time, we need to set up a Python3 server on port 80 in the terminal to listen and pass us the admin's cookies
![Pasted image 20240409203528](/VaultSite/wiki-images/Pasted%20image%2020240409203528.png)
- Now we inspect the page and go to the Storage section, where we find the cookie currently in use. We need to replace it with the new one, which is the admin's cookie, to gain permissions and access the dashboard
![Pasted image 20240409203739](/VaultSite/wiki-images/Pasted%20image%2020240409203739.png)
- Perfect, what previously showed an error message has now turned into this
![Pasted image 20240409203919](/VaultSite/wiki-images/Pasted%20image%2020240409203919.png)
- Now we intercept again with Burp Suite
![Pasted image 20240409204319](/VaultSite/wiki-images/Pasted%20image%2020240409204319.png)
- We see that if we add `; ls` at the end, it shows the documents, or `whoami` tells us who we are, etc.
![Pasted image 20240409204416](/VaultSite/wiki-images/Pasted%20image%2020240409204416.png)
- We need to create a `shell.sh` to execute it with bash
![Pasted image 20240409215758](/VaultSite/wiki-images/Pasted%20image%2020240409215758.png)
- Once created, we add this line at the end of the Burp Suite code
![Pasted image 20240409215859](/VaultSite/wiki-images/Pasted%20image%2020240409215859.png)
- Now, in the terminal, we set up netcat to listen before sending anything, and we also start a Python3 server on port 80. IMPORTANT: netcat and Python3 must be started in the same location where the shell is
![Pasted image 20240409220028](/VaultSite/wiki-images/Pasted%20image%2020240409220028.png)
- Now that we're in, we run `sudo -l` to start privilege escalation
- After some analysis, we see there's a manipulable file `initdb.sh`
![Pasted image 20240409220916](/VaultSite/wiki-images/Pasted%20image%2020240409220916.png)
- If we analyze the file, we find that it's manipulating a filename `initdb.sh`.
- Well, we can create the file by changing the permissions of bash with the bit for our users and then execute `syscheck`.
![Pasted image 20240409221440](/VaultSite/wiki-images/Pasted%20image%2020240409221440.png)
- Now all that's left is to search for the flags by running `cd /root` for the root flag and `cd` simply for the user flag. 