**GraphQL** is a query language for **APIs** (**Application Programming Interfaces**) that has become increasingly popular in recent years. Unlike traditional APIs with fixed endpoints, GraphQL allows clients to request only the information they need and receive a customized response based on their requirements.

**Introspection** in GraphQL is a mechanism that enables clients to **retrieve information** about a GraphQL API's schema. This means clients can explore and discover the data types, fields, and relationships available in the API, which is highly useful for developers building GraphQL clients. However, attackers can also leverage introspection to gather sensitive information about the API's structure and data, which can be used to carry out more sophisticated attacks.

On the other hand, **Mutations** in GraphQL are operations that allow clients to **modify data** in the API. Unlike queries, which only permit data retrieval, mutations enable clients to add, update, or delete data. This means mutations have the potential to make significant changes to the API's underlying database. If not properly secured, attackers can exploit mutations to perform malicious actions, such as deleting critical data or creating unauthorized records.

In the context of GraphQL, **IDORs** (Insecure Direct Object References) can occur when an attacker is able to guess or enumerate object **IDs** within the API and use those IDs to access objects they shouldn't have permission to view. This can happen if API developers fail to implement proper authentication and authorization mechanisms.

For example, suppose a GraphQL API allows users to access their own order information using an order ID. If the API developer hasn't implemented proper authorization, an attacker could use GraphQL introspection to discover all existing order IDs in the API, including those belonging to other users. The attacker could then use these IDs to access other users' orders without authorization, constituting an IDOR.

Attackers can also use GraphQL Mutations to carry out IDOR attacks. For instance, if a GraphQL API allows users to update their own order information but lacks proper authorization checks, an attacker could use a mutation to modify other users' order data using IDs obtained through introspection.

In summary, GraphQL is a query language for APIs that allows clients to request only the data they need. API developers must properly secure introspection and mutations to prevent malicious exploitation by attackers.

**LAB**
- **GraphQL Introspection**: [https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Graphql-Introspection](https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Graphql-Introspection)
- **GraphQL Mutations**: [https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Graphql-Mutations](https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Graphql-Mutations)
- **GraphQL Injection**: [https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Graphql-Injection](https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Graphql-Injection)
- **GraphQL IDOR**: [https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Graphql-IDOR](https://github.com/blabla1337/skf-labs/tree/master/nodeJs/Graphql-IDOR)

**GraphQL IDOR**  
![Pasted image 20260212155311](/VaultSite/wiki-images/Pasted%20image%2020260212155311.png)  
We are given credentials: jhondoe:password1  
![Pasted image 20260212155342](/VaultSite/wiki-images/Pasted%20image%2020260212155342.png)  

Let's fuzz the endpoints using GoBuster, Wfuzz, or FFuF.  
![Pasted image 20260212155438](/VaultSite/wiki-images/Pasted%20image%2020260212155438.png)  
We find a `/settings` endpoint.  
![Pasted image 20260212155450](/VaultSite/wiki-images/Pasted%20image%2020260212155450.png)  
Let's intercept this request with Burp.  
We see the request is sending a GraphQL query via POST.  
![Pasted image 20260212155536](/VaultSite/wiki-images/Pasted%20image%2020260212155536.png)  
![Pasted image 20260212155744](/VaultSite/wiki-images/Pasted%20image%2020260212155744.png)  

Let's test changing the `id` parameter—we can see the API key and other users' info.  
![Pasted image 20260212155733](/VaultSite/wiki-images/Pasted%20image%2020260212155733.png)  

**GraphQL Introspection**  
Here we see a similar web app, but intercepting the request:  
![Pasted image 20260212160227](/VaultSite/wiki-images/Pasted%20image%2020260212160227.png)  
We can identify the query sent to GraphQL to fetch the displayed data.  
![Pasted image 20260212160350](/VaultSite/wiki-images/Pasted%20image%2020260212160350.png)  
If we go to `localhost:5000/graphql` and check HackTricks, we can grab a query to list all types.  

![Pasted image 20260212160519](/VaultSite/wiki-images/Pasted%20image%2020260212160519.png)  
![Pasted image 20260212160504](/VaultSite/wiki-images/Pasted%20image%2020260212160504.png)  
![Pasted image 20260212160535](/VaultSite/wiki-images/Pasted%20image%2020260212160535.png)  
We see various properties, some of which are particularly interesting.  

To visualize this better, we can use introspection—a special query to enumerate the entire database schema.  
![Pasted image 20260212160747](/VaultSite/wiki-images/Pasted%20image%2020260212160747.png)  
Pasting this into the URL may return errors:  
![Pasted image 20260212161047](/VaultSite/wiki-images/Pasted%20image%2020260212161047.png)  
This is normal, as type names sometimes don't match. We adjust based on the errors—for example, `Type` should be `__Type`.  
![Pasted image 20260212161212](/VaultSite/wiki-images/Pasted%20image%2020260212161212.png)  
Once corrected, the schema is displayed.  
![Pasted image 20260212161313](/VaultSite/wiki-images/Pasted%20image%2020260212161313.png)  
Copy the output and paste it into [GraphQL Voyager](https://apis.guru/graphql-voyager/) for an interactive visualization. Under "Introspection," paste the schema.  
![Pasted image 20260212161446](/VaultSite/wiki-images/Pasted%20image%2020260212161446.png)  
![Pasted image 20260212161502](/VaultSite/wiki-images/Pasted%20image%2020260212161502.png)  

Now that we understand the schema, we can intercept the request again and modify the query parameters to fetch specific data.  
![Pasted image 20260212161713](/VaultSite/wiki-images/Pasted%20image%2020260212161713.png)  
![Pasted image 20260212161744](/VaultSite/wiki-images/Pasted%20image%2020260212161744.png)  

This is read-only. For data modification, we move to:  
**GraphQL Mutations**  
In this new web app, we see a button to create posts.  
![Pasted image 20260212161952](/VaultSite/wiki-images/Pasted%20image%2020260212161952.png)  
Intercepting this shows the query includes fields like `title`, `body`, and the author's `id`, which we can edit.  

![Pasted image 20260212162055](/VaultSite/wiki-images/Pasted%20image%2020260212162055.png)  
![Pasted image 20260212162110](/VaultSite/wiki-images/Pasted%20image%2020260212162110.png)  
We can also add more fields based on the introspection findings.  

Sending the modified request executes the mutation.  
![Pasted image 20260212162240](/VaultSite/wiki-images/Pasted%20image%2020260212162240.png)
