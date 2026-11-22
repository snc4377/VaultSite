When we talk about API abuse, we're referring to the exploitation of vulnerabilities in **Application Programming Interfaces (APIs)** used to enable communication and data exchange between different applications and services on a network.

A simple example of an API could be the integration of Google Maps into a transportation app. Imagine a transportation app that needs to display a map and route so users can see the vehicle's location and the path to their destination. Instead of creating its own map, the app could use the Google Maps API to display the map within its interface.

In this example, the Google Maps API provides a set of functions and protocols that allow the transportation app to communicate with Google's servers and access the data needed to display the map and route. The Google Maps API also handles the complexity of rendering the map and route across different devices and browsers, letting the transportation app focus on its core functionality.

Additionally, one of the tools we use in this context is **Postman**. Postman is a widely used tool for testing and debugging APIs. Developers can use Postman to send requests to various endpoints and inspect responses to verify the API is functioning correctly. However, attackers can also use Postman to explore API endpoints for security vulnerabilities and weaknesses.

Some API endpoints may accept different request methods, such as GET, POST, PUT, DELETE, etc. Attackers can use fuzzing tools to send a large number of requests to an endpoint in search of vulnerabilities. For example, an attacker might send GET requests to enumerate all available resources or POST requests to add or modify data.

Common vulnerabilities exploitable through API abuse include:

- **SQL Injection**: Attackers can send malicious data in requests to inject SQL code into the underlying database.
- **Cross-Site Request Forgery (CSRF)**: Attackers can send malicious requests to an API on behalf of an authenticated user to perform unauthorized actions.
- **Exposure of Sensitive Information**: Attackers can probe API endpoints to obtain confidential data, such as API keys, passwords, and usernames.

To prevent API abuse, developers must ensure the API is securely designed and that all incoming requests are properly validated and authenticated. Strong encryption and authentication are also essential to protect data transmitted via the API.

Developers can use tools like Postman to test APIs and identify potential vulnerabilities before attackers exploit them.

**LAB**

