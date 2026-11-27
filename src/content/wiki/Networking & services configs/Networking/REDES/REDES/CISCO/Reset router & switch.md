---
title: "Reset Router & Switch"
category: ["Networking & services configs", "Networking", "REDES", "REDES", "CISCO", "Reset router & switch"]
---

# Reset Router & Switch

**RESET SWITCH WITH PASSWORD:**
https://echaleunvistazo.wordpress.com/2013/04/19/resetear-password-y-actualizar-catalyst-2950/
Hold the "MODE" button for a while and it will restart.

**RESET SWITCH CONFIGURATION:**
```
enable
write erase
delete flash:vlan.dat
reload
```

For example, if we want to delete VLAN 10, we use "no vlan 10", and so on for everything else.

**RESET ROUTER CONFIGURATION:**
```
enable
write erase
reload
```

**VIEW VLAN CONFIGURATION:**
```
show vlan
```

**SAVE CONFIGURATION:**
```
copy running-config startup-config
```