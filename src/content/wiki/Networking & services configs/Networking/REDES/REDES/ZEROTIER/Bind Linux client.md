---
title: "Bind Linux Client"
category: ["Networking & services configs", "Networking", "REDES", "REDES", "ZEROTIER", "Bind Linux client"]
---

# Bind Linux Client

Now I'll add a Linux client, in this case a Pi-hole machine. This will allow connected users to browse without ads, since we'll set the Pi-hole machine's ZeroTier interface IP as the DNS server.

First, install ZeroTier:
Go to this page and find your OS (recommended: if installing in a Proxmox container, use Ubuntu instead of Debian to avoid silly issues):
https://www.zerotier.com/download/

Just follow the instructions:
![Pasted image 20240321115458](/VaultSite/wiki-images/Pasted%20image%2020240321115458.png)
We can check ZeroTier's status:
![Pasted image 20240321115557](/VaultSite/wiki-images/Pasted%20image%2020240321115557.png)

Now join the network with this command: If sudo isn't installed by chance, install it first (since it sometimes causes errors):
![Pasted image 20240321130756](/VaultSite/wiki-images/Pasted%20image%2020240321130756.png)

```bash
sudo zerotier-cli join NETWORK_ID
```
Note title: Bind Linux Client

![Pasted image 20240321115720](/VaultSite/wiki-images/Pasted%20image%2020240321115720.png)
From here we get the network ID.
![Pasted image 20240321115822](/VaultSite/wiki-images/Pasted%20image%2020240321115822.png)
![Pasted image 20240321115838](/VaultSite/wiki-images/Pasted%20image%2020240321115838.png)

Now from the network we accept the machine and can assign it a name, for example:
![Pasted image 20240321120011](/VaultSite/wiki-images/Pasted%20image%2020240321120011.png)

Now if we run `ip a` the ZeroTier interface will appear:
![Pasted image 20240321131033](/VaultSite/wiki-images/Pasted%20image%2020240321131033.png)

IMPORTANT: DOES NOT WORK WITH CONTAINERS, ONLY WITH VMs