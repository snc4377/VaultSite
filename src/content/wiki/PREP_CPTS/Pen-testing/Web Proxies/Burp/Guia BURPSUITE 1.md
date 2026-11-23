---
title: "Guia BURPSUITE 1"
category: ["PREP_CPTS", "Pen-testing", "Web Proxies", "Burp", "Guia BURPSUITE 1"]
---


Note title: Untitled

We can see in the ejpt s4vitar folder more concepts with Burp Suite  
**Proxy**  
Check the box in Options > Intercept Server Responses > Intercept responses based on the following rules.  
In the Proxy section, what we will see is the first packet we intercept. This tab (Proxy) will be treated as the starting point, as all responses pass through here, and then we decide to send them. Here, we can also, for example, in the Options section, find another section that allows us to replace text. For instance, we can change the error code from 200 to 201.  
![Pasted image 20251210175303](/VaultSite/wiki-images/Pasted%20image%2020251210175303.png)

**Repeater**  
Ctrl+R  
This tab is used to keep traces with custom names, thus organizing everything by requests.

**Target**  
Here, it shows us all the targets that Burp Suite has detected. Normally, several domains will appear because we haven't defined specific targets, making it harder to visually locate the domains we want to audit. To change this, go to ==Proxy > Options > Don't send items to proxy history or live tasks, if out of scope==. Now, let's define the scope or target. This can be done in ==Target > Scope > Include in Scope > Add==, where we paste the URL we want to audit.

**Intruder**  
Ctrl+I  
This tool is useful for performing brute force attacks.  
![Pasted image 20251210180240](/VaultSite/wiki-images/Pasted%20image%2020251210180240.png)  
There are four different types of attacks, but this runs very slowly, so it's always recommended to write a script in Python or Bash unless you have Burp Suite Pro.  

In the adjacent tab labeled "Add," we choose where we want the payload to be injected for the brute force attack in the request.  

In the Payloads section, we can select which library to use.  
![Pasted image 20251210180540](/VaultSite/wiki-images/Pasted%20image%2020251210180540.png)  
It's important to remove the URL encoding of special characters.

**Decoder**  
Decoder does what its name implies: it helps us decode in different languages.

**Comparer**  
This tab helps us compare two requests if they are very similar but not identical.  
![Pasted image 20251210181557](/VaultSite/wiki-images/Pasted%20image%2020251210181557.png)

**Extender**  
This tab is used to add addons to Burp Suite. 


