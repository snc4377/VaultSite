---
title: "Switch Cisco Comandos"
category: ["apuntes david", "2024", "Switch cisco comandos"]
---

10.2.4 Shortcut and Hotkeys

The IOS CLI provides hotkeys and shortcuts that facilitate configuration, monitoring, and troubleshooting.

Commands and keywords can be shortened to the minimum number of characters that uniquely identify a selection. For example, the **configure** command can be shortened to **conf**, since **configure** is the only command starting with **conf**. A shorter version like **con** won't work, as multiple commands start with **con**. Keywords can also be abbreviated.

The table shows key combinations for enhanced command line editing.

| Key Combination | Description |
|---|---|
| **Tab** | Completes a partial command name entry. |
| **Backspace** | Deletes the character to the left of the cursor. |
| **Ctrl+D** | Deletes the character at the cursor position. |
| **Ctrl+K** | Deletes all characters from the cursor to the end of the command line. |
| **Esc D** | Deletes all characters from the cursor to the end of the word. |
| **Ctrl+U** or **Ctrl+X** | Deletes all characters from the cursor to the start of the command line. |
| **Ctrl+W** | Deletes the word to the left of the cursor. |
| **Ctrl+A** | Moves cursor to the beginning of the line. |
| **Left Arrow** or **Ctrl+B** | Moves cursor one character left. |
| **Esc B** | Moves cursor one word left. |
| **Esc F** | Moves cursor one word right. |
| **Right Arrow** or **Ctrl-F** | Moves cursor one character right. |
| **Ctrl+E** | Moves cursor to the end of the command line. |
| **Up Arrow** or **Ctrl-P** | Recalls previous command from history buffer, starting with most recent. |
| **Down Arrow** or **Ctrl+N** | Goes to next line in history buffer. |
| **Ctrl-R**, **Ctrl-I** or **Ctrl-L** | Redisplays system prompt and command line after receiving a console message. |

**Note:** While the **Delete** key typically removes the character to the right of the prompt, the IOS command structure doesn't recognize the **Delete** key.

When command output exceeds terminal window capacity, IOS displays a **«—More—»** message. The following table describes key combinations available during this prompt.

| Key Combination | Description |
|---|---|
| **Enter** | Displays next line. |
| **Space** | Displays next screen. |
| Any other key* | Ends display output and returns to prompt. <br>*Except "y", which answers "yes" to the **--More--** prompt and acts as **Space**. |

This table lists commands for exiting operations.

| Key Combination | Description |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ctrl-C** | In any configuration mode: exits configuration mode and returns to privileged EXEC mode. In configuration mode: aborts and returns to system prompt. |
| **Ctrl-Z** | In any configuration mode: exits configuration mode and returns to privileged EXEC mode. |
| **Ctrl-Shift-6** | Multipurpose break sequence used to cancel DNS lookups, traceroutes, pings, and interrupt IOS processes. |

**show running-config**

Verifies current configuration and settings.

```
R1# show running-config
(Output omitted)!versión 15.5service timestamps debug datetime msecservice timestamps log datetime msecservice password-encryption!hostname R1!interface GigabiteThernet0/0/0 description Enlace a R2 ip address 209.165.200.225 255.255.255.252 negotiation auto!interface GigabitEthernet0/0/1 description Enlace a LAN ip address 192.168.10.1 255.255.255.0 negotiation auto!router ospf 10 network 192.168.10.0 0.0.0.255 area 0 network 209.165.200.224 0.0.0.3 area 0!banner motd ^C ¡Solamente acceso autorizado! ^C!líne con 0 password 7 14141B180F0B loginline vty 0 4 password 7 00071A150754 login transport input telnet ssh!endR1#
```



**show interfaces**

Checks the interface status and displays any error messages.

