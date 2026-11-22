

Note title: Untitled

Attacker machine IP 192.168.100.5



Machine 1 Windows Has Apache and a db server OS Name:                   Microsoft Windows Server 2012 R2 Standard

192.168.100.50
80 http, 135  msrpc ,139  netbios-ssn , 445  microsoft-ds , 3307  opsession-prxy , 3389  ms-wbt-server135 , 5985 , 47001 , 49152 , 49153 , 49154 , 49155 , 49156 , 49178

Entry via phpmyadmin mariadb root with no password   we found WordPress admin credentials: estrella

When accessing WordPress, we edit the 404.php template and insert a shell to gain remote access to the system 

Interface: 192.168.100.50 --- 0xc
  Internet Address      Physical Address      Type
  169.254.169.254       02-dd-4d-a6-d6-2f     dynamic   
  192.168.100.1         02-dd-4d-a6-d6-2f     dynamic   
  192.168.100.5         02-77-fa-58-6a-7f     dynamic   
  192.168.100.255       ff-ff-ff-ff-ff-ff     static    
  224.0.0.22            01-00-5e-00-00-16     static    
  224.0.0.252           01-00-5e-00-00-fc     static    
  255.255.255.255       ff-ff-ff-ff-ff-ff     static    


User mike:diamond     flag a46be65770984ec0825f061aa6578bdd
![[Pasted image 20260410193341.png]]


Machine 2 WINSERVER02   Microsoft Windows Server 2012 R2 Standard      ftp anonymous

192.168.100.51
PORT      STATE SERVICE
21/tcp    open  ftp
80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
5985/tcp  open  wsman
47001/tcp open  winrm
![[Pasted image 20260410190316.png]]





Machine 3 
192.168.100.52  Apache db server  ftp anon drupal  linux
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
25/tcp   open  smtp
80/tcp   open  http
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3306/tcp open  mysql
3389/tcp open  ms-wbt-server

admin:
dbadmin:sayang
Vincenzo:789456
auditor:qwertyuiop







Machine 4 Windows Server 2019   
192.168.100.55
PORT      STATE SERVICE
80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
5985/tcp  open  wsman
47001/tcp open  winrm


Greetings gents!

I have setup this server to host our production services.
I will be sharing changelogs and updates on the HTTP File Server.

So far this server does not have any running services, as a result, you must login via RDP or SMB.

- Administrator:swordfish


Ethernet adapter Ethernet:

   Connection-specific DNS Suffix  . : eu-central-1.compute.internal
   Link-local IPv6 Address . . . . . : fe80::8ce4:e9ba:2b0f:6753%8
   IPv4 Address. . . . . . . . . . . : 192.168.100.55
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.100.1

Ethernet adapter Ethernet 4:

   Connection-specific DNS Suffix  . : eu-central-1.compute.internal
   Link-local IPv6 Address . . . . . : fe80::d4b9:4c93:49f1:65b1%27
   IPv4 Address. . . . . . . . . . . : 192.168.0.50
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.0.1



User : mary:hotmama
  Hash NTLM: 11637a16fca11b3604e3e68d5221b3c7 
RID  : 000003f1 (1009)
User : lawrence:computadora
  Hash NTLM: 18aa104784f77431563b1a1b67f6096c
RID  : 000003f0 (1008)
User : student:
  Hash NTLM: bd4ca1fbe028f3c5066467a7f6a73b0b
RID  : 000001f8 (504)
User : WDAGUtilityAccount:
  Hash NTLM: 58f8e0214224aebc2c5f82fb7cb47ca1
RID  : 000001f4 (500)
User : Administrator:swordfish
  Hash NTLM: 61fb34469b9989b01be4e8630c52eed6



Machine 5  windows 
192.168.100.63
PORT     STATE SERVICE
3389/tcp open  ms-wbt-server
5985/tcp open  wsman



Machine 6  linux 
192.168.100.67
PORT   STATE SERVICE
22/tcp open  ssh




New machines 

192.168.0.51 Ubuntu Apache
80 
22
3389


192.168.0.57 linux 
22


192.168.0.61 windows

5985
3389