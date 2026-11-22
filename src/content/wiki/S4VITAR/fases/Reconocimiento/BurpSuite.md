With the Foxy Proxy add-on, we add the proxy 127.0.0.1:8080.

---

**CA CERTIFICATE FOR HTTPS WEBSITES**

Go to https://burp, navigate to the CA certificate section, and download it.

In the browser settings, go to the certificates section and import what we just installed. Select the first option to trust for websites.

---

**REPEATER**

Allows us to send the request and see what would happen. This is the most common tool and where payloads are typically injected.

---

**INTRUDER**

In this explanation, we're working on the Vulnhub CVE for ImageTragick.

![[Pasted image 20251203200752.png]]

We can perform different types of attacks by selecting the attack type.

In the payloads section, we can inject, for example in our practice case, file extensions for brute force.

![[Pasted image 20251203201000.png]]

Then in the options section, we can go to "Grep Extract" to have the server return the error. We select the specific part we want returned.

![[Pasted image 20251203201153.png]]

And we start the attack.

![[Pasted image 20251203201217.png]]

Here we can see which files are being accepted.

---

Now we return to Repeater and edit the file type.

![[Pasted image 20251203201350.png]]

Here we're injecting code into a hidden GIF (though this isn't strictly necessary). The command `fill` examines the JPG, and `curl` checks the IP with the path we specify.

![[Pasted image 20251203201709.png]]

Now we start an HTTP server to see if we receive the request.

![[Pasted image 20251203201738.png]]

This confirms we have remote command execution.

---

Let's create our file.gif.

![[Pasted image 20251203201909.png]]

We can see an `echo` and Base64 code.

Let's see what this Base64 contains.

![[Pasted image 20251203201951.png]]

It's setting up a reverse shell to port 8889 of our IP to give us a console.

We upload the file and set up netcat to listen.

![[Pasted image 20251203202328.png]]

We now have access. 