---
title: "Subinterfaces , Encapsultaion & DHCP ROUTER CISCO"
category: ["Networking & services configs", "Networking", "REDES", "REDES", "CISCO", "Subinterfaces , encapsultaion  & DHCP ROUTER CISCO"]
---

 # Subinterfaces, Encapsulation & DHCP on Cisco Routers

If the router only has one interface, the configuration line would look like this:  
  `interface FastEthernet0.10`

Example configuration:  
```
interface gigabitEthernet0/0.80  
encapsulation dot1Q 80  
ip address 172.80.0.1 255.255.0.0  
ip dhcp pool WIFI  
 network 172.80.0.0 255.255.0.0  
 default-router 172.80.0.1  
 dns-server 8.8.8.8  
exit
```
 