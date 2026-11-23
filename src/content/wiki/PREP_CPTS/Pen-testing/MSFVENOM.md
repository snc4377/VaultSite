---
title: "MSFVENOM"
category: ["PREP_CPTS", "Pen-testing", "MSFVENOM"]
---

# Encoders

---

Over the 15 years of existence of the Metasploit Framework, `Encoders` have assisted with making payloads compatible with different processor architectures while at the same time helping with antivirus evasion. `Encoders` come into play with the role of changing the payload to run on different operating systems and architectures. These architectures include:

|`x64`|`x86`|`sparc`|`ppc`|`mips`|
|---|---|---|---|---|

They are also needed to remove hexadecimal opcodes known as `bad characters` from the payload. Not only that but encoding the payload in different formats could help with the AV detection as mentioned above. However, the use of encoders strictly for AV evasion has diminished over time, as IPS/IDS manufacturers have improved how their protection software deals with signatures in malware and viruses.

Shikata Ga Nai (`SGN`) was one of the most utilized encoding schemes back in the day because it was very hard to detect payloads encoded through its mechanism. However nowadays, modern detection methods have caught up, and these encoded payloads are far from being universally undetectable anymore. The name (`仕方がない`) means `It cannot be helped` or `Nothing can be done about it`, and rightfully so if we were reading this a few years ago. However, there are other methodologies we will explore to evade protection systems. [This article from FireEye](https://www.fireeye.com/blog/threat-research/2019/10/shikata-ga-nai-encoder-still-going-strong.html) details the why and the how of Shikata Ga Nai's previous rule over the other encoders.

---

## Selecting an Encoder

Before 2015, the Metasploit Framework had different submodules that took care of payloads and encoders. They were packed separately from the msfconsole script and were called `msfpayload` and `msfencode`. These two tools are located in `/usr/share/framework2/`.

If we wanted to create our custom payload, we could do so through `msfpayload`, but we would have to encode it according to the target OS architecture using `msfencode` afterward. A pipe would take the output from one command and feed it into the next, which would generate an encoded payload, ready to be sent and run on the target machine.

 ![Pasted image 20260505173103](/VaultSite/wiki-images/Pasted%20image%2020260505173103.png)

After 2015, updates to these scripts have combined them within the `msfvenom` tool, which takes care of payload generation and Encoding. We will be talking about `msfvenom` in detail later on. Below is an example of what payload generation would look like with today's `msfvenom`:

#### Generating Payload - Without Encoding

![Pasted image 20260505173111](/VaultSite/wiki-images/Pasted%20image%2020260505173111.png)
We should now look at the first line of the `$buf` and see how it changes when applying an encoder like `shikata_ga_nai`.

#### Generating Payload - With Encoding

![Pasted image 20260505173120](/VaultSite/wiki-images/Pasted%20image%2020260505173120.png)

#### Shikata Ga Nai Encoding

![GIF showcasing the Shikata Ga Nai encoding with various XOR keys.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/39/shikata_ga_nai.gif)Source: [https://hatching.io/blog/metasploit-payloads2/](https://hatching.io/blog/metasploit-payloads2/)

If we want to look at the functioning of the `shikata_ga_nai` encoder, we can look at an excellent post [here](https://hatching.io/blog/metasploit-payloads2/).

Suppose we want to select an Encoder for an `existing payload`. Then, we can use the `show encoders` command within the `msfconsole` to see which encoders are available for our current `Exploit module + Payload` combination.

![Pasted image 20260505173134](/VaultSite/wiki-images/Pasted%20image%2020260505173134.png)
In the previous example, we only see a few encoders fit for x64 systems. Like the available payloads, these are automatically filtered according to the Exploit module only to display the compatible ones. For example, let us try the `MS09-050 Microsoft SRV2.SYS SMB Negotiate ProcessID Function Table Dereference Exploit`.

![Pasted image 20260505173151](/VaultSite/wiki-images/Pasted%20image%2020260505173151.png)

Take the above example just as that—a hypothetical example. If we were to encode an executable payload only once with SGN, it would most likely be detected by most antiviruses today. Let's delve into that for a moment. Picking up `msfvenom`, the subscript of the Framework that deals with payload generation and Encoding schemes, we have the following input:

![Pasted image 20260505173159](/VaultSite/wiki-images/Pasted%20image%2020260505173159.png)

This will generate a payload with the `exe` format, called TeamViewerInstall.exe, which is meant to work on x86 architecture processors for the Windows platform, with a hidden Meterpreter reverse_tcp shell payload, encoded once with the Shikata Ga Nai scheme. Let us take the result and upload it to VirusTotal.

![VirusTotal report showing 54 out of 69 engines detected TeamViewerInstall.exe as malicious, listing various trojans and suspicious detections by different antivirus engines.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/39/S8_SS01.png)

One better option would be to try running it through multiple iterations of the same Encoding scheme:

![Pasted image 20260505173210](/VaultSite/wiki-images/Pasted%20image%2020260505173210.png)

![VirusTotal report showing 52 out of 65 engines detected TeamViewerInstall.exe as malicious, listing various trojans and suspicious detections by different antivirus engines.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/39/S8_SS02.png)

As we can see, it is still not enough for AV evasion. There is a high number of products that still detect the payload. Alternatively, Metasploit offers a tool called `msf-virustotal` that we can use with an API key to analyze our payloads. However, this requires free registration on VirusTotal.

#### MSF - VirusTotal

![Pasted image 20260505173235](/VaultSite/wiki-images/Pasted%20image%2020260505173235.png)

As expected, most anti-virus products that we will encounter in the wild would still detect this payload so we would have to use other methods for AV evasion that are outside the scope of this module.

