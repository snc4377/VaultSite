The reality is that many organizations do not know everything on their network, and some organizations have very little visibility, and we can help them with this. The enumeration that we perform can be highly beneficial to our clients to help them enhance or start building an asset inventory. We may very likely identify applications that have been forgotten, demo versions of software that perhaps have had their trial license expired and converted to a version that does not require authentication (in the case of Splunk), applications with default/weak credentials, unauthorized/misconfigured applications, and applications that suffer from public vulnerabilities. We can provide this data to our clients as a combination of the findings in our reports (i.e., an application with default credentials `admin:admin`, as appendices such as a list of identified services mapped to hosts, or supplemental scan data). We can even take it a step further and educate our clients on some of the tools that we use daily so they can begin to perform periodic and proactive recon of their networks and find gaps before penetration testers, or worse, attackers, find them first.

As penetration testers, we need to have strong enumeration skills and be able to get the "lay of the land" on any network starting with very little to no information (black box discovery or just a set of CIDR ranges). Typically, when we connect to a network, we'll start with a ping sweep to identify "live hosts." From there, we will usually begin targeted port scanning and, eventually, deeper port scanning to identify running services. In a network with hundreds or thousands of hosts, this enumeration data can become unwieldy. Let's say we perform an Nmap port scan to identify common web services such as:

#### Nmap - Web Discovery

```
nmap -p 80,443,8000,8080,8180,8888,10000 --open -oA web_discovery -iL scope_list

```

We may find an enormous amount of hosts with services running on ports 80 and 443 alone. What do we do with this data? Sifting through the enumeration data by hand in a large environment would be far too time-consuming, especially since most assessments are under strict time constraints. Browsing to each IP/hostname + port would also be highly inefficient.

