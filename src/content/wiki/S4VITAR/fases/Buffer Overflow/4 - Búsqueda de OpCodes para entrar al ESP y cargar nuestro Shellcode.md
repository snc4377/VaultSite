Once the malicious shellcode has been generated and the badchars have been identified, the next step is to make the program flow enter the shellcode so it can be interpreted. The idea is to make the EIP register point to a memory address where an **opcode** that performs a jump to the **ESP** register (**JMP ESP**) is applied, as this is where the shellcode resides. This is necessary because initially, we cannot make EIP point directly to our shellcode.

To find the **JMP ESP** opcode, various tools can be used, such as **mona.py**, which allows searching for opcodes in specific modules of the target program's memory. Once the ‘**JMP ESP**‘ opcode has been found, the value of the EIP register can be overwritten with the memory address where the opcode is located, enabling a jump to the ESP register and execution of the malicious shellcode.

The search for opcodes to enter the ESP register and load the shellcode is a technique used to make the program flow enter the shellcode for interpretation. The JMP ESP opcode is used to jump to the memory address of the ESP register, where the shellcode resides.

![[Búsqueda de OpCodes para entrar al ESP y cargar nuestro Shellcode.mp4]]