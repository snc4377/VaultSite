---
title: "Abuso De Subida De Archivos"
category: ["S4VITAR", "fases", "6-OWASP 10", "Subida de archivos", "Abuso de Subida de Archivos"]
---

File upload abuse is a type of attack that occurs when an attacker exploits vulnerabilities in web applications that allow users to **upload files** to the server. This type of attack is commonly known as a "**malicious file upload**" attack.

In a malicious file upload attack, an attacker uploads a malicious file to a web application, which is then stored on the server. For example, if the attacker manages to upload a PHP file and the web server stores it, they could achieve remote command execution and take control of the server.

Attackers may also use "**file type spoofing**" techniques to trick a web application into accepting a malicious file as if it were legitimate.

In this class, we will explore some of the most common techniques for exploiting the file upload phase in web applications. You will learn how attackers can upload malicious content and bypass various restrictions implemented to prevent it.

**LABORATORY**  
- **File Upload Laboratory**: [https://github.com/moeinfatehi/file_upload_vulnerability_scenarios](https://github.com/moeinfatehi/file_upload_vulnerability_scenarios)  

Once the container is deployed on local port 9001, we will see a web page with progressively more challenging exercises.  
![Pasted image 20260201182252](/VaultSite/wiki-images/Pasted%20image%2020260201182252.png)  

**LAB1**  
If we go to upload 1, we see a page that only allows JPEG or GIF uploads, and the code is not sanitized.  

We will upload a system-level call to execute `whoami`:  
![Pasted image 20260201182458](/VaultSite/wiki-images/Pasted%20image%2020260201182458.png)  
![Pasted image 20260201182506](/VaultSite/wiki-images/Pasted%20image%2020260201182506.png)  
Once uploaded, it gives us the path directly, but we could have brute-forced it with tools like `gobuster` or `wfuzz`.  
![Pasted image 20260201182512](/VaultSite/wiki-images/Pasted%20image%2020260201182512.png)  
Using Wappalyzer, we see that the server interprets this language, so the command will execute.  
![Pasted image 20260201182702](/VaultSite/wiki-images/Pasted%20image%2020260201182702.png)  
![Pasted image 20260201182713](/VaultSite/wiki-images/Pasted%20image%2020260201182713.png)  
If we wanted to control the command, we could use `$_GET['cmd']` and specify the command in the URL.  
![Pasted image 20260201182941](/VaultSite/wiki-images/Pasted%20image%2020260201182941.png)  
![Pasted image 20260201183007](/VaultSite/wiki-images/Pasted%20image%2020260201183007.png)  

**LAB3**  
Here, the code is more sanitized—if we try to upload a PHP file, we get a pop-up.  
![Pasted image 20260201183052](/VaultSite/wiki-images/Pasted%20image%2020260201183052.png)  
Now, we will check whether this validation is server-side or client-side.  
Examining the code, we find something interesting: a JavaScript file that validates our upload.  
![Pasted image 20260201183417](/VaultSite/wiki-images/Pasted%20image%2020260201183417.png)  
The JS file shows that validation is done on our side, not the server.  
![Pasted image 20260201183506](/VaultSite/wiki-images/Pasted%20image%2020260201183506.png)  
Since this is client-side validation, we can bypass it by pressing `Ctrl+Shift+C`, clicking the upload button, or removing the `onsubmit` line in the code.  
![Pasted image 20260201183726](/VaultSite/wiki-images/Pasted%20image%2020260201183726.png)  
![Pasted image 20260201183751](/VaultSite/wiki-images/Pasted%20image%2020260201183751.png)  
Now we can execute commands.  
![Pasted image 20260201183838](/VaultSite/wiki-images/Pasted%20image%2020260201183838.png)  

**LAB10**  
Here, the validation is server-side, as we see a redirect and a response.  
![Pasted image 20260201183913](/VaultSite/wiki-images/Pasted%20image%2020260201183913.png)  
We open Burp and capture the request.  
![Pasted image 20260201184035](/VaultSite/wiki-images/Pasted%20image%2020260201184035.png)  
We will test whether the server can interpret alternative PHP extensions, even if they are not `.php`. Searching online or in HackTricks for alternative PHP extensions:  
![Pasted image 20260201184256](/VaultSite/wiki-images/Pasted%20image%2020260201184256.png)  
HackTricks:  
![Pasted image 20260201184308](/VaultSite/wiki-images/Pasted%20image%2020260201184308.png)  
This works if the developer only blocked `.php` extensions.  
We edit the request and change the extension to `.php3`.  
![Pasted image 20260201184523](/VaultSite/wiki-images/Pasted%20image%2020260201184523.png)  
The file uploads, but the server does not interpret it.  
![Pasted image 20260201184609](/VaultSite/wiki-images/Pasted%20image%2020260201184609.png)  
We try different extensions until `.php5` works.  
![Pasted image 20260201184711](/VaultSite/wiki-images/Pasted%20image%2020260201184711.png)  

**LAB11**  
This lab is similar to the previous one but uses the `.pht` extension.  
![Pasted image 20260201184753](/VaultSite/wiki-images/Pasted%20image%2020260201184753.png)  
![Pasted image 20260201184851](/VaultSite/wiki-images/Pasted%20image%2020260201184851.png)  

**LAB12**  
In this lab, no extension works except `.htaccess`. Why? The `.htaccess` file allows defining a custom extension to execute PHP. For example, we could configure `.david` files to run as PHP.  

Using Burp, we edit the request to upload an `.htaccess` file allowing the `.test` extension.  
We add the following line in the file content via Burp:  
![Pasted image 20260201185531](/VaultSite/wiki-images/Pasted%20image%2020260201185531.png)  
![Pasted image 20260201185651](/VaultSite/wiki-images/Pasted%20image%2020260201185651.png)  
![Pasted image 20260201185702](/VaultSite/wiki-images/Pasted%20image%2020260201185702.png)  
Now, if we upload a `.test` file, the code will execute.  
![Pasted image 20260201185737](/VaultSite/wiki-images/Pasted%20image%2020260201185737.png)  
![Pasted image 20260201185806](/VaultSite/wiki-images/Pasted%20image%2020260201185806.png)  
A mitigation is to block users from uploading `.htaccess` files.  

**LAB16**  
Now, the sanitization checks file size.  
![Pasted image 20260201185949](/VaultSite/wiki-images/Pasted%20image%2020260201185949.png)  
If we wanted a reverse shell, we could use MonkeyPentester's PHP script or Metasploit, but they are too large and would be blocked.  

In Burp:  
![Pasted image 20260201191425](/VaultSite/wiki-images/Pasted%20image%2020260201191425.png)  
We see the file size limit. We change it to 80, and the upload succeeds.  
![Pasted image 20260201191526](/VaultSite/wiki-images/Pasted%20image%2020260201191526.png)  
![Pasted image 20260201191545](/VaultSite/wiki-images/Pasted%20image%2020260201191545.png)  
We can also shorten the PHP code by removing unnecessary spaces and renaming `cmd` to `a` (this does not affect functionality).  
![Pasted image 20260201191743](/VaultSite/wiki-images/Pasted%20image%2020260201191743.png)  
![Pasted image 20260201191751](/VaultSite/wiki-images/Pasted%20image%2020260201191751.png)  

**LAB17**  
This lab is similar to the previous one, so we edit the size in Burp.  
![Pasted image 20260201191831](/VaultSite/wiki-images/Pasted%20image%2020260201191831.png)  
If size editing is blocked, we can further minimize the payload. For example, `<?php system($_GET['a']); ?>` can be reduced significantly.  
![Pasted image 20260201192159](/VaultSite/wiki-images/Pasted%20image%2020260201192159.png)  
Commands still execute.  

**LAB21**  
Now, the server validates whether the uploaded file is an image.  
![Pasted image 20260201192337](/VaultSite/wiki-images/Pasted%20image%2020260201192337.png)  
It checks the `Content-Type`.  
![Pasted image 20260201192424](/VaultSite/wiki-images/Pasted%20image%2020260201192424.png)  
(Normally, file types are determined by "magic numbers"—the first few bytes of the file.)  

We edit the `Content-Type` to `image/jpg`.  
![Pasted image 20260201192759](/VaultSite/wiki-images/Pasted%20image%2020260201192759.png)  
![Pasted image 20260201192807](/VaultSite/wiki-images/Pasted%20image%2020260201192807.png)  

**LAB23**  
Here, only GIF uploads are allowed.  
![Pasted image 20260201193418](/VaultSite/wiki-images/Pasted%20image%2020260201193418.png)  
Burp interception fails because both server-side and client-side validation exist.  
![Pasted image 20260201193823](/VaultSite/wiki-images/Pasted%20image%2020260201193823.png)  
We remove the `onsubmit` section to bypass client-side validation and inspect the request.  
![Pasted image 20260201193926](/VaultSite/wiki-images/Pasted%20image%2020260201193926.png)  

In Burp, we try changing the `Content-Type` as before, but we get a message:  
![Pasted image 20260201194041](/VaultSite/wiki-images/Pasted%20image%2020260201194041.png)  
This happens because the server checks magic numbers.  
For GIFs, we can prepend `GIF8;` to the file, as this is a valid GIF header.  
![Pasted image 20260201193040](/VaultSite/wiki-images/Pasted%20image%2020260201193040.png)  
Using `xxd` and `file`, we confirm the file is recognized as a GIF.  
![Pasted image 20260201193124](/VaultSite/wiki-images/Pasted%20image%2020260201193124.png)  

Editing the request in Burp now works.  
![Pasted image 20260201194200](/VaultSite/wiki-images/Pasted%20image%2020260201194200.png)  

**LAB31**  
This lab allows JPEG and GIF uploads.  
![Pasted image 20260201194310](/VaultSite/wiki-images/Pasted%20image%2020260201194310.png)  

In Burp, we upload a PHP file without edits, but the response includes a GIF.  
![Pasted image 20260201194519](/VaultSite/wiki-images/Pasted%20image%2020260201194519.png)  
The code shows this GIF is in `uploads/` with a random name.  
![Pasted image 20260201194728](/VaultSite/wiki-images/Pasted%20image%2020260201194728.png)  
Sometimes, developers restrict directory listing in `uploads/`.  
![Pasted image 20260201194838](/VaultSite/wiki-images/Pasted%20image%2020260201194838.png)  
We cannot see stored files in `uploads/`. Searching for `cmd.php` fails—either it does not exist or was renamed.  
![Pasted image 20260201194953](/VaultSite/wiki-images/Pasted%20image%2020260201194953.png)  

The GIF suggests the server renames files using MD5 hashing.  
Hashing `cmd` in MD5 and appending `.php` in the URL allows code execution.  
![Pasted image 20260201195236](/VaultSite/wiki-images/Pasted%20image%2020260201195236.png)

**LAB33**  
This exercise is quite similar to the previous one  
![Pasted image 20260201195345](/VaultSite/wiki-images/Pasted%20image%2020260201195345.png)  
![Pasted image 20260201195415](/VaultSite/wiki-images/Pasted%20image%2020260201195415.png)  
We see it's MD5 again, but if we search for the previous cmd string, the file doesn't exist  
![Pasted image 20260201195532](/VaultSite/wiki-images/Pasted%20image%2020260201195532.png)  
In this exercise, instead of just encrypting the cmd from cmd.php, it encrypts the entire cmd.php file, and that's the filename  
![Pasted image 20260201195655](/VaultSite/wiki-images/Pasted%20image%2020260201195655.png)  
![Pasted image 20260201195706](/VaultSite/wiki-images/Pasted%20image%2020260201195706.png)  

**LAB35**  
We know the encryption simply by counting the characters in the web's GIF  
This also follows the same exercise format but encrypts the file's content as well, using SHA1SUM  
![Pasted image 20260201195812](/VaultSite/wiki-images/Pasted%20image%2020260201195812.png)  
This also follows the same exercise format but is encrypted with SHA1SUM  
![Pasted image 20260201200017](/VaultSite/wiki-images/Pasted%20image%2020260201200017.png)  
![Pasted image 20260201200030](/VaultSite/wiki-images/Pasted%20image%2020260201200030.png)  

**LAB41**  
In this exercise, we can upload any type of file, but when saving it, we don't know where it's stored—it's not in the Uploads folder  
![Pasted image 20260201200228](/VaultSite/wiki-images/Pasted%20image%2020260201200228.png)  
So, we'll use Gobuster to brute-force and find where the files are saved  
![Pasted image 20260201200306](/VaultSite/wiki-images/Pasted%20image%2020260201200306.png)  
We see two directories. If we test "images," we find the file  
![Pasted image 20260201200414](/VaultSite/wiki-images/Pasted%20image%2020260201200414.png)  

**LAB51**  
![Pasted image 20260201200433](/VaultSite/wiki-images/Pasted%20image%2020260201200433.png)  
We intercept with Burp and see it only allows JPG  
![Pasted image 20260201200530](/VaultSite/wiki-images/Pasted%20image%2020260201200530.png)  
We try changing the Content-Type, using GIF8, adding JPG magic numbers, or changing the extension to PHP, but none of this works.  
Here, we find that the developer has set the filename to *contain* the string "JPG," not necessarily end with it.  

So, we'll perform a double extension attack: simply adding "cmd.jpg.php" to the file cmd.php, bypassing the validation while the server still interprets the last extension.  
![Pasted image 20260201200929](/VaultSite/wiki-images/Pasted%20image%2020260201200929.png)  
![Pasted image 20260201200945](/VaultSite/wiki-images/Pasted%20image%2020260201200945.png)