```
R1# show interfaces
GigabitEthernet0/0/0 is up, line protocol is up  Hardware is ISR4321-2x1GE, address is a0e0.af0d.e140 (bia a0e0.af0d.e140)  Description: Enlace a R2  Internet address is 209.165.200.225/30  MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec,    reliability 255/255, txload 1/255, rxload 1/255  Encapsulation ARPA, loopback not set  Keepalive not supported  Full Duplex, 100Mbps, link type is auto, media type is RJ45  output flow-control is off, input flow-control is off  ARP type: ARPA, ARP Timeout 04:00:00  Last input 00:00:01, output 00:00:21, output hang never  Last clearing of "show interface" counters never  Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0  Queueing strategy: fifo  Output queue: 0/40 (size/max)  5 minute input rate 0 bits/sec, 0 packets/sec  5 minute output rate 0 bits/sec, 0 packets/sec    5127 packets input, 590285 bytes, 0 no buffer    Received 29 broadcasts (0 IP multicasts)    0 runts, 0 giants, 0 throttles    0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored    0 watchdog, 5043 multicast, 0 pause input    0 watchdog, 5043 multicast, 0 pause input    0 output errors, 0 collisions, 2 interface resets    0 unknown protocol drops    0 babbles, 0 late collision, 0 deferred    1 lost carrier, 0 no carrier, 0 pause output    0 output buffer failures, 0 output buffers swapped out
```


**show ip interface**

Checks Layer 3 information for an interface.

```
R1# show ip interface
GigabitEthernet0/0/0 is up, line protocol is up  Internet address is 209.165.200.225/30  Broadcast address is 255.255.255.255  Address determined by setup command  MTU is 1500 bytes  Helper address is not set  Directed broadcast forwarding is disabled  Multicast reserved groups joined: 224.0.0.5 224.0.0.6  Outgoing Common access list is not set  Outgoing access list is not set  Inbound Common access list is not set  Inbound access list is not set  Proxy ARP is enabled  Local Proxy ARP is disabled  Security level is default  Split horizon is enabled  ICMP redirects are always sent  ICMP unreachables are always sent  ICMP mask replies are never sent  IP fast switching is enabled  IP Flow switching is disabled  IP CEF switching is enabled  IP CEF switching turbo vector  IP Null turbo vector  Associated unicast routing topologies:        Topology "base", operation state is UP  IP multicast fast switching is enabled  IP multicast distributed fast switching is disabled  IP route-cache flags are Fast, CEF  Router Discovery is disabled  IP output packet accounting is disabled  IP access violation accounting is disabled  TCP/IP header compression is disabled  RTP/IP header compression is disabled  Probe proxy name replies are disabled  Policy routing is disabled  Network address translation is disabled  BGP Policy Mapping is disabled  Input features: MCI Check  IPv4 WCCP Redirect outbound is disabled  IPv4 WCCP Redirect inbound is disabled  IPv4 WCCP Redirect exclude is disabled (Output omitted)
```

Note title: Untitled

**show arp**

Checks the list of known hosts on the local Ethernet LAN.

```
R1# show arp
Protocol   Address          Age (min) Hardware Addr Type InterfaceInternet   192.168.10.1      - a0e0.af0d.e141 ARPA GigabitEthernet0/0/1Internet   192.168.10.10     95 c07b.bcc4.a9c0 ARPA GigabitEthernet0/0/1Internet   209.165.200.225   - a0e0.af0d.e140 ARPA GigabitEthernet0/0/0Internet   209.165.200.226   138 a03d.6fe1.9d90 ARPA GigabitEthernet0/0/0R1#
```

**show ip route**

Checks Layer 3 routing information.

