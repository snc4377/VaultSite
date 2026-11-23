---
title: "Intro To IDOR"
category: ["PREP_CPTS", "Pen-testing", "WEB ATTACK", "IDOR", "Intro to IDOR"]
---

**Key Concepts:**

- **Insecure Direct Object Reference (IDOR):** This is a vulnerability where a web application exposes a direct link or reference to an internal object, like a file or a database entry (e.g., `download.php?file_id=123`). An attacker can manipulate this reference (e.g., change `123` to `124`) to access resources they shouldn't have permission to see or modify.
- **Weak Access Control:** The true cause of an IDOR vulnerability is a weak or non-existent access control system on the application's back-end. Simply hiding a button or link on the front-end is not enough security. The back-end must always verify that the user making a request is actually authorized to access the specific object they are asking for.

**Impact and Application:**

- **Information Disclosure:** The most common impact is an attacker gaining access to other users' private data, such as personal files, messages, or financial details.
- **Privilege Escalation:** IDOR can also lead to an attacker performing actions reserved for administrators. If an admin function is exposed via an API call or URL parameter, a regular user might be able to call it directly and perform unauthorized actions like changing another user's password or granting themselves admin rights.

**Watch Out For:**

- The danger of IDOR isn't limited to just viewing data. Depending on the application's functionality, it can also allow an attacker to **modify or delete** data belonging to other users, potentially leading to a full account takeover.



