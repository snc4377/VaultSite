This is the English version of your OpenVAS (GVM) guide, optimized for your website. I have updated the terminal prompts to your username **5nch7344**, improved the technical flow, and organized the troubleshooting steps for better readability.

---

## OpenVAS: The Open Source Vulnerability Management Guide

**OpenVAS** (Open Vulnerability Assessment System) is a powerful, full-featured vulnerability scanner and a core component of the **Greenbone Vulnerability Manager (GVM)**. It is the leading open-source alternative to proprietary scanners, allowing security professionals to perform both authenticated and unauthenticated testing across networks and servers.

Unlike other tools, OpenVAS is completely free and integrated directly into the Kali Linux repositories.
![[Pasted image 20260428175940.png]]

---

### Installation

**Install GVM**

```
5nch7344@kali$ sudo apt update
5nch7344@kali$ sudo apt install gvm -y
```

**Initial Setup** Run the setup script. This will configure the database and download the latest vulnerability feeds (SCAP, CERT, and GVMD).

```
5nch7344@kali$ sudo gvm-setup
```

**Security** 

```
5nch7344@kali$ sudo apt install ufw
5nch7344@kali$ sudo ufw allow 80
5nch7344@kali$ sudo ufw allow 9392
5nch7344@kali$ sudo ufw enable
```

**Manual Database Initialization**

If the automatic setup fails, you must manually create the PostgreSQL database and extensions required by GVM.


```
5nch7344@kali$ sudo runuser -u postgres -- /usr/share/gvm/create-postgresql-database

[i] User _gvm already exists in PostgreSQL
[*] Creating database
[*] Creating permissions... CREATE ROLE
[*] Applying permissions... GRANT ROLE
[*] Creating extension uuid-ossp... CREATE EXTENSION
[*] Creating extension pgcrypto... CREATE EXTENSION
[*] Creating extension pg-gvm... CREATE EXTENSION
```

### User Management & Vulnerability Feeds


**Create a New User**

```
5nch7344@kali$ sudo runuser -u _gvm -- gvmd --create-user=5nch7344 --password=YourPassword
User created.
```

**Synchronize Feeds**

```
5nch7344@kali$ sudo greenbone-feed-sync
```


**Starting/Stopping the Service:**

```
5nch7344@kali$ sudo gvm-start  # Access via https://localhost:9392
5nch7344@kali$ sudo gvm-stop   # Stop all GVM services
```
---

### Troubleshooting Common Installation Errors

GVM is sensitive to PostgreSQL versions and system library updates. Here is how to fix the most common "roadblocks."

#### PostgreSQL Version Mismatch (v16 vs v17)

If `gvm-setup` fails stating that version 17 is required but 16 is running on the default port (5432):
> [!shell] shellsession
sudo gvm-setup
[>] Starting PostgreSQL service
[-] ERROR: The default PostgreSQL version (16) is not 17 that is required by libgvmd
[-] ERROR: libgvmd needs PostgreSQL 17 to use the port 5432
[-] ERROR: Use pg_upgradecluster to update your PostgreSQL cluster

1. **Check clusters:**
    
    ```
    5nch7344@kali$ pg_lsclusters
    ```
    
2. **Stop the old version:**
    
    ```
    5nch7344@kali$ sudo pg_ctlcluster 16 main stop
    ```
    
3. **Change Port for Version 17:** Edit `/etc/postgresql/17/main/postgresql.conf` and change `port = 5433` to `port = 5432`.
    
4. **Restart & Resume Setup:**
    
    ```
    5nch7344@kali$ sudo pg_ctlcluster 17 main start
    5nch7344@kali$ sudo gvm-setup
    ```
    

#### Database Collation Error

If you see an error regarding "collation version mismatch" (usually after a system update), follow these steps inside the PostgreSQL prompt:

```
5nch7344@kali$ sudo -u postgres psql
```

**SQL prompt**

```
-- Fix template1
UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template1';
REINDEX DATABASE template1;
ALTER DATABASE template1 REFRESH COLLATION VERSION;
UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template1';

-- Fix template0
UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template0';
REINDEX DATABASE template0;
ALTER DATABASE template0 REFRESH COLLATION VERSION;
UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template0';
\q
```

---
### Running Your First Scan

After logging into the web interface (`https://localhost:9392`), follow these steps:
![[Pasted image 20260428180414.png]]
1. **Check Feed Status:** Navigate to **Administration > Feed Status**. Do not start a scan until the status is **Current**.
    ![[Pasted image 20260428180441.png]]
    ![[Pasted image 20260428180454.png]]
    
2. **Add a Target:** * Go to **Configuration > Targets**.
    
    - Click the "New Target" icon.
        
    - Enter the IP/Range. To scan all ports, use: `T:1-65535,U:1-65535`.
        ![[Pasted image 20260428180512.png]]
1. **Create a Task:**
    
    - Go to **Scans > Tasks**.
        
    - Create a "New Task" and link it to the Target you just created.
        
    - Select your **Scan Config** (e.g., _Full and Fast_).
        ![[Pasted image 20260428180528.png]]
