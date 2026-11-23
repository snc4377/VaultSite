Session Puzzling, Session Fixation, and Session Variable Overloading are different names corresponding to security vulnerabilities that affect **session management** in a web application.

The **Session Fixation** vulnerability occurs when an attacker sets a valid session identifier for a user and then waits for the user to log in. If the user logs in with that session identifier, the attacker could access the user's session and perform malicious actions on their behalf. To achieve this, the attacker may trick the user into clicking a link that includes a valid session identifier or exploit a weakness in the web application to set the session identifier.

The term **"Session Puzzling"** is sometimes used to refer to the same vulnerability but from the attacker's perspective, attempting to **guess** or **generate valid session identifiers**.

Finally, the term **"Session Variable Overloading"** refers to a specific type of Session Fixation attack where the attacker sends a large amount of data to the web application with the goal of overloading the session variables. If the web application does not properly validate the amount of data that can be stored in session variables, the attacker could overload them with malicious data and cause performance issues in the application.

To prevent these vulnerabilities, it is important to use random and secure session identifiers, validate user authentication and authorization before establishing a session, and limit the amount of data that can be stored in session variables.

For this lab, we will again use the SKF Labs machine.  
![Pasted image 20260211194910](/VaultSite/wiki-images/Pasted%20image%2020260211194910.png)  
If we log in, we see that it assigns us a JWT cookie.  
![Pasted image 20260211195158](/VaultSite/wiki-images/Pasted%20image%2020260211195158.png)  
If we analyze the JWT, we see its format.  
![Pasted image 20260211195236](/VaultSite/wiki-images/Pasted%20image%2020260211195236.png)  
Once inside, we see the dashboard.  
![Pasted image 20260211195334](/VaultSite/wiki-images/Pasted%20image%2020260211195334.png)  
If we log out and enter `/dashboard` in the URL, we won't see anything because we need to be logged in.  
![Pasted image 20260211195405](/VaultSite/wiki-images/Pasted%20image%2020260211195405.png)  
If we check the storage, we'll see that we no longer have the JWT.  

We see a "forgot password" option in case we forget the user's password. Let's intercept this request with Burp.  
![Pasted image 20260211195537](/VaultSite/wiki-images/Pasted%20image%2020260211195537.png)  
In Burp, we see that it is giving us a session cookie when we didn't have one before.  
![Pasted image 20260211195623](/VaultSite/wiki-images/Pasted%20image%2020260211195623.png)  
![Pasted image 20260211195634](/VaultSite/wiki-images/Pasted%20image%2020260211195634.png)  
If we use this cookie, we can log in.  
![Pasted image 20260211195700](/VaultSite/wiki-images/Pasted%20image%2020260211195700.png)  

This vulnerability involves attempting to persuade the victim to hijack their session.  
Let's take an example where our session cookie has a field `session_id: 1234`, and we assume other users might also have similar cookies. If we manually edit our cookie to, say, `1234567`, reload, and nothing happens, we could then send the user a URL with this new cookie.  
![Pasted image 20260211200059](/VaultSite/wiki-images/Pasted%20image%2020260211200059.png)  
If the cookies are misconfigured and not regenerated but remain fixed for each user, this person would log in with the cookie we created, and we would see their session. 

