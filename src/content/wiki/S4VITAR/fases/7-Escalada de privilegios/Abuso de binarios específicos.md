---
title: "Abuso De Binarios Específicos"
category: ["S4VITAR", "fases", "7-Escalada de privilegios", "Abuso de binarios específicos"]
---

Note title: Untitled

In this class, we will analyze how to elevate our user privileges by exploiting two different binaries as illustrative examples.

The first example focuses on exploiting the legitimate binary **exim-4.84-7**, which has a vulnerability identified as **CVE-2016-1531**. This vulnerability allows an attacker to execute privileged commands by abusing certain environment variables. We will study how to leverage this vulnerability to escalate privileges and access restricted functions.

The second example addresses a **Buffer Overflow** in a custom binary on a **32-bit Linux** machine with **active protections** and **ASLR** enabled. In this case, we will focus on exploiting a **ret2libc** in a binary that has SUID permissions and is owned by root. Through the buffer overflow, we will demonstrate how to inject privileged commands and, consequently, elevate user privileges.

The goal of this class is to demonstrate how certain binaries, both legitimate and custom, can be exploited to obtain elevated privileges, highlighting the importance of proper system configuration and protection.


