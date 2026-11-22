**Json Web Tokens** (**JWT**) are a type of token used for **authentication** and **authorization** in web applications. JWT is an open standard (**RFC 7519**) that defines a compact and secure format for reliably transmitting information between parties.

Regarding the enumeration and exploitation phase of a JWT, this occurs when an attacker can gather information about the JWTs used in the application, potentially allowing them to exploit weaknesses in authentication and authorization.

JWT enumeration happens when an attacker uses brute-force techniques or reverse engineering to obtain information about the JWTs used by the web application. For example, the attacker might attempt to guess JWT values by constructing **fake tokens**, testing whether the web application accepts them. If successful, the attacker could extract sensitive information such as usernames, passwords, user roles, and other authentication and authorization data.

JWT exploitation occurs when an attacker uses information gathered during enumeration to exploit vulnerabilities in the application. For instance, if the web application uses JWTs for authentication but does not properly validate the **signature**, an attacker could forge a token and gain access as a legitimate user.

To prevent JWT enumeration and exploitation, it is essential to follow secure web development practices, such as proper input validation, secure JWT signing key management, and setting short expiration times for JWTs.

**LABORATORY**

- **SKF-LABS**: [https://github.com/blabla1337/skf-labs](https://github.com/blabla1337/skf-labs)  
The machine provides two users:  
![[Pasted image 20260211200520.png]]  
We log in and click "authenticate" to receive a JWT, which sets `user:guest` for admin.  
![[Pasted image 20260211200623.png]]  
Guest 2:  
![[Pasted image 20260211200641.png]]  

The goal of this machine is to escalate from `guest` to `guest2` by manipulating the JWT.

We examine the guest token:  
![[Pasted image 20260211200756.png]]  

If we decode this token on jwt.io, we see its structure:  
![[Pasted image 20260211200910.png]]  
An interesting detail is that the signature always uses a secret key in JWTs. If we had an LFI or another vulnerability allowing us to inspect the application's structure, we might discover this secret and use it to create valid JWTs. Some tokens also set the encryption method in the header to `none`.

We can attempt to reconstruct the token from the terminal.  
The actual token is Base64-encoded:  
![[Pasted image 20260211201450.png]]  

We can build the token step-by-step from the console. Note that if the header does not accept `NONE` as the encryption algorithm, we cannot create a valid JWT without the signature.

**HEADERS**  
![[Pasted image 20260211201542.png]]  

**PAYLOAD**  
We change the ID:  
![[Pasted image 20260211201805.png]]  

We create the token without the signature since we don’t know it—if `NONE` is accepted, it’s unnecessary.  
![[Pasted image 20260211201904.png]]  
![[Pasted image 20260211201917.png]]  
![[Pasted image 20260211201931.png]]  

If the header validation were enforced, it would be more challenging.  

Testing in a similar JWT lab where `none` is not allowed in the `alg` field, pasting our crafted token results in this error:  
![[Pasted image 20260211202358.png]]  
The error states that the signature is required. The secret should ideally be a strong password, but sometimes it isn’t.  
We could try guessing the secret.  

To brute-force the token, we could use Hashcat.