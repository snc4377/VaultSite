---
title: "Zap Spider Assesment"
category: ["PREP_CPTS", "Pen-testing", "Web Proxies", "Burp", "zap spider assesment"]
---

## ZAP Spider

Let's start with `ZAP Spider`, which is similar to Burp's Crawler function. To initiate a Spider scan on any website, we can locate a request in our History tab and select (`Attack > Spider`) from the context menu. Another option is to use the HUD in the preconfigured browser. Once we visit the page or website where we want to start the Spider scan, we can click the second button on the right panel (`Spider Start`), which will prompt us to begin the scan:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2Facademy.hackthebox.com%2Fstorage%2Fmodules%2F110%2Fzap_spider.jpg&width=768&dpr=3&quality=100&sign=1cfc9615&sv=2)

ZAP Spider

**Note**: When we click the Spider button, ZAP may notify us that the current website is not within our scope and will ask us to automatically add it to the scope before starting the scan, to which we can answer "Yes." The scope is the set of URLs that ZAP will test if we initiate a generic scan, and we can customize it to scan multiple websites and URLs. Try adding several targets to the scope to see how the scan would execute differently.

Once we click the `Start` popup window, our Spider scan should begin crawling the website, searching for links and validating them, very similar to how Burp Crawler works. We can monitor the Spider scan's progress both in the HUD's `Spider` button and in ZAP's main UI, which should automatically switch to the current Spider tab to show progress and sent requests. When our scan is complete, we can check the Sites tab in ZAP's main UI, or we can click the first button on the right panel (`Sites Tree`), which should display an expandable tree list of all identified websites and their subdirectories:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2Facademy.hackthebox.com%2Fstorage%2Fmodules%2F110%2Fzap_sites.jpg&width=768&dpr=3&quality=100&sign=b88a6154&sv=2)

**Tip**: ZAP also has a different type of Spider called `Ajax Spider`, which can be started from the third button on the right panel. The difference between this and the normal scanner is that Ajax Spider also attempts to identify links requested via JavaScript AJAX calls, which may be running on the page even after it loads. Try running it after the normal Spider finishes its scan, as this may provide better results and add some links the normal Spider might have missed, though it may take slightly longer to complete.

---

## Passive Scanner

As ZAP Spider runs and makes requests to various endpoints, it automatically executes its passive scanner on each response to check for potential issues in the source code, such as missing security headers or DOM-based XSS vulnerabilities. This is why, even before running the active scanner, we might see the alerts button filling up with some identified issues. The alerts in the left panel show us problems detected on the current page we're visiting, while the right panel displays general alerts for this web application, including those found on other pages:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2Facademy.hackthebox.com%2Fstorage%2Fmodules%2F110%2Fzap_alerts.jpg&width=768&dpr=3&quality=100&sign=88adc5e3&sv=2)

We can also check the `Alerts` tab in ZAP's main UI to see all identified issues. If we click on any alert, ZAP will show us its details and the pages where it was found:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2Facademy.hackthebox.com%2Fstorage%2Fmodules%2F110%2Fzap_site_alerts.jpg&width=768&dpr=3&quality=100&sign=a7df477b&sv=2)

---

## Active Scanner

Once our site tree is populated, we can click the `Active Scan` button on the right panel to start an active scan on all identified pages. If we haven't run a Spider scan on the web application yet, ZAP will automatically execute it to create a site tree as the scan target. Once the active scan starts, we can monitor its progress similarly to how we did with the Spider scan:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2Facademy.hackthebox.com%2Fstorage%2Fmodules%2F110%2Fzap_active_scan.jpg&width=768&dpr=3&quality=100&sign=2b5e647a&sv=2)

