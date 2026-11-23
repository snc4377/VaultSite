---
title: "Nessus"
category: ["PREP_CPTS", "Pen-testing", "Vuln Assessment", "Tools", "Nessus"]
---

## Nessus: Professional Vulnerability Scanning Guide

https://docs.tenable.com/nessus/10_5/Content/PDF/Nessus_10_5.pdf

**Nessus**, developed by **Tenable Inc.**, is the industry-standard tool for vulnerability assessment. It allows security professionals to identify, evaluate, and manage security risks across networks, operating systems, and applications.

For lab environments and learning, **Nessus Essentials** is free to use for up to **16 IP addresses**, making it perfect for preparing for certifications or testing personal projects.

---

### Installation

Follow these steps to get Nessus running on your Kali machine:

**Step A: Download and Install**

Download the `.deb` package from Tenable and install it using `dpkg`:
![Pasted image 20260428174020](/VaultSite/wiki-images/Pasted%20image%2020260428174020.png)

```
5nch7344@kali$ sudo dpkg -i Nessus-10.8.3-ubuntu1604_amd64.deb
[sudo] password for 5nch7344: 
Selecting previously unselected package nessus.
Unpacking nessus (10.8.3) ...
Setting up nessus (10.8.3) ...
INSTALL PASSED
```

**Start the Service**

You can manage the Nessus scanner using `systemctl`:

```
5nch7344@kali$ sudo systemctl start nessusd.service
```

**Web Access**

1. Navigate to `https://localhost:8834` in your browser.
    
2. **Note:** You will see an SSL certificate warning. This is normal; click "Advanced" and "Accept the Risk and Continue."
    
3. Choose **Nessus Essentials** and follow the activation prompts to download the latest plugins.
    ![Pasted image 20260428174125](/VaultSite/wiki-images/Pasted%20image%2020260428174125.png)
---

###  Scanning Workflow

Once the plugins are initialized, you can start your first scan:
[Types oF Scan Teamplates](https://docs.tenable.com/nessus/Content/ScanAndPolicyTemplates.htm)

|**Phase**|**Action**|
|---|---|
|**Setup**|Select a **Scan Template** (e.g., _Basic Network Scan_).|
|**Targeting**|Define the target IP, range, or hostname.|
|**Discovery**|Choose between a fast "port scan" or a more comprehensive "deep scan."|
|**Credentials**|(Optional) Add SSH/Windows credentials for an **Authenticated Scan**, which provides much deeper visibility into installed software and patches.|
![Pasted image 20260428174204](/VaultSite/wiki-images/Pasted%20image%2020260428174204.png)

![Pasted image 20260428174322](/VaultSite/wiki-images/Pasted%20image%2020260428174322.png)

---

###  Export Reporting (CLI)

For pentesting workflows, you might want to export results via the command line. Using tools like [`nessus-report-downloader`](https://raw.githubusercontent.com/eelsivart/nessus-report-downloader/master/nessus6-report-downloader.rb) allows you to bypass the GUI for exports.


```
5nch7344@kali$ ./nessus_downloader.rb 
Enter the Nessus Server IP: 127.0.0.1
Enter your Nessus Username: admin
...
[+] Exporting scan report, scan id: 1, type: csv
[+] Report ready for download...
[+] Downloading report to: /assessment_data/scans/nessus/internal_network_results.csv
```

---

### Network Impact & Optimization

Vulnerability scanning can be "noisy" and resource-heavy. Monitoring your interface with `vnstat` reveals the significant difference between idle traffic and an active scan:

- **Idle Traffic:** ~300 bit/s
    ![Pasted image 20260428174604](/VaultSite/wiki-images/Pasted%20image%2020260428174604.png)
- **Scanning Traffic:** ~300-500 kbit/s (per host)
    ![Pasted image 20260428174625](/VaultSite/wiki-images/Pasted%20image%2020260428174625.png)

> [!IMPORTANT]
> 
> **Pro-Tip:** If you are scanning a fragile network or a low-bandwidth environment, go to **Settings > Performance** in your scan policy and reduce the "Max simultaneous checks per host" and "Max simultaneous hosts per scan." This will prevent network congestion or crashing sensitive devices.

---

###  Summary of Severity Levels

Nessus categorizes findings into five levels:

- **Critical:** Immediate risk (e.g., Remote Code Execution).
    
- **High:** Serious vulnerabilities (e.g., Missing major security patches).
    
- **Medium:** Significant risks (e.g., Weak encryption).
    
- **Low:** Minor issues (e.g., Information disclosure).
    
- **Info:** Purely informational data about the target.