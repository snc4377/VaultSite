---
title: "Pins Sweep For Host Discovering"
category: ["PREP_CPTS", "Pins Sweep for host discovering"]
---

#### Ping Sweep

`meterpreter > run post/multi/gather/ping_sweep RHOSTS=172.16.5.0/23 [*] Performing ping sweep for IP range 172.16.5.0/23`

We could also perform a ping sweep using a `for loop` directly on a target pivot host that will ping any device in the network range we specify. Here are two helpful ping sweep for loop one-liners we could use for Linux-based and Windows-based pivot hosts.

#### Ping Sweep For Loop on Linux Pivot Hosts
`for i in {1..254} ;do (ping -c 1 172.16.5.$i | grep "bytes from" &) ;done`
#### Ping Sweep For Loop Using CMD
`for /L %i in (1 1 254) do ping 172.16.5.%i -n 1 -w 100 | find "Reply"`
#### Ping Sweep Using PowerShell

`1..254 | % {"172.16.5.$($_): $(Test-Connection -count 1 -comp 172.16.5.$($_) -quiet)"}`

Note: It is possible that a ping sweep may not result in successful replies on the first attempt, especially when communicating across networks. This can be caused by the time it takes for a host to build its arp cache. In these cases, it is good to attempt our ping sweep at least twice to ensure the arp cache gets built.

There could be scenarios when a host's firewall blocks ping (ICMP), and the ping won't get us successful replies. In these cases, we can perform a TCP scan on the 172.16.5.0/23 network with Nmap. Instead of using SSH for port forwarding, we can also use Metasploit's post-exploitation routing module `socks_proxy` to configure a local proxy on our attack host. We will configure the SOCKS proxy for `SOCKS version 4a`. This SOCKS configuration will start a listener on port `9050` and route all the traffic received via our Meterpreter session.
