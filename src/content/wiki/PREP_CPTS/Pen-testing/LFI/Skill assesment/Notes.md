---
title: "Notes"
category: ["PREP_CPTS", "Pen-testing", "LFI", "Skill assesment", "Notes"]
---

Note title: Untitled

https://medium.com/@0xBlk/skills-assessment-file-inclusion-write-up-d3cf6e40adf1
## Mini Guide: From File Upload to RCE (Explained Summary)

I'll explain the complete flow and the "why" behind each step, in simple terms.

### 1. Initial Reconnaissance

Available pages are explored (`index.php`, `contact.php`, `apply.php`). `apply.php` stands out because it has a form with **file upload** (a field to upload a CV). File uploads are always a hot spot because if the server doesn't validate what type of file it accepts, you can upload executable code.

**Why it matters:** if you upload a `.php` file with malicious code and the server doesn't block it, you now have a "weapon" stored on the server... the problem is you usually can't access it directly (you don't know the exact path).

### 2. Webshell Upload

A simple PHP file is uploaded:

```php
<?php system($_GET["cmd"]); ?>
```

This is a "webshell": if you manage to execute it, it lets you run operating system commands through a URL parameter (`cmd`).

**Why the upload works:** there is no extension or content validation on the backend. The server accepts any file.

### 3. Finding how to include/execute that file (LFI)

Uploading the file is useless if you can't make the server **execute** it. This is where **LFI (Local File Inclusion)** comes in: a vulnerability where the server includes/loads files based on a parameter you control.

- They tried `thanks.php?n=...` but it wasn't vulnerable (it only reflected the text, didn't include files).
- Reviewing the page's source code, they saw that images were loaded via `/api/image.php?p=<hash>`. This made them suspect that the `p` parameter might be reading files from disk.

**Why fuzz:** instead of guessing manually, they used `ffuf` with a wordlist of typical LFI payloads (paths with `../../../` variants) to automatically find which combination makes the server return different content (in this case, filtering by response size ≠ 0).

- They found that `....//....//....//etc/passwd` worked → confirmed LFI, because they could read a system file that shouldn't be accessible.

### 4. Reading the source code with `php://filter`

Once LFI was confirmed, instead of reading `/etc/passwd`, they used a PHP trick:

```
php://filter/read=convert.base64-encode/resource=archivo.php
```

**Why:** If you try to include a `.php` file directly, the server _executes_ it instead of showing you the text. But if you request it encoded in base64, the server doesn't "understand" it as PHP code and returns the content as-is, which you then decode yourself. This lets you read the source code without executing it.

### 5. Analyzing the Found Source Code

Two key files:

**`application.php`** (handles file uploads):

- Saves the uploaded file to `../uploads/`
- Names it using the **MD5 hash of the file's content** + original extension.

**Why it matters:** This means the final filename of the uploaded file isn't secretly random—it's predictable if you already know the file's content (because you uploaded it). You just need to calculate the MD5 of your own webshell to know what it's called on the server.

**`contact.php`** (the truly vulnerable one):

```php
if (str_contains($_GET["region"], ".") || str_contains($_GET["region"], "/")) {
    // bloquea
} else {
    $region = urldecode($_GET["region"]);
}
include "./regions/" . $region . ".php";
```

**The logic flaw here is critical:** first it checks if the parameter contains `.` or `/` (to block path traversal like `../../`), but **then** does `urldecode()`. Meaning it validates the text _before_ decoding it. If you send the payload URL-encoded (`%2E` = `.`, `%2F` = `/`), at validation time there are no literal `.` or `/`... but after decoding, they appear. The filter bypasses itself.

### 6. Exploitation Strategy

**Step A — Calculate the name of the uploaded shell:**

```
md5sum shell.php
```

This gives the hash that the server used as the filename in `uploads/`.

**Step B — Attempt to include it via `contact.php`:**  
Since `include` automatically adds `.php` and looks in `./regions/`, we need to construct a path like `../uploads/<hash>` to "escape" from the `regions/` folder and point to the uploaded file.

**Step C — Bypass the filter with double URL encoding:**

- If you encode it once (`%2E%2E%2F...`), the browser (or server) decodes it automatically _before_ it reaches the check, so the filter detects the `.` and `/` and blocks you.
- If you encode it **twice** (`%252E%252E%252F...`), the first "level" of decoding (automatic, by the browser/server) only converts `%25` → `%`, leaving the text as `%2E%2E%2F...` — with no literal dots or slashes yet. It passes the filter. Then the code manually calls `urldecode()`, which performs the **second** decoding, now converting `%2E%2E%2F` into `../`. By then, the check has already passed.

**Why this is so effective:** it's a classic "time of check vs time of use" bypass — the filter checks the data in one state, but the data is _used_ (decoded) in a later state, and the attacker exploits this difference in "views" of the same data.

### 7. Result: RCE

With the final payload:

```
contact.php?region=%252E%252E%252Fuploads%252F<hash_del_shell>&cmd=ls
```

The server:

1. Passes the filter (doesn't see `.` or `/`)
2. Decodes and constructs the real path to the uploaded webshell
3. Includes it with `include` → **executes** it as PHP
4. The `cmd=ls` is passed to the `system()` inside the shell → arbitrary command execution

From there, changing `cmd=ls` to `cmd=cat /flag.txt` (or similar) gives the flag.

---

**Full chain summary (the key concept to remember):**

1. **Unrestricted upload** → you get malicious code onto the server.
2. **Predictable filename** → you know where your code landed.
3. **Poorly filtered LFI** (`include` with user input) → you can tell the server to execute _your_ file instead of a legitimate one.
4. **Filter bypass with double encoding** → you trick validation by exploiting that it validates before decoding.
5. **RCE** → you control system commands.