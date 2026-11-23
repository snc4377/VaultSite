---
title: "Enumeración Y Explotación De WebDAV"
category: ["S4VITAR", "fases", "6-OWASP 10", "Enumeración y explotación de WebDAV"]
---

**WebDAV** (**Web Distributed Authoring and Versioning**) is an extension of the HTTP protocol that allows users to **access** and **manipulate** **files** on a web server through a secure connection.

When we talk about enumerating a WebDAV server, we refer to the process of gathering information about the available resources on the WebDAV server. Attackers can use WebDAV enumeration tools to search for protected resources on the server, such as configuration files, passwords, and other sensitive data. The information collected during enumeration can be used by attackers to plan more sophisticated attacks against the server.

Similarly, this initial reconnaissance phase involves attempting to identify the **file extensions** allowed on the server. Once the permitted file extensions are detected, attackers can exploit this to upload and execute files containing malicious code. If malicious files are successfully uploaded and executed on the web server, attackers can gain unauthorized access to the server and compromise the system's security.

One of the tools covered in this class is **Davtest**. Davtest is a command-line tool used for penetration testing on WebDAV servers. Davtest can be used to enumerate protected resources on a WebDAV server, as well as to test the server's security configuration. Davtest can also be used to test server authentication and authorization and to detect known vulnerabilities.

Another tool covered in this class is **Cadaver**. Cadaver is another command-line tool used to interact with WebDAV servers. Cadaver allows users to browse server resources, upload and download files, and execute commands on the server. Cadaver can also be used for penetration testing on WebDAV servers, such as enumerating protected resources and exploiting known vulnerabilities.

To prevent WebDAV enumeration and exploitation, it is crucial for system administrators to implement appropriate security measures on the server. This may include limiting the available resources on the server and using strong authentication and authorization. Additionally, users should protect their passwords and avoid using weak or easily guessable passwords.