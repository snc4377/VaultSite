---
title: "Kobold"
category: ["HTB", "Machines", "Kobold"]
---



Here we will list by Docker since we have seen an Arcane for Docker on port 3552.

https://nvd.nist.gov/vuln/detail/CVE-2025-64714  
Here we see that it is vulnerable to LFI, but we need to be able to execute PHP.

And now we will mount the root filesystem in a container to become root.

| Parameter         | Meaning                                      |
|-------------------|----------------------------------------------|
| Container Name    | `pwned` _(we can write anything)_           |
| Image             | `privatebin/nginx-fpm-alpine:2.0.2`         |
| Domain            | `/bin/bash`                                 |
| User              | `0`                                         |

Dump the root.
