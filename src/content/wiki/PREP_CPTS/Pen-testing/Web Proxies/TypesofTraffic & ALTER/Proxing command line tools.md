---
title: "Proxing Command Line Tools"
category: ["PREP_CPTS", "Pen-testing", "Web Proxies", "TypesofTraffic & ALTER", "Proxing command line tools"]
---

An important aspect of using web proxies is enabling the interception of web requests made by command-line tools and thick client applications. This gives us transparency into the web requests made by these applications and allows us to utilize all of the different proxy features we have used with web applications.

To route all web requests made by a specific tool through our web proxy tools, we have to set them up as the tool's proxy (i.e. `http://127.0.0.1:8080`), similarly to what we did with our browsers. Each tool may have a different method for setting its proxy, so we may have to investigate how to do so for each one.

This section will cover a few examples of how to use web proxies to intercept web requests made by such tools. You may use either Burp or ZAP, as the setup process is the same.

Note: Proxying tools usually slows them down, therefore, only proxy tools when you need to investigate their requests, and not for normal usage.

---

## Proxychains

One very useful tool in Linux is [proxychains](https://github.com/haad/proxychains), which routes all traffic coming from any command-line tool to any proxy we specify. `Proxychains` adds a proxy to any command-line tool and is hence the simplest and easiest method to route web traffic of command-line tools through our web proxies.

To use `proxychains`, we first have to edit `/etc/proxychains.conf`, comment out the final line and add the following line at the end of it:

```
#socks4         127.0.0.1 9050
http 127.0.0.1 8080
```

We should also make use of the `-q` option, which makes `proxychains` operate in "quiet" mode, suppressing the output of connection information to the console. This can be useful for reducing clutter in the terminal and focusing on the output of the application being proxied. For example, let's try using `cURL` on one of our previous exercises:

```
snchh337@htb$ proxychains -q curl http://SERVER_IP:PORT

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Ping IP</title>
    <link rel="stylesheet" href="./style.css">
</head>
...SNIP...
</html>
```

If we go back to our web proxy (Burp in this case), we will see that the request has indeed gone through it:

![Proxy tab showing HTTP GET request details with buttons: Forward, Drop, Intercept is on, Action, Open Browser.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/110/proxying_proxychains_curl.png)