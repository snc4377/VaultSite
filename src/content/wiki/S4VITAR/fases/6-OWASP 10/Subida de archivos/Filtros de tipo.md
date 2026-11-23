---
title: "Filtros De Tipo"
category: ["S4VITAR", "fases", "6-OWASP 10", "Subida de archivos", "Filtros de tipo"]
---

# Type Filters

---

So far, we have only dealt with type filters that solely consider the file extension in the filename. However, as we saw in the previous section, we can still potentially gain control over the _back-end_ server even with image extensions (e.g., `shell.php.jpg`). Additionally, we can use some allowed extensions (e.g., SVG) to carry out other attacks. All this indicates that merely testing the file extension is not enough to prevent file upload attacks.

This is why many modern web servers and web applications also test the content of the uploaded file to ensure it matches the specified type. While extension filters may accept multiple extensions, content filters typically specify a single category (e.g., images, videos, documents), which is why they usually do not use blacklists or whitelists. This is because web servers provide functions to verify the file's content type, and it generally falls within a specific category.

There are two common methods for validating file content: the `Content-Type` header or the file's content. Let's see how we can identify each filter and how to bypass both.

---

## Content-Type

Let's start the exercise at the end of this section and try to upload a PHP script:

http://SERVER_IP:PORT/

![Profile image update prompt with upload button, placeholder image, only images allowed.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/136/file_uploads_content_type_upload.jpg)

We see that we receive a message saying `Only images are allowed`. The error message persists, and our file is not uploaded, even if we try some of the tricks we learned in the previous sections. If we rename the file to `shell.jpg.phtml` or `shell.php.jpg`, or even if we use `shell.jpg` with web shell content, our upload will fail. Since the file extension does not affect the error message, the web application must be testing the file's content for type validation. As mentioned earlier, this could be in the `Content-Type` header or the file's content.

The following is an example of how a PHP web application tests the Content-Type header to validate the file type:
```
$type = $_FILES['uploadFile']['type'];

if (!in_array($type, array('image/jpg', 'image/jpeg', 'image/png', 'image/gif'))) {
    echo "Only images are allowed";
    die();
}
```
The code sets the variable (`$type`) based on the `Content-Type` header of the uploaded file. Our browsers automatically set the Content-Type header when selecting a file through the file selection dialog, typically derived from the file extension. However, since our browsers set this, this operation is a client-side operation, and we can manipulate it to change the perceived file type and potentially bypass the type filter.

We could start by fuzzing the Content-Type header with the [Content-Type wordlist](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/web-all-content-types.txt) from SecLists via Burp Intruder, to see which types are allowed. However, the message tells us that only images are allowed, so we can limit our scan to image types, reducing the wordlist to just `45` types (compared to the original ~700). We can do this as follows:

```
wget https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/web-all-content-types.txt

cat web-all-content-types.txt | grep 'image/' > image-content-types.txt

```

**Exercise:** Try running the previous scan to find which Content-Types are allowed.

To simplify, let's pick an image type (e.g., `image/jpg`), then intercept our upload request and change the Content-Type header to that value:

http://SERVER_IP:PORT/
![POST request to /upload.php with the file 'shell.php' disguised as an image.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/136/file_uploads_bypass_content_type_request.jpg)

This time we get `File successfully uploaded`, and if we visit our file, we see it was uploaded successfully:

http://SERVER_IP:PORT/profile_images/shell.php?cmd=id
![UID, GID, and groups, all set to 33 (www-data).](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/136/file_uploads_php_manual_shell.jpg)

**Note:** An HTTP file upload request has two Content-Type headers, one for the file attachment (at the bottom) and one for the entire request (at the top). Generally we need to modify the file's Content-Type header, but in some cases the request will only contain the main Content-Type header (e.g., if the uploaded content was sent as `POST` data), in which case we'll need to modify the main Content-Type header.

---

## MIME Type

The second and most common type of file content validation is testing the uploaded file's `MIME type`. `Multipurpose Internet Mail Extensions` (MIME) is an internet standard that determines a file's type through its general format and byte structure.

This is typically done by inspecting the first bytes of the file's content, which contain the [file signature](https://en.wikipedia.org/wiki/List_of_file_signatures) or [magic bytes](https://web.archive.org/web/20240522030920/https://opensource.apple.com/source/file/file-23/file/magic/magic.mime). For example, if a file starts with (`GIF87a` or `GIF89a`), this indicates it's a `GIF` image, while a file starting with plain text is generally considered a `text` file. If we change the first bytes of any file to GIF's magic bytes, its MIME type would change to a GIF image, regardless of its remaining content or extension.

**Tip:** Many other image types have non-printable bytes for their file signatures, while a `GIF` image starts with printable ASCII bytes (as shown above), making it the easiest to mimic. Additionally, since the string `GIF8` is common to both GIF signatures, it's usually sufficient to mimic a GIF image.

