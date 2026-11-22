
A padding oracle attack (**Padding Oracle Attack**) is a type of attack against encrypted data that allows the attacker to **decrypt** the data's content **without knowing the key**.

An oracle refers to a "hint" that provides an attacker with information about whether the action they are performing is correct or not. Imagine playing a board or card game with a child: their face lights up with a big smile when they think they're about to make a good move. That's an oracle. As their opponent, you can use this oracle to plan your next move accordingly.

Padding is a specific cryptographic term. Some ciphers, which are the algorithms used to encrypt data, operate on **fixed-size data blocks**. If the data you want to encrypt doesn't perfectly fit these blocks, it is automatically **padded** until it does. Many padding schemes require padding to always be present, even if the original input was the correct size. This ensures the padding can always be safely removed after decryption.

Combining these two elements, a software implementation with a padding oracle reveals whether the decrypted data has valid padding. The oracle could be as simple as returning a "Invalid padding" message, or something more subtle like taking significantly different time to process a valid versus invalid block.

Block ciphers have another property called "**mode**," which determines how the first block's data relates to the second block's data, and so on. One of the most common modes is **CBC**. CBC uses an initial random block called the "**initialization vector**" (**IV**), and combines the previous block with the static cipher output so that encrypting the same message with the same key doesn't always produce the same encrypted output.

An attacker can use a padding oracle, combined with CBC's data structure, to send slightly modified messages to the code exposing the oracle and keep sending data until the oracle indicates correctness. From this response, the attacker can decrypt the message byte by byte.

Modern computer networks are so high-quality that an attacker can detect very small timing differences (less than 0.1 ms) in remote systems. Applications that assume correct decryption only occurs when data is unaltered may be vulnerable to attacks from tools designed to observe differences between correct and incorrect decryption. While this timing difference may be more significant in some languages or libraries than others, it is now considered a practical threat for all languages and libraries when considering the application's error response.

This type of attack relies on the ability to modify encrypted data and test the result with the oracle. The only way to fully mitigate the attack is to detect changes in the encrypted data and reject any actions on them. The standard way to do this is to create a signature for the data and validate it before performing any operations. The signature must be verifiable, and the attacker must not be able to create it; otherwise, they could modify the encrypted data and compute a new signature based on the altered data.

A common type of suitable signature is a "**Hash-based Message Authentication Code**" (**HMAC**). An HMAC differs from a checksum in that it requires a secret key, known only to the HMAC generator and validator. Without this key, a correct HMAC cannot be generated. When receiving data, you can independently compute the HMAC using the secret key shared between you and the sender, then compare the sent HMAC with your computed one. This comparison must be constant-time; otherwise, you've introduced another detectable oracle, enabling a different type of attack.

In summary, to securely use CBC-padded block ciphers, they must be combined with an HMAC (or other data integrity check) validated via constant-time comparison before attempting decryption. Since all modified messages take the same time to generate a response, the attack is prevented.

The padding oracle attack may seem complex, as it involves a feedback process to guess the encrypted content and modify the padding. However, tools like **PadBuster** can automate much of the process.

PadBuster is a tool designed to automate the decryption of messages encrypted in **CBC** mode using **PKCS #7** padding. It allows attackers to send HTTP requests with **malicious padding** to determine if the padding is valid. This way, attackers can guess the encrypted content and decrypt the entire message.

#### Lab
For this lab, we'll use a VulnHub machine: PENTESTER LAB PADDING ORACLE.

First, we'll perform an `arp-scan` for network reconnaissance:

Execute:
```bash
arp-scan -I ens33 --localnet --ignoredups
```
![[Pasted image 20260126210015.png]]
We've located the machine at IP 192.168.111.35.

Now, let's run `nmap` to check open ports:
```bash
nmap -p- -sS --open --min-rate 5000 -vvv -n -Pn 192.168.111.35
```
![[Pasted image 20260126210221.png]]
We see port 80 (HTTP) is open, so let's check the website:
![[Pasted image 20260126210304.png]]

##### ENCRYPTION EXPLANATION
This website uses CBC (Cipher-Block Chaining) encryption, a block cipher method that encrypts user-provided data while ensuring authentication.
![[Pasted image 20260126210601.png]]
The cipher uses fixed-size blocks:
![[Pasted image 20260126210825.png]]
To ensure the text fits perfectly into the blocks, padding is used. A common method is PKCS7. Our string above is "SUPERSECRET123", which is missing 2 bytes to fill the block, so it pads with the number of missing bytes (e.g., 0x02 for 2 bytes, 0x05 for 5 bytes).

When an application decrypts this message, it first decrypts the text and then removes the padding. If during padding removal there's detectable behavior (errors, missing results, slower responses, etc.), we have a Padding Oracle.

As attackers, we want to detect this behavior to decrypt the data. We could also start with plaintext and encrypt it.

https://www.youtube.com/watch?v=3nhiZ_bdBz8

**XOR**
###### 1. XOR: The Binary "Master Key"

**XOR** ($\oplus$) is a logical operation that compares two bits. Its rule is simple: **If different, output 1; if equal, output 0.**

$$\begin{array}{|c|c|c|} \hline A & B & A \oplus B \\ \hline 0 & 0 & 0 \\ \hline 0 & 1 & 1 \\ \hline 1 & 0 & 1 \\ \hline 1 & 1 & 0 \\ \hline \end{array}$$

**Why is it vital in hacking?**

Because of its magical property: If $A \oplus B = C$, then $A \oplus C = B$.

If you know the result and one part, you can derive the other.

##### LAB
Let's proceed to register on the website:
![[Pasted image 20260126213634.png]]

Once logged in, if we press Ctrl+Shift+C and go to Storage, we'll see a session cookie:
![[Pasted image 20260126213740.png]]

If the website is vulnerable to padding oracle, we can decrypt the cookie with PadBuster.

**PadBuster**
PadBuster is a tool designed to automate the decryption of messages encrypted in **CBC** mode using **PKCS7** padding. It allows attackers to send HTTP requests with **malicious padding** to determine if the padding is valid. This way, attackers can guess the encrypted content and decrypt the entire message.

![[Pasted image 20260126213905.png]]

The PadBuster command format is:
```bash
padbuster "URL" "EncryptedStuff" "BlockSize" 'auth=Cookie'
```
For us, it would look like:
![[Pasted image 20260126214501.png]]
We see it successfully decoded the cookie:
![[Pasted image 20260126214559.png]]
Now that we've seen the plaintext cookie is "user=s4vitar", we'll encode "user=admin" to replace our cookie.

We'll do this by adding `-plaintext 'user=admin'` to the command  
![[Pasted image 20260126214813.png]]  
![[Pasted image 20260126214827.png]]  
Paste the cookie in the browser and if we refresh, we're admin  
![[Pasted image 20260126214923.png]]  
![[Pasted image 20260126214933.png]]  

To make it easier, we created a user named 'cdmin' so the bit flipping is faster  
Another way to do it is by capturing the packet with Burp Suite and using the Intruder to perform a bitflipper attack (which is brute-forcing by modifying bits until the server stops returning errors)  
![[Pasted image 20260126215155.png]]  
Select the cookie and set the attack to Sniper mode  

Now go to the Payloads section, set Payload type to Bitflipper, set Format of original data to Literal Value, and uncheck URL-encode characters  
Start the attack  
![[Pasted image 20260126215420.png]]  
We see one request that's different, and if we check the Response tab, it shows we're logged in as admin, so we copy the cookie  
![[Pasted image 20260126215916.png]]  
![[Pasted image 20260126215929.png]]



