To perform SQL injection, we have the tool SQLMAP.

However, it's always good to try doing it manually first and then use the tool to learn or understand what the tool is doing at all times.  
Watch this video to understand SQLi well: https://www.youtube.com/watch?v=C-FiImhUviM

- **Error-based SQL Injection**: This type of SQL injection exploits **errors in SQL code** to extract information. For example, if a query returns an error with a specific message, that message can be used to gather additional system information.

- **Time-based SQL Injection**: This type of SQL injection uses a query that **takes a long time to execute** to extract information. For example, if a query performs a table search and a delay is added, that delay can be used to gather additional data.

- **Boolean-based SQL Injection**: This type of SQL injection uses **boolean expressions** in queries to extract additional information. For example, a boolean expression can determine whether a user exists in a database.

- **UNION-based SQL Injection**: This type of SQL injection uses the **UNION** clause to combine two or more queries into one. For example, if a query returns user information and a **UNION** clause is added with another query returning permission data, additional user permission details can be extracted.

- **Stacked Queries SQL Injection**: This type of SQL injection exploits the ability to **execute multiple queries** in a single statement to gather additional information. For example, a query inserting a record into a table can be followed by an additional query returning table information.

It's worth noting that beyond these techniques, many other types of SQL injections exist. However, these are some of the most popular and commonly used by attackers on vulnerable websites.

Additionally, a brief distinction should be made between different types of databases:

- **Relational Databases**: SQL injections are more common in relational databases like MySQL, SQL Server, Oracle, PostgreSQL, etc. These databases use SQL queries to access and manipulate data.

- **NoSQL Databases**: While SQL injections are less common in NoSQL databases, this type of attack is still possible. NoSQL databases like MongoDB or Cassandra don't use SQL but a different data model. However, command injection in queries is still feasible. We'll cover this in later classes.

- **Graph Databases**: Graph databases like Neo4j can also be vulnerable to SQL injections. These databases use queries to access stored nodes and relationships.

- **Object Databases**: Object databases like db4o can also be vulnerable to SQL injections. These databases use queries to access stored objects.

Understanding different SQL injection types and how they can extract sensitive data or control a database is crucial. Developers must ensure proper user input validation and use defense techniques like input sanitization and prepared SQL statements to prevent SQL injections in their web applications.

Below is the link to the online utility **ExtendsClass** used in this class:

- **ExtendsClass MySQL Online**: [https://extendsclass.com/mysql-online.html](https://extendsclass.com/mysql-online.html)  

Here’s a script from s4vitar's class for brute-forcing databases when, for example, the input is sanitized and not corrupted with characters like `'` or `"`. This script would need editing depending on the type of injection we want to perform.  
**![Pasted image 20251218203911](/VaultSite/wiki-images/Pasted%20image%2020251218203911.png)**  
![Pasted image 20251218203935](/VaultSite/wiki-images/Pasted%20image%2020251218203935.png)  
For example, here we're adapting the script for a time-based injection:  
![Pasted image 20251218204451](/VaultSite/wiki-images/Pasted%20image%2020251218204451.png)




