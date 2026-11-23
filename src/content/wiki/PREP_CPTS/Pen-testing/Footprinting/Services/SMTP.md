---
title: "SMTP"
category: ["PREP_CPTS", "Pen-testing", "Footprinting", "Services", "SMTP"]
---

Each SMTP server can be configured in many ways, as can all other services. However, there are differences because the SMTP server is only responsible for sending and forwarding emails.
Port 25 or 445 for encrypted smtp with ssl
#### Default Configuration

        shellsession
`snchh337@htb[/htb]$ cat /etc/postfix/main.cf | grep -v "#" | sed -r "/^\s*$/d" smtpd_banner = ESMTP Server  biff = no append_dot_mydomain = no readme_directory = no compatibility_level = 2 smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache myhostname = mail1.inlanefreight.htb alias_maps = hash:/etc/aliases alias_database = hash:/etc/aliases smtp_generic_maps = hash:/etc/postfix/generic mydestination = $myhostname, localhost  masquerade_domains = $myhostname mynetworks = 127.0.0.0/8 10.129.0.0/16 mailbox_size_limit = 0 recipient_delimiter = + smtp_bind_address = 0.0.0.0 inet_protocols = ipv4 smtpd_helo_restrictions = reject_invalid_hostname home_mailbox = /home/postfix`

The sending and communication are also done by special commands that cause the SMTP server to do what the user requires.

|**Command**|**Description**|
|---|---|
|`AUTH PLAIN`|AUTH is a service extension used to authenticate the client.|
|`HELO`|The client logs in with its computer name and thus starts the session.|
|`MAIL FROM`|The client names the email sender.|
|`RCPT TO`|The client names the email recipient.|
|`DATA`|The client initiates the transmission of the email.|
|`RSET`|The client aborts the initiated transmission but keeps the connection between client and server.|
|`VRFY`|The client checks if a mailbox is available for message transfer.|
|`EXPN`|The client also checks if a mailbox is available for messaging with this command.|
|`NOOP`|The client requests a response from the server to prevent disconnection due to time-out.|
|`QUIT`|The client terminates the session.|

To interact with the SMTP server, we can use the `telnet` tool to initialize a TCP connection with the SMTP server. The actual initialization of the session is done with the command mentioned above, `HELO` or `EHLO`.

#### Telnet - HELO/EHLO

        shellsession
`snchh337@htb[/htb]$ telnet 10.129.14.128 25 Trying 10.129.14.128... Connected to 10.129.14.128. Escape character is '^]'. 220 ESMTP Server  HELO mail1.inlanefreight.htb 250 mail1.inlanefreight.htb EHLO mail1 250-mail1.inlanefreight.htb 250-PIPELINING 250-SIZE 10240000 250-ETRN 250-ENHANCEDSTATUSCODES 250-8BITMIME 250-DSN 250-SMTPUTF8 250 CHUNKING`

