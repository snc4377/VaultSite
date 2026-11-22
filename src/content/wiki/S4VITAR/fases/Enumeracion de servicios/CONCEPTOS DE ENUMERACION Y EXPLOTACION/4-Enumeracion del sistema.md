This is done after we've compromised the system and gained access. Next, we perform system reconnaissance to identify flaws that allow privilege escalation. These tools are permitted in OSCP (lse).

###### LSE (Linux Smart Enumeration)
- Download the tool from https://github.com/diego-treitos/linux-smart-enumeration
- When executed, this tool will prompt for the password of the user we've compromised
- The tool has 3 reconnaissance levels; use `-h` for more info. Typically we use `-l 2`
- ![[Pasted image 20251209185221.png]]
- This reveals potential privilege escalation paths
- Here we can see other users with shell access
- ![[Pasted image 20251209185359.png]]
- We can check if sudo is possible without a password, read sudoers, etc.
![[Pasted image 20251209185533.png]]
- Critical vulnerabilities are highlighted in red

-------
###### SUID-based Escalation
We'd use this for privilege escalation when we don't have the user's password.

Run `find -perm -4000 -ls 2>/dev/null` to search for SUID permissions. If owned by root with SUID, this lets us temporarily execute the binary as root without passwords.
![[Pasted image 20251209190756.png]]
For example, let's assign SUID to Python:
![[Pasted image 20251209190829.png]]
![[Pasted image 20251209190856.png]]

Now executing python3.9 as non-root user:
![[Pasted image 20251209190934.png]]
![[Pasted image 20251209190955.png]]
Changing the ID shows it's temporarily executing with sudo:
![[Pasted image 20251209191109.png]]
Now we have an interactive shell

-----
###### Capabilities
These are minimal permissions for programs to function normally. Assigned individually to avoid granting full privileges.

`getcap -r / 2>/dev/null` recursively searches from root for capabilities.

**EXAMPLE**
Set with `setcap cap_setuid+ep /usr/bin/python3.9`

Now search again with getcap:
![[Pasted image 20251209193026.png]]
Check for SUID (none found):
![[Pasted image 20251209193327.png]]
But we see the capability in parallel:
![[Pasted image 20251209193359.png]]
This specific capability allows setting user ID:
![[Pasted image 20251209193455.png]]
LSE should report this, but this is the manual method for better understanding.

----
###### SCHEDULED TASKS
We check if root periodically executes any writable scripts we could modify.

**PSPY**
This tool monitors tasks/commands on the victim machine. Used post-compromise.
![[Pasted image 20251209193942.png]]

**ps -eo user,command**
Can be used to create a custom bash script:
```bash
#!/bin/bash

# Ctrl+C
trap ctrl_c SIGINT
old_process=$(ps -eo user,command)                   # Stores full command output
while true; do                                      # Infinite loop
new_process=$(ps -eo user,command)                 # New captures more commands over time
diff <(echo "$old_process") <(echo "$new_process") | grep "[\>\<]" | grep -v ""  # Compare old vs new, filter changes
old_process=$new_process                           # Update baseline
done
```

![[Pasted image 20251209195543.png]]

###### **GTFOBINS**
Critical resource: https://gtfobins.github.io/

Shows how to exploit found binaries.

Example: if `find` has SUID permissions:
![[Pasted image 20251209200119.png]]
Executing the shown command grants elevated privileges:
![[Pasted image 20251209200204.png]]
![[Pasted image 20251209200309.png]]
Also shows capability exploitation for binaries:
![[Pasted image 20251209200351.png]]
