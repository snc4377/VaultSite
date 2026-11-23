---
title: "3 Generación De Bytearrays Y Detección De Badchars"
category: ["S4VITAR", "fases", "Buffer Overflow", "3 - Generación de Bytearrays y detección de Badchars"]
---

In generating our malicious shellcode for buffer overflow exploitation, some characters may not be interpreted correctly by the target program. These characters are known as **"badchars"** and can cause the shellcode to fail or the target program to crash unexpectedly.

To prevent this, it's crucial to identify and remove badchars from the shellcode. In this class, we'll see how to use Immunity Debugger's **Mona** functionality to generate different bytearrays containing nearly all possible characters, then identify which ones the target program fails to interpret.

Once badchars are identified, they can be excluded from the final shellcode, generating new shellcode without these characters. To identify badchars, various techniques can be used, such as injecting different bytearrays with consecutive hexadecimal characters, which helps detect characters the target program cannot interpret.

These characters will appear in the stack (**ESP**), where we'll observe which ones aren't being properly represented, thus identifying the badchars.


