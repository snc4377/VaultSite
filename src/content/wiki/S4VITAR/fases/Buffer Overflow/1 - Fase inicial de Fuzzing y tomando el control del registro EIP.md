Note title: Untitled

In the initial phase of exploiting a buffer overflow, one of the first tasks is to determine the limits of the target program. This is done by testing the input of more characters than allowed in various input fields of the program, such as a text string or a file, until it is detected that the application becomes corrupted or crashes.

Once the limit of the input field is found, the next step is to determine the **offset**, which corresponds to the exact number of characters that need to be input to cause corruption in the program and, therefore, to overwrite the value of the EIP register.

The **EIP** (**Extended Instruction Pointer**) register is a CPU register that points to the memory address where the next instruction to be executed is located. In a successful buffer overflow, the value of the EIP register is overwritten with **an address controlled by the attacker**, allowing malicious code to be executed instead of the program's original code.

Therefore, the goal of determining the offset is to identify the exact number of characters that need to be input into the field to overwrite the value of the EIP register and point to the memory address controlled by the attacker. Once the offset is known, the attacker can design a custom exploit for the target program that allows taking control of the EIP register and executing malicious code.

