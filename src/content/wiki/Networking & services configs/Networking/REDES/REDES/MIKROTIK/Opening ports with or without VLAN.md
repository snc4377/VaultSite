---
title: "Opening Ports With Or Without VLAN"
category: ["Networking & services configs", "Networking", "REDES", "REDES", "MIKROTIK", "Opening ports with or without VLAN"]
---

# Opening Ports With Or Without VLAN

Imagine we want to open port 8006 to access Proxmox from outside, and we have Proxmox, for example, in VLAN 20, with the ISP router, a MikroTik router, and a MikroTik switch. Proxmox is in VLAN 20.

First, we will go to the MikroTik router and create a NAT rule:
![Pasted image 20240310163400](/VaultSite/wiki-images/Pasted%20image%2020240310163400.png)

![Pasted image 20240310163529](/VaultSite/wiki-images/Pasted%20image%2020240310163529.png)
In CHAIN, we will set dstnat.
In protocol, we will set TCP.
In dst port, we will set the service port, in my case it is 8006; if, for example, we had an FTP, we would set 21.
And in IN INTERFACE, we will set the interface through which we receive the IP on the MikroTik.

![Pasted image 20240310163808](/VaultSite/wiki-images/Pasted%20image%2020240310163808.png)
Now in Action, we will set dst-nat.
In TO ADDRESSES, the IP to which we want to redirect the port, in this case, the private IP of Proxmox is the one we see on the screen.
And in to ports, the port of Proxmox.

Finally, we will go to the ISP router configuration and specify that all traffic coming through the chosen port be redirected to the MikroTik router, meaning we will set the IP of the MikroTik router.
![Pasted image 20240310164046](/VaultSite/wiki-images/Pasted%20image%2020240310164046.png)
![Pasted image 20240310164140](/VaultSite/wiki-images/Pasted%20image%2020240310164140.png)

And if, for example, I enter the domain name associated with my IP, which in this case is provided by my MikroTik, + port 8006, which is Proxmox:
![Pasted image 20240310164303](/VaultSite/wiki-images/Pasted%20image%2020240310164303.png)