The active scanner will attempt various types of attacks against all identified pages and HTTP parameters to uncover as many vulnerabilities as possible. For this reason, the active scan will take longer to complete. As the active scan runs, we'll see the alerts button filling up with more alerts as ZAP discovers additional issues. We can also check ZAP's main UI for more details about the ongoing scan and view the different requests sent by ZAP:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2Facademy.hackthebox.com%2Fstorage%2Fmodules%2F110%2Fzap_active_scan_progress.jpg&width=768&dpr=3&quality=100&sign=243009d8&sv=2)

Once the Active Scan finishes, we can review the alerts to determine which ones require follow-up. While all alerts should be reported and considered, `High` alerts are the ones that typically lead to direct compromise of the web application or back-end server. If we click the `High Alerts` button, it will show us the identified High Alert:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2Facademy.hackthebox.com%2Fstorage%2Fmodules%2F110%2Fzap_high_alert.jpg&width=768&dpr=3&quality=100&sign=369dc455&sv=2)

We can also click on it to see more details and learn how to replicate and patch this vulnerability:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2Facademy.hackthebox.com%2Fstorage%2Fmodules%2F110%2Fzap_alert_details.jpg&width=768&dpr=3&quality=100&sign=e5625aaf&sv=2)

In the alert details window, we can also click the URL to view the request and response details ZAP used to identify this vulnerability, and we can repeat the request via ZAP HUD or ZAP Request Editor:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2Facademy.hackthebox.com%2Fstorage%2Fmodules%2F110%2Fzap_alert_evidence.jpg&width=768&dpr=3&quality=100&sign=b722759a&sv=2)

---

## Reports

Finally, we can generate a report with all findings identified by ZAP through its various scans. To do this, we can select (`Report > Generate HTML Report`) from the top bar, which will prompt us for the location to save the report. We can also export the report in other formats like `XML` or `Markdown`. Once we generate our report, we can open it in any browser to review it:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2Facademy.hackthebox.com%2Fstorage%2Fmodules%2F110%2Fzap_report.jpg&width=768&dpr=3&quality=100&sign=abab5cf6&sv=2)

ZAP Spider

As we can see, the report displays all identified details in an organized manner, which can be useful for keeping records of the various web applications we scan during a penetration test.

---

## Exercise

Run ZAP Scanner on the previous target to identify directories and potential vulnerabilities. Once you find the high-level vulnerability, try using it to read the flag at '/flag.txt'.



```
Objetivo: 94.237.49.212:53545
```

We start ZAP with the HUD and access the browser, launching the Spider module and the Active Scan:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FeZvbBDTQmshuffeWTVl9%252Fimage.png%3Falt%3Dmedia%26token%3D9bd2c4fc-15ab-4d58-85c6-839301992096&width=768&dpr=3&quality=100&sign=1a6ee5a2&sv=2)

Once it finishes, it detects a critical `OS Command Injection` vulnerability, which would allow us to inject commands to gather information:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252F8cPDsjXaReLd0d1rwAgU%252Fimage.png%3Falt%3Dmedia%26token%3Dcc0e04b5-8c60-4012-b53d-8c6071575420&width=768&dpr=3&quality=100&sign=12b1edbd&sv=2)



```
http://94.237.49.212:53545/devtools/ping.php?ip=127.0.0.1%26cat+%2Fetc%2Fpasswd%26
```

Note title: Untitled

Upon accessing, we effectively see that it executes `cat /etc/passwd` and retrieves all system users:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FzF6r2yyTTUmBolIzoMXT%252Fimage.png%3Falt%3Dmedia%26token%3Da65cac37-d53f-4f92-988d-9778625c0f22&width=768&dpr=3&quality=100&sign=95ad2d5a&sv=2)

By modifying the URL, we can read the flag in the root directory:



```
https://94.237.49.212:53545/devtools/ping.php?ip=127.0.0.1%26cat+%2Fflag.txt
```

Note title: Untitled

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FvrEIBHorwzHgMoaz1IsU%252Fimage.png%3Falt%3Dmedia%26token%3D73d77a76-1093-48de-88b8-e5159be18c90&width=768&dpr=3&quality=100&sign=cfbf47df&sv=2)