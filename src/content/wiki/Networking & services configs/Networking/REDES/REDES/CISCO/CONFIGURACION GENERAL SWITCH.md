---
title: "CONFIGURACION GENERAL SWITCH"
category: ["Networking & services configs", "Networking", "REDES", "REDES", "CISCO", "CONFIGURACION GENERAL SWITCH"]
---


Note title: GENERAL SWITCH CONFIGURATION

Create the VLANs
vlan 10
name students
exit

vlan 20
name teachers
exit

vlan 30
name staff
exit

vlan 99
name management
exit

exit
------------------------------------------------
Switch:
interface range fa0/13 - 24
switchport mode access
exit
interface range fa0/5 - 8
switchport mode access
switchport access vlan 20
exit
interface range fa0/9 - 12
switchport mode access
switchport access vlan 30
exit
switchport mode trunk
------------------------------------------------
Switch 1
interface range fa0/1-20
switchport mode access
switchport access vlan 40
exit
interface gig0/26
switchport mode trunk
------------------------------------------------
Switch2
interface range fa0/1-20
switchport mode access
switchport access vlan 20
exit
interface gig0/26
switchport mode trunk
------------------------------------------------
Switch3
interface range fa0/1-10
switchport mode access
switchport access vlan 10
exit
interface range fa0/11-22
switchport mode access
switchport access vlan 30
exit
------------------------------------------------
To copy switch configuration
show running-config
copy the configuration and paste it
-------------------------------------------------
Subnetting
Administrative (VLAN 10):
Number of users: 30
Subnet: 192.168.10.0/27
Address range: 192.168.10.1 to 192.168.10.30
Subnet mask: 255.255.255.224

Marketing (VLAN 20):
Number of users: 60
Subnet: 192.168.20.0/26
Address range: 192.168.20.1 to 192.168.20.62
Subnet mask: 255.255.255.192

Sales (VLAN 30):
Number of users: 36
Subnet: 192.168.30.0/26
Address range: 192.168.30.1 to 192.168.30.62
Subnet mask: 255.255.255.192

Production (VLAN 40):
Number of users: 45
Subnet: 192.168.40.0/26
Address range: 192.168.40.1 to 192.168.40.62
Subnet mask: 255.255.255.192

Management (VLAN 50):
Number of users: 6
Subnet: 192.168.50.0/29
Address range: 192.168.50.1 to 192.168.50.6
Subnet mask: 255.255.255.248
--------------------------------------------------
DHCP
interface gig0/0.50
 encapsulation dot1Q 50
 ip address 192.168.50.1 255.255.255.248
 ip dhcp pool Management
  network 192.168.50.0 255.255.255.248
  default-router 192.168.50.1
  dns-server 8.8.8.8
 exit
--------------------------------------------------