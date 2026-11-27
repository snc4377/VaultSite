---
title: "HACKING WIFI"
category: ["Networking & services configs", "Networking", "HACKING WIFI", "HACKING WIFI", "HACKING WIFI"]
---

# HACKING WIFI

We install a dictionary:
![Pasted image 20240118161054](/VaultSite/wiki-images/Pasted%20image%2020240118161054.png)
![Pasted image 20240118161143](/VaultSite/wiki-images/Pasted%20image%2020240118161143.png)
We download the tool:
![Pasted image 20240118161409](/VaultSite/wiki-images/Pasted%20image%2020240118161409.png)

We locate our WLAN:
![Pasted image 20240118161523](/VaultSite/wiki-images/Pasted%20image%2020240118161523.png)

And set the interface to monitor mode to listen to other networks:
![Pasted image 20240118161735](/VaultSite/wiki-images/Pasted%20image%2020240118161735.png)
As we can see, we're now in monitor mode:
![Pasted image 20240118161818](/VaultSite/wiki-images/Pasted%20image%2020240118161818.png)
Now we enumerate the WiFi networks within range of our antenna. In this case, I'll do it locally using my mobile hotspot. We note the channel and BSSID:
![Pasted image 20240118162010](/VaultSite/wiki-images/Pasted%20image%2020240118162010.png)
![Pasted image 20240118171218](/VaultSite/wiki-images/Pasted%20image%2020240118171218.png)

Now we copy the BSSID, memorize the channel, and open a new tab:
![Pasted image 20240118171616](/VaultSite/wiki-images/Pasted%20image%2020240118171616.png)
In the -c parameter we specify the channel, with -w the file where network data will be saved, and at the end the monitor mode interface name.

Now airodump is waiting for traffic on the network we're auditing. In this case, I'll generate traffic by connecting a phone to the network:

![Pasted image 20240118171726](/VaultSite/wiki-images/Pasted%20image%2020240118171726.png)

Now we run the following to send traffic to the network. On the left after the 0 we put the SSID, on the right after -c the station, and at the end the WiFi interface. WE RUN THIS COMMAND 3 OR 4 TIMES:
What we're doing here is forcing the station off to capture the handshake:
![Pasted image 20240118171947](/VaultSite/wiki-images/Pasted%20image%2020240118171947.png)
![Pasted image 20240118164535](/VaultSite/wiki-images/Pasted%20image%2020240118164535.png)

Now we'll get the handshake:
![Pasted image 20240118205649](/VaultSite/wiki-images/Pasted%20image%2020240118205649.png)

If done correctly, the following files will be created. The one we care about is the .cap file.
This means we'll now perform a brute force attack:
![Pasted image 20240118210236](/VaultSite/wiki-images/Pasted%20image%2020240118210236.png)

And as we can verify, it reveals the key:
![Pasted image 20240118210336](/VaultSite/wiki-images/Pasted%20image%2020240118210336.png)

Finally, we disable monitor mode on the antenna or WiFi won't work:
![Pasted image 20240118230247](/VaultSite/wiki-images/Pasted%20image%2020240118230247.png)