```
R1# show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP   D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area   N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2   E1 - OSPF external type 1, E2 - OSPF external type 2   i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2   ia - IS-IS inter area, * - candidate default, U - per-user static route   o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP   a - application route   + - replicated route, % - next hop override, p - overrides from PfRGateway of last resort is 209.165.200.226 to network 0.0.0.0O*E2 0.0.0.0/0 [110/1] via 209.165.200.226, 02:19:50, GigabitEthernet0/0/0   10.0.0.0/24 is subnetted, 1 subnetsO   10.1.1.0 [110/3] via 209.165.200.226, 02:05:42, GigabitEthernet0/0/0   192.168.10.0/24 is variably subnetted, 2 subnets, 2 masksC   192.168.10.0/24 is directly connected, GigabitEthernet0/0/1L   192.168.10.1/32 is directly connected, GigabitEthernet0/0/1   209.165.200.0/24 is variably subnetted, 3 subnets, 2 masksC   209.165.200.224/30 is directly connected, GigabitEthernet0/0/0L   209.165.200.225/32 is directly connected, GigabitEthernet0/0/0O   209.165.200.228/30 [110/2] via 209.165.200.226, 02:07:19, GigabitEthernet0/0/0R1#
```


# Untitled

show protocols

**show protocols**

Checks which protocols are operational.

```
R1# show protocols
Global values:  Internet Protocol routing is enabledGigabitEthernet0/0/0 is up, line protocol is up  Internet address is 209.165.200.225/30GigabitEthernet0/0/1 is up, lin protocol is up  Internet address is 192.168.10.1/24Serial0/1/0 is down, line protocol is downSerial0/1/1 is down, line protocol is downGigabitEthernet0 is administratively down, line protocol is downR1#
```


**show version**

Checks the device's memory, interfaces, and licenses.

```
R1# show version
Cisco IOS XE Software, Version 03.16.08.S - Extended Support ReleaseCisco IOS Software, ISR Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 15.5(3)S8, RELEASE SOFTWARE(fc2)Technical Support: http://www.cisco.com/techsupportCopyright (c) 1986-2018 by Cisco Systems, Inc.Compiled Wed 08-Aug-18 10:48 by mcpre(Output omitted)ROM: IOS-XE ROMMONR1 uptime is 2 hours, 25 minutesUptime for this control processor is 2 hours, 27 minutesSystem returned to ROM by reloadSystem image file is "bootflash:/isr4300-universalk9.03.16.08.S.155-3.S8-ext.SPA.bin"Last reload reason: LocalSoft(Output omitted)Technology Package License Information:-----------------------------------------------------------------Technology     Technology-package     Technology-package               Current      Type          Next reboot------------------------------------------------------------------appxk9         appxk9       RightToUse    appxk9uck9           None         None          Nonesecurityk9     securityk9   Permanent     securityk9ipbase         ipbasek9     Permanent     ipbasek9cisco ISR4321/K9 (1RU) processor with 1647778K/6147K bytes of memory.Processor board ID FLM2044W0LT2 Gigabit Ethernet interfaces2 Serial interfaces32768K bytes of non-volatile configuration memory.4194304K bytes of physical memory.3207167K bytes of flash memory at bootflash:.978928K bytes of USB flash at usb0:.Configuration register is 0x2102R1#
```
When a host or gateway receives a packet it cannot deliver, it may use an ICMP destination unreachable message to notify the source that the destination or service is unreachable. The message includes a code indicating the reason why the packet could not be delivered.

Some of the destination unreachable codes for ICMPv4 are as follows:

- 0 - Network unreachable  
- 1 - Host unreachable  
- 2 - Protocol unreachable  
- 3 - Port unreachable  
- A technician uses the command **ping 127.0.0.1**. What is the technician testing?  
  The TCP/IP stack on a network host

The correct sequence for establishing a TCP session (also known as the **three-way handshake**) is as follows:

- **Step 1: SYN (A)**  
  The client sends a **SYN** segment to the server to initiate the connection.
  
- **Step 2: SYN + ACK (B)**  
  The server responds with a **SYN + ACK** segment, acknowledging the client's SYN and sending its own SYN to initiate the connection from its side.
  
- **Step 3: ACK (C)**  
  The client sends an **ACK** segment to the server, acknowledging the SYN + ACK and completing the session establishment.


