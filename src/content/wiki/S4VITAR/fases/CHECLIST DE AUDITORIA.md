---
title: "CHECLIST DE AUDITORIA"
category: ["S4VITAR", "fases", "CHECLIST DE AUDITORIA"]
---

Note title: Untitled

- [ ] Perform reconnaissance (Content management systems (their APIs, their versions), services and their versions, technologies, etc.)
- [ ] Network scanning
- [ ] Vulnerability search and exploitation
- [ ] Once inside the system, check the permissions we have, for example with `sudo -l`, `find / -perm -u=s -type f 2>/dev/null`, etc.
- [ ] If we try everything and don't see how to perform privilege escalation, then we'll resort to tools like linpeas or LSE (since we don't have the OSEE yet, we'll leave Zero-Days for the future).