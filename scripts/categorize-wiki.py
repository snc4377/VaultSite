#!/usr/bin/env python3
"""
categorize-wiki.py — derive `category` frontmatter from vault folder paths.

For every .md file under ROOT:
  * take the path relative to ROOT;
  * drop blacklisted root folders (case-insensitive);
  * use the remaining directories plus the filename stem as the category path;
  * humanize each segment (separators -> spaces, acronyms preserved);
  * insert or replace `category: [...]` in the YAML frontmatter.

The body, title, date and every other key are preserved. A leading `---`
block that is not valid YAML (usually a horizontal rule) is treated as
content: a valid frontmatter block is prepended instead of splicing into it.

Usage:
    python3 scripts/categorize-wiki.py --dry-run --limit 10
    python3 scripts/categorize-wiki.py --dry-run --limit 10 --directory-only
    python3 scripts/categorize-wiki.py --dry-run
    python3 scripts/categorize-wiki.py              # writes; full backup first
    python3 scripts/categorize-wiki.py --root /tmp/vault --backup-dir /tmp/backups

Requires: Python 3.11+, PyYAML.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import NoReturn

try:
    import yaml
except ImportError:  # pragma: no cover - dependency guard
    sys.exit("categorize-wiki: missing dependency 'pyyaml' — run: pip install pyyaml")

DEFAULT_ROOT = Path("/opt/obsidian-vault-en")
DEFAULT_BACKUP_DIR = Path("/opt/obsidian-vault-en-backups")

# Root folders that should not appear in the published hierarchy.
BLACKLIST = {
    "s4vitar",
    "prep_cpts",
    "apuntes david",
    "htb",
    "homelab",
    "content bin",
}

# All-caps words that should stay acronyms instead of becoming "Ntlm", "Xss".
ACRONYMS = {
    "AD", "API", "ATT&CK", "AWS", "BD", "CBBH", "CD", "CI", "CLI", "CPTS",
    "CRTO", "CRTP", "CSRF", "CVE", "CWE", "CWEE", "DHCP", "DNS", "DOM",
    "EC2", "FTP", "GIT", "GPO", "HTB", "HTTP", "HTTPS", "IAM", "ICMP",
    "IDOR", "IMAP", "IP", "JSON", "JWT", "LAN", "LDAP", "LFI", "LLMNR",
    "MAC", "MITRE", "MSF", "NBT", "NMAP", "NS", "NTLM", "OS", "OSCE", "OSCP",
    "OSINT", "OSWE", "PHP", "PNPT", "POP3", "RCE", "RDP", "RDS", "RFI",
    "S3", "SMB", "SMTP", "SNMP", "SQL", "SQLI", "SSH", "SSL", "SSRF",
    "SSTI", "TCP", "TLS", "UDP", "UI", "URL", "VPC", "VPN", "WAN", "WIFI",
    "XML", "XSS", "XXE", "YAML",
}

# Mixed-case terms whose spelling should survive humanization.
PRESERVE_CASE = {
    "eCPPT", "eJPT", "GitHub", "iOS", "JavaScript", "macOS", "McAfee",
    "Nmap", "PowerShell", "SQLi", "WiFi",
}

FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)
CATEGORY_RE = re.compile(r"^category\s*:")


def die(message: str) -> NoReturn:
    print(f"categorize-wiki: {message}", file=sys.stderr)
    raise SystemExit(1)


def capitalize(word: str) -> str:
    """Uppercase the first alphanumeric character, lowercase the rest.

    Leading punctuation is preserved: "(STEP" -> "(Step", "⭐" -> "⭐".
    """
    index = 0
    while index < len(word) and not word[index].isalnum():
        index += 1
    if index == len(word):
        return word
    return word[:index] + word[index].upper() + word[index + 1 :].lower()


def humanize(segment: str) -> str:
    """Turn a folder/file stem into a readable category label."""
    text = re.sub(r"[-_]+", " ", segment)
    words = re.sub(r"\s+", " ", text).strip().split(" ")
    out: list[str] = []
    for word in words:
        if not word:
            continue
        if word in PRESERVE_CASE:
            out.append(word)
        elif word.isupper():
            out.append(word if word in ACRONYMS else capitalize(word))
        elif word[:1].isupper() and any(char.isupper() for char in word[1:]):
            out.append(word)  # SQLi, NTLM, McAfee
        else:
            out.append(capitalize(word))
    return " ".join(out)


def categories_for(rel: Path, include_stem: bool = True) -> list[str]:
    """Path -> category array, dropping blacklisted roots.

    By default the filename stem is the last category element, matching the
    examples in the brief. Pass include_stem=False to keep notes directly
    under their directory.
    """
    directories = list(rel.parts[:-1])
    while directories and directories[0].strip().casefold() in BLACKLIST:
        directories.pop(0)

    segments = [*directories, rel.stem] if include_stem else directories
    categories: list[str] = []
    for segment in segments:
        label = humanize(segment)
        if label:
            categories.append(label)
    return categories


def split_frontmatter(text: str) -> tuple[str, str, str] | None:
    """Return (raw_frontmatter, body, newline) or None when absent."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    newline = "\r\n" if text.startswith("---\r\n") else "\n"
    return match.group(1), text[match.end() :], newline


def category_line(categories: list[str]) -> str:
    # JSON flow sequences are valid YAML and quote safely.
    return f"category: {json.dumps(categories, ensure_ascii=False)}"


