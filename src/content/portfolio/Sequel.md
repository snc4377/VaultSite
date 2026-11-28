---
title: "Sequel"
category: ["Sequel"]
---


- MySQL machine
- To get more info in nmap, we also have the `-sC` option
- In this MariaDB instance (the community-developed version of MySQL), the root user doesn't require a password
- We run `mysql -h` (indicates the host to connect to or where the database is located) `ip_server -u` (user) `root`
- ![Pasted image 20240301224118](/VaultSite/wiki-images/Pasted%20image%2020240301224118.png)
- We execute `show databases;` to display all available databases
- Then we use `use database_name;`
- And `show tables;` to view the information
![Pasted image 20240301225039](/VaultSite/wiki-images/Pasted%20image%2020240301225039.png)
- Now with `SELECT * from table_name_we_want_to_access;` we go to `config`
- And there we find the flag
- ![Pasted image 20240301225158](/VaultSite/wiki-images/Pasted%20image%2020240301225158.png)