The command `VRFY` can be used to enumerate existing users on the system. However, this does not always work. Depending on how the SMTP server is configured, the SMTP server may issue `code 252` and confirm the existence of a user that does not exist on the system. A list of all SMTP response codes can be found [here](https://serversmtp.com/smtp-error/).

#### Telnet - VRFY

        shellsession
`snchh337@htb[/htb]$ telnet 10.129.14.128 25 Trying 10.129.14.128... Connected to 10.129.14.128. Escape character is '^]'. 220 ESMTP Server  VRFY root 252 2.0.0 root VRFY cry0l1t3 252 2.0.0 cry0l1t3 VRFY testuser 252 2.0.0 testuser VRFY aaaaaaaaaaaaaaaaaaaaaaaaaaaa 252 2.0.0 aaaaaaaaaaaaaaaaaaaaaaaaaaaa`

Therefore, one should never entirely rely on the results of automatic tools. After all, they execute pre-configured commands, but none of the functions explicitly state how the administrator configures the tested server.

Sometimes we may have to work through a web proxy. We can also make this web proxy connect to the SMTP server. The command that we would send would then look something like this: `CONNECT 10.129.14.128:25 HTTP/1.0`

All the commands we enter in the command line to send an email we know from every email client program like Thunderbird, Gmail, Outlook, and many others. We specify the `subject`, to whom the email should go, CC, BCC, and the information we want to share with others. Of course, the same works from the command line.

#### Send an Email

        shellsession
`snchh337@htb[/htb]$ telnet 10.129.14.128 25 Trying 10.129.14.128... Connected to 10.129.14.128. Escape character is '^]'. 220 ESMTP Server EHLO inlanefreight.htb 250-mail1.inlanefreight.htb 250-PIPELINING 250-SIZE 10240000 250-ETRN 250-ENHANCEDSTATUSCODES 250-8BITMIME 250-DSN 250-SMTPUTF8 250 CHUNKING MAIL FROM: <cry0l1t3@inlanefreight.htb> 250 2.1.0 Ok RCPT TO: <mrb3n@inlanefreight.htb> NOTIFY=success,failure 250 2.1.5 Ok DATA 354 End data with <CR><LF>.<CR><LF> From: <cry0l1t3@inlanefreight.htb> To: <mrb3n@inlanefreight.htb> Subject: DB Date: Tue, 28 Sept 2021 16:32:51 +0200 Hey man, I am trying to access our XY-DB but the creds don't work.  Did you make any changes there? . 250 2.0.0 Ok: queued as 6E1CF1681AB QUIT 221 2.0.0 Bye Connection closed by foreign host.`

The mail header is the carrier of a large amount of interesting information in an email. Among other things, it provides information about the sender and recipient, the time of sending and arrival, the stations the email passed on its way, the content and format of the message, and the sender and recipient.

Some of this information is mandatory, such as sender information and when the email was created. Other information is optional. However, the email header does not contain any information necessary for technical delivery. It is transmitted as part of the transmission protocol. Both sender and recipient can access the header of an email, although it is not visible at first glance. The structure of an email header is defined by [RFC 5322](https://datatracker.ietf.org/doc/html/rfc5322).

---

## Dangerous Settings

To prevent the sent emails from being filtered by spam filters and not reaching the recipient, the sender can use a relay server that the recipient trusts. It is an SMTP server that is known and verified by all others. As a rule, the sender must authenticate himself to the relay server before using it.

Often, administrators have no overview of which IP ranges they have to allow. This results in a misconfiguration of the SMTP server that we will still often find in external and internal penetration tests. Therefore, they allow all IP addresses not to cause errors in the email traffic and thus not to disturb or unintentionally interrupt the communication with potential and current customers.

#### Open Relay Configuration

        shellsession
`mynetworks = 0.0.0.0/0`

With this setting, this SMTP server can send fake emails and thus initialize communication between multiple parties. Another attack possibility would be to spoof the email and read it.

---

## Footprinting the Service

The default Nmap scripts include `smtp-commands`, which uses the `EHLO` command to list all possible commands that can be executed on the target SMTP server.

#### Nmap

        shellsession
`snchh337@htb[/htb]$ sudo nmap 10.129.14.128 -sC -sV -p25 Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-27 17:56 CEST Nmap scan report for 10.129.14.128 Host is up (0.00025s latency). PORT   STATE SERVICE VERSION 25/tcp open  smtp    Postfix smtpd |_smtp-commands: mail1.inlanefreight.htb, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING,  MAC Address: 00:00:00:00:00:00 (VMware) Service detection performed. Please report any incorrect results at https://nmap.org/submit/ . Nmap done: 1 IP address (1 host up) scanned in 14.09 seconds`

However, we can also use the [smtp-open-relay](https://nmap.org/nsedoc/scripts/smtp-open-relay.html) NSE script to identify the target SMTP server as an open relay using 16 different tests. If we also print out the output of the scan in detail, we will also be able to see which tests the script is running.

#### Nmap - Open Relay

        shellsession
`snchh337@htb[/htb]$ sudo nmap 10.129.14.128 -p25 --script smtp-open-relay -v 

PORT   STATE SERVICE
25/tcp open  smtp
| smtp-open-relay: Server is an open relay (16/16 tests)
|  MAIL FROM:<> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@nmap.scanme.org> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@ESMTP> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest%nmap.scanme.org@[10.129.14.128]>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest%nmap.scanme.org@ESMTP>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<"relaytest@nmap.scanme.org">
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<"relaytest%nmap.scanme.org">
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest@nmap.scanme.org@[10.129.14.128]>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<"relaytest@nmap.scanme.org"@[10.129.14.128]>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest@nmap.scanme.org@ESMTP>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<@[10.129.14.128]:relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<@ESMTP:relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<nmap.scanme.org!relaytest>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<nmap.scanme.org!relaytest@[10.129.14.128]>
|_ MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<nmap.scanme.org!relaytest@ESMTP>
MAC Address: 00:00:00:00:00:00 (VMware)`
