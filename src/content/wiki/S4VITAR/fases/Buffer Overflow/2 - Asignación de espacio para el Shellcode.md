Once the **offset** has been found and the value of the **EIP** register has been overwritten in a buffer overflow, the next step is to identify where in memory the characters entered in the input field are being represented.

After overwriting the value of the EIP register, any additional characters we input into the field will be represented, as seen in Immunity Debugger, at the beginning of the **stack** in the **ESP** (**Extended Stack Pointer**) register. The ESP (Extended Stack Pointer) is a CPU register used to manage the stack in a program. The stack is a temporary memory area used to store values and **return addresses** of functions as they are called in the program.

Once the location of the characters in memory has been identified, the main idea at this point is to introduce a **shellcode** in that location, which consists of low-level instructions that, in this case, will correspond to a malicious instruction.

The shellcode is introduced into the stack and placed at the same memory address where the overwritten characters were located. In other words, the buffer overflow is exploited to execute the malicious shellcode and take control of the system.

It is important to note that the shellcode must be carefully designed to avoid detection as a malicious program and must be compatible with the CPU architecture and operating system being targeted.

In summary, allocating space for the shellcode involves identifying the location in memory where the overwritten characters were placed in the buffer overflow and placing the malicious shellcode there. However, not all characters of the shellcode can be interpreted. 