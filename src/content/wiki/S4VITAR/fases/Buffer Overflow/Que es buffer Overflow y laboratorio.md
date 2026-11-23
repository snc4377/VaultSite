---
title: "Que Es Buffer Overflow Y Laboratorio"
category: ["S4VITAR", "fases", "Buffer Overflow", "Que es buffer Overflow y laboratorio"]
---

**Buffer overflow** is a common software vulnerability that can allow an attacker to execute malicious code or take control of a compromised system.

This vulnerability occurs when a program attempts to store **more data** in a **buffer** (temporary memory area for data storage) than was allocated, and when exceeding the buffer's capacity, the extra data is written to adjacent memory areas.

This can allow an attacker to write malicious code into these memory areas and overwrite other critical system data, such as a function's return address or the memory address where a variable is stored, enabling the attacker to take control of the program's flow.

The impacts of a buffer overflow can be severe, as an attacker can exploit this vulnerability to obtain confidential information, steal data, or even gain full control of the system. With sufficient knowledge, attackers may even execute malicious commands on the compromised system.

For the lab, we will set up the environment to practice our first buffer overflow cases.

You will need to install the following:

- **Windows 7 Home Premium**: [https://windows-7-home-premium.uptodown.com/windows](https://windows-7-home-premium.uptodown.com/windows)
- **Immunity Debugger**: [https://immunityinc.com/products/debugger/](https://immunityinc.com/products/debugger/)
- **mona.py**: [https://raw.githubusercontent.com/corelan/mona/master/mona.py](https://raw.githubusercontent.com/corelan/mona/master/mona.py)
- **SLMail**: [https://slmail.software.informer.com/download/](https://slmail.software.informer.com/download/)

Also, remember it is crucial to disable **DEP** (**Data Execution Prevention**), otherwise the buffer overflows we will perform won't work.

DEP (Data Execution Prevention) is a security measure used to prevent the execution of malicious code on compromised systems via buffer overflow.

DEP works by marking certain memory areas as **"non-executable"**, meaning any attempt to execute code in those memory areas will be blocked and trigger an exception.

This is particularly useful for preventing buffer overflow attacks that attempt to exploit code execution in vulnerable memory areas. By marking these memory areas as "non-executable," DEP can prevent malicious code from executing and protect the system from potential damage. However, this may not always be enough to stop an attacker from injecting their malicious instructions.