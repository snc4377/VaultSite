---
title: "Ataques De Transferencia De Zona (AXFR Full Zone Transfer)"
category: ["S4VITAR", "fases", "6-OWASP 10", "Ataques de transferencia de zona (AXFR  Full Zone Transfer)"]
---



Zone transfer attacks, also known as **AXFR** attacks, are a type of attack targeting **DNS** servers (**Domain Name System**) that allows attackers to obtain sensitive information about an organization's domains.

In simple terms, DNS servers are responsible for translating human-readable domain names into machine-usable IP addresses. AXFR attacks enable attackers to obtain information about the DNS records stored on a DNS server.

The AXFR attack is carried out by sending a zone transfer request from a fake DNS server to a legitimate DNS server. This request uses the DNS zone transfer protocol (AXFR), which is employed by DNS servers to transfer DNS records from one server to another.

If the legitimate DNS server is not properly configured, it may respond to the zone transfer request and provide the attacker with detailed information about the DNS records stored on the server. This includes information such as domain names, IP addresses, email servers, and other sensitive data that can be used in future attacks.

One of the tools for exploiting AXFR is **dig**. The dig command is a command-line tool used to perform DNS queries and obtain information about the DNS records of a specific domain.

The syntax to perform an AXFR attack on a DNS server is as follows:

➜ `dig @<DNS-server> <domain-name> AXFR`

Where:
 --DNS-server-- is the IP address of the DNS server to query.
--domain-name-- is the domain name for which the zone transfer is requested.
AXFR is the query type, indicating to the DNS server that a full zone transfer is desired.

To prevent AXFR attacks, it is crucial for network administrators to properly configure DNS servers and restrict zone transfers only to authorized servers. It is also important to keep DNS server software updated and use strong encryption and authentication techniques to protect data transmitted over the network. Administrators can also use DNS monitoring tools to detect and prevent potential zone transfer attacks.
![Pasted image 20260201203509](/VaultSite/wiki-images/Pasted%20image%2020260201203509.png)





