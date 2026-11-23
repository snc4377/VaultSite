---
title: "5 Guia BURPSUITE"
category: ["S4VITAR", "fases", "Enumeracion de servicios", "CONCEPTOS DE ENUMERACION Y EXPLOTACION", "5-Guia BURPSUITE"]
---

**Proxy**  
Check the box in Options > Intercept Server Responses > Intercept responses based on the following rules.  
In the Proxy section, what we'll see is the first packet we intercept. This tab (Proxy) will serve as our starting point—this is where all responses pass through and where we later decide to forward them. Here, we can also, for example, in the Options section, find another feature that allows us to replace text. For instance, we can change an error code from 200 to 201.  
![Pasted image 20251210175303](/VaultSite/wiki-images/Pasted%20image%2020251210175303.png)  

**Repeater**  
Ctrl + R  
This tab is used to keep traces with custom names, helping us organize everything by requests.  

**Target**  
Here, it shows all the targets Burp Suite has detected. Normally, multiple domains appear because we haven't defined specific targets, making it harder to visually identify the domains we actually want to audit. To change this, go to **Proxy > Options > Don't send items to proxy history or live tasks, if out of scope**. Now, let's define the scope or target. Navigate to **Target > Scope > Include in Scope > Add**, and paste the URL we want to audit.  

**Intruder**  
Ctrl + I  
This tool is used for brute-force attacks.  
![Pasted image 20251210180240](/VaultSite/wiki-images/Pasted%20image%2020251210180240.png)  
There are four different attack types, but this runs very slowly, so it's always recommended to write a Python or Bash script unless you have Burp Suite Pro.  

In the adjacent tab labeled **Add**, we select where we want the payload injected for the brute-force attack in the request.  

Under the **Payloads** section, we can choose which library to use.  
![Pasted image 20251210180540](/VaultSite/wiki-images/Pasted%20image%2020251210180540.png)  
It's important to disable URL encoding for special characters.  

**Decoder**  
Decoder does exactly what its name suggests—it helps decode data in different formats.  

**Comparer**  
This tab helps compare two requests if they are very similar but not identical.  
![Pasted image 20251210181557](/VaultSite/wiki-images/Pasted%20image%2020251210181557.png)  

**Extender**  
This tab is used to add add-ons to Burp Suite. 


