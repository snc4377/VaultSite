---
title: "CSRF"
category: ["Networking & services configs", "Networking", "HACKING WIFI", "info de herramientas y conceptos", "CSRF"]
---

**CSRF (Cross-Site Request Forgery)** is a type of attack where an attacker tricks a user into performing an unauthorized action in a web application where they are authenticated. The attacker exploits the trust the application has in the user.

### How does a CSRF attack work?

1. **Login**: The user logs into a website (e.g., a bank or social media app) and maintains an active session.  
2. **User deception**: The attacker creates a malicious page that, when visited, sends an HTTP request to the web application where the user is authenticated, using the user's session credentials.  
3. **Unauthorized action**: The request appears legitimate because it comes from an authenticated user. For example, it could transfer money, change account settings, or delete data.  

### Attack example:

An attacker may send a malicious link to a user via email or a website message. If the user clicks the link and is authenticated on the target site, the attack could execute actions as if performed by the user themselves.

### Example of CSRF attack code (educational purposes only):

A simple example of a CSRF form could be:

```html
<!-- Hidden form that submits automatically -->
<form action="https://www.examplebank.com/transfer" method="POST" id="csrfForm">
  <input type="hidden" name="amount" value="1000">
  <input type="hidden" name="recipient" value="attacker123">
</form>
<script>
  document.getElementById('csrfForm').submit();
</script>
```

### Mitigation techniques:

- **Use CSRF tokens**: Each form should include a unique token verified by the server to ensure the request came from an authorized source.  
- **Validate HTTP headers**: Check the `Referer` or `Origin` headers of requests to ensure they originate from your own application.  
- **Use secure cookies**: Configure cookies to be sent only with `SameSite` requests to prevent them from being sent in third-party requests.  
- **Additional user authentication**: Implement extra authentication for critical actions, such as entering a password or using a second authentication factor.  

https://www.youtube.com/watch?v=B_SLegHO_xU&ab_channel=s4vitar min 10
