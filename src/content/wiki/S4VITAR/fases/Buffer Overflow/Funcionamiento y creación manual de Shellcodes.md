# Shellcodes

**Shellcodes** are small, highly optimized programs used to exploit security vulnerabilities and execute malicious code on a target machine. Shellcodes are typically written in **assembly language** to ensure fast and efficient execution.

In this class, we will explore how shellcodes work behind the scenes by manually creating some shellcodes. For example, we will attempt to create a shellcode that displays the message "**Hello World**" on the console using system interrupts. Additionally, we will try to apply a system-level call to execute a desired command.

Once the resulting binary is generated, the **objdump** command can be used to convert the generated binary file into a shellcode that can be used in a Buffer Overflow.

We will experiment with manually creating a shellcode to understand what happens under the hood when using tools like MSFVenom. The goal is to go from a simple Python instruction to machine code that the Linux kernel executes directly.

### 1. Generation and Initial Analysis

First, we generate a 32-bit ELF binary that simply performs an `echo`. If we use `xxd`, we see that the strings are reversed due to **Little-Endian**.

- **Command:** `msfvenom -p linux/x86/exec cmd="echo hello world" -f elf -o binary`
    
- **Hex Analysis:** `xxd binary`
    

If we try to read it as text, we won't see anything clear, but that's where disassembly comes in.

### 2. Understanding Syscalls (System Calls)

For the binary to do something, it has to communicate with the Kernel. In 32-bit systems, this is done through the `int 0x80` interrupt.

- **How does the system know what to do?** We look at the **EAX** register.
    
- **Example:** If we want to use the `write` function (to display text), the ID is **4**.
    
- **Structure of `write`:**
    
    - `EAX`: 4 (Function ID)
        
    - `EBX`: 1 (Standard Output / Screen)
        
    - `ECX`: Memory address where the text is located.
        
    - `EDX`: Length of the text.
        

### 3. Manual Shellcode Creation (`.asm`)

We prepare our own assembly code to print "Hello World" without relying on automatic generators.

- **Stack:** We use `push` to place the text "Hello World" on the stack. Since we work in 4-byte increments, we need to align the strings and insert them in reverse order.
    
- **Example Code:**
    
    Code snippet
    
    ```
    mov eax, 4      ; Syscall write
    mov ebx, 1      ; STDOUT
    push 0x0a6f646e ; "ndo\n"
    push 0x756d2061 ; "a mu"
    push 0x6c6f6820 ; " hol"
    mov ecx, esp    ; ECX apunta al tope de la pila (donde está nuestro texto)
    mov edx, 11     ; Longitud
    int 0x80        ; ¡Ejecuta!
    ```
    

### 4. Compilation and OpCode Extraction

Once we have the `.asm` file, we compile it and extract the bytes (the "OpCodes") that will form our final shellcode.

1. **Assemble:** `nasm -f elf code.asm`
    
2. **Link:** `ld -m elf_i386 -o final code.o`
    
3. **Extract bytes:** We use a Bash "one-liner" with `objdump` to get the string in the format `\xbb\x01\x00...`
    

### 5. Privilege Escalation: The `/bin/sh` Shellcode

The final step is to create a shellcode that gives us a shell. We use the `execve` syscall (ID **11** in 32-bit).

- **The trick:** We push `/bin//sh` onto the stack (the double slash is to align to 8 bytes and avoid null bytes).
    
- **Execution:** Upon completion, the `EAX` register will contain 11, `EBX` will point to the shell path on the stack, and the system will return control to us as an active shell.
