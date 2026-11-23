---
title: "Area Of Investigation"
category: ["Area of investigation"]
---

## Areas

During this process, our goal is to identify as much information as possible from the following areas:

### Domains and Subdomains

Often, we are provided with a single domain or perhaps a list of domains and subdomains belonging to an organization. Many organizations do not have an accurate asset inventory and may have forgotten about externally exposed domains and subdomains. This is an essential part of the reconnaissance phase. We may encounter several subdomains that map to IP addresses within scope, increasing the overall attack surface of our engagement (or bug bounty program). Hidden and forgotten subdomains may have outdated/vulnerable versions of applications or development versions with additional functionality (a Python debug console, for example). Bug bounty programs often set the scope as something like `*.inlanefreight.com`, meaning all subdomains of `inlanefreight.com`, in this example, are within scope (i.e., `acme.inlanefreight.com`, `admin.inlanefreight.com`, and so on). We may also discover subdomains of subdomains. For example, suppose we discover something like `admin.inlanefreight.com`. We could then run additional subdomain enumeration against this subdomain and perhaps find `dev.admin.inlanefreight.com`—a very attractive target. There are many ways to find subdomains (both passively and actively) that we will cover later in this module.

### IP Ranges

Unless we are limited to a very specific scope, we want to know as much as possible about our target. Finding additional IP ranges owned by our target can lead us to discover other domains and subdomains and further expand our potential attack surface.

### Infrastructure

We want to learn as much as possible about our target. We need to know what technologies our target is using. Are all their applications ASP.NET? Do they use Django, PHP, Flask, etc.? What type(s) of API/web services are used? Do they use content management systems (CMS) like WordPress, Joomla, Drupal, or DotNetNuke, which have their own types of vulnerabilities and misconfigurations we can find? We also care about the web servers in use, such as IIS, Nginx, Apache, and version numbers. If our target runs outdated frameworks or web servers, we want to dig deeper into the associated web applications. We are also interested in the types of back-end databases in use (MSSQL, MySQL, PostgreSQL, SQLite, Oracle, etc.), as this will give us an indication of the types of attacks we can perform.

### Vhosts

Finally, we want to enumerate virtual hosts (vhosts), which are similar to subdomains but indicate that an organization hosts multiple applications on the same web server. We will also cover vhost enumeration later in the module.
