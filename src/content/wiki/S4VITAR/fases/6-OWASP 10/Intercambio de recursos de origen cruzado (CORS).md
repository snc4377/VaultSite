**Cross-Origin Resource Sharing (CORS)** is a mechanism that allows a web server to **restrict access to resources** from **different origins**, meaning different domains or protocols. CORS is used to protect user privacy and security by preventing other websites from accessing sensitive information without permission.

Suppose we have a web application on the domain "**example.com**" that uses a web API on the domain "**api.example.com**" to retrieve data. If the web application is properly configured for CORS, it will only allow cross-origin requests from the domain "**example.com**" to the API on "**api.example.com**". If a request is made from a different domain, such as "**attacker.com**", the request will be blocked by the web browser.

However, if the web application is not properly configured for CORS, an attacker could exploit this weakness to access sensitive resources and data. For example, if the web application does not validate user authorization to access resources, an attacker could inject malicious code into a webpage to make requests to the application's API on "**api.example.com**".

The attacker could use automated tools to test different CORS header values and find a misconfiguration that allows requests from another domain. If successful, the attacker could access sensitive resources and data that should not be available from their website. For instance, they could retrieve user login information, modify application data, etc.

To prevent this type of attack, it is crucial to properly configure CORS in the web application and ensure that cross-origin requests are only allowed from trusted domains.

SOP (Same-Origin Policy) is the blocking mechanism that only allows reading and executing from the same domain, while CORS is the opposite—it enables access through rules set by the user. For example, if you want domain B to execute and read resources, and also allow domain A to do so, but domain C is not defined in CORS, then domain C would not be permitted.

## 🛡️ Web Security: SOP, CORS, and XSS (Quick Guide)

### 1. The Concept of Origin

For the browser, an **Origin** is the combination of: **Protocol + Domain + Port**.

- `https://store.com` is different from `http://store.com` (Protocol).
- `https://store.com` is different from `https://api.store.com` (Subdomain).

### 2. SOP (Same-Origin Policy) - "The Wall"

This is the browser's golden rule. It is enabled by default.

- **What it does:** Prevents a webpage from **reading** data from another webpage with a different origin.
- **Why it exists:** So that a pirated movie site cannot read your Gmail emails even if you have both tabs open.
- **Limitation:** SOP allows _loading_ resources (images, external scripts) but does not allow _reading_ the content of responses if they come from another origin.

### 3. CORS (Cross-Origin Resource Sharing) - "The Gate"

This is the special permission configured by the **server** (usually an API) to relax SOP.

- **Purpose:** Allows your Frontend (`app.com`) to legally request data from your Backend (`api.com`).
- **How it works:** The server sends a header called `Access-Control-Allow-Origin`.
- **The danger:** If the server uses an asterisk (`*`) or trusts domains it shouldn’t, any attacker can use a victim’s browser to steal data from that API.

### 4. XSS (Cross-Site Scripting) - "The Infiltrator"

This is a vulnerability where you execute JavaScript in the victim’s domain.

- **Relation to CORS:** XSS does not require CORS misconfiguration to work. XSS is already "inside" the house.
- **The "Leap":** If you have an XSS in Web A but want to steal data from Web B (API), the **CORS policy of Web B** will determine whether you can read that data or not.

---

## 🏦 Bank Analogy (To Understand the Strategy)

|**Attack**|**Analogy**|**Objective**|
|---|---|---|
|**SQLi / RCE**|**Blowing up the vault.** You break into the server and steal everyone’s database.|The Server / Infrastructure.|
|**XSS / CORS**|**Pickpocketing at the door.** You wait for the user to use their session and steal their specific data.|The User / Their Privacy.|

>CORS doesn’t break the server, but it is the **damage multiplier**. An XSS "trapped" in a boring website becomes critical if the CORS policy of a banking API allows it to read sensitive data.

**LABORATORY**  
https://github.com/blabla1337/skf-labs  
![[Pasted image 20260210174105.png]]  
We authenticate with the credentials admin:admin  
![[Pasted image 20260210174215.png]]  
As attackers, let’s assume we want the victim, when accessing our malicious resource (e.g., on localhost), to unknowingly send everything they see on the other webpage to our site.  
![[Pasted image 20260210175439.png]]  
If we intercept the request from the victim’s page, we’ll see something interesting in the headers:  
![[Pasted image 20260210174633.png]]  
This CORS is configured to allow all domains to fetch resources without restrictions.  

Let’s test setting an `Origin` header in our request:  
![[Pasted image 20260210174803.png]]  
We see it allows this. Normally, it should have a predefined origin to restrict which domains can make requests to load resources from this domain.  

Now, we could set up a malicious server and, by including it in the request, we’d be telling the victim’s page that our LOCALHOST (us) can load a resource from their page and display it on our site.  
![[Pasted image 20260210175245.png]]  

Let’s create the file so that when the victim accesses our malicious webpage on localhost, we can steal all their privileged information.  
![[Pasted image 20260210175612.png]]  

Once the code is created and our malicious web server is running:  
![[Pasted image 20260210180959.png]]  
If the victim, who also has the other webpage open, accesses ours, they’d see something like this:  
The information from the real webpage, but displayed incorrectly because the images are loaded from repositories we don’t have.  
![[Pasted image 20260210181050.png]]  
If we check our HTTP server, we’ll see image paths—these are the routes we need to create and where to store the images to make our webpage identical.  
![[Pasted image 20260210181306.png]]  
We’d need to use `mkdir` to create each route and `wget` to download each image directly from the real webpage.  
![[Pasted image 20260210181354.png]]  
![[Pasted image 20260210181422.png]]  

![[Pasted image 20260210181405.png]]  
Now we’ve successfully included another domain from a third-party domain.  

If we edit the CORS configuration on the target machine to add filtering:  
![[Pasted image 20260210181655.png]]  
We’ll see our page return to normal because CORS now blocks us.  
![[Pasted image 20260210181722.png]]  
![[Pasted image 20260210181743.png]]
