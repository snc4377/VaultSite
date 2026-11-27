---
title: "VTP"
category: ["Networking & services configs", "Networking", "REDES", "REDES", "CISCO", "VTP"]
---

# VTP

VLAN Trunking Protocol is a Cisco switch protocol where, if you set a switch to server mode, the VLANs created on this switch will automatically be created on the other switches.

SERVER CONFIGURATION (MAIN SWITCH):
```
en
conf t
vtp domain NAME
vtp password PASSWORD
vtp mode server
```

CLIENT CONFIGURATION (OTHER SWITCHES):
```
vtp mode client
vtp domain NAME
vtp password PASSWORD
```