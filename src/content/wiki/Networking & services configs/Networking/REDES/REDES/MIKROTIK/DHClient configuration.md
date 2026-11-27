---
title: "DHClient Configuration"
category: ["Networking & services configs", "Networking", "REDES", "REDES", "MIKROTIK", "DHClient configuration"]
---

# DHClient Configuration

This is to receive an IP and connect to the internet.
![Pasted image 20231019130216](/VaultSite/wiki-images/Pasted%20image%2020231019130216.png)
We select the port where the cable is connected.
![Pasted image 20231019130317](/VaultSite/wiki-images/Pasted%20image%2020231019130317.png)
![Pasted image 20231019130406](/VaultSite/wiki-images/Pasted%20image%2020231019130406.png)
Now we will configure an interface, for example the WLAN. We enable masquerading in the NAT firewall.
![Pasted image 20231019131643](/VaultSite/wiki-images/Pasted%20image%2020231019131643.png)
In Out Interface, we select the one through which we receive internet. And in Action, we set masquerade.
![Pasted image 20231019131715](/VaultSite/wiki-images/Pasted%20image%2020231019131715.png)