Let's take a basic example to demonstrate this. The `file` command in Unix systems detects a file's type through its MIME type. If we create a basic file with text, it would be considered a text file, as follows:

```
echo "this is a text file" > text.jpg 

file text.jpg 
 
text.jpg: ASCII text
```

As we can see, the file's MIME type is `ASCII text`, even though its extension is `.jpg`. However, if we write `GIF8` at the beginning of the file, it will be considered a `GIF` image, even though its extension remains `.jpg`:

```
echo "GIF8" > text.jpg 

file text.jpg
text.jpg: GIF image data

```

Web servers can also use this standard to determine file types, which is generally more accurate than checking the file extension. The following example shows how a PHP web application can test the MIME type of an uploaded file:

```
$type = mime_content_type($_FILES['uploadFile']['tmp_name']);

if (!in_array($type, array('image/jpg', 'image/jpeg', 'image/png', 'image/gif'))) {
    echo "Only images are allowed";
    die();
}

```

As we can see, the MIME types are similar to those found in Content-Type headers, but their origin is different, since PHP uses the `mime_content_type()` function to get a file's MIME type. Let's try repeating our last attack, but now with an exercise that tests both the Content-Type header and the MIME type:

http://SERVER_IP:PORT/
![POST request to /upload.php with the file 'shell.php' disguised as an image.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/136/file_uploads_bypass_content_type_request.jpg)

Once we resend our request, we notice we receive the error message `Only images are allowed`. Now, let's try adding `GIF8` before our PHP code to mimic a GIF image while keeping our file's extension as `.php`, so it still executes the PHP code:

http://SERVER_IP:PORT/
![POST request to /upload.php with the file 'shell.php' disguised as an image.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/136/file_uploads_bypass_mime_type_request.jpg)

This time we get `File successfully uploaded`, and our file is successfully uploaded to the server:

http://SERVER_IP:PORT/
![Profile image update prompt with upload button, placeholder image, file uploaded successfully.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/136/file_uploads_bypass_mime_type.jpg)

Now we can visit our uploaded file, and we'll see that we can successfully execute system commands:

http://SERVER_IP:PORT/profile_images/shell.php?cmd=id
![GIF8 header with UID, GID, and groups set to 33 (www-data).](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/136/file_uploads_php_manual_shell_gif.jpg)

**Note:** We see the command output starts with `GIF8`, since this was the first line in our PHP script to mimic GIF magic bytes, and now it's displayed as plain text before our PHP code executes.

We can use a combination of the two methods discussed in this section, which may help us evade some more robust content filters. For example, we can try using an `allowed MIME type with a disallowed Content-Type`, an `allowed MIME/Content-Type with a disallowed extension`, or a `disallowed MIME/Content-Type with an allowed extension`, and so on. Similarly, we can try other combinations and permutations to confuse the web server, and depending on the code's security level, we might be able to bypass multiple filters.


## Practical Case

The server mentioned above employs Client-Side, Blacklist, Whitelist, Content-Type, and MIME-Type filters to ensure the uploaded file is an image. Try combining all the attacks you've learned so far to bypass these filters and upload a PHP file to read the flag in "`/flag.txt`".



```
Objetivo: http://94.237.54.239:48561
```

Things are getting complicated, but let's get to it!

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252Fmkm8ykF4q5fYOAWpYvCR%252FCaptura%2520de%2520pantalla%25202024-08-20%2520a%2520las%252014.05.30.png%3Falt%3Dmedia%26token%3D83e42eb9-e90a-41fc-ad7a-fed27c8ff410&width=768&dpr=3&quality=100&sign=2ed424c62e1113464d02ba991249e025&sv=3)

We're already very familiar with this application. Let's try all the techniques we know to bypass shell upload.

### Client-Side Validation
As we know, we need to remove the validation script and accepted formats from the inspector:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FPUmsToYAcq4GbxmGUjnh%252Fimage.png%3Falt%3Dmedia%26token%3Dc8d6e033-cebd-4b5d-9b5d-fa43bd00a021&width=768&dpr=3&quality=100&sign=48c0db4490c90aa37b29ece7d0dbb3ca&sv=3)

We upload the webshell `phpbash.php` and the first error we get is `Extension not allowed`:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FaanZyEdApOJURxCaI3IX%252Fimage.png%3Falt%3Dmedia%26token%3D485cdacb-96d5-4f3e-8d91-5c12bf46bdb0&width=768&dpr=3&quality=100&sign=e56d238b60acc102e22510e3c4135d03&sv=3)

### Extension Fuzzing (Whitelist)

Let's send the request to `Intruder` to fuzz possible extensions, just like we saw in the previous section. We'll use the extensions wordlist from [Seclists](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/web-extensions.txt)

First, we add the extension as a variable in Intruder:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FF0OV7dj2CwpjmldH9sbe%252Fimage.png%3Falt%3Dmedia%26token%3Dcf9985c3-0498-4c10-ad7e-d5f231a28e0b&width=768&dpr=3&quality=100&sign=61367ed2e21a4033ac3b02c4151736d9&sv=3)

