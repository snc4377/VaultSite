
Note title: Untitled

crt.sh
This website is for enumerating subdomains from a primary domain 
![Pasted image 20260417195234](/VaultSite/wiki-images/Pasted%20image%2020260417195234.png)

Virustotal does the same but with less information 
![Pasted image 20260417195358](/VaultSite/wiki-images/Pasted%20image%2020260417195358.png)

Subdomain identification involves searching for and enumerating subdomains associated with a primary domain.

## Passive Subdomain Enumeration

---

Subdomain enumeration refers to mapping all available subdomains within a domain name. It increases our attack surface and can uncover hidden admin panels or intranet web applications that network administrators hoped to keep hidden through "security by obscurity." At this stage, we'll only perform passive subdomain enumeration using third-party services or publicly available information. However, we'll expand the data we gather in future active subdomain enumeration activities.

---

### VirusTotal

VirusTotal maintains its DNS replication service, which preserves DNS resolutions performed when users visit the URLs they submit. To get information about a domain, enter the domain name in the search bar and click the "Relationships" tab.

---

### Certificates

Another interesting information source we can use to extract subdomains is SSL/TLS certificates. The main reason is Certificate Transparency (CT), a project that requires every SSL/TLS certificate issued by a Certificate Authority (CA) to be published in a publicly accessible log.

We'll learn how to examine CT logs to discover additional domain names and subdomains for a target organization using two main resources:

- [https://censys.io](https://censys.io/)
    
- [https://crt.sh](https://crt.sh/)
    

We can navigate to https://search.censys.io/certificates or https://crt.sh and enter our target organization's domain name to start discovering new subdomains.

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2Facademy.hackthebox.com%2Fstorage%2Fmodules%2F144%2Fcensys_facebook.png&width=768&dpr=3&quality=100&sign=d0854721&sv=2)

censys.io/certificates

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FMZFkqUsY6qb4qLlaRxjv%252Fimage.png%3Falt%3Dmedia%26token%3Dfe149d1c-3a29-4e3b-b804-816f2bac820b&width=768&dpr=3&quality=100&sign=5b0335c4&sv=2)

crt.sh

Although the website is excellent, we'd like to have this information organized and combine it with other sources found during the information gathering process. Let's perform a curl request to the target website asking for JSON output, as it's more manageable to process. We can do this through the following commands:

**Certificate Transparency**



```
afsh4ck$ export TARGET="facebook.com"
afsh4ck$ curl -s "https://crt.sh/?q=${TARGET}&output=json" | jq -r '.[] | "\(.name_value)\n\(.common_name)"' | sort -u > "${TARGET}_crt.sh.txt"
```



```
afsh4ck$ head -n20 facebook.com_crt.sh.txt

*.adtools.facebook.com
*.ak.facebook.com
*.ak.fbcdn.net
*.alpha.facebook.com
*.assistant.facebook.com
*.beta.facebook.com
*.channel.facebook.com
*.cinyour.facebook.com
*.cinyourrc.facebook.com
*.connect.facebook.com
*.cstools.facebook.com
*.ctscan.facebook.com
*.dev.facebook.com
*.dns.facebook.com
*.extern.facebook.com
*.extools.facebook.com
*.f--facebook.com
*.facebook.com
*.facebookcorewwwi.onion
*.facebookmail.com
```

`curl -s`

Make the request with minimal output.

`https://crt.sh/?q=<DOMAIN>&output=json`

Request the JSON output.

`jq -r '.[]' "\(.name_value)\n\(.common_name)"'`

Process the JSON output and print the certificate name value and common name, one per line.

`sort -u`

Sort the provided result alphabetically and remove duplicates.

We can also perform this operation manually against a target using OpenSSL:


```
export TARGET="facebook.com"
export PORT="443"
openssl s_client -ign_eof 2>/dev/null <<<$'HEAD / HTTP/1.0\r\n\r' -connect "${TARGET}:${PORT}" | openssl x509 -noout -text -in - | grep 'DNS' | sed -e 's|DNS:|\n|g' -e 's|^\*.*||g' | tr -d ',' | sort -u

*.facebook.com
*.facebook.net
*.fbcdn.net
*.fbsbx.com
*.m.facebook.com
*.messenger.com
*.xx.fbcdn.net
*.xy.fbcdn.net
*.xz.fbcdn.net
facebook.com
messenger.com
```

## Passive Subdomain Enumeration Automation

We've learned how to gather useful information about our target organization, such as subdomains, naming patterns, alternative TLDs, IP ranges, etc., using third-party services without directly interacting with their infrastructure or relying on automated tools. Now we'll learn how to enumerate subdomains using tools and previously obtained information.

### The Harvester

