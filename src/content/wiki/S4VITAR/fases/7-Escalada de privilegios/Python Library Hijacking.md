When we talk about **Python Library Hijacking**, we are referring to an attack technique that exploits the way Python searches for and loads libraries to inject malicious code into a script. The attack occurs when an attacker creates or modifies a library in a path accessible by the Python script, such that when the script imports it, the malicious version is loaded instead of the legitimate one.

The attack is carried out as follows: the attacker searches for a library used by the script and replaces it with their own malicious version. This library can be a standard Python library or an external library downloaded and installed by the user. The attacker places their malicious version of the library in an accessible path before the legitimate library is found.

Generally, Python starts searching for these libraries in the current working directory and then in the paths defined in the `sys.path` variable. If the attacker has write access to any of the paths defined in `sys.path`, they can place their own malicious version of the library there and cause the script to load it instead of the legitimate one.

Additionally, the attacker can also create their own library in the current working directory, as Python starts the search in this directory by default. If during the loading of these libraries from the legitimate script, the attacker manages to hijack them, they will achieve an alternative execution of the program.

---

Let's imagine we have two users: `s4vitar`, a normal user, and `manolito`, who is root. When running `sudo -l`, we see that we can execute a `.py` file as the user `manolito`.

![Pasted image 20260213210636](/VaultSite/wiki-images/Pasted%20image%2020260213210636.png)

We see that it's a normal `.py` file, nothing important.

![Pasted image 20260213210813](/VaultSite/wiki-images/Pasted%20image%2020260213210813.png)
![Pasted image 20260213210832](/VaultSite/wiki-images/Pasted%20image%2020260213210832.png)

However, by importing the `sys` library and displaying the `sys.path`, we can see different paths. We notice a blank space that refers to the current directory, which is why it doesn't appear.

![Pasted image 20260214115530](/VaultSite/wiki-images/Pasted%20image%2020260214115530.png)

In the script, we use the `hashlib` library and search for its path. This concept is very similar to path hijacking with `ls`. When you run `ls` to list a directory, the system searches for the absolute path of that command among a series of directories. Let's imagine there are 15 paths where it searches, and the `ls` command is in the 5th path. If I create my own `ls` command that, for example, runs `whoami`, and place it in the 3rd directory, when I execute `ls`, it will run `whoami`.

![Pasted image 20260214115627](/VaultSite/wiki-images/Pasted%20image%2020260214115627.png)

The same thing happens here. We see that `hashlib` is in the 3rd path. If we create a `hashlib` library in the first path that launches an interactive shell:

![Pasted image 20260214120249](/VaultSite/wiki-images/Pasted%20image%2020260214120249.png)

If we execute it, we would gain a bash shell as the `manolito` user (root).

![Pasted image 20260214120346](/VaultSite/wiki-images/Pasted%20image%2020260214120346.png)

---

The important thing about both path hijacking and Python library hijacking is to review the paths where Python searches for modules or the `$PATH` in path hijacking, and check in which directories we have write permissions. We also need to see if those directories are positioned to the left of where the file we want to impersonate is located.

And, of course, if we have write permissions on the library, we could edit it to give ourselves a root shell.

![Pasted image 20260214121123](/VaultSite/wiki-images/Pasted%20image%2020260214121123.png)


