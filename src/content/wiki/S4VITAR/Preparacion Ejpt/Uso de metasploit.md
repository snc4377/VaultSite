---
title: "Uso De Metasploit"
category: ["S4VITAR", "Preparacion Ejpt", "Uso de metasploit"]
---

Note title: Untitled

https://hackviser.com/tactics/tools/metasploit


Pivoting with Metasploit
https://books.spartan-cybersec.com/cppj/pivoting-for-juniors/doble-pivoting-y-triple-pivoting
https://www.youtube.com/watch?v=RotyKByc8Jc



With hashdump using a meterpreter console in Windows, we can view a system's hashes and crack them with John or Hashcat.
The path where Windows stores passwords is **C:\Windows\System32\Config\**

Steps for pivoting:
Open Metasploit on the attacker machine.

Use the multi/handler exploit
![Pasted image 20260404170354](/VaultSite/wiki-images/Pasted%20image%2020260404170354.png)
Once inside, we need to set the parameters requested in `show options`, which are our machine's IP and the listening port.
![Pasted image 20260404170500](/VaultSite/wiki-images/Pasted%20image%2020260404170500.png)
Now we need to specify the payload module used, which is the one we created with msfvenom for the reverse shell.
![Pasted image 20260404170632](/VaultSite/wiki-images/Pasted%20image%2020260404170632.png)
This reverse shell must be uploaded to the victim machine. Typically, we first gain access to the machine through other methods, then set up an HTTP server on our attacker machine and download the file using wget or certutil.exe in Windows.
![Pasted image 20260404170856](/VaultSite/wiki-images/Pasted%20image%2020260404170856.png)

Once the payload is on the victim machine and everything is configured in Metasploit, we simply need to set Metasploit to listen by running `run` and execute the reverse shell on the victim.

After connecting, we would press Ctrl+Z in Metasploit and add the new network (only visible from the victim machine) with: `run autoroute -s <internal_network>/24`



Important command if we're in a CTF and want to search for flags across an entire Windows system:
`search -f flag*.txt /s`
