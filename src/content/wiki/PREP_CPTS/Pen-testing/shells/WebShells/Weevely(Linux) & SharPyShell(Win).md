---
title: "Weevely(Linux) & SharPyShell(Win)"
category: ["PREP_CPTS", "Pen-testing", "shells", "WebShells", "Weevely(Linux) & SharPyShell(Win)"]
---


# Weevely3(Linux)
https://github.com/epinna/weevely3

**Weevely3** is a stealth PHP web shell that simulates a telnet-like connection. It is designed for post-exploitation on PHP-based web servers where stealth and efficiency are priorities.

- **Stealthy Communication:** It uses HTTP cookies to obfuscate the traffic, making it look like legitimate web requests to bypass WAFs (Web Application Firewalls).
    
- **Modular Architecture:** It features over 30 modules to automate tasks such as database auditing, file management, and establishing reverse shells.
    
- **Authentication:** Every session is password-protected, ensuring that only you can access the shell.







# SharPyShell(Win)
https://github.com/antoniococo/sharpyshell

**SharPyShell** is a tiny, obfuscated ASP.NET webshell designed specifically for C# post-exploitation. It is highly effective in modern Windows/IIS environments where EDR (Endpoint Detection and Response) might be active.

- **In-Memory Execution:** It executes commands by compiling C# code in the server's memory, which significantly reduces its disk footprint and helps evade signature-based detection.
    
- **Interactive Terminal:** Provides a seamless interactive shell experience similar to a real terminal.
    
- **Dynamic Payloads:** The tool generates unique, obfuscated payloads for each deployment to stay ahead of antivirus signatures.
