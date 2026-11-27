---
title: "SolarLab(temporada)"
category: ["HTB", "Machines", "SolarLab(temporada)"]
---


Note title: SolarLab(season)

Crackmapexec (SMB, RDP, LDAP, FTP...)

- This command performs (an SMB service scan and enumeration because we specified it) and as we can see, it denies access.

![Pasted image 20240513185836](/VaultSite/wiki-images/Pasted%20image%2020240513185836.png)
- We go to the website and see there are 3 profiles. Let's try with the previous tool to see if we can access with their users.
![Pasted image 20240513185905](/VaultSite/wiki-images/Pasted%20image%2020240513185905.png)

- We see that two can, but one cannot.
![Pasted image 20240513191016](/VaultSite/wiki-images/Pasted%20image%2020240513191016.png)
- We access, for example, with the user claudia.
![Pasted image 20240513191309](/VaultSite/wiki-images/Pasted%20image%2020240513191309.png)

- We download files to check if any contain the password.
![Pasted image 20240513191948](/VaultSite/wiki-images/Pasted%20image%2020240513191948.png)
![Pasted image 20240513191936](/VaultSite/wiki-images/Pasted%20image%2020240513191936.png)
![Pasted image 20240513191923](/VaultSite/wiki-images/Pasted%20image%2020240513191923.png)





























