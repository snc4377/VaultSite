---
title: "EC2"
category: ["Networking & services configs", "Networking", "AWS", "Services", "EC2"]
---

# EC2

Amazon Elastic Compute Cloud is a core part of Amazon.com's cloud computing platform called Amazon Web Services. EC2 allows users to rent virtual computers on which they can run their own applications.
![Pasted image 20240215210954](/VaultSite/wiki-images/Pasted%20image%2020240215210954.png)

With this, we will create INSTANCES (they are like virtual machines, so to speak) to create the server.
![Pasted image 20240215215542](/VaultSite/wiki-images/Pasted%20image%2020240215215542.png)
![Pasted image 20240215215821](/VaultSite/wiki-images/Pasted%20image%2020240215215821.png)
WE MAKE SURE TO SELECT THE FREE TIER OPTION:![Pasted image 20240215215911](/VaultSite/wiki-images/Pasted%20image%2020240215215911.png)

We select the instance type:
![Pasted image 20240215220040](/VaultSite/wiki-images/Pasted%20image%2020240215220040.png)

We create the keys to connect via SSH:
![Pasted image 20240215220240](/VaultSite/wiki-images/Pasted%20image%2020240215220240.png)
![Pasted image 20240215220345](/VaultSite/wiki-images/Pasted%20image%2020240215220345.png)
THIS KEY CANNOT BE SENT OR SHARED WITH ANYONE BECAUSE OTHERWISE THEY COULD ALSO ACCESS THE SERVER.

Now the key will be downloaded:
![Pasted image 20240215220455](/VaultSite/wiki-images/Pasted%20image%2020240215220455.png)
![Pasted image 20240215220540](/VaultSite/wiki-images/Pasted%20image%2020240215220540.png)And we launch the instance:
![Pasted image 20240215220753](/VaultSite/wiki-images/Pasted%20image%2020240215220753.png)
![Pasted image 20240215220823](/VaultSite/wiki-images/Pasted%20image%2020240215220823.png)
![Pasted image 20240215220838](/VaultSite/wiki-images/Pasted%20image%2020240215220838.png)
![Pasted image 20240215220918](/VaultSite/wiki-images/Pasted%20image%2020240215220918.png)

Now we will access the machine:
![Pasted image 20240215221115](/VaultSite/wiki-images/Pasted%20image%2020240215221115.png)
![Pasted image 20240215221206](/VaultSite/wiki-images/Pasted%20image%2020240215221206.png)
![Pasted image 20240215221248](/VaultSite/wiki-images/Pasted%20image%2020240215221248.png)
Now we go to the folder where we previously downloaded the key:

And we will execute the following command:
![Pasted image 20240215221429](/VaultSite/wiki-images/Pasted%20image%2020240215221429.png)
![Pasted image 20240215221502](/VaultSite/wiki-images/Pasted%20image%2020240215221502.png)
This is in case we were on Linux, and then we would enter the command from section 4:

Otherwise, we can connect directly by doing the following:
![Pasted image 20240215222304](/VaultSite/wiki-images/Pasted%20image%2020240215222304.png)
And now we could manage the server:
![Pasted image 20240215222403](/VaultSite/wiki-images/Pasted%20image%2020240215222403.png)

And for example, we can now create a web server or whatever we want:
![Pasted image 20240215223045](/VaultSite/wiki-images/Pasted%20image%2020240215223045.png)
![Pasted image 20240215223102](/VaultSite/wiki-images/Pasted%20image%2020240215223102.png)
