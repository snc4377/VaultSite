---
title: "Dancing"
category: ["HTB", "Machines", "Dancing"]
---

-We will use SMB
-We perform an nmap scan as usual to determine which port SMB is running on
-We use `man smbclient` to understand the command's functionality
-We use `smbclient -L machine_ip` to list the shares and find a user without a password (WorkShares)
-To access the SMB share, we use `smbclient //machine_ip/WorkShares`
-We navigate through directories using `cd` until we locate the txt file and download it with `get`
![Pasted image 20240226213137](/VaultSite/wiki-images/Pasted%20image%2020240226213137.png)