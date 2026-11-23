The open redirection vulnerability, also known as **Open Redirect**, is a common web application vulnerability that attackers can exploit to redirect users to malicious websites. This vulnerability occurs when a web application allows attackers to manipulate the URL of a redirect page to redirect the user to a malicious site.

For example, suppose a web application uses a redirect parameter in a URL to direct the user to an external page after authentication. If this URL does not properly validate the redirect parameter and allows attackers to modify it, attackers can redirect the user to a malicious website instead of the legitimate one.

An example of how attackers can exploit the open redirection vulnerability is by creating **phishing** emails that appear legitimate but actually contain manipulated links that redirect users to a malicious website. Attackers can use **social engineering** techniques to convince the user to click on the link, such as offering an attractive deal or a unique opportunity.

To prevent the open redirection vulnerability, it is important for developers to implement appropriate security measures in their code, such as validating redirect URLs and limiting redirection options to legitimate websites. Developers can also use secure coding techniques to prevent URL manipulation, such as encoding special characters and removing invalid characters.

- **Open Redirect 1**: [https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Url-redirection](https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Url-redirection)

**LABORATORY**
![Pasted image 20260203174457](/VaultSite/wiki-images/Pasted%20image%2020260203174457.png)
If we click the button, it applies a redirect to a new website.
![Pasted image 20260203174549](/VaultSite/wiki-images/Pasted%20image%2020260203174549.png)
We open BURP.
We see the redirect and a path.
![Pasted image 20260203174732](/VaultSite/wiki-images/Pasted%20image%2020260203174732.png)
We see that in `newurl`, the website to which we are redirected is entered, so if we copy `redirect?newurl=` and put an alternative URL, we can make it send us there.
![Pasted image 20260203174850](/VaultSite/wiki-images/Pasted%20image%2020260203174850.png)
![Pasted image 20260203174856](/VaultSite/wiki-images/Pasted%20image%2020260203174856.png)
And this is an Open Redirect.
This is dangerous when, for example, using [UFONET](https://github.com/epsylon/ufonet), which allows us to create massive botnets that abuse Open Redirect and Google Dorking.

**LABORATORY2**
We have exactly the same website but with a bit more security.
Let's open BURP.
![Pasted image 20260203175611](/VaultSite/wiki-images/Pasted%20image%2020260203175611.png)
If we try to change the redirect, we see that it doesn't allow us. In the message, we see that it says "I cannot use '.'".
![Pasted image 20260203175648](/VaultSite/wiki-images/Pasted%20image%2020260203175648.png)
If we apply URL-ENCODE to the dot, we see that the same message still appears.
![Pasted image 20260203175845](/VaultSite/wiki-images/Pasted%20image%2020260203175845.png)
But if we apply URL-Encode to the `%`, the server will no longer detect the dot.
![Pasted image 20260203175951](/VaultSite/wiki-images/Pasted%20image%2020260203175951.png)

The power of Open Redirect itself seems very low-risk and simple, but if we combine it with phishing, we can encounter cases like this:

We know the corporate emails of a company, for example, 300 emails, and we know the company's domain. We could send an email to all employees impersonating the department head, saying that we have suffered a security breach and that they must change their account passwords immediately. For example, if the domain is `windows.com`, we could buy a domain like `windows.es` or something very similar and perfectly duplicate the website. We send them this link via email, and we include the redirect, thus leading all users to our server, and we capture the credentials they enter. 
