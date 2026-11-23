The mass assignment attack (**Mass Assignment Attack**) is based on manipulating input parameters in an HTTP request to create or modify fields in a data model object within the web application. Instead of adding new parameters, attackers attempt to exploit the functionality of existing parameters to modify fields that should not be user-accessible.

For example, in a user management web application, a registration form may have fields for username, email, and password. However, if the application uses a library or framework that allows mass parameter assignment, an attacker could manipulate the HTTP request to add an additional parameter, such as the user's privilege level. This way, the attacker could register as a high-privilege user simply by adding an extra parameter to the HTTP request.


**LAB**  
- **Juice Shop**: [https://hub.docker.com/r/bkimminich/juice-shop](https://hub.docker.com/r/bkimminich/juice-shop)  
![Pasted image 20260202183027](/VaultSite/wiki-images/Pasted%20image%2020260202183027.png)  
On the website, we can see an account section where we can register or create a new account.  
![Pasted image 20260202183122](/VaultSite/wiki-images/Pasted%20image%2020260202183122.png)  
![Pasted image 20260202183129](/VaultSite/wiki-images/Pasted%20image%2020260202183129.png)  
We will intercept this registration with Burp.  
![Pasted image 20260202183202](/VaultSite/wiki-images/Pasted%20image%2020260202183202.png)  
And here is the response:  
![Pasted image 20260202183230](/VaultSite/wiki-images/Pasted%20image%2020260202183230.png)  
We see a `role` field in the response that wasn't in our request, so let's try adding it to see if we can set ourselves as admin.  
![Pasted image 20260202183349](/VaultSite/wiki-images/Pasted%20image%2020260202183349.png)  
In the response, we see that our role is now set to admin. This happens because the system trusts that the request won't be manipulated and automatically accepts the fields.  
![Pasted image 20260202183435](/VaultSite/wiki-images/Pasted%20image%2020260202183435.png)
