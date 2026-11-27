---
title: "VLAN Native"
category: ["Networking & services configs", "Networking", "REDES", "REDES", "CISCO", "VLAN Native"]
---

# VLAN Native

In Cisco networking devices, the native VLAN refers to the default VLAN used for traffic that is not tagged with any specific VLAN. This VLAN is important in environments where the IEEE 802.1Q standard is implemented for VLAN traffic tagging. Traffic that does not carry a VLAN tag is considered part of the native VLAN.

```
Switch(config)# interface gigabitethernet0/1
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport trunk native vlan 10
```
