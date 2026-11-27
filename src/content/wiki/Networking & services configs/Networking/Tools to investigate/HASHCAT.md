---
title: "HASHCAT"
category: ["Networking & services configs", "Networking", "Tools to investigate", "HASHCAT"]
---

# HASHCAT

### ⚡ What is it?

**Hashcat** is the world's fastest password cracking tool. It leverages your **GPU's** power to perform brute force and dictionary attacks against hashes.

### 🎯 When to use it?

- When you obtain a password **hash** (from a database, `/etc/shadow`, Windows NTLM, etc.).
  
- When you have a **JWT** and want to discover its "Secret".
  
- To crack **Wi-Fi** handshakes (WPA2).
  
- To open protected files (ZIP, PDF, Office) if you have their extracted hash.

---

### 📝 Basic Syntax

Bash

```
hashcat -m [MODO] -a [ATAQUE] [ARCHIVO_HASH] [DICCIONARIO]
```

Note title: HASHCAT

### 🚩 Essential Flags

- `-m <number>`: **Hash Type**. Defines which hash type you're attacking (MD5, SHA, JWT...).
    
- `-a <number>`: **Attack Mode**. How you'll attack.
    
    - `0`: Dictionary (Wordlist).
        
    - `3`: Pure brute force (Mask).
        
- `-o <file>`: Saves results to an output file.
    
- `--show`: Shows hashes you've **already** cracked (doesn't crack them again).
    
- `-O`: Optimized (faster, but limits password length).
    
- `--force`: Required if using a VM without dedicated graphics (ignores warnings).
    

---

### 🔢 Common Modes (-m)

_(You can search for them with `hashcat --help | grep "name"`)_

|**Code**|**Hash Type**|**Common Use**|
|---|---|---|
|**0**|MD5|Legacy CMS, old databases|
|**1000**|NTLM|Windows (SAM/LSASS dumps)|
|**1800**|sha512crypt|Linux (`/etc/shadow`)|
|**3200**|bcrypt|Modern web, protected Linux systems|
|**16500**|JWT (JSON Web Token)|APIs, Web Authentication|
|**22000**|WPA-PBKDF2-PMKID|Wi-Fi handshakes|

---

### 🔥 Example Commands

#### 1. Dictionary Attack (Basic)

Standard attack using `rockyou.txt`.

Bash

```
hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt
```

Note title: HASHCAT

#### 2. Cracking a JWT (Web)

To extract the secret from a token.

Bash

```
hashcat -m 16500 jwt.txt /usr/share/wordlists/rockyou.txt
```

Note title: HASHCAT

#### 3. Rule-Based Attack (Best64)

Adds suffixes, prefixes, and mutations to the dictionary (e.g., transforms "password" into "password123"). **Highly effective**.

Bash

```
hashcat -m 1000 -a 0 hash.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

Note title: HASHCAT

#### 4. View already cracked passwords

If Hashcat finishes and you didn't see the password, use this:

Bash

```
hashcat -m 0 hashes.txt --show
```

Note title: HASHCAT

---

### 💡 Pro Tips

- **Identify the Hash:** If you don't know what hash it is, use an online tool like `haiti` or the command `hashid hash.txt`.