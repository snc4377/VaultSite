Alongside the discussion on hardening an AD domain, we wanted to talk about `AD auditing`. We aim to provide our clients with as much information as possible to help address potential issues we find. Doing so will give them more data to demonstrate they have a problem and help secure backing and funding to address those fixes. The tools in this section can be used to provide different visualizations and data outputs for this purpose.

---

## Creating an AD Snapshot with Active Directory Explorer

[AD Explorer](https://docs.microsoft.com/en-us/sysinternals/downloads/adexplorer) is part of the Sysinternal Suite and is described as:

"An advanced Active Directory (AD) viewer and editor. You can use AD Explorer to easily navigate an AD database, define favorite locations, view object properties and attributes without opening dialog boxes, edit permissions, view an object's schema, and execute sophisticated searches that you can save and re-run."

AD Explorer can also be used to save snapshots of an AD database for offline viewing and comparison. We can take a snapshot of AD at a given time and explore it later during the reporting phase, just as we would any other database. It can also be used to perform a before-and-after comparison of AD to uncover changes in objects, attributes, and security permissions.

When we first load the tool, we are prompted for login credentials or to load a previous snapshot. We can log in with any valid domain user.

#### Logging in with AD Explorer

![Active Directory Explorer connection window with fields for Connect to, User, Password, and Path, plus options to save the connection.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/47/AD_explorer1.png)

Once logged in, we can freely navigate AD and view information about all objects.

#### Navigating AD with AD Explorer

![Active Directory Explorer window showing the directory structure and attributes for DC=INLANEFREIGHT,DC=LOCAL.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/47/AD_explorer_logged_in.png)

To take an AD snapshot, go to File --> `Create Snapshot` and enter a name for the snapshot. Once completed, we can move it offline for deeper analysis.

#### Creating an AD Snapshot with AD Explorer

![Active Directory Explorer window with the snapshot dialog open, showing fields for description, path, and server utilization settings.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/47/AD_explorer_snapshot.png)

---

## PingCastle

[PingCastle](https://www.pingcastle.com/documentation/) is a powerful tool that assesses the security posture of an AD environment and provides us with results in various maps and charts. Thinking about security for a second, if you don't have an active inventory of hosts in your company, PingCastle can be a great resource to help compile one into a user-friendly domain map. PingCastle differs from tools like PowerView and BloodHound because, in addition to providing enumeration data that can inform our attacks, it also delivers a detailed report on the target domain's security level using a risk assessment/maturity framework-based methodology. The score shown in the report is based on the [Capability Maturity Model Integration](https://en.wikipedia.org/wiki/Capability_Maturity_Model_Integration) (CMMI). For a quick look at the provided help context, you can use the `--help` argument at the command prompt.

Note: If you encounter issues launching the tool, please change the system date to one before July 31, 2023, using the Control Panel (Set Time and Date).

#### Viewing the PingCastle Help Menu

```
C:\htb> PingCastle.exe --help

switch:
  --help              : display this message
  --interactive       : force the interactive mode
  --log               : generate a log file
  --log-console       : add log to the console
  --log-samba <option>: enable samba login (example: 10)

Common options when connecting to the AD
  --server <server>   : use this server (default: current domain controller)
                        the special value * or *.forest do the healthcheck for all domains
  --port <port>       : the port to use for ADWS or LDAP (default: 9389 or 389)
  --user <user>       : use this user (default: integrated authentication)
  --password <pass>   : use this password (default: asked on a secure prompt)
  --protocol <proto>  : selection the protocol to use among LDAP or ADWS (fastest)
                      : ADWSThenLDAP (default), ADWSOnly, LDAPOnly, LDAPThenADWS

<SNIP>
```
#### Running PingCastle

To run PingCastle, we can call the executable by typing `PingCastle.exe` in our CMD or PowerShell window or by clicking the executable, which will take us to interactive mode, presenting a menu of options within the `Terminal User Interface` (`TUI`).

#### PingCastle Interactive TUI

```
|:.      PingCastle (Version 2.10.1.0     1/19/2022 8:12:02 AM)
|  #:.   Get Active Directory Security at 80% in 20% of the time
# @@  >  End of support: 7/31/2023
| @@@:
: .#                                 Vincent LE TOUX (contact@pingcastle.com)
  .:       twitter: @mysmartlogon                    https://www.pingcastle.com
What do you want to do?
=======================
Using interactive mode.
Do not forget that there are other command line switches like --help that you can use
  1-healthcheck-Score the risk of a domain
  2-conso      -Aggregate multiple reports into a single one
  3-carto      -Build a map of all interconnected domains
  4-scanner    -Perform specific security checks on workstations
  5-export     -Export users or computers
  6-advanced   -Open the advanced menu
  0-Exit
==============================
This is the main functionnality of PingCastle. In a matter of minutes, it produces a report which will give you an overview of your Active Directory security. This report can be generated on other domains by using the existing trust links.
```
The default option is the `healthcheck` execution, which will establish a baseline overview of the domain and provide us with relevant information about misconfigurations and vulnerabilities. Even better, PingCastle can report on susceptibility to recent vulnerabilities, our shared resources (shares), trust relationships (trusts), permission delegation, and much more about the status of our users and devices. Under the Scanner option, we can find most of these checks.

#### Scanner Options

```
|:.      PingCastle (Version 2.10.1.0     1/19/2022 8:12:02 AM)
|  #:.   Get Active Directory Security at 80% in 20% of the time
# @@  >  End of support: 7/31/2023
| @@@:
: .#                                 Vincent LE TOUX (contact@pingcastle.com)
  .:       twitter: @mysmartlogon                    https://www.pingcastle.com
Select a scanner
================
What scanner whould you like to run ?
WARNING: Checking a lot of workstations may raise security alerts.
  1-aclcheck                                                  9-oxidbindings
  2-antivirus                                                 a-remote
  3-computerversion                                           b-share
  4-foreignusers                                              c-smb
  5-laps_bitlocker                                            d-smb3querynetwork
  6-localadmin                                                e-spooler
  7-nullsession                                               f-startup
  8-nullsession-trust                                         g-zerologon
  0-Exit
==============================
Check authorization related to users or groups. Default to everyone, authenticated users and domain users

```

Now that we understand how it works and how to start scans, let's look at the report.

#### Viewing the Report

Throughout the report, there are sections like domain information, user, group, and trust relationships, and a specific table that points out "anomalies" or issues that may require immediate attention. We'll also be presented with the domain's overall risk score.

![GIF showing the report generated by PingCastle.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/143/report-example.png)

Besides being useful for performing very thorough domain enumeration when combined with other tools, PingCastle can help provide clients with a quick analysis of their domain's security posture, or it can be used by internal teams for self-assessment to find areas of concern or opportunities for further hardening. Take some time to explore the reports and maps that PingCastle can generate in the Inlanefreight domain.

#### Group Policy

Since Group Policy is a major part of how Active Directory manages users and computers, it makes sense that we'd want to audit its configuration and highlight any potential holes. `Group3r` is an excellent tool for this.

---

## Group3r

[Group3r](https://github.com/Group3r/Group3r) is a tool specifically designed to find vulnerabilities in Group Policy associated with Active Directory. Group3r must be run from a domain-joined host with a domain user (it doesn't need to be an admin), or in the context of a domain user (i.e., using `runas /netonly`).

#### Basic Usage of Group3r

```
C:\htb> group3r.exe -f <filepath-name.log>
```

When running Group3r, we must specify the `-s` or `-f` flag. These will determine whether results are sent to standard output (stdout) (-s), or to the file we want to send the results to (-f). For more options and usage information, use the `-h` flag, or check the usage info in the link above.

Below is an example of how to start Group3r.

#### Reading the Output

![Screenshot of GPO configuration showing 'Disallow LM Hash' and 'Default Domain Controllers Policy' with details about creation, modification, and registry settings.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/143/grouper-output.png)

When reading Group3r's output, each indentation represents a different level, so unindented text will show the GPO, one level of indentation will show policy settings, and another will show findings within those settings. Next, we'll look at the output displayed for a finding.

#### Group3r Finding

![Command prompt showing registry updates for LDAPServerIntegrity, RequireSignOrSeal, RequireSecuritySignature, and EnableSecuritySignature, with details about user rights assignments.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/143/grouper-finding.png)

In the image above, you'll see an example of a Group3r finding. It will present it as a box linked to the policy setting, define the relevant part, and give us a reason for the finding. It's worth the effort to run Group3r if you have the chance. It often finds interesting paths or objects that other tools overlook.

---

## ADRecon

Finally, there are several other tools useful for collecting large amounts of AD data at once. In an assessment where stealth isn't required, it's also worth running a tool like [ADRecon](https://github.com/adrecon/ADRecon) and analyzing the results, in case our previous enumeration missed something minor that could be useful or worth pointing out to our client.

#### Running ADRecon

```
PS C:\htb> .\ADRecon.ps1

[*] ADRecon v1.1 by Prashant Mahajan (@prashant3535)
[*] Running on INLANEFREIGHT.LOCAL\MS01 - Member Server
[*] Commencing - 03/28/2022 09:24:58
[-] Domain
[-] Forest
[-] Trusts
[-] Sites
[-] Subnets
[-] SchemaHistory - May take some time
[-] Default Password Policy
[-] Fine Grained Password Policy - May need a Privileged Account
[-] Domain Controllers
[-] Users and SPNs - May take some time
[-] PasswordAttributes - Experimental
[-] Groups and Membership Changes - May take some time
[-] Group Memberships - May take some time
[-] OrganizationalUnits (OUs)
[-] GPOs
[-] gPLinks - Scope of Management (SOM)
[-] DNS Zones and Records
[-] Printers
[-] Computers and SPNs - May take some time
[-] LAPS - Needs Privileged Account
[-] BitLocker Recovery Keys - Needs Privileged Account
[-] GPOReport - May take some time
[*] Total Execution Time (mins): 11.05
[*] Output Directory: C:\Tools\ADRecon-Report-20220328092458
```

Once completed, ADRecon will leave a report in a new folder under the directory from which it was executed. We can see an example of the results in the terminal below. You'll get an HTML report and a directory with CSV results. When generating the report, note that Excel must be installed, otherwise the script won't automatically generate the report in that format; it will simply leave you with the .csv files. If you want Group Policy results, ensure the host you're running it from has the PowerShell `GroupPolicy` module installed. We can return later and generate the Excel report from another host using the `-GenExcel` argument and providing the report folder.

#### Reports

```
PS C:\htb> ls

    Directory: C:\Tools\ADRecon-Report-20220328092458

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         3/28/2022  12:42 PM                CSV-Files
-a----         3/28/2022  12:42 PM        2758736 GPO-Report.html
-a----         3/28/2022  12:42 PM         392780 GPO-Report.xml
```

We've covered so many tools and tactics within this module, but we felt it was prudent to showcase and explain some other ways to audit a target domain. Keep in mind that your actions must have a purpose, and our ultimate goal is to improve the client's security posture. So, with that in mind, gathering more evidence of issues will only serve to:

`Make our reports more compelling and provide the client with the tools they need to fix and actively secure their domain.`