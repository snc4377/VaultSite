## Connection Instructions

For this lab, you will utilize RDP and have access to a non-domain-joined Windows host from which you can perform any actions needed to complete the lab. You will be using an RDP connection, much like in Part one.

- Click below in the Questions section to spawn the target host and obtain an IP address.
    - IP ==
    - Username == `image`
    - Password == `Academy_student_AD!`

---

## Task 4 Add and Remove Computers To The Domain

Our new users will need computers to perform their daily duties. The helpdesk has just finished provisioning them and requires us to add them to the INLANEFREIGHT domain. Since these analyst positions are new, we will need to ensure that the hosts end up in the correct OU once they join the domain so that group policy can take effect properly.

The host we need to join to the INLANEFREIGHT domain is named: `ACADEMY-IAD-W10` and has the following credentials for use to login and finish the provisioning process:

- User == `image`
- Password == `Academy_student_AD!`

Once you have access to the host, utilize your `htb-student_adm`: `Academy_student_DA!` account to join the host to the domain.

`Solution: Task 4`

To add the localhost to a domain via PowerShell, Open a PowerShell session as administrator, and then we can use the following command:

#### PowerShell Join a Domain


`PS C:\htb> Add-Computer -DomainName INLANEFREIGHT.LOCAL -Credential INLANEFREIGHT\HTB-student_adm -Restart`

This string utilizes the `domain` (INLANEFREIGHT.LOCAL) we wish to join the host to, and we must specify the `user` whose credentials we will use to authorize the join. (HTB-student_ADM). Specifying the restart at the string is necessary because the join will not occur until the host restarts again, allowing it to acquire settings and policies from the domain.

#### Add via the GUI

To add the computer to the domain from the localhost GUI is a bit different. Follow these steps to join it to the domain:

- From the computer you wish to join the domain, open the `Control Panel` and navigate to "System and Security > System."
- Now select the "Change Settings" icon in the `Computer name` section. Another dialog box will pop up asking you for administrator credentials. In the next window, we need to select the change icon next to the portion that says, "To rename this computer or change its domain or workgroup, click change" This will open yet another window for you to modify the computer's name, domain, and workgroup. Check that the computer's name matches the naming standard you wish to use for the domain before joining. Doing so will ease the administrative burden of renaming a domain-joined host later.
- next, we need to enter the name of the domain we wish to join the computer to (`INLANEFREIGHT.LOCAL`) and click OK. You may receive a warning about NetBIOS name resolution. That is an issue outside the scope of this lab. For now, move forward.
    - You will be prompted for domain credentials to complete this action. Utilize the domain administrator account you have been given at the beginning of this lab. (`htb-student_adm`).
    - If all goes well, you will be presented with a prompt welcoming you to the domain. The computer needs to restart to apply changes and new group policy settings it will receive from the domain.

## Add A Computer To The Domain

We are going to use the Windows GUI to add this PC to the domain.

![System information for Windows 10 Pro showing processor, RAM, system type, and computer name. 'Change settings' option is highlighted.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/74/join-domain1.png)

1. From the control panel, open up system properties for the pc. Click on Change Settings in the Computer name section.

![System Properties window showing Computer Name tab. Fields for computer description, full computer name 'ACADEMY-IAD-TEMPJ', and workgroup 'WORKGROUP'. 'Change' button is highlighted.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/74/join-domain2.png)

2. In this window, select the Change button beside "rename this computer or change its domain."

![Computer Name/Domain Changes window showing computer name 'ACADEMY-IAD-TEMPJ' and domain 'INLANEFREIGHT.LOCAL'. 'OK' button is highlighted.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/74/join-domain3.png)

3. Enter the domain you wish to join the host to. (INLANEFREIGHT.LOCAL) Hit OK.

![Windows Security dialog for Computer Name/Domain Changes. Domain: INLANEFREIGHT.LOCAL\htb-student_adm with password field. 'OK' button is highlighted.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/74/join-domain4.png)

4. Enter the domain administrator credentials provided to join the host to the domain.

![Computer Name/Domain Changes confirmation dialog. Message: 'Welcome to the INLANEFREIGHT.LOCAL domain.' 'OK' button is highlighted.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/74/join-domain5.png)

5. If all goes well, you will be prompted with a Welcome to the domain popup.

❮❯

#### Add a Remote Computer to a Domain


`PS C:\htb> Add-Computer -ComputerName ACADEMY-IAD-W10 -LocalCredential ACADEMY-IAD-W10\image -DomainName INLANEFREIGHT.LOCAL -Credential INLANEFREIGHT\htb-student_adm -Restart`

When we added the computer to the domain, we did not stage an AD object for it in the OU we wanted the computer in beforehand, so we have to move it to the correct OU now. To do so via PowerShell:

#### Check OU Membership of a Host


`PS C:\htb> Get-ADComputer -Identity "ACADEMY-IAD-W10" -Properties * | select CN,CanonicalName,IPv4Address`

The CanonicalName property (seen above) will tell us the full path of the host by printing out the name in the format "Domain/OU/Name." We can use this to locate the host and validate where it is in our AD structure.

Utilizing the ADUC snap-in, you can also move computer objects pretty quickly. You do so by:

#### Add to a New OU

## Move A Computer Object To A New OU

We need to find the new host, and move it to the "Security Analysts" OU in the same manner we moved the user account earlier.

![Active Directory Users and Computers interface showing Computers under INLANEFREIGHT.LOCAL. Context menu for ACADEMY-1 with 'Move' option highlighted.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/74/moveou1.png)

1. Looking in the Computers OU, select our newly joined host and right click it. Select the option to "Move"

![Active Directory Users and Computers interface showing the 'Move' dialog for ACADEMY-1. 'Computers' container is highlighted for selection.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/74/moveou2.png)

2. In the popup, drill down to the Security Analysts OU.

![Move object dialog in Active Directory. 'Corp' and 'Security Analysts' containers are highlighted for selection. 'OK' button is highlighted.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/74/moveou3.png)

3. Select the Security Analysts OU and hit OK.

![Active Directory Users and Computers interface showing ACADEMY-IAD-TEM computer under INLANEFREIGHT.LOCAL in the Computers container.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/74/moveou4.png)

4. If we look in that OU we will now see a new Computer object within.

❮❯

---

## Summary

This wraps up our administration duties for the day. Hopefully, this lab helped reinforce the basic concepts surrounding AD management. It is always great to get hands-on experience with topics and technologies like Active Directory. This experience provides a better understanding of how it functions and how it can possibly be taken advantage of. New vulnerabilities and attacks are being released every day that affect the Windows operating system, and by extension, Active Directory. A fundamental understanding of AD, the attacks that plague it, and defensive measures will take us a long way as security Professionals.