---
title: "Insecure Direct Object Reference (IDORs)"
category: ["S4VITAR", "fases", "6-OWASP 10", "Insecure Direct Object Reference (IDORs)"]
---

**Insecure Direct Object References (IDOR)** are a type of security vulnerability that occurs when a web application uses **internal identifiers** (such as numbers or names) to identify and access resources (like files or data) without properly validating the user's authorization to access them.

For example, if a web application uses a numeric identifier to identify a record in a database, an attacker may attempt to guess this identifier and access the records without proper authorization. This can allow attackers to access confidential information, modify data, create unauthorized user accounts, and perform other malicious actions.

The IDOR vulnerability can occur when a web application **does not implement proper access controls** for the resources it handles. For instance, an application may validate access through authentication and authorization for resources displayed in the user interface but fail to apply the same validation for resources accessed directly through a URL.

To exploit an IDOR vulnerability, an attacker may attempt to manually modify an object's identifier in the URL or use an automated tool to test different values. If the attacker finds an identifier that grants access to a resource that should not be available, the IDOR vulnerability has been successfully exploited.

For example, suppose user **A** has an order with the numeric identifier **123**, and user **B** has an order with the numeric identifier **124**. If the attacker attempts to access the URL **"https://example.com/orders/124"**, the web application might allow access to that order without validating whether the user has permission to view it. This way, the attacker could access user **B**'s order without proper authorization.

To prevent IDOR vulnerabilities, it is crucial to properly validate user authorization for accessing resources, both in the user interface and in direct URL requests. Additionally, it is recommended to restrict resource access permissions and keep software and operating systems up to date.

**LAB**  
- **XVWA 1**: [https://www.vulnhub.com/entry/xtreme-vulnerable-web-application-xvwa-1,209/](https://www.vulnhub.com/entry/xtreme-vulnerable-web-application-xvwa-1,209/)  
https://www.youtube.com/shorts/1RmUJaCo6qA
