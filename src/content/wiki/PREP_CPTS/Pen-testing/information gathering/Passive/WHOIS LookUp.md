Whois is a network protocol used to look up information about a domain, IP address, or block of IP addresses in a public database. Information obtainable through a Whois query includes the domain owner's name, contact information, registration date, expiration date, and associated domain name servers.

**Why is WhoIs Important** 

WHOIS data serves as a treasure trove of information for penetration testers during the reconnaissance phase of an assessment. It offers valuable insights into the target organisation's digital footprint and potential vulnerabilities:

- `Identifying Key Personnel`: WHOIS records often reveal the names, email addresses, and phone numbers of individuals responsible for managing the domain. This information can be leveraged for social engineering attacks or to identify potential targets for phishing campaigns.
- `Discovering Network Infrastructure`: Technical details like name servers and IP addresses provide clues about the target's network infrastructure. This can help penetration testers identify potential entry points or misconfigurations.
- `Historical Data Analysis`: Accessing historical WHOIS records through services like [WhoisFreaks](https://whoisfreaks.com/) can reveal changes in ownership, contact information, or technical details over time. This can be useful for tracking the evolution of the target's digital presence.

``whois tesla.com
   `Domain Name: TESLA.COM
   `Registry Domain ID: 187902_DOMAIN_COM-VRSN
   `Registrar WHOIS Server: whois.markmonitor.com
   `Registrar URL: http://www.markmonitor.com
   `Updated Date: 2022-10-02T09:36:05Z
   `Creation Date: 1992-11-04T05:00:00Z
   `Registry Expiry Date: 2024-11-03T06:00:00Z
   `Registrar: MarkMonitor Inc.
``   Registrar IANA ID: 292
   `Registrant Name: Domain Administrator
``   Registrant Organization: DNStination Inc.
 ``  Registrant Street: 3450 Sacramento Street, Suite 405
 ``  Registrant City: San Francisco
 ``  Registrant State/Province: CA
 ``  Registrant Postal Code: 94118
   `Registrant Country: US
   `Registrant Phone: +1.4155319335
``   Registrant Phone Ext: 
``   Registrant Fax: +1.4155319336
  `` Registrant Fax Ext: 
  `` Registrant Email: admin@dnstinations.com
  `` Registry Admin ID: 
  `` Admin Name: Domain Administrator
 ``  Admin Organization: DNStination Inc.
 ``  Admin Street: 3450 Sacramento Street, Suite 405
 ``  Admin City: San Francisco
 ``  Admin State/Province: CA
  `` Admin Postal Code: 94118
  `` Admin Country: US
 ``  Admin Phone: +1.4155319335
   `Admin Phone Ext: 
 ``  Admin Fax: +1.4155319336
  `` Admin Fax Ext: 
  `` Admin Email: admin@dnstinations.com``

**Scenarios of usage** 
## Scenario 1: Phishing Investigation

An email security gateway flags a suspicious email sent to multiple employees within a company. The email claims to be from the company's bank and urges recipients to click on a link to update their account information. A security analyst investigates the email and begins by performing a WHOIS lookup on the domain linked in the email.

The WHOIS record reveals the following:

- `Registration Date`: The domain was registered just a few days ago.
- `Registrant`: The registrant's information is hidden behind a privacy service.
- `Name Servers`: The name servers are associated with a known bulletproof hosting provider often used for malicious activities.

This combination of factors raises significant red flags for the analyst. The recent registration date, hidden registrant information, and suspicious hosting strongly suggest a phishing campaign. The analyst promptly alerts the company's IT department to block the domain and warns employees about the scam.

Further investigation into the hosting provider and associated IP addresses may uncover additional phishing domains or infrastructure the threat actor uses.

## Scenario 2: Malware Analysis

A security researcher is analysing a new strain of malware that has infected several systems within a network. The malware communicates with a remote server to receive commands and exfiltrate stolen data. To gain insights into the threat actor's infrastructure, the researcher performs a WHOIS lookup on the domain associated with the command-and-control (C2) server.

The WHOIS record reveals:

- `Registrant`: The domain is registered to an individual using a free email service known for anonymity.
- `Location`: The registrant's address is in a country with a high prevalence of cybercrime.
- `Registrar`: The domain was registered through a registrar with a history of lax abuse policies.

Based on this information, the researcher concludes that the C2 server is likely hosted on a compromised or "bulletproof" server. The researcher then uses the WHOIS data to identify the hosting provider and notify them of the malicious activity.

## Scenario 3: Threat Intelligence Report

A cybersecurity firm tracks the activities of a sophisticated threat actor group known for targeting financial institutions. Analysts gather WHOIS data on multiple domains associated with the group's past campaigns to compile a comprehensive threat intelligence report.

By analysing the WHOIS records, analysts uncover the following patterns:

- `Registration Dates`: The domains were registered in clusters, often shortly before major attacks.
- `Registrants`: The registrants use various aliases and fake identities.
- `Name Servers`: The domains often share the same name servers, suggesting a common infrastructure.
- `Takedown History`: Many domains have been taken down after attacks, indicating previous law enforcement or security interventions.