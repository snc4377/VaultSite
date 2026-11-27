---
title: "Vlan Encapsulation"
category: ["Networking & services configs", "Networking", "REDES", "REDES", "MIKROTIK", "Vlan Encapsulation"]
---

# Vlan Encapsulation

To create VLANs, go here:
![Pasted image 20240205130924](/VaultSite/wiki-images/Pasted%20image%2020240205130924.png)

Here we create the VLAN in VLAN ID and select the port where we want the VLAN to be created. This is useful when working with a switch that has the same VLANs.
For example, we create a switch with VLAN100 and VLAN200. In MikroTik, we do the same and assign the VLANs to ether2. Then, on the switch, we set a port to trunk mode, connect it to the MikroTik interface where we created the VLANs, and set up DHCP, for example. The MikroTik will assign IPs to devices in those VLANs.
![Pasted image 20240205131235](/VaultSite/wiki-images/Pasted%20image%2020240205131235.png)

Next, we assign an IP to the VLAN, both in MikroTik and on the switch.
![Pasted image 20240205131645](/VaultSite/wiki-images/Pasted%20image%2020240205131645.png)

We set up DHCP for the VLAN.
![Pasted image 20240205131859](/VaultSite/wiki-images/Pasted%20image%2020240205131859.png)
![Pasted image 20240205131913](/VaultSite/wiki-images/Pasted%20image%2020240205131913.png)
![Pasted image 20240205131935](/VaultSite/wiki-images/Pasted%20image%2020240205131935.png)
![Pasted image 20240205132002](/VaultSite/wiki-images/Pasted%20image%2020240205132002.png)
