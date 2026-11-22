**Client-Side Template Injection (CSTI)** is a security vulnerability where an attacker can inject malicious code into a **client-side template**, which executes in the user's **browser** rather than on the server.

Unlike **Server-Side Template Injection (SSTI)**, where the server-side template runs on the server and is responsible for generating dynamic content, in CSTI, the client-side template executes in the user's browser and is used to generate dynamic content on the client side.

Attackers can exploit a CSTI vulnerability to inject malicious code into a client-side template, allowing them to execute commands in the user's browser and gain unauthorized access to the web application and sensitive data.

For example, imagine a web application uses client-side templates to generate dynamic content. An attacker could exploit a CSTI vulnerability to inject malicious code into the client-side template, enabling them to execute commands in the user's browser and gain unauthorized access to the web application's sensitive data.

A common outcome of a Client-Side Template Injection (CSTI) attack is leveraging it to perform a **Cross-Site Scripting (XSS)** attack.

Once an attacker has injected malicious code into the client-side template, they can manipulate the data displayed to the user, allowing them to execute JavaScript code in the user's browser. Through this malicious code, the attacker could attempt to steal the user's session cookie, enabling unauthorized access to the user's account and allowing them to perform malicious actions on their behalf.

To prevent CSTI attacks, web application developers must properly validate and filter user input and use secure templating tools and frameworks that implement security measures to prevent malicious code injection.

#### Lab  
![[Pasted image 20260126191044.png]]  
![[Pasted image 20260126191117.png]]  

We see that if we enter something in the "fill me in plz" field, it is reflected on the web page afterward.  
![[Pasted image 20260126191229.png]]  
Let's try the same approach as with SSTI—we'll test if it evaluates `{{7 * 7}}`.  
![[Pasted image 20260126191415.png]]  
![[Pasted image 20260126191405.png]]  
At this point, we can see that it closely resembles SSTI. However, if we attempt to load internal machine files or execute commands as in SSTI, we'll find that it doesn't work.  

If we go to https://book.hacktricks.wiki/en/generic-methodologies-and-resources/pentesting-methodology.html or https://github.com/swisskyrepo/PayloadsAllTheThings and search for CSTI, we find different types of payloads.  

Let's see what's being used in the background. We press Ctrl+U.  
![[Pasted image 20260126191735.png]]  
We see that it uses AngularJS 1.5.0, so we'll search for CSTI payloads for this version of AngularJS.  

On GitHub, we find various payloads, all of which have one thing in common: `alert(1)`, which pops up a window if the payload executes successfully.  

Let's try this one:  
![[Pasted image 20260126192123.png]]  
![[Pasted image 20260126192140.png]]  
Nothing happened.  
Let's try the one above it:  
![[Pasted image 20260126192209.png]]  
Now we see that, through CSTI, the XSS is executed.  
![[Pasted image 20260126192236.png]]  
What could we do with this? We could modify the payload—replace `alert(1)` with, for example, `<script src="[our server IP]">` to load a script and escalate this to stealing user cookies, gaining unauthorized access, or performing actions on behalf of another user.  

For example, we made the pop-up display "pwned":  
![[Pasted image 20260126193329.png]]  
![[Pasted image 20260126193340.png]]
