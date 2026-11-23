---
title: "Cloud Resources"
category: ["PREP_CPTS", "Pen-testing", "Footprinting", "Cloud Resources"]
---

# Cloud Security & Reconnaissance

**Tags:** #cloud-security #recon #OSINT #pentesting #misconfiguration

**Related:** [[AWS]], [[Azure]], [[GCP]]

## ☁️ The Cloud Security Gap

While providers (**AWS, GCP, Azure**) secure the underlying infrastructure, the **customer** is responsible for secure configuration. Misconfigurations by administrators are the primary cause of data breaches in the cloud.

### Common Exposed Services

- **AWS:** S3 Buckets
    
- **Azure:** Blobs / Container Storage
    
- **GCP:** Cloud Storage
    

> [!CAUTION]
> 
> Infrastructure security $\neq$ Data security. Publicly accessible storage without authentication is the most common entry point for attackers.

---

## 🔍 Discovery Techniques (Recon)

### 1. DNS & IP Analysis

Companies often map cloud storage to their subdomains for easier management.

- **Method:** Run a `host` command or use tools like `subfinder` to identify IPs belonging to cloud provider ranges.
    
- **Example:** Seeing `s3-website-us-west-2.amazonaws.com` in a DNS lookup confirms the use of AWS S3.
    
![Pasted image 20260421184616](/VaultSite/wiki-images/Pasted%20image%2020260421184616.png)
### 2. Google Dorking

Using advanced operators to find indexed files in cloud buckets.

- `inurl:s3.amazonaws.com "company_name"`
    
- `intext:"index of" "company_name" storage`
    
- `filetype:pdf` or `filetype:xlsx` associated with cloud URLs.
    ![Pasted image 20260421184633](/VaultSite/wiki-images/Pasted%20image%2020260421184633.png)
![Pasted image 20260421184649](/VaultSite/wiki-images/Pasted%20image%2020260421184649.png)
### 3. Source Code Analysis

Reviewing the HTML/JS of a target website often reveals:

- Direct links to buckets where images, scripts, or CSS are hosted.
    
- Leaked API keys or hardcoded cloud credentials.
    
![Pasted image 20260421184704](/VaultSite/wiki-images/Pasted%20image%2020260421184704.png)
### 4. Third-Party Intelligence Tools

| **Tool**           | **Purpose**                                                                          |
| ------------------ | ------------------------------------------------------------------------------------ |
| **Domain.glass**   | Identify infrastructure, DNS providers, and security layers (e.g., Cloudflare).      |
| **GrayHatWarfare** | A dedicated search engine to discover and filter public AWS, Azure, and GCP storage. |

Domain.Glass
![Pasted image 20260421184735](/VaultSite/wiki-images/Pasted%20image%2020260421184735.png)

GrayHatWarfare
![Pasted image 20260421184754](/VaultSite/wiki-images/Pasted%20image%2020260421184754.png)


---

## 🚩 Critical Impact: Sensitive Data Leaks

Human error and high-pressure environments often lead to the exposure of:

- **Identity & Access:** Private **SSH Keys** (`id_rsa`) allowing passwordless server access.
    
- **Source Code:** Hardcoded credentials or proprietary logic.
    
- **Personal Data:** PDFs, spreadsheets, and internal documents containing PII or company secrets.
![Pasted image 20260421184813](/VaultSite/wiki-images/Pasted%20image%2020260421184813.png)
