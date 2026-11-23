
Domain information is a core component of any penetration test, and it is not just about the subdomains but about the entire presence on the Internet. Therefore, we gather information and try to understand the company's functionality and which technologies and structures are necessary for services to be offered successfully and efficiently.
This type of information is gathered passively without direct and active scans. In other words, we remain hidden and navigate as "customers" or "visitors" to avoid direct connections to the company that could expose us. The OSINT relevant sections are only a tiny part of how in-depth OSINT goes and describe only a few of the many ways to obtain information in this way. 


For passively gathering informatioon we have some third-party tools or services to understand the company better . 

**First step**

As first step we need to examine the main website of the company , in search of some technologies for make the   network map and  structure the company services and IoT

For example, many IT companies offer app development, IoT, hosting, data science, and IT security services, depending on their industry. If we encounter a service that we have had little to do with before, it makes sense and is necessary to get to grips with it and find out what activities it consists of and what opportunities are available. Those services also give us a good overview of how the company can be structured.

This part of the OSINT focus in two main concepts , we need to pay attention in **what we see** and **what we do not see** 


**Second Step**

Once we have the first impression and knowledge of the company and what they do we can go to check the presence of it in Internet . For this we hace 2 different main web [crt.sh](https://crt.sh/?utm_source=hackdb.com&utm_medium=referral&utm_campaign=navigation)
or [censys](https://search.censys.io/) 
As example : medium-sized company has hired us to test their entire infrastructure from a black-box perspective. This means we have only received a scope of targets and must obtain all further information ourselves.


The first point of presence on the internet can be the SSL certificate of the main website. This website may have several subdomains associated with the same certificate.
![Pasted image 20260421171057](/VaultSite/wiki-images/Pasted%20image%2020260421171057.png)\

Another way is using some services as crt.sh or censys

This website is for ennumerate subdomains from a principal domain [[Subdomain ennum]]


Another option is to process this request with cURL via the terminal, which will make it more manageable and give it a cleaner look. 

**curl -s https://crt.sh/\?q\=inlanefreight.com\&output\=json | jq . | grep name | cut -d":" -f2 | grep -v "CN=" | cut -d'"' -f2 | awk '{gsub(/\\n/,"\n");}1;' | sort -u** 

account.ttn.inlanefreight.com 
blog.inlanefreight.com 
bots.inlanefreight.com 
console.ttn.inlanefreight.com
ct.inlanefreight.com 
data.ttn.inlanefreight.com 
*.inlanefreight.com 
inlanefreight.com
integrations.ttn.inlanefreight.com 
iot.inlanefreight.com 
mails.inlanefreight.com 
marina.inlanefreight.com
www.inlanefreight.com

**Third step**
[[Shodan]]
After identifying hosts for further investigation, we can modify the cut command to generate a list of IP addresses and analyze them using Shodan. Shodan scans the Internet for devices and systems connected permanently, focusing on open TCP/IP ports. It filters findings based on terms like open HTTP, FTP, SSH, and others, allowing us to locate devices such as surveillance cameras, servers, smart home systems, industrial controllers, and various network components.

`snchh337@htb[/htb]$ for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f1,4;done 
blog.inlanefreight.com 10.129.24.93 
inlanefreight.com 10.129.27.33 
matomo.inlanefreight.com 10.129.127.22
www.inlanefreight.com 10.129.127.33 
s3-website-us-west-2.amazonaws.com 10.129.95.250`

**Fourth Step**

snchh337@htb[/htb]$ **dig any inlanefreight.com**

; <<>> DiG 9.16.1-Ubuntu <<>> any inlanefreight.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52058
;; flags: qr rd ra; QUERY: 1, ANSWER: 17, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;inlanefreight.com.             IN      ANY

;; ANSWER SECTION:
inlanefreight.com.      300     IN      **A**       10.129.27.33
inlanefreight.com.      300     IN      **A**       10.129.95.250
inlanefreight.com.      3600    IN      **MX**      1 aspmx.l.google.com.
inlanefreight.com.      3600    IN      **MX**      10 aspmx2.googlemail.com.
inlanefreight.com.      3600    IN      **MX**      10 aspmx3.googlemail.com.
inlanefreight.com.      3600    IN      **MX**      5 alt1.aspmx.l.google.com.
inlanefreight.com.      3600    IN      **MX**      5 alt2.aspmx.l.google.com.
inlanefreight.com.      21600   IN      **NS**      ns.inwx.net.
inlanefreight.com.      21600   IN      **NS**      ns2.inwx.net.
inlanefreight.com.      21600   IN      **NS**      ns3.inwx.eu.
inlanefreight.com.      3600    IN      **TXT**     "MS=ms92346782372"
inlanefreight.com.      21600   IN      **TXT**     "atlassian-domain-verification=IJdXMt1rKCy68JFszSdCKVpwPN"
inlanefreight.com.      3600    IN      **TXT**     "google-site-verification=O7zV5-xFh_jn7JQ31"
inlanefreight.com.      300     IN      **TXT**     "google-site-verification=bow47-er9LdgoUeah"
inlanefreight.com.      3600    IN      **TXT**     "google-site-verification=gZsCG-BINLopf4hr2"
inlanefreight.com.      3600    IN      **TXT**     "logmein-verification-code=87123gff5a479e-61d4325gddkbvc1-b2bnfghfsed1-3c789427sdjirew63fc"
inlanefreight.com.      300     IN      **TXT**     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.24.8 ip4:10.129.27.2 ip4:10.72.82.106 ~all"
inlanefreight.com.      21600   IN      SOA     ns.inwx.net. hostmaster.inwx.net. 2021072600 10800 3600 604800 3600

;; Query time: 332 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
;; WHEN: Mi Sep 01 18:27:22 CEST 2021
;; MSG SIZE  rcvd: 940

- **A records**: Identifies IP addresses for specific (sub)domains; only one known record observed.  
- **MX records**: Indicates mail server responsible for emails; managed by Google in this case, noted for future reference.  
- **NS records**: Displays name servers for FQDN resolution; typically indicative of hosting provider.  
- **TXT records**: Often contain verification keys and security aspects (SPF, DMARC, DKIM) for email origin verification; valuable information present in the results.