Lucky for us, several great tools exist that can greatly assist in this process. Two phenomenal tools that every tester should have in their arsenal are [EyeWitness](https://github.com/FortyNorthSecurity/EyeWitness) and [Aquatone](https://github.com/michenriksen/aquatone). Both of these tools can be fed raw Nmap XML scan output (Aquatone can also take Masscan XML; EyeWitness can take Nessus XML output) and be used to quickly inspect all hosts running web applications and take screenshots of each.

These screenshots can help us narrow down potentially 100s of hosts and build a more targeted list of applications that we should spend more time enumerating and attacking. These tools are available for both Windows and Linux, so we can utilize them on whatever we choose for our attack box in a given environment. Let's walk through some examples of each to create an inventory of applications present in the target `INLANEFREIGHT.LOCAL` domain.

---

## Getting Organized

For this section, I would break down the `Enumeration & Discovery` section of my notebook into a separate `Application Discovery` section. Here I would create subsections for the scope, scans (Nmap, Nessus, Masscan, etc.), application screenshotting, and interesting/notable hosts to dig more into later. It is important to time and date stamp every scan that we perform and save all output and the exact scan syntax that was performed and the targeted hosts. This can be useful later on if the client has any questions about the activity they saw during the assessment. Being organized from the start and keeping detailed logs and notes will help us greatly with the final report. I typically set up the skeleton of the report at the beginning of the assessment along with my notebook so I can begin filling in certain sections of the report while waiting for a scan to finish. All of this will save time at the end of the engagement, leave us more time for the fun stuff (testing misconfigurations and exploits!), and ensure that we are as thorough as possible.

An example OneNote (also applicable to other tools) structure may look like the following for the discovery phase:

`External Penetration Test - <Client Name>`

- `Scope` (including in-scope IP addresses/ranges, URLs, any fragile hosts, testing timeframes, and any limitations or other relative information we need handy)
- `Client Points of Contact`
- `Credentials`
- `Discovery/Enumeration`
    - `Scans`
    - `Live hosts`
- `Application Discovery`
    - `Scans`
    - `Interesting/Notable Hosts`
- `Exploitation`
    - `<Hostname or IP>`
    - `<Hostname or IP>`
- `Post-Exploitation`
    - `<Hostname or IP>`
    - `<Hostname or IP>`



---

## Initial Enumeration

Let's assume our client provided us with the following scope: 

```
cat scope_list 

app.inlanefreight.local
dev.inlanefreight.local
drupal-dev.inlanefreight.local
drupal-qa.inlanefreight.local
drupal-acc.inlanefreight.local
drupal.inlanefreight.local
blog-dev.inlanefreight.local
blog.inlanefreight.local
app-dev.inlanefreight.local
jenkins-dev.inlanefreight.local
jenkins.inlanefreight.local
web01.inlanefreight.local
gitlab-dev.inlanefreight.local
gitlab.inlanefreight.local
support-dev.inlanefreight.local
support.inlanefreight.local
inlanefreight.local
10.129.201.50
```
  
**If we don’t have this list from the client, we can obtain the information using tools explained here—such as crt.sh for manual retrieval, or theHarvester for automation.-- [[Subdomain ennum]] --

The security assessment process begins with an Nmap scan of common web ports (80, 443, 8000, 8080, 8180, 8888, and 10000), followed by the use of tools such as EyeWitness or Aquatone to capture screenshots. A more comprehensive scan—covering 10,000 ports or all TCP ports—may be performed, depending on the available resources. For non-evasive penetration tests, the use of tools like Nessus is recommended to maximize value for the client, though the methodology should remain flexible and adaptable. It is essential not to rely solely on automated scanning tools; these should be complemented by manual testing to identify vulnerabilities and misconfigurations. This methodology aims to establish a repeatable and thorough enumeration process, providing a solid foundation for further exploration.
 

Note: Not all hosts in the scope list above will be accessible when spawning the target below. There will be separate, similar, exercises at the end of this section in order to reproduce much of what is shown here.

```
sudo  nmap -p 80,443,8000,8080,8180,8888,10000 --open -oA web_discovery -iL scope_list 

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-07 21:49 EDT
Stats: 0:00:07 elapsed; 1 hosts completed (4 up), 4 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 81.24% done; ETC: 21:49 (0:00:01 remaining)

Nmap scan report for app.inlanefreight.local (10.129.42.195)
Host is up (0.12s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap scan report for app-dev.inlanefreight.local (10.129.201.58)
Host is up (0.12s latency).
Not shown: 993 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
8000/tcp open  http-alt
8009/tcp open  ajp13
8080/tcp open  http-proxy
8180/tcp open  unknown
8888/tcp open  sun-answerbook

Nmap scan report for gitlab-dev.inlanefreight.local (10.129.201.88)
Host is up (0.12s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
8081/tcp open  blackice-icecap

Nmap scan report for 10.129.201.50
Host is up (0.13s latency).
Not shown: 991 closed ports
PORT     STATE SERVICE
80/tcp   open  http
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
5357/tcp open  wsdapi
8000/tcp open  http-alt
8080/tcp open  http-proxy
8089/tcp open  unknown

<SNIP>
```

Several hosts have been identified running web servers on various ports; it is suspected that one is running Windows and the others Linux, though this is not certain. Attention is drawn to the hostnames and the role of virtual hosts (Vhosts) in simulating a company's subdomains. Hosts with "dev" in their FQDN may feature untested functionality or have debug mode enabled. 

It is recommended to investigate `gitlab-dev.inlanefreight.local` for any public Git repositories that might contain sensitive information. Some GitLab instances may allow registration without administrator approval, potentially granting access to additional repositories.

To gather more information about a specific host, it is suggested to perform a service scan using Nmap (`-sV`) across the top 1,000 ports.

```
sudo nmap --open -sV 10.129.201.50

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-07 21:58 EDT
Nmap scan report for 10.129.201.50
Host is up (0.13s latency).
Not shown: 991 closed ports
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
5357/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
8000/tcp open  http          Splunkd httpd
8080/tcp open  http          Indy httpd 17.3.33.2830 (Paessler PRTG bandwidth monitor)
8089/tcp open  ssl/http      Splunkd httpd (free license; remote login disabled)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 38.63 seconds
```

We can see that an IIS web server is running on the default port 80, and it appears that `Splunk` is running on port 8000/8089, while `PRTG Network Monitor` is present on port 8080. 

---

## Using EyeWitness

First up is EyeWitness. As mentioned before, EyeWitness can take the XML output from both Nmap and Nessus and create a report with screenshots of each web application present on the various ports using Selenium. It will also take things a step further and categorize the applications where possible, fingerprint them, and suggest default credentials based on the application. It can also be given a list of IP addresses and URLs and be told to pre-pend `http://` and `https://` to the front of each. It will perform DNS resolution for IPs and can be given a specific set of ports to attempt to connect to and screenshot.

Running `eyewitness -h` will show us the options available to us:

Let's run the default `--web` option to take screenshots using the Nmap XML output from the discovery scan as input.

```
eyewitness --web -x web_discovery.xml -d inlanefreight_eyewitness

################################################################################
#                                  EyeWitness                                  #
################################################################################
#           FortyNorth Security - https://www.fortynorthsecurity.com           #
################################################################################

Starting Web Requests (26 Hosts)
Attempting to screenshot http://app.inlanefreight.local
Attempting to screenshot http://app-dev.inlanefreight.local
Attempting to screenshot http://app-dev.inlanefreight.local:8000
Attempting to screenshot http://app-dev.inlanefreight.local:8080
Attempting to screenshot http://gitlab-dev.inlanefreight.local
Attempting to screenshot http://10.129.201.50
Attempting to screenshot http://10.129.201.50:8000
Attempting to screenshot http://10.129.201.50:8080
Attempting to screenshot http://dev.inlanefreight.local
Attempting to screenshot http://jenkins-dev.inlanefreight.local
Attempting to screenshot http://jenkins-dev.inlanefreight.local:8000
Attempting to screenshot http://jenkins-dev.inlanefreight.local:8080
Attempting to screenshot http://support-dev.inlanefreight.local
Attempting to screenshot http://drupal-dev.inlanefreight.local
[*] Hit timeout limit when connecting to http://10.129.201.50:8000, retrying
Attempting to screenshot http://jenkins.inlanefreight.local
Attempting to screenshot http://jenkins.inlanefreight.local:8000
Attempting to screenshot http://jenkins.inlanefreight.local:8080
Attempting to screenshot http://support.inlanefreight.local
[*] Completed 15 out of 26 services
Attempting to screenshot http://drupal-qa.inlanefreight.local
Attempting to screenshot http://web01.inlanefreight.local
Attempting to screenshot http://web01.inlanefreight.local:8000
Attempting to screenshot http://web01.inlanefreight.local:8080
Attempting to screenshot http://inlanefreight.local
Attempting to screenshot http://drupal-acc.inlanefreight.local
Attempting to screenshot http://drupal.inlanefreight.local
Attempting to screenshot http://blog-dev.inlanefreight.local
Finished in 57.859838008880615 seconds

[*] Done! Report written in the /home/mrb3n/Projects/inlanfreight/inlanefreight_eyewitness folder!
Would you like to open the report now? [Y/n]
```

---

## Using Aquatone

[Aquatone](https://github.com/michenriksen/aquatone), as mentioned before, is similar to EyeWitness and can take screenshots when provided a `.txt` file of hosts or an Nmap `.xml` file with the `-nmap` flag. `

In this example, we provide the tool the same `web_discovery.xml` Nmap output specifying the `-nmap` flag, and we're off to the races.

```
cat web_discovery.xml | ./aquatone -nmap

aquatone v1.7.0 started at 2021-09-07T22:31:03-04:00

Targets    : 65
Threads    : 6
Ports      : 80, 443, 8000, 8080, 8443
Output dir : .

http://web01.inlanefreight.local:8000/: 403 Forbidden
http://app.inlanefreight.local/: 200 OK
http://jenkins.inlanefreight.local/: 403 Forbidden
http://app-dev.inlanefreight.local/: 200 
http://app-dev.inlanefreight.local/: 200 
http://app-dev.inlanefreight.local:8000/: 403 Forbidden
http://jenkins.inlanefreight.local:8000/: 403 Forbidden
http://web01.inlanefreight.local:8080/: 200 
http://app-dev.inlanefreight.local:8000/: 403 Forbidden
http://10.129.201.50:8000/: 200 OK

<SNIP>

http://web01.inlanefreight.local:8000/: screenshot successful
http://app.inlanefreight.local/: screenshot successful
http://app-dev.inlanefreight.local/: screenshot successful
http://jenkins.inlanefreight.local/: screenshot successful
http://app-dev.inlanefreight.local/: screenshot successful
http://app-dev.inlanefreight.local:8000/: screenshot successful
http://jenkins.inlanefreight.local:8000/: screenshot successful
http://app-dev.inlanefreight.local:8000/: screenshot successful
http://app-dev.inlanefreight.local:8080/: screenshot successful
http://app.inlanefreight.local/: screenshot successful

<SNIP>

Calculating page structures... done
Clustering similar pages... done
Generating HTML report... done

Writing session file...Time:
 - Started at  : 2021-09-07T22:31:03-04:00
 - Finished at : 2021-09-07T22:31:36-04:00
 - Duration    : 33s

Requests:
 - Successful : 65
 - Failed     : 0

 - 2xx : 47
 - 3xx : 0
 - 4xx : 18
 - 5xx : 0

Screenshots:
 - Successful : 65
 - Failed     : 0

Wrote HTML report to: aquatone_report.html

```

---

## Interpreting the Results

The report presented organizes information about hosts into categories, starting with high-value targets. In large environments—for instance, those with 500 or 5,000 hosts—using tools like EyeWitness can be essential, as they generate comprehensive reports that highlight significant hosts. For example, an instance of ManageEngine OpManager was discovered with default credentials, which allowed for remote code execution and compromised the network. 

It is recommended to examine Tomcat during penetration tests by testing for default credentials on specific endpoints like  `/manager` and `/host-manager` endpoints. If we can access either, we can upload a malicious WAR file and achieve remote code execution on the underlying host using [JSP code](https://en.wikipedia.org/wiki/Jakarta_Server_Pages). More on this later in the module.

![The image shows a report with a table of contents listing categories like High Value Targets, Uncategorized, Content Management System (CMS), 401/403 Unauthorized, and Splash Pages. It includes a section titled "High Value Targets" with web request info and a screenshot of an Apache Tomcat page. The report was generated on 09/07/2021.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/113/eyewitness4.png)

Continuing through the report, it looks like the main `http://inlanefreight.local` website is next. Custom web applications are always worth testing as they may contain a wide variety of vulnerabilities. Here I would also be interested to see if the website was running a popular CMS such as WordPress, Joomla, or Drupal. 

The next application, `http://support-dev.inlanefreight.local`, is interesting because it appears to be running [osTicket](https://osticket.com/), which has suffered from various severe vulnerabilities over the years. Support ticketing systems are of particular interest because we may be able to log in and gain access to sensitive information. 



![Web report showing Inlanefreight homepage and helpdesk info, including server details and response codes.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/113/eyewitness3.png)

During the evaluation phase of a penetration test, it is crucial to continue analyzing the findings, documenting relevant hosts along with their associated URLs and application versions. This process focuses on information gathering, where every detail can be vital. Launching attacks prematurely could result in the loss of important information. In external penetration tests, one may encounter custom applications, content management systems (CMS), and platforms such as Tomcat, Jenkins, and Splunk, as well as remote access points, SSL VPN endpoints, and Outlook Web Access (OWA).

Your mileage may vary, and sometimes we will come across applications that absolutely should not be exposed, such as a single page with a file upload button I encountered once with a message that stated, "Please only upload .zip and .tar.gz files". I, of course, did not heed this warning (as this was in-scope during a client-sanctioned penetration test) and proceeded to upload a test `.aspx` file. To my surprise, there was no sort of client-side or back-end validation, and the file appeared to upload. Doing some quick directory brute-forcing, I was able to locate a `/files` directory that had directory listing enabled, and my `test.aspx` file was there. From here, I proceeded to upload a `.aspx` web shell and gained a foothold into the internal environment. This example shows that we should leave no stone unturned and that there can be an absolute treasure trove of data for us in our application discovery data.

In internal testing, a similar pattern is observed, including login pages for printers—which can be used to obtain LDAP credentials in clear text—as well as login portals for ESXi and vCenter, network devices, IoT, and internal repositories.

