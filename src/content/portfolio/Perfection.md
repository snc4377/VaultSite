---
title: "Perfection"
category: ["Perfection"]
---


- We start by running `nmap -sV -sV -O ip`
- Then we add the name and IP to `/etc/hosts`
- We see on the page that it uses Webrick 1.7.0, but we don't find any exploit for this version with searchsploit. However, we do find an exploit for Ruby that is associated with it.
- ![Pasted image 20240318190654](/VaultSite/wiki-images/Pasted%20image%2020240318190654.png)
- ![Pasted image 20240320192752](/VaultSite/wiki-images/Pasted%20image%2020240320192752.png)
- ![Pasted image 20240318192535](/VaultSite/wiki-images/Pasted%20image%2020240318192535.png)
- We will use FFuF, which is used to discover directories and subdomains, and then with fuzz, which sends random inputs to an application to make it fail. We use the FFuF tool to perform a brute force scan on a web application and use the path where the passwords are located to test.
- ![Pasted image 20240320185402](/VaultSite/wiki-images/Pasted%20image%2020240320185402.png)
- Now we search for an exploit again with Ruby and we have this:
- ![Pasted image 20240320190523](/VaultSite/wiki-images/Pasted%20image%2020240320190523.png)
- Now with FoxyProxy and Burp Suite, we intercept the questionnaire we sent on the page.
- ![Pasted image 20240320192032](/VaultSite/wiki-images/Pasted%20image%2020240320192032.png)
- ![Pasted image 20240320192356](/VaultSite/wiki-images/Pasted%20image%2020240320192356.png)
- We will try to insert scripts into what we intercepted.
- ![Pasted image 20240326105433](/VaultSite/wiki-images/Pasted%20image%2020240326105433.png)
- We have placed the message that appears when the script is blocked in the bottom right search bar so that when it works, we don't have to search for whether it appears or not.
- ![Pasted image 20240326105633](/VaultSite/wiki-images/Pasted%20image%2020240326105633.png)
- Now it lets us pass.
- ![Pasted image 20240326110448](/VaultSite/wiki-images/Pasted%20image%2020240326110448.png)
- We had to encrypt the script with right-click > Convert Selection > URL > Encode Key Characters.
- Now in the script, we will replace things like `7*7` with `ls` to show permissions and directories.
- ![Pasted image 20240326110847](/VaultSite/wiki-images/Pasted%20image%2020240326110847.png)
- Now we run `tcpdump` (which is used to view ICMP traffic on the specified port).
- ![Pasted image 20240326111022](/VaultSite/wiki-images/Pasted%20image%2020240326111022.png)
- Now in the script, we make a ping, and if everything is correct, we should receive it with `tcpdump`.
- ![Pasted image 20240326111337](/VaultSite/wiki-images/Pasted%20image%2020240326111337.png)
- We run `which bash python3`.
- ![Pasted image 20240326111604](/VaultSite/wiki-images/Pasted%20image%2020240326111604.png)
- Now comes the important step: we go to a page that creates reverse shells and create one with Python3 and the IP and port we want.
- ![Pasted image 20240326111842](/VaultSite/wiki-images/Pasted%20image%2020240326111842.png)
- We copy it into Burp Suite and encode it (only the key characters).
- ![Pasted image 20240326112036](/VaultSite/wiki-images/Pasted%20image%2020240326112036.png)
- We can't, we don't know why, so we check, and the problem was that the firewall was blocking the port connections. So we add the rules, save them, and now we can connect without issues.
- Before executing the reverse shell we created above, we need to listen on port 9001 with `nc -lvnp`.
- Once inside, we stabilize the shell with:
  ```
  python3 -c 'import pty;pty.spawn("/bin/bash")'
  export TERM=xterm
  ctrl + z
  stty raw -echo; fg
  ```
- ![Pasted image 20240326174459](/VaultSite/wiki-images/Pasted%20image%2020240326174459.png)
- We retrieve the user flag by searching a bit.
- ![Pasted image 20240326174706](/VaultSite/wiki-images/Pasted%20image%2020240326174706.png)
- Now it's time to escalate privileges, and we will use SQLite because we found a DB file in the Migration directory that might be written in SQLite.
- To start, we need to be in the previously mentioned directory and open SQLite.
- ![Pasted image 20240326175514](/VaultSite/wiki-images/Pasted%20image%2020240326175514.png)
- Here we can see that we used it to extract 4 more users besides the one we already had, along with all their hashes.
- With the help of Hash Identifier, which will give us the hash type, and `linpeas.sh` to exploit it, we will crack them to escalate privileges.
- Now we will exploit Susan's hash with Hashcat.
- ![Pasted image 20240326181845](/VaultSite/wiki-images/Pasted%20image%2020240326181845.png)
- ![Pasted image 20240326181920](/VaultSite/wiki-images/Pasted%20image%2020240326181920.png)
- Now with the same command we just used, we add `--show` at the end, and it shows us the password of the hash (i.e., Susan's password to perform privilege escalation).
- ![Pasted image 20240326183612](/VaultSite/wiki-images/Pasted%20image%2020240326183612.png)
- And we're done. Now we just need to run `sudo su`, enter the password, and start searching.
- ![Pasted image 20240326183712](/VaultSite/wiki-images/Pasted%20image%2020240326183712.png)
