---
title: "5 Uso De NOPs, Desplazamientos En Pila E Interpretación Del Shellcode Para Lograr RCE"
category: ["S4VITAR", "fases", "Buffer Overflow", "5 - Uso de NOPs, desplazamientos en pila e interpretación del Shellcode para lograr RCE"]
---

Once the address of the opcode that performs the jump to the **ESP** register has been found, the shellcode may not be interpreted correctly because its execution might require more time than the processor has available before moving to the next program instruction.

To solve this problem, techniques such as inserting **NOPS** (**no-operation instructions**) before the shellcode on the stack are commonly used. NOPS perform no operation but allow the processor additional time to interpret the shellcode before proceeding to the next program instruction.

Another commonly used technique is stack shifting, which involves modifying the ESP register to reserve additional space for the shellcode and allow it to execute smoothly. For example, the instruction "**sub esp, 0x10**" can be used to shift the ESP register **16 bytes** down the stack and reserve extra space for the shellcode.

With this, we would have successfully exploited the system through Buffer Overflow.





