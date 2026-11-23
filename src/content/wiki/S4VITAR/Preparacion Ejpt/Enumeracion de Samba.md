https://github.com/iabdullah215/eJPT-CheatSheet

**First Tool**  
SMBClient  
https://hackviser.com/tactics/tools/smbclient  

Command for unauthenticated enumeration:  
smbclient -L target -N  

View shared resources:  

![Pasted image 20260401155053](/VaultSite/wiki-images/Pasted%20image%2020260401155053.png)  

**Second Tool**  

SMBMAP  
https://www.poplabsec.com/smbmap-full-guide-enumerating-smb/  
This tool also shows permissions:  
![Pasted image 20260401155451](/VaultSite/wiki-images/Pasted%20image%2020260401155451.png)  

**Third Tool**  
CrackMapExec or NetExec  
https://hackviser.com/tactics/tools/crackmapexec  
![Pasted image 20260401155600](/VaultSite/wiki-images/Pasted%20image%2020260401155600.png)  
We can also list users:  
![Pasted image 20260401160427](/VaultSite/wiki-images/Pasted%20image%2020260401160427.png)  

**Fourth Tool**  
Enum4linux  
https://hackviser.com/tactics/tools/enum4linux  
This is the most powerful tool as it can enumerate users:  
![Pasted image 20260401155825](/VaultSite/wiki-images/Pasted%20image%2020260401155825.png)  
![Pasted image 20260401155842](/VaultSite/wiki-images/Pasted%20image%2020260401155842.png)  

The best tool combination is **smbmap or crackmapexec + smbclient** for connecting.  

Now we connect with smbclient to the shared anonymous resource:  
![Pasted image 20260401160048](/VaultSite/wiki-images/Pasted%20image%2020260401160048.png)  
Here we start listing items and can download them with `get`. If we want to download multiple files at once, we use `mget`:  
![Pasted image 20260401160211](/VaultSite/wiki-images/Pasted%20image%2020260401160211.png)  

**Credential validation with crackmapexec** (we created a file with possible passwords from the attention.txt in the smb)  

With crackmapexec, it fails:  
![Pasted image 20260401160649](/VaultSite/wiki-images/Pasted%20image%2020260401160649.png)  
But smbmap validates the entry. It's important with tools like these, especially with such clear hints, to try multiple options just in case:  
![Pasted image 20260401160851](/VaultSite/wiki-images/Pasted%20image%2020260401160851.png)  
![Pasted image 20260401160859](/VaultSite/wiki-images/Pasted%20image%2020260401160859.png)  
![Pasted image 20260401161041](/VaultSite/wiki-images/Pasted%20image%2020260401161041.png)  

**NMAP for SMB enumeration**  

With nmap, we can also enumerate vulnerabilities in the SMB service. Using the `--script=` command and selecting the script, similar to `http-enum` for HTTP:  
![Pasted image 20260403124901](/VaultSite/wiki-images/Pasted%20image%2020260403124901.png)  
![Pasted image 20260403125042](/VaultSite/wiki-images/Pasted%20image%2020260403125042.png)  
We see the different scripts it used, and one returns a response with a CVE (MS08-067) and that it's also vulnerable to EternalBlue. 



