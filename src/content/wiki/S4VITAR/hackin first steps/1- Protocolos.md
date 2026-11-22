

TCP - Guarantees data delivery and that the order matches the transmission sequence  
	-Three way handshake SYN ACK ACK ACK (WE WILL ALWAYS SEE THESE THREE PACKETS WHEN CONNECTING VIA TCP)
![[Pasted image 20251120182141.png]]

UDP - Sends data blindly without any verification  
TCP 
-------------------
21 - ftp file transfer  
22 - ssh connection requiring username and password  
23 - Telnet allows remote machine access as if physically present  
25 SMTP - email sending and receiving  
53 - dns  
80 - http  
443 - https  
110 - POP3  
139, 445 - SMB shared file/printer access or Windows network resources (SMB Relay hijacks legitimate user authentication to redirect credentials to a different system/resource![[Pasted image 20251120182849.png]])  
143 - IMAP  


UDP
--------------
53 - DNS  
67/68 - DHCP  
69 - TFTP FTP BUT OVER UDP  
123 - **NTP** (Network Time Protocol) – a protocol for synchronizing device clocks on a network.  
161 - SNMP a protocol for managing and monitoring network devices.  

IP calculation tool  
https://www.ipaddressguide.com/cidr



