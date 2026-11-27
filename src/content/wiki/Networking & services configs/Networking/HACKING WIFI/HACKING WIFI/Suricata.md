---
title: "Suricata"
category: ["Networking & services configs", "Networking", "HACKING WIFI", "HACKING WIFI", "Suricata"]
---

# Suricata

Suricata on Zorin OS acting as IDS (Intrusion Detection System) and IPS (Intrusion Prevention System)

## IDS
- Monitors network or system activity to detect anomalies. Only alerts, doesn't prevent intrusions.

## IPS
- Monitors the network like IDS but actively blocks suspicious activity when detected and alerts you.

## Install Suricata
- `sudo add-apt-repository ppa:oisf/suricata-stable`
- `sudo apt install suricata`
- `sudo systemctl status suricata`

We need to configure Suricata via the .yaml file since our interface might be eth0 while Suricata comes configured with enp0s:
- `sudo nano /etc/suricata/suricata.yaml`
  - Ctrl+W to search for eth0 and set our interface
  - Go to the homenet section and set our IP ranges and netmasks
  - Ctrl+W search for log/suricata to see where logs are stored
- `sudo suricata-update` (rules are stored in /usr/share/suricata/rules/)

To create custom rules: `sudo nano name.rules`
![Pasted image 20241124222101](/VaultSite/wiki-images/Pasted%20image%2020241124222101.png)
Multiple rules can be loaded simultaneously:
![Pasted image 20241124222122](/VaultSite/wiki-images/Pasted%20image%2020241124222122.png)

- `sudo nano /etc/suricata/suricata.yaml`
  - Ctrl+W search for rule-files and add our .rules filename
  - Change default-rule-path to /usr/share/suricata/rules/ or our rules location
- `sudo systemctl restart suricata`

`tail -f /var/log/suricata/fast.log` (to monitor Suricata logs)

## Test with Apache
- `sudo apt get install apache2`
- `sudo systemctl start apache2`
- Access Apache page in browser

Clear fast.log:
- `sudo su`
- `> /var/log/suricata/fast.log`
- `tail -f /var/log/suricata/fast.log`

Accessing Apache from another machine will trigger alerts in Suricata logs.

## Create Alerts
- `cd /var/www/html`
- `mkdir admin`
- `nano index.html` (add any content)
![Pasted image 20241125003219](/VaultSite/wiki-images/Pasted%20image%2020241125003219.png)
- Create/edit a rule in /usr/share/suricata/rules/ with:
![Pasted image 20241125003417](/VaultSite/wiki-images/Pasted%20image%2020241125003417.png)
![Pasted image 20241125003510](/VaultSite/wiki-images/Pasted%20image%2020241125003510.png)
*Each rule must increment the final sid number*
Modify content to point to our HTML folder
Restart Suricata

Normal Apache traffic shows HTTP alerts:
![Pasted image 20241125003725](/VaultSite/wiki-images/Pasted%20image%2020241125003725.png)
But accessing /admin triggers our custom rule:
![Pasted image 20241125003816](/VaultSite/wiki-images/Pasted%20image%2020241125003816.png)

To detect page visits (only from local machine):
![Pasted image 20241125004131](/VaultSite/wiki-images/Pasted%20image%2020241125004131.png)
Restart Suricata:
![Pasted image 20241125004251](/VaultSite/wiki-images/Pasted%20image%2020241125004251.png)

## Detect Port Scanning
![Pasted image 20241125005152](/VaultSite/wiki-images/Pasted%20image%2020241125005152.png)
This rule detects port scans using SYN packets (TCP connections that don't complete, like nmap -sS):
![Pasted image 20241125005645](/VaultSite/wiki-images/Pasted%20image%2020241125005645.png)
This section controls scan intensity.

Monitor Suricata logs and see how nmap is easily detected:
![Pasted image 20241125005820](/VaultSite/wiki-images/Pasted%20image%2020241125005820.png)
Test with this nmap command:
![Pasted image 20241125010000](/VaultSite/wiki-images/Pasted%20image%2020241125010000.png)
-sS always requires sudo:
![Pasted image 20241125010021](/VaultSite/wiki-images/Pasted%20image%2020241125010021.png)
-Pn to disable ping probes:
![Pasted image 20241125010201](/VaultSite/wiki-images/Pasted%20image%2020241125010201.png)
-T1 for minimal intensity:
![Pasted image 20241125010100](/VaultSite/wiki-images/Pasted%20image%2020241125010100.png)
--scan-delay 500 for delay between scans:
![Pasted image 20241125010211](/VaultSite/wiki-images/Pasted%20image%2020241125010211.png)
--max-retries 1 to minimize traffic:
![Pasted image 20241125010321](/VaultSite/wiki-images/Pasted%20image%2020241125010321.png)
--max-scan-delay to set max milliseconds between packets:
![Pasted image 20241125010403](/VaultSite/wiki-images/Pasted%20image%2020241125010403.png)
-f to fragment packets:
![Pasted image 20241125010437](/VaultSite/wiki-images/Pasted%20image%2020241125010437.png)
-p- to scan all open ports:
![Pasted image 20241125010502](/VaultSite/wiki-images/Pasted%20image%2020241125010502.png)

Nmap runs very slowly but avoids IDS detection:
*20 minutes later*
![Pasted image 20241125010545](/VaultSite/wiki-images/Pasted%20image%2020241125010545.png)
