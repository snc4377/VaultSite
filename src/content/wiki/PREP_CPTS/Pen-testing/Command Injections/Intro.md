There are many types of injections in web applications, depending on the type of web query being executed. The following are some of the most common types of injections:

|Injection|Description|
|---|---|
|OS Command Injection|Occurs when user input is used directly as part of an OS command.|
|Code Injection|Occurs when user input is placed directly within a function that evaluates code.|
|SQL Injections|Occurs when user input is used directly as part of an SQL query.|
|Cross-Site Scripting/HTML Injection|Occurs when the exact user input is displayed on a webpage.|

There are many other types of injections beyond those listed above, such as `LDAP injection`, `NoSQL injection`, `HTTP header injection`, `XPath injection`, `IMAP injection`, `ORM injection`, and others. Whenever user input is used within a query without being properly sanitized, it may be possible to escape the boundaries of the user input string into the parent query and manipulate it to change its intended purpose. This is why, as more web technologies are introduced into web applications, we will see new types of injections emerge.

---

## OS Command Injections

When it comes to OS command injections, the user input we control must directly or indirectly (or in some way affect) a web query that executes system commands. All web programming languages have different functions that allow developers to execute operating system commands directly on the backend server whenever needed. This can be used for various purposes, such as installing plugins or running certain applications.

#### PHP Example

For example, a web application written in `PHP` may use the `exec`, `system`, `shell_exec`, `passthru`, or `popen` functions to execute commands directly on the backend server, each with a slightly different use case. The following code is an example of PHP code vulnerable to command injection:

```
<?php
if (isset($_GET['filename'])) {
    system("touch /tmp/" . $_GET['filename'] . ".pdf");
}
?>
```

Note title: Untitled

Perhaps a particular web application has a functionality that allows users to create a new `.pdf` file in the `/tmp` directory with a filename provided by the user, which can then be used by the web application for document processing purposes. However, since the user input for the `filename` parameter in the `GET` request is used directly with the `touch` command (without being sanitized or escaped first), the web application becomes vulnerable to OS command injection. This flaw can be exploited to execute arbitrary system commands on the back-end server.

#### Example in NodeJS

This is not exclusive to `PHP`, but can occur in any web development framework or language. For example, if a web application is developed in `NodeJS`, a developer might use `child_process.exec` or `child_process.spawn` for the same purpose. The following example implements a functionality similar to what we discussed earlier:

```
app.get("/createfile", function(req, res){
    child_process.exec(`touch /tmp/${req.query.filename}.txt`);
})
```

The above code is also vulnerable to command injection, since it uses the `filename` parameter from the `GET` request as part of the command without sanitizing it first. Both `PHP` and `NodeJS` web applications can be exploited using the same command injection methods.