- **crAPI**: [https://github.com/OWASP/crAPI](https://github.com/OWASP/crAPI)

Once the container is deployed, navigate to localhost on port 8888.  
![[Pasted image 20260131114924.png]]  
Let's attempt to register.  
![[Pasted image 20260131114955.png]]  

Before sending the request, we could intercept it with Burp, but we'll go to the Network tab and filter by XHR to only show API communications.  
![[Pasted image 20260131120340.png]]  
We can see we've intercepted a POST request to `/login`, and hovering reveals it points to an API route.  
![[Pasted image 20260131120521.png]]  
We also see three other GET requests pointing to APIs.  
![[Pasted image 20260131120552.png]]  

Upon closer inspection, we see we're sending our email and password in JSON format to the server, which generates a JSON Web Token (identifiable by its three-part structure: header, payload, signature).  
![[Pasted image 20260131120825.png]]  

We'll use Postman, a tool for testing and debugging APIs, to enumerate as many API endpoints as possible.  
![[Pasted image 20260131121123.png]]  
Go to "Create Collection" and name it.  
![[Pasted image 20260131121312.png]]  
After naming it, click "New" in the top-left and select "HTTP Request."  
![[Pasted image 20260131121404.png]]  

We'll extract the HTTP request from the login. Open the Network tab with `Ctrl+Shift+C`, log out, then log back in. Copy the POST request route.  
![[Pasted image 20260131121607.png]]  
Set the method to POST and enter the URL.  
![[Pasted image 20260131121649.png]]  

Now, go to the "Body" tab since sending the request now would result in a 400 Bad Request due to missing fields. Copy the JSON in raw format.  
![[Pasted image 20260131121838.png]]  
Set the text type to JSON to ensure proper headers. Now the request is correctly formatted.  
![[Pasted image 20260131121847.png]]  
![[Pasted image 20260131122014.png]]  
Save it to the collection for organized work.  

Next, we'll do the same for the GET request to `/dashboard`.  
![[Pasted image 20260131122210.png]]  
The API returns data, but only when logged in, so we need to include the JSON Web Token. We could do this manually (key, value, description), but Postman supports variables.  

Under the collection's "Variables" tab:  
![[Pasted image 20260131122550.png]]  
Name the token variable, set an initial value (two hyphens), and paste the JWT from the login into "CURRENT VALUE."  
![[Pasted image 20260131122740.png]]  

Under "Authorization," set the type to "Bearer Token" (as indicated by the request) and reference the token variable.  
![[Pasted image 20260131122920.png]]  
Now the token is automatically included, and we see the API response.  
![[Pasted image 20260131123040.png]]  

We'll repeat this for all endpoints.  

Navigate to the shop section:  
![[Pasted image 20260131123210.png]]  
![[Pasted image 20260131123303.png]]  
Create another request block in Postman and continue for the rest of the site.  
![[Pasted image 20260131123347.png]]  
![[Pasted image 20260131123409.png]]  

Clicking "Buy" generates two more requests:  
![[Pasted image 20260131123515.png]]  
![[Pasted image 20260131123523.png]]  
![[Pasted image 20260131123538.png]]  
![[Pasted image 20260131123621.png]]  
![[Pasted image 20260131123629.png]]  

Now we'll copy all API routes to understand the workflow.  

Let's test changing the email of the user we created:  
![[Pasted image 20260131124342.png]]  
Enter a new email, and the system requests a token sent to the email for verification.  
![[Pasted image 20260131124500.png]]  

This machine has a mail server on port 8025:  
![[Pasted image 20260131124534.png]]  
The token appears robust, so brute-forcing is impractical here.  

**VECTOR 1**  
Log out and select "Forgot Password."  
![[Pasted image 20260131124656.png]]  

Assume the email `s4vitar` belongs to someone else, but as attackers, we know it exists.  
![[Pasted image 20260131124813.png]]  
The system requests an OTP and a new password.  

The OTP sent to the email is vulnerable to brute-forcing:  
![[Pasted image 20260131124929.png]]  
Before fuzzing, copy the request into Postman and test with an incorrect OTP.  
![[Pasted image 20260131125353.png]]  
![[Pasted image 20260131125403.png]]  
![[Pasted image 20260131125423.png]]  

We'll use `ffuf` to perform the brute-force attack.

ffuf -u https://localhost:8888/identity/api/auth/v3/check-otp -w /usr/share/seclists/Fuwwing/4-digits-0000-9999.txt -X POST -d 'and the request data replacing with FUZZ the parameter to fuzz'
![[Pasted image 20260131125825.png]]
After a while, we see no progress or reports
If we return to Postman and make a few requests, we see the server indicates we've exceeded the number of attempts and throws an error
![[Pasted image 20260131130036.png]] ![[Pasted image 20260131130048.png]]
It's blocking brute force attempts which looks bad

But if we have everything properly represented in Postman, we can draw conclusions about how things work. If we go to the dashboard request
![[Pasted image 20260131130255.png]]
We see it says api/v2/ but in the OTP request we see api/auth/v3/
![[Pasted image 20260131130336.png]]
Let's try changing from v3 to v2 since an older version might not have attempt blocking
![[Pasted image 20260131130424.png]]
We see no version error, just that the OTP is invalid as before
![[Pasted image 20260131130542.png]]
Let's change the URL in ffuf and now it allows brute forcing (we might need to regenerate the OTP as it may have expired)

We'll also add the header (-H) to the command since it's JSON and would likely conflict without it
![[Pasted image 20260131130851.png]]
We see a 200 code, so the user's password would have been automatically changed
![[Pasted image 20260131130944.png]]

**VECTOR 2** 
Let's try another attack vector

Returning to the available products request
![[Pasted image 20260131131237.png]]
We see it uses GET. Let's try sending it as POST
We can do this in Postman or with ffuf using the dictionary /usr/share/SecLists/Fuzzing/http-request-methods.txt and putting FUZZ in the -X method parameter
![[Pasted image 20260131131440.png]]
We see some requests return 401 and 200 status codes
![[Pasted image 20260131131608.png]]
The OPTIONS method is typically used to discover which methods an API accepts. If we change the method to OPTIONS in Postman's headers section, we'll see the same methods we found with ffuf
![[Pasted image 20260131131759.png]]
Let's try POST and see the body output suggests we need to create the product ourselves
![[Pasted image 20260131132054.png]]
In the body, we'll set raw with JSON format and try creating the object with the specified fields, putting a negative number in the price field to see if it adds money to our wallet (this is called a mass assignment attack)
![[Pasted image 20260131132322.png]]
Before sending, since we reauthenticated, we need to check if we have the same token defined in Postman, otherwise we'll change it.

It let us create the new product
![[Pasted image 20260131132552.png]]
![[Pasted image 20260131132606.png]]![[Pasted image 20260131132615.png]]

In the buy product request we saw earlier, it showed the quantity we selected. Let's buy 100 of this created product
![[Pasted image 20260131132742.png]]
![[Pasted image 20260131132752.png]]
Above we notice a coupon window, so we'll do the usual: send the request and copy it
![[Pasted image 20260131132925.png]]
![[Pasted image 20260131133000.png]]

The request is sent in JSON format. Let's try a [[NoSQLi]]
We see it processed and gave us a $75 coupon
![[Pasted image 20260131133253.png]]
![[Pasted image 20260131133316.png]]

**Vector 3**
We see we can add a vehicle
![[Pasted image 20260131133409.png]]
It sends a PIN code and VIN code to email
![[Pasted image 20260131133453.png]]
The PIN could be brute-forced but wouldn't make sense since the VIN can't
![[Pasted image 20260131133534.png]]
We see a car and a map of its supposed location
![[Pasted image 20260131133630.png]]
Looking at the request, we see a location sent via GET
![[Pasted image 20260131133720.png]]
The JSON shows carId, the car's position, and the name of the person who owns it
![[Pasted image 20260131133810.png]]
Each user should only see their own, otherwise it would be BOLA (Broken Object Level Authorization)

Let's copy everything to Postman
![[Pasted image 20260131133951.png]]
Seeing id 3 suggests there are at least two other cars

The web interface has a Community tab showing more users like a forum
![[Pasted image 20260131134113.png]]
Sometimes APIs provide more information than needed
Let's make a request about Adam's post
![[Pasted image 20260131134217.png]]
The JSON contains everything we need including VehicleId
![[Pasted image 20260131134300.png]]
Let's test if this id is real in Postman
With this we have Adam's geolocation or any user we want
![[Pasted image 20260131134441.png]]