In the `Payloads` tab, we paste the extensions from Seclists and disable the `Payload encoding` option:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252F9W1LjS6aWorQL5qZIulc%252Fimage.png%3Falt%3Dmedia%26token%3Dd553cab8-dc36-40ab-bdb6-b146d92c2aa3&width=768&dpr=3&quality=100&sign=d90f524e0856f9be02a14c1ea4dd6ce8&sv=3)

We start the fuzzing and observe the results. We get 2 types of responses:

- `Length 225: Extension not allowed`
    

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FQOglq8lZd4pwngNWDsax%252Fimage.png%3Falt%3Dmedia%26token%3Dae70ff64-4654-446a-a694-e08e07fb4a57&width=768&dpr=3&quality=100&sign=b9b1390a8b75de72fce799eed41a8989&sv=3)

- `Length 227/226: Only images are allowed`
    
![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FM2A5GpxuP3oMeiiadZ6A%252Fimage.png%3Falt%3Dmedia%26token%3D6ca485a1-811d-440d-8834-3b7b12c1e60f&width=768&dpr=3&quality=100&sign=ee09c9c05bef7427c2b8a02d2911e2e0&sv=3)

We could try, for example, that `.phar` extension with a character injection using a double extension, which might bypass the filters.

### Content-Type Fuzzing

Let's try uploading a legitimate image to test content-types with status 200, and we'll add `Content-Type` as a variable:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FjVDvTy34Ryg6r4CennUq%252Fimage.png%3Falt%3Dmedia%26token%3De40bf158-772f-4135-90b4-33043f64a847&width=768&dpr=3&quality=100&sign=d36e20c543314e1024033b8dfb80e788&sv=3)

In the Payloads tab, we'll paste the wordlist from [Seclists Content-Type](https://github.com/danielmiessler/SecLists/blob/master/Miscellaneous/Web/content-type.txt), but to make the fuzzing more effective we'll filter only image formats, significantly reducing the fuzzing time:

```
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Miscellaneous/Web/content-type.txt
cat content-type.txt | grep 'image/' > image-content-types.txt
```

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FNUF0BMlCgRXT5H2qfANx%252Fimage.png%3Falt%3Dmedia%26token%3D1ac3884f-959d-4c64-9c58-fbf3bf2e7cd9&width=768&dpr=3&quality=100&sign=7adf134d357961aa1df913041abe8b5d&sv=3)

We launch the fuzzing and observe the results. We see many allowed image extensions, such as `gif`, `jpeg`, `png`...

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252Fajao3xP3ZT0fWGHUTWeN%252Fimage.png%3Falt%3Dmedia%26token%3De22741c7-7db8-462e-9e61-df475e995b78&width=768&dpr=3&quality=100&sign=a9a81e29acf620e7d68d64b1f860c8e8&sv=3)

We see that it allows uploading `GIFs`, so we could try changing the file's `MIME-Type` to attempt loading a `shell.php` that mimics a GIF.

### MIME Type

Let's try adding `GIF8` before our shell.php:


```
cat shell.php     
GIF8 <?php system($_REQUEST[cmd]); ?>
```

We upload it and capture the request. It gives us an `extension not allowed`, but notice what happens if we use a double extension for the shell like `shell.gif.phar`:

Note: For executable files, it's important to place the extension at the end (.phar, .php...), otherwise the server will throw an error when opening the file

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FEHJh4qCD19HwvswFpmh8%252Fimage.png%3Falt%3Dmedia%26token%3D6e6b8efd-9b2e-4777-9b28-061f75153a6f&width=768&dpr=3&quality=100&sign=35a895a44b79403b9d0dcb9a551da40e&sv=3)

The shell uploads successfully!

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FiGwzCvd8yJL31Mzy9SPH%252Fimage.png%3Falt%3Dmedia%26token%3Dc520afe9-178d-4e0d-9467-862b8d7bc936&width=768&dpr=3&quality=100&sign=8ec770ff8ca15353a1d9f183d14c3224&sv=3)

Now if we access the following URL, we confirm the shell works and it returns the user ID:

```
http://94.237.54.239:48561/profile_images/shell.gif.phar?cmd=id
```

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252F51Vo7jEWJemVmk3SO95X%252Fimage.png%3Falt%3Dmedia%26token%3D2a91b286-e2c4-4a76-8357-ab08478a65ac&width=768&dpr=3&quality=100&sign=be68c269d622475335e175235a96871e&sv=3)

We obtain the flag in the same way, and as we can see before the flag, the text GIF8 is inserted which corresponds to the Magic Bytes of the GIF format:

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FuSEGSim0lexunWClYalq%252Fimage.png%3Falt%3Dmedia%26token%3D251611ed-1b51-4bc6-9cc9-6a6476e73add&width=768&dpr=3&quality=100&sign=f7829b9b32876092302127ec54fccaf4&sv=3)
