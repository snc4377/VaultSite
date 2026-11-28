---
title: "Spooky Pass"
category: ["Retos Htb", "Spooky Pass"]
---


We are given a zip file with a password. We unzip it in the working directory and use the `file` command on the extracted file to see that it is a Linux executable:
![Pasted image 20251222173840](/VaultSite/wiki-images/Pasted%20image%2020251222173840.png)
When executing it, we can see that it asks for a password to let us pass, which we don't have. The challenge requires us to perform reversing.

We will use LTRACE since it will allow us to see what happens in the code and which libraries are called during execution:
![Pasted image 20251222175545](/VaultSite/wiki-images/Pasted%20image%2020251222175545.png)
We can see that it is comparing our text input with a string, and that string determines whether we pass or not since it is the password. When we enter it, it doesn't let us in because it's missing a character. If we use `strings pass` to see all the strings in the code, we will find the complete password:
![Pasted image 20251222180115](/VaultSite/wiki-images/Pasted%20image%2020251222180115.png)

![Pasted image 20251222175715](/VaultSite/wiki-images/Pasted%20image%2020251222175715.png)
If we enter it, we can see that it lets us in and we have the flag.

