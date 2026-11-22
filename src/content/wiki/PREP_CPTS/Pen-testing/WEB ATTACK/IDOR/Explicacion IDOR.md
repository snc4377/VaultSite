An **IDOR (Insecure Direct Object Reference)** or _Insecure Direct Object Reference_ occurs when a web application exposes an internal identifier (such as a user ID in the database or a filename) and **does not verify on the server (back-end)** whether the person making the request has actual permission to view or modify that resource.

In short: the application blindly trusts the data sent by the user without verifying if that data belongs to them.

## The 3 Keys to Understanding an IDOR

- **Exposing an ID is not the real flaw:** A website using links like `profile.php?id=50` is not a vulnerability by itself. The real issue is the **lack of access control (Access Control)** on the server to verify that you own `id=50`.
    
- **The Front-end Illusion:** Many developers believe that hiding a button in the graphical interface (Front-end) or displaying only your own files on the screen is enough. However, if an attacker intercepts the HTTP request (e.g., using tools like _Burp Suite_) and manually changes the parameter, the server will deliver the data if there is no internal validation.
    
- **Why They Are So Common:** Designing robust access control (like a role-based system or _RBAC_) without breaking the functionality of a large application is complex. Additionally, **automated scanners often fail to detect them**, as a machine doesn't always understand the business logic (it can't distinguish whether document `124` should be public or private), so manual testing is required during an audit or pentest.
    

## Impact and Escalation Types

The text you shared highlights different impact levels, which in cybersecurity are also divided based on the direction of privilege escalation:

|**Impact Type / Escalation**|**What Does It Involve?**|**Risk Level**|
|---|---|---|
|**Information Disclosure**|Read-only. You can view other users' private data (invoices, messages, banking details, uploaded files).|High (Data leak / GDPR)|
|**Data Modification / Deletion**|Write access. You alter other users' data. If you change another user's email or password, you achieve **Account Takeover** (complete account theft).|Critical|
|**Insecure Function Calls**|Execution of hidden administrative actions in the front-end code but unprotected in the back-end (e.g., elevating your user to admin).|Critical (Total web compromise)|
|**Horizontal vs. Vertical Escalation**|**Horizontal:** Access resources of a user with the same rank (User A views User B's data).<br><br>  <br><br>**Vertical:** Access resources or functions of a higher rank (Regular user performs Admin actions).|High to Critical|

## Practical Examples

### 1. The Classic: Information Theft via URL (Horizontal Escalation)

Imagine uploading your resume or downloading a medical bill from a clinic, and the website redirects you to this link:

> `[https://example-clinic.com/download.php?file_id=123](https://example-clinic.com/download.php?file_id=123)`

1. You notice the parameter `file_id=123` is a very easy-to-guess sequential number.
    
2. You go to the address bar, change it to `124`, and press Enter:
    
    > `[https://example-clinic.com/download.php?file_id=124](https://example-clinic.com/download.php?file_id=124)`
    
3. **What Happens on the Server?** Since there's no access control asking, _"Does file 124 belong to the logged-in user?"_, the server simply searches for file `124` and downloads another patient's medical history for you.
    

### 2. Data Modification and _Account Takeover_ (In the Request Body)

Not all IDORs are in the address bar (URL). Many occur invisibly when updating your profile via an API.

Imagine changing your account password (your user ID is `500`). When clicking the "Save" button, your browser sends this hidden `POST` request to the server:

HTTP

```
POST /api/v1/users/change-password HTTP/1.1
Host: aplicacion-vulnerable.com
Content-Type: application/json
Cookie: session_id=tu_sesion_valida_del_usuario_500

{
  "user_id": 500,
  "new_password": "MiNuevaPassword123!"
}
```

An attacker captures this request before it leaves their computer and changes `"user_id": 500` to `"user_id": 1` (which is usually the main administrator's account).

- If the server only verifies that you have a valid session (`Cookie`), but **does not check that your session matches the `user_id` in the JSON**, you will change the administrator's password and take control of their account.
    

### 3. Calling Administrative Functions (_Insecure Function Calls_ / Vertical Escalation)

A normal user accesses the website's source code (by pressing F12 in the browser) and, while reading a JavaScript file, discovers references to an API route that doesn't appear on their screen because it's disabled for normal users:

> `/api/admin/promote_user?id=500&role=admin`

Even though the "Make Admin" button isn't visible on their screen, the user types this route directly or sends the request. If the developer only hid the button in the visual design but forgot to program a server-side rule stating _"Only users who are already administrators can call this API"_, the normal user will become the application's administrator.