def inject_category(text: str, categories: list[str]) -> tuple[str, str]:
    """Return (new_text, action), where action is insert/update/prepend/unchanged."""
    parts = split_frontmatter(text)
    if parts is None:
        newline = "\r\n" if "\r\n" in text else "\n"
        block = f"---{newline}{category_line(categories)}{newline}---{newline}{newline}"
        return block + text, "insert"

    raw, body, newline = parts
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        data = None
        valid = False
    else:
        valid = data is None or isinstance(data, dict)

    if not valid:
        # A horizontal rule or other non-mapping block: keep it in the body.
        block = f"---{newline}{category_line(categories)}{newline}---{newline}{newline}"
        return block + text, "prepend"

    data = data or {}
    if isinstance(data.get("category"), list) and data["category"] == categories:
        return text, "unchanged"

    lines = raw.splitlines()
    index = next(
        (i for i, line in enumerate(lines) if CATEGORY_RE.match(line)),
        None,
    )

    if index is None:
        lines.append(category_line(categories))
        action = "insert"
    else:
        end = index + 1
        rest = lines[index].split(":", 1)[1].strip()

        if rest.startswith("[") and rest.count("[") > rest.count("]"):
            depth = rest.count("[") - rest.count("]")
            while end < len(lines) and depth > 0:
                depth += lines[end].count("[") - lines[end].count("]")
                end += 1
        elif rest == "" or rest.startswith(("|", ">")):
            while end < len(lines) and (
                lines[end].strip() == ""
                or lines[end].startswith((" ", "\t"))
                or lines[end].startswith("- ")
            ):
                end += 1

        lines[index:end] = [category_line(categories)]
        action = "update"

    new_raw = newline.join(lines)
    return f"---{newline}{new_raw}{newline}---{newline}{body}", action


def iter_notes(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def create_backup(root: Path, backup_dir: Path) -> Path:
    """Copy the whole vault to a timestamped sibling directory."""
    backup_dir = backup_dir.expanduser().resolve()
    if backup_dir == root or root in backup_dir.parents:
        die("backup directory must live outside the vault")

    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        die(
            f"cannot create {backup_dir}. Run:\n"
            f'  sudo mkdir -p "{backup_dir}"\n'
            f'  sudo chown -R "$(id -u):$(id -g)" "{backup_dir}"'
        )
    if not backup_dir.is_dir():
        die(f"backup directory is not usable: {backup_dir}")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = backup_dir / f"{root.name}-{stamp}"
    suffix = 1
    while dest.exists():
        dest = backup_dir / f"{root.name}-{stamp}-{suffix}"
        suffix += 1

    try:
        shutil.copytree(root, dest, symlinks=True)
    except OSError as exc:
        die(f"backup failed: {exc}")
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Derive wiki categories from the vault's folder structure."
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help=f"vault root (default {DEFAULT_ROOT})")
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=DEFAULT_BACKUP_DIR,
        help=f"backup parent directory (default {DEFAULT_BACKUP_DIR})",
    )
    parser.add_argument("--dry-run", action="store_true", help="print the result without writing")
    parser.add_argument("--limit", type=int, metavar="N", help="process only the first N notes")
    parser.add_argument(
        "--directory-only",
        action="store_true",
        help="omit the filename stem from the category path",
    )
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.is_dir():
        die(f"vault not found: {root}")
    if args.limit is not None and args.limit < 1:
        die("--limit must be at least 1")

    files = iter_notes(root)
    if not files:
        die(f"no .md files under {root}")
    selected = files[: args.limit] if args.limit else files

    print(f"categorize-wiki: {root} ({len(files)} notes)")
    if args.limit:
        print(f"limit: first {len(selected)} notes")
    if args.dry_run:
        print("DRY RUN: no files will be written; no backup will be created.")
    print()

    plans: list[tuple[Path, Path, list[str], str, str]] = []
    errors: list[tuple[Path, str]] = []
    counts = {"insert": 0, "update": 0, "prepend": 0, "unchanged": 0}

    for path in selected:
        rel = path.relative_to(root)
        categories = categories_for(rel, include_stem=not args.directory_only)
        text = path.read_text(encoding="utf-8-sig")

        try:
            new_text, action = inject_category(text, categories)
        except Exception as exc:  # noqa: BLE001 - report one bad file, keep going
            errors.append((rel, str(exc)))
            print(f"[skip] {rel.as_posix()}: {exc}")
            continue

        counts[action] = counts.get(action, 0) + 1
        plans.append((path, rel, categories, action, new_text))

        if args.dry_run or action == "unchanged":
            label = action if action == "unchanged" else action.upper()
            print(f"[{label}] {rel.as_posix()}")
            if action != "unchanged":
                print(f"         category: {json.dumps(categories, ensure_ascii=False)}")

    if not args.dry_run:
        changes = [plan for plan in plans if plan[3] != "unchanged"]
        if not changes:
            print("\nno changes; no backup created.")
        else:
            backup = create_backup(root, args.backup_dir)
            print(f"\nbackup: {backup}")
            for path, rel, categories, action, new_text in changes:
                path.write_text(new_text, encoding="utf-8")
                print(
                    f"[{action}] {rel.as_posix()} -> "
                    f"{json.dumps(categories, ensure_ascii=False)}"
                )

    print()
    print(
        f"summary: {len(plans)} processed — "
        f"{counts['insert']} insert, {counts['update']} update, "
        f"{counts['prepend']} prepend, {counts['unchanged']} unchanged"
        + (f", {len(errors)} skipped" if errors else "")
    )
    if args.dry_run:
        print("dry run: re-run without --dry-run to write; a full backup is created first.")
    if errors:
        print(
            "skipped notes: " + ", ".join(str(rel) for rel, _ in errors),
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