[![Logo](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2Fgithub.com%2Ffluidicon.png&width=20&dpr=3&quality=100&sign=6967507a&sv=2)GitHub - laramies/theHarvester: E-mails, subdomains and names Harvester - OSINTGitHub](https://github.com/laramies/theHarvester)

The Harvester is an easy-to-use yet powerful and effective tool for early-stage penetration testing and Red Team exercises. We can use it to collect information that helps identify a company's attack surface. The tool gathers `emails`, `names`, `subdomains`, `IP addresses` and `URLs` from various public data sources for passive information gathering. For now, we'll use the following modules:

[Baidu](http://www.baidu.com/)

Baidu search engine

`Bufferoverun`

Uses data from Rapid7's Project Sonar: [www.rapid7.com/research/project-sonar/](http://www.rapid7.com/research/project-sonar/)

[Crtsh](https://crt.sh/)

Comodo certificate search.

[Hackertarget](https://hackertarget.com/)

Online vulnerability scanners and network intelligence

`Otx`

AlienVault's Open Threat Exchange: [https://otx.alienvault.com](https://otx.alienvault.com/)

[Rapiddns](https://rapiddns.io/)

DNS query tool that simplifies subdomain or same-IP site queries

[Sublist3r](https://github.com/aboul3la/Sublist3r)

Fast subdomain enumeration tool for penetration testers

[Threatcrowd](http://www.threatcrowd.org/)

Open-source threat intelligence

[Threatminer](https://www.threatminer.org/)

Data mining for threat intelligence

`Trello`

Search Trello boards (uses Google search)

[Urlscan](https://urlscan.io/)

A web sandbox for scanning websites and URLs

`Vhost`

Bing virtual host search

[Virustotal](https://www.virustotal.com/gui/home/search)

Domain search

[Zoomeye](https://www.zoomeye.org/)

Chinese version of Shodan

To automate this, we'll create a file called `sources.txt` with the following content.


```
cat sources.txt

baidu
bufferoverun
crtsh
hackertarget
otx
projectdiscovery
rapiddns
sublist3r
threatcrowd
trello
urlscan
vhost
virustotal
zoomeye
```

Once the file is created, we will execute the following commands to gather information from these sources.

```
export TARGET="facebook.com"
cat sources.txt | while read source; do theHarvester -d "${TARGET}" -b $source -f "${source}_${TARGET}";done

<SNIP>
*******************************************************************
*  _   _                                            _             *
* | |_| |__   ___    /\  /\__ _ _ ____   _____  ___| |_ ___ _ __  *
* | __|  _ \ / _ \  / /_/ / _` | '__\ \ / / _ \/ __| __/ _ \ '__| *
* | |_| | | |  __/ / __  / (_| | |   \ V /  __/\__ \ ||  __/ |    *
*  \__|_| |_|\___| \/ /_/ \__,_|_|    \_/ \___||___/\__\___|_|    *
*                                                                 *
* theHarvester 4.0.0                                              *
* Coded by Christian Martorella                                   *
* Edge-Security Research                                          *
* cmartorella@edge-security.com                                   *
*                                                                 *
*******************************************************************


[*] Target: facebook.com

[*] Searching Urlscan.

[*] ASNS found: 29
--------------------
AS12578
AS13335
AS13535
AS136023
AS14061
AS14618
AS15169
AS15817

<SNIP>
```

When the process completes, we can extract all found subdomains and sort them using the following command:


```
cat *.json | jq -r '.hosts[]' 2>/dev/null | cut -d':' -f 1 | sort -u > "${TARGET}_theHarvester.txt"
```

Now we can merge all passive reconnaissance files using:


```
cat facebook.com_*.txt | sort -u > facebook.com_subdomains_passive.txt
cat facebook.com_subdomains_passive.txt | wc -l

11947
```

We can also run theHarvester in a simple way with the following command:



```
theHarvester -d facebook.com -l 400 -b all
```

### Sublist3r

Sublist3r is a command-line tool that uses multiple public data sources to search for subdomains associated with a main domain. This tool is easy to use and provides accurate results quickly. Sublist3r also supports integration with other security tools, such as Nmap and Maltego.



```
sudo apt install sublist3r

# el parámetro -b es para hacer fuerza bruta
sublist3r -d hackthissite.org -v -b -o output.txt

# Encuentra puertos abiertos en subdominios. (Recon. Activo)
sublist3r -d hackthissite.org -v -p 80,443 
```

Note title: Untitled

![](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet/~gitbook/image?url=https%3A%2F%2F2648005400-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FRolFIJKRJaxKzAUqQKJb%252Fuploads%252FPTF6wF9sIDWjSUkXKUBK%252Fimage.png%3Falt%3Dmedia%26token%3D31a4516d-56a3-4869-9a93-68f9c9d804b2&width=768&dpr=3&quality=100&sign=96e17655&sv=2)