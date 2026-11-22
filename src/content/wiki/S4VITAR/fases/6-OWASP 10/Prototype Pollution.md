The **Prototype Pollution** attack is a technique that exploits vulnerabilities in JavaScript object implementations. This attack method is used to modify the "**prototype**" property of an object in a web application, which may allow an attacker to execute malicious code or manipulate the application's data.

In JavaScript, the "prototype" property is used to define an object's properties and methods. Attackers can exploit this JavaScript feature to modify an object's properties and methods and take control of the application.

A Prototype Pollution attack occurs when an attacker modifies the "prototype" property of an object in a web application. This can be achieved by manipulating data sent through forms or AJAX requests, or by injecting malicious code into the application's JavaScript code.

Once the object has been manipulated, the attacker can execute malicious code in the application, manipulate the application's data, or take control of a user's session. For example, an attacker could modify the "prototype" property of a user authentication object to allow access to an account without requiring a password.

The impact of a Prototype Pollution attack can be significant, as attackers may take control of the application or compromise user data. Additionally, since the attack relies on vulnerabilities in JavaScript object implementations, it can be difficult to detect and fix.

**LABORATORY**
- **SKF-LABS**: [https://github.com/blabla1337/skf-labs](https://github.com/blabla1337/skf-labs)

Once the Docker container is deployed, navigate to localhost:5000  
Register and log in:  
![[Pasted image 20260131142819.png]]  
![[Pasted image 20260131142835.png]]  
We see it displays "admin:" because we are not administrators, and below we see we can send a message.  
Prototype pollution is like poisoning the prototype (the property), allowing us to escalate our privileges and set ourselves as administrators.  

If we examine the machine's code in the `index.js` file, we see some objects defined here:  
![[Pasted image 20260131143201.png]]  
And if we scroll further down, we see a merge operation (which combines two code branches into one). It processes the request body (the email and message to the admin defined on the page) and the IP address:  
![[Pasted image 20260131143354.png]]  
![[Pasted image 20260131143520.png]]  

Let’s open Burp and intercept:  
![[Pasted image 20260131144208.png]]  
We see the structure and format are not optimal. Let’s try changing the `Content-Type` to JSON to see if it allows us to send it that way:  
![[Pasted image 20260131144402.png]]  
It allows JSON submission, so let’s attempt to pollute it by adding a new structure called `__proto__` (`__proto__` is the invisible thread connecting an object to its technical ancestry, enabling inheritance in JavaScript) with a field `admin:true` to see if we can pollute the prototype:  
![[Pasted image 20260131144550.png]]  
If we refresh the page, we are now admin:  
![[Pasted image 20260131144627.png]]  
There are many scenarios where we can pollute the prototype to escalate privileges, upload files, etc.  
The `admin` field is not normally visible since we don’t have the code, but we could perform some brute-forcing to try and discover it. 
