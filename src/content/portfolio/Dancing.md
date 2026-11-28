---
title: "Dancing"
category: ["Dancing"]
---

Note title: Dancing

- We'll use SMB
- First run nmap as usual to identify which port SMB is running on
- Check `man smbclient` to see the command's usage
- Use `smbclient -L machine_ip` to list available shares, noticing an unprotected user (workshares)
- To access the SMB share: `smbclient //machine_ip/WorkShares`
- Navigate directories with `cd` until finding the txt file, then download it with `get`
![Pasted image 20240226213137](/VaultSite/wiki-images/Pasted%20image%2020240226213137.png)