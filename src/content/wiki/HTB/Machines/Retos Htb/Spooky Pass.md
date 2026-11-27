---
title: "Spooky Pass"
category: ["HTB", "Machines", "Retos Htb", "Spooky Pass"]
---

Note title: Spooky Pass

We're given a zip file with a password. We unzip it in the working directory and use `file` on the extracted file to see that it's a Linux executable:
![Pasted image 20251222173840](/VaultSite/wiki-images/Pasted%20image%2020251222173840.png)
When we try to execute it, we see it asks for a password to let us through, which we don't have. The challenge asks us to perform reversing.

We'll use LTRACE since it will let us see what happens in the code and which libraries it calls during execution:
![Pasted image 20251222175545](/VaultSite/wiki-images/Pasted%20image%2020251222175545.png)
We can see it's comparing our text input with a string, and that string determines whether we pass or not since it's the password.
When we enter it, it doesn't let us through because it's missing a character. If we do a `strings pass` to see all the strings in the code, we'll find the complete password there:
![Pasted image 20251222180115](/VaultSite/wiki-images/Pasted%20image%2020251222180115.png)

![Pasted image 20251222175715](/VaultSite/wiki-images/Pasted%20image%2020251222175715.png)
If we enter it, we can see it lets us through and we get the flag.

