---
title: "MEOW"
category: ["HTB", "Machines", "MEOW"]
---

# MEOW

- Connect to the VPN using OpenVPN: `openvpn nombre_vpn`
- Run nmap to identify open ports
- Access the machine via telnet: `telnet ip_maquina` and log in as the root user (no password required)
- Run `ls` to view the directory contents and locate a `.txt` file named `flag`
- Execute it with `cat` to obtain the root flag 