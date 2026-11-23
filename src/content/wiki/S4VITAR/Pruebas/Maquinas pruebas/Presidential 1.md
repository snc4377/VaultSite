We performed an nmap scan with -sS on all ports of the machine  
![Pasted image 20260313154237](/VaultSite/wiki-images/Pasted%20image%2020260313154237.png)

We see port 80 and port 2082, so we'll scan them with the parameters -sC -sV  
![Pasted image 20260313154403](/VaultSite/wiki-images/Pasted%20image%2020260313154403.png)

Now with whatweb or wappalyzer, we'll check what services the web uses  
![Pasted image 20260313154437](/VaultSite/wiki-images/Pasted%20image%2020260313154437.png)  
![Pasted image 20260313154538](/VaultSite/wiki-images/Pasted%20image%2020260313154538.png)  
We'll try enumerating directories with gobuster to see if we find anything interesting  
![Pasted image 20260313154622](/VaultSite/wiki-images/Pasted%20image%2020260313154622.png)  
But we don't see anything, so we'll add --add-slash to append a trailing slash and see if that improves visibility  

![Pasted image 20260313154714](/VaultSite/wiki-images/Pasted%20image%2020260313154714.png)  
We see a cgi-bin, so we could attempt a shell shock, but that's not the vulnerability this machine is looking for  

Let's also try listing PHP files  
![Pasted image 20260313154842](/VaultSite/wiki-images/Pasted%20image%2020260313154842.png)  
We find a config.php, but accessing it shows nothing  
![Pasted image 20260313154906](/VaultSite/wiki-images/Pasted%20image%2020260313154906.png)  

Since directory enumeration didn't work, we'll try listing subdomains with the vhost parameter  
![Pasted image 20260313155035](/VaultSite/wiki-images/Pasted%20image%2020260313155035.png)  
We find a subdomain and add it to /etc/hosts  

Upon accessing it, we see a PhpMyAdmin where we test credentials, but none work  
![Pasted image 20260313155128](/VaultSite/wiki-images/Pasted%20image%2020260313155128.png)  

We'll list files again to see if we find other file types  
![Pasted image 20260313155242](/VaultSite/wiki-images/Pasted%20image%2020260313155242.png)  
We find a config.php.bak, and upon accessing it, we see something interesting: credentials  
![Pasted image 20260313155324](/VaultSite/wiki-images/Pasted%20image%2020260313155324.png)  

We try reusing these passwords and successfully gain access  

![Pasted image 20260313155358](/VaultSite/wiki-images/Pasted%20image%2020260313155358.png)  
Here we see that the PhpMyAdmin version is 4.8.1 and outdated, so we'll check for related CVEs  
![Pasted image 20260313155517](/VaultSite/wiki-images/Pasted%20image%2020260313155517.png)  
We have several options. We notice this vulnerability uses an LFI to escalate to RCE  

Analyzing the first LFI script, we see a Directory Path Traversal allowing file access  
![Pasted image 20260313155644](/VaultSite/wiki-images/Pasted%20image%2020260313155644.png)  
And reviewing the RCE Python script, it uses the same logic to execute code by targeting /var/lib/php/session and the session ID  
![Pasted image 20260313160118](/VaultSite/wiki-images/Pasted%20image%2020260313160118.png)  
We remove the Windows part and attempt to list /etc/passwd  
![Pasted image 20260313155723](/VaultSite/wiki-images/Pasted%20image%2020260313155723.png)  
It works, and we also see in /etc/passwd that the admin user has a valid bash shell. We check if the admin user has an id_rsa public key for SSH on port 2082, but nothing is found  
![Pasted image 20260313161058](/VaultSite/wiki-images/Pasted%20image%2020260313161058.png)  

We check internally open ports by examining /proc/net/tcp  
![Pasted image 20260313160231](/VaultSite/wiki-images/Pasted%20image%2020260313160231.png)  
![Pasted image 20260313160258](/VaultSite/wiki-images/Pasted%20image%2020260313160258.png)  
We see port 3306 (MySQL) is open internally  

We also check running processes via /proc/sched_debug  
![Pasted image 20260313160514](/VaultSite/wiki-images/Pasted%20image%2020260313160514.png)  
Nothing useful here, but sometimes we can find binaries or applications to research for typical paths, potentially locating configuration files readable via LFI  

Given this, we consider that Apache is running in the background, and a common RCE method is [[Log Poisoning]]. We attempt to target /var/log/apache2/access.log, but it fails. We try the SSH log /var/log/auth.log, but no luck  
![Pasted image 20260313161025](/VaultSite/wiki-images/Pasted%20image%2020260313161025.png)  

As seen in the exploit, we can target /var/lib/session/sess with our session ID  
![Pasted image 20260313161153](/VaultSite/wiki-images/Pasted%20image%2020260313161153.png)  

In storage, we find our session ID  
![Pasted image 20260313161259](/VaultSite/wiki-images/Pasted%20image%2020260313161259.png)  

Now we attempt to gain a reverse shell.  
Under the SQL tab, we try embedding a system call within a SELECT statement to execute a reverse shell  
![Pasted image 20260313161759](/VaultSite/wiki-images/Pasted%20image%2020260313161759.png)  
If executed and the system function exists, this should establish a reverse shell. However, this PHP code won't be interpreted directly.  
But through the LFI, if we point to our session ID as if it were a file, it will interpret the PHP code.  

So we copy the line from the exploit, insert our session ID, and get the reverse shell.  
![Pasted image 20260313162336](/VaultSite/wiki-images/Pasted%20image%2020260313162336.png)  

This works because the session stores all session-related data, and the LFI from index.php can interpret it. With other file types, this wouldn't work.  

Once inside, we find an admin user.  

Earlier, while reviewing the PhpMyAdmin panel, we found bcrypt-encrypted admin credentials  
![Pasted image 20260313162827](/VaultSite/wiki-images/Pasted%20image%2020260313162827.png)  

Cracking them with John and rockyou reveals the password is "Stella"  
![Pasted image 20260313163043](/VaultSite/wiki-images/Pasted%20image%2020260313163043.png)  
![Pasted image 20260313163050](/VaultSite/wiki-images/Pasted%20image%2020260313163050.png)  

Now we attempt privilege escalation. Running sudo -l, id, and checking SUID privileges shows nothing, but checking capabilities reveals an odd one: tarS  
![Pasted image 20260313163612](/VaultSite/wiki-images/Pasted%20image%2020260313163612.png)  
Examining it shows it's just a regular tar  
![Pasted image 20260313163655](/VaultSite/wiki-images/Pasted%20image%2020260313163655.png)  
Checking its associated capability, we see it allows reading files we shouldn't access  

We try compressing with tarS from the /tmp directory using -cvf to archive /root/.ssh, and BINGO  
![Pasted image 20260313164040](/VaultSite/wiki-images/Pasted%20image%2020260313164040.png)  

Now we just extract the tar and use the key to SSH as root on local port 2082  
![Pasted image 20260313164309](/VaultSite/wiki-images/Pasted%20image%2020260313164309.png)  
If the key were encrypted, we could use John's ssh2john script to convert it into a crackable hash. 