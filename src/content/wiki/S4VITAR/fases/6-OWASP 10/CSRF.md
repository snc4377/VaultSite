**Cross-Site Request Forgery (CSRF)** is a security vulnerability where an attacker **tricks** a legitimate user into performing an unwanted action on a website without their knowledge or consent.

In a CSRF attack, the attacker deceives the victim into clicking a malicious link or visiting a malicious webpage. This malicious page may contain an HTTP request that performs an unwanted action on the victim's website.

For example, imagine a user has logged into their online banking account and then visits a malicious webpage. The malicious page contains a form that submits an HTTP request to the bank's website to transfer funds from the user's account to the attacker's account. If the user clicks the submit button without realizing they're making a transfer, the CSRF attack will have succeeded.

CSRF attacks can be used to perform a wide range of unwanted actions, including transferring funds, modifying account information, deleting data, and more.

To prevent CSRF attacks, web application developers must implement proper security measures, such as including CSRF tokens in forms and HTTP requests. These CSRF tokens allow the web application to verify that the request comes from a legitimate user and not a malicious attacker (though be careful, as even these can be exploited in certain ways).

## CSRF Lab Test  

Seedsecurity lab test  

We are given two users with their credentials:  
alice:seedalice  
samy:seedsamy  

We log in to www.seed-server.com as alice.  

In the members tab, we can see different users. If we access their profiles by hovering over the "Add Friend" button, we'll see each has an assigned ID.  
![[Pasted image 20260124145149.png]]  

To test for CSRF, we'll try editing a user's profile on the page and intercept the request with Burp Suite.  
![[Pasted image 20260124145303.png]]  
![[Pasted image 20260124145314.png]]  
We see two interesting parameters: `__elgg_token` and `__elgg_ts`.  
The request is sent via POST. Right-clicking the request in Burp allows us to change the method.  
![[Pasted image 20260124145506.png]]  
![[Pasted image 20260124145524.png]]  

Let's test if the server validates the tokens by removing them.  
![[Pasted image 20260124145648.png]]  
If we reload the browser page, we see the name has still changed, so those tokens aren't validated.  
![[Pasted image 20260124145745.png]]  

We'll use samy as the attacker and alice as the victim.  

If we go to the messages section and send alice a message with the URL captured in Burp (with some parameters edited, like the ID depending on the target user), we can, for example, change her name just by her reading the message (in this example, each user has an ID represented in the URL as GUID).  

Here, we're hiding in an `img src=` the server URL from Burp targeting alice with ID 56 to change her name to "HACKED".  
![[Pasted image 20260124152217.png]]![[Pasted image 20260124152248.png]]  
![[Pasted image 20260124152257.png]]  

In the password parameter, we see this:  
![[Pasted image 20260124152340.png]]  
If it didn't require the current password for validation, we could try changing the request to GET and attempt to set a new password, like we did with the name.  

Let's verify if the current password field is actually validated.  
![[Pasted image 20260124152515.png]]  
Again, we see the tokens that aren't necessary, as we saw earlier.  
![[Pasted image 20260124153123.png]]  
We confirm the current password field is validated.  

Let's try deleting it to see if the request still works without it.  
![[Pasted image 20260124153308.png]]  
It doesn't.  
We could also try entering `[]`, but it still rejects the request.  

This lab is complete.  
We could also try making other users add each other—for example, having user alice (ID 56) add user 57. We could also change alice's profile description. We just need to capture the packet with samy, then post the URL as we did earlier in messages and modify the relevant parts.  
We can do the same thing but in the user description field, which also allows HTML input.


