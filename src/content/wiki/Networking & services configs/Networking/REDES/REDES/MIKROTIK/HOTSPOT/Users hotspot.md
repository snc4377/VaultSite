---
title: "Users Hotspot"
category: ["Networking & services configs", "Networking", "REDES", "REDES", "MIKROTIK", "HOTSPOT", "Users hotspot"]
---

Note title: Users Hotspot

In user profiles, we can create "groups", for example we create a profile for users who can browse at 2 Mbps.
![Pasted image 20231111231702](/VaultSite/wiki-images/Pasted%20image%2020231111231702.png)

In shared users we can specify how many people can use the user profile we're creating, and in rate limit the upload and download speed. For example, if we want the user to browse at 100 Mbps we enter 1000k.
![Pasted image 20231111231844](/VaultSite/wiki-images/Pasted%20image%2020231111231844.png)
![Pasted image 20231111231928](/VaultSite/wiki-images/Pasted%20image%2020231111231928.png)

Then in users, we'll create the users:
![Pasted image 20231111232050](/VaultSite/wiki-images/Pasted%20image%2020231111232050.png)
![Pasted image 20231111232209](/VaultSite/wiki-images/Pasted%20image%2020231111232209.png)
![Pasted image 20231111232231](/VaultSite/wiki-images/Pasted%20image%2020231111232231.png)
Then in server profiles, I recommend removing the "Cookie" option so it doesn't save the login session:
![Pasted image 20231111232430](/VaultSite/wiki-images/Pasted%20image%2020231111232430.png)
![Pasted image 20231111232449](/VaultSite/wiki-images/Pasted%20image%2020231111232449.png)
In the active section, we can delete a user session by clicking the red dash.
![Pasted image 20231111232732](/VaultSite/wiki-images/Pasted%20image%2020231111232732.png)