---
title: "Subdomains BruteForcing"
category: ["PREP_CPTS", "Pen-testing", "information gathering", "Active", "Subdomains BruteForcing"]
---

It is an active and effective subdomain discovery technique that leverages predefined lists of potential subdomain names. This approach systematically tests these names against the target domain to identify valid subdomains. By using carefully crafted wordlists, you can significantly increase the efficiency and effectiveness of your subdomain discovery efforts.

| Tool                                                    | Description                                                                                                                     |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| [bbot](https://github.com/blacklanternsecurity/bbot)    | OpenCode Tool with many options among them active and passive subdomain recon .                                                 |
| [dnsenum](https://github.com/fwaeytens/dnsenum)         | Comprehensive DNS enumeration tool that supports dictionary and brute-force attacks for discovering subdomains.                 |
| [fierce](https://github.com/mschwager/fierce)           | User-friendly tool for recursive subdomain discovery, featuring wildcard detection and an easy-to-use interface.                |
| [dnsrecon](https://github.com/darkoperator/dnsrecon)    | Versatile tool that combines multiple DNS reconnaissance techniques and offers customisable output formats.                     |
| [amass](https://github.com/owasp-amass/amass)           | Actively maintained tool focused on subdomain discovery, known for its integration with other tools and extensive data sources. |
| [assetfinder](https://github.com/tomnomnom/assetfinder) | Simple yet effective tool for finding subdomains using various techniques, ideal for quick and lightweight scans.               |
| [puredns](https://github.com/d3mondev/puredns)          | Powerful and flexible DNS brute-forcing tool, capable of resolving and filtering results effectively.                           |

**1 - BBOT**
Bbot is an open-source tool used for data collection and security testing. Its primary purpose is to facilitate the identification of network infrastructures by enabling the enumeration of subdomains, the collection of services, open ports, and other important details.
In the github Page they say us this tools finds 20-50% more subdomains than other tools. 
[Guide](https://www.blacklanternsecurity.com/bbot/Dev/how_it_works/)
> [!shell] shellsession
> # find subdomains of evilcorp.com
> bbot -t evilcorp.com -p subdomain-enum
> # passive sources only
> bbot -t evilcorp.com -p subdomain-enum -rf passive


**2 - DNSENUM**
A versatile and widely used command-line tool written in Perl. It's a comprehensive toolset for DNS reconnaissance, providing various functionalities for gathering information about the DNS infrastructure of a target domain and its subdomains. The tool offers several key features:

Let's see `dnsenum` in action by demonstrating how to enumerate subdomains for our target, `inlanefreight.com`. In this demonstration, we'll use the `subdomains-top1million-20000.txt` wordlist from [SecLists](https://github.com/danielmiessler/SecLists), which contains the top 20000 most common subdomains.

> [!shell] shellsession
> dnsenum --enum inlanefreight.com -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -r
> dnsenum VERSION:1.2.6 
> ----- inlanefreight.com ----- 
> 
> Host's addresses: 
> __________________ 
> inlanefreight.com.                                                               300                IN             A               134.209.24.248 
> [...] 
> Brute forcing with /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt:
>  _______________________________________________________________________________________
>   www.inlanefreight.com.                                                   300                IN              A               134.209.24.248  
>   support.inlanefreight.com.                                              300                IN              A               134.209.24.248 
>   [...] 
>   
>   done.

