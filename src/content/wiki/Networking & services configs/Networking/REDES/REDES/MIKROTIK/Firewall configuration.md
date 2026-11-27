---
title: "Firewall Configuration"
category: ["Networking & services configs", "Networking", "REDES", "REDES", "MIKROTIK", "Firewall configuration"]
---

Note title: Firewall Configuration

Let's go to NAT firewall
![Pasted image 20231020090237](/VaultSite/wiki-images/Pasted%20image%2020231020090237.png)
In the out interface, we set the one we want to use to connect to the internet.
![Pasted image 20231020090312](/VaultSite/wiki-images/Pasted%20image%2020231020090312.png)

Then we go to action and set masquerade.
![Pasted image 20231020090417](/VaultSite/wiki-images/Pasted%20image%2020231020090417.png)

Next, we go to routes![Pasted image 20231020093843](/VaultSite/wiki-images/Pasted%20image%2020231020093843.png)

And in gateway, we'll set the actual gateway for ether1 - in this case it was this one
![Pasted image 20231020094650](/VaultSite/wiki-images/Pasted%20image%2020231020094650.png)
And then it should look like this:
![Pasted image 20231020094722](/VaultSite/wiki-images/Pasted%20image%2020231020094722.png)
To verify we configured it correctly, we can ping from the new terminal