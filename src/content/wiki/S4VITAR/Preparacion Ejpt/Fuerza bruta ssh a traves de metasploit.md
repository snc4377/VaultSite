For this we'll use the Metasploit ssh_login module  
![[Pasted image 20260404175531.png]]  
![[Pasted image 20260404175538.png]]  
For this module, the parameters to edit are pass_file (the dictionary we'll use, rockyou.txt), rhosts (the remote machine's IP we now see), and we'll set username to root  
![[Pasted image 20260404175754.png]]  
Then with run we start it working  
![[Pasted image 20260404175825.png]]  

If we wanted to use Hydra, we'd do port forwarding for port 22 like we did with port 80 in [[Pivoting with Metasploit and host discovery]]  

![[Pasted image 20260404180006.png]]  
This module automatically opens a separate session that we can view and select with sessions  
![[Pasted image 20260404180101.png]]  
![[Pasted image 20260404180112.png]]  

And now if we wanted, we could forward port 22 to our local port 2222 and connect via SSH directly from our Kali terminal without going through Meterpreter  
![[Pasted image 20260404180322.png]]  
![[Pasted image 20260404180352.png]]
