
Note title: Untitled

In the reconnaissance phase with nmap, if we've obtained the version, it's recommended to search for the version followed by "launchpad" in the browser. This will take us to a website that provides the codename and more information that, while not very relevant, doesn't hurt to have.
![[Pasted image 20251204172558.png]]

**FTP PORT** 21
File Transfer Protocol

FTP has the user "anonymous" which allows us to connect without logging in.
![[Pasted image 20251204171417.png]]

To enumerate this port, we'll use hydra, a brute force tool for different protocols.

**HYDRA**

Some syntax we'll use now is:

-l: This is used to specify the user (when we use -l in lowercase, it's because we know the user; if we didn't know, we'd use -L and a user dictionary for it to try).

-p: Same concept as -l but for passwords. Lowercase means we know it, and uppercase means we pass it a dictionary.
![[Pasted image 20251204171245.png]]

**SSH PORT 22**

To brute force SSH, it's more or less the same, but at the end, we indicate ssh://ipofssh -s 2222
![[Pasted image 20251204171959.png]]
-s: PORT in case the service we want to attack is on a different port, here we tell it to point there.
-t: Threads we want to use.
![[Pasted image 20251204172235.png]]

**HTTP PORT 80**

For web, we'd normally use whatweb to see what API tools are behind the manager (WordPress, Joomla, etc.).
Then with wfuzz, fuzz, etc., to discover files and directories, etc.

When it has HTTPS, sometimes we could check the certificate; sometimes we see emails or subdirectories, but it's not common.

**SSL HEARTBLEED VULNERABILITY**
We can use nmap scripts to see if the machine is vulnerable.
![[Pasted image 20251204180126.png]]
We download the executable we find on GitHub or the one we make ourselves and indicate the port and victim IP.
![[Pasted image 20251204180313.png]]![[Pasted image 20251204180343.png]]
We can see things from the machine's memory here; sometimes we can see processes or cookies.

**SMB PROTOCOL** =/ samba

What is Samba: It's an application on Linux systems to share printers, files, and other resources between Linux and Windows, and to do this, it uses SMB (which is the protocol itself).

SMBMAP

Crackmapexec (normally for Windows)
https://github.com/byt3bl33d3r/CrackMapExec
