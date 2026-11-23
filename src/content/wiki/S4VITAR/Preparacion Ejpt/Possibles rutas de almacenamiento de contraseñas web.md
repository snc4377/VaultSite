---
title: "Possibles Rutas De Almacenamiento De Contraseñas Web"
category: ["S4VITAR", "Preparacion Ejpt", "Possibles rutas de almacenamiento de contraseñas web"]
---

Note title: Untitled

`/var/www/html/` go to this path and list to see folders or files and search

default storage path for linpeas on attacking machine usr/share/peass/linpeas



CMS (Content Management Systems)

- **WordPress:** `/var/www/html/wp-config.php`
- **Joomla:** `/var/www/html/configuration.php`
- **Drupal:** `/var/www/html/sites/default/settings.php`
- **PrestaShop (Modern):** `/var/www/html/app/config/parameters.php`
- **Magento 2:** `/var/www/html/app/etc/env.php`
- **OpenCart:** `/var/www/html/config.php` and `/var/www/html/admin/config.php`

Development Frameworks

- **Laravel:** `/var/www/html/.env`
- **Symfony:** `/var/www/html/.env`
- **CodeIgniter:** `/var/www/html/application/config/database.php`

Critical System Files (Linux)

- **User password hashes:** `/etc/shadow` (root read-only).
- **MySQL/MariaDB configuration:** `/etc/mysql/my.cnf` or `/etc/mysql/mariadb.conf.d/50-server.cnf`.
- **PostgreSQL configuration:** `/etc/postgresql/[version]/main/pg_hba.conf`.
- **Access logs (may contain credentials by mistake):** `/var/log/apache2/access.log` or `/var/log/nginx/access.log`.
- **Command history (passwords typed by mistake):** `/home/[user]/.bash_history` or `/root/.bash_history`.

**Note:** In control panels like **cPanel** or **Plesk**, the absolute path usually changes to `/home/[user]/public_html/` instead of `/var/www/html/`
