---
title: "Wifi Connection"
category: ["Networking & services configs", "Networking", "REDES", "REDES", "MIKROTIK", "Wifi Connection"]
---

Note title: Wifi Connection

On the WLAN we want to connect to, we'll click scan and set it to station mode. Then we'll create a security profile with the password of the WiFi network we want to connect to.
![Pasted image 20231120195848](/VaultSite/wiki-images/Pasted%20image%2020231120195848.png)

Next, we go to the WiFi interface we want to use to connect to another network and click Scan > Start > select the desired WiFi network, then click Connect and choose the security profile we created earlier.
![Pasted image 20231120200433](/VaultSite/wiki-images/Pasted%20image%2020231120200433.png)
And it will look like this:
![Pasted image 20231120200705](/VaultSite/wiki-images/Pasted%20image%2020231120200705.png)

Now we simply run dhclient on the WLAN interface and we're done.
![Pasted image 20231120200847](/VaultSite/wiki-images/Pasted%20image%2020231120200847.png)

