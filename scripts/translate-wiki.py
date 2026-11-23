#!/usr/bin/env python3
"""
translate-wiki.py — vault -> Astro translation pipeline.

Reads every .md file under SRC (default /opt/obsidian-vault), detects its
language, and writes an English copy into DST (default /opt/obsidian-vault-en).

  * Spanish  -> translated to professional, technical English via DeepSeek.
  * English  -> copied byte-for-byte (no LLM call).
  * Anything else -> left untranslated; the run exits non-zero so it cannot
    be mistaken for a complete English vault.

The source vault is NEVER written to. Filenames are never changed, so
Obsidian `[[Wikilinks]]` keep resolving inside the output vault.

Usage:
    python3 scripts/translate-wiki.py --check            # list languages, no API calls
    python3 scripts/translate-wiki.py --dry-run          # plan, no API calls, no writes
    python3 scripts/translate-wiki.py --dry-run --force  # include existing notes in the plan
    python3 scripts/translate-wiki.py                    # translate + write
    python3 scripts/translate-wiki.py --force            # rewrite every existing note
    python3 scripts/translate-wiki.py --only "Some Note.md"

Public image URLs default to /wiki-images/...; pass `--public-base /VaultSite`
for a GitHub Pages project site served under that base.

API keys are provider-specific (DEEPSEEK_API_KEY or OPENROUTER_API_KEY),
read from the environment first and then from the active Hermes profile's
.env (falling back to ~/.hermes/.env). --provider auto picks whichever key
is configured. Keys are never printed.

Requires: Python 3.11+, `pip install pyyaml`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import quote, unquote
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, NoReturn

try:
    import yaml
except ImportError:  # pragma: no cover - dependency guard
    sys.exit("translate-wiki: missing dependency 'pyyaml' — run: pip install pyyaml")

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

SRC = Path("/opt/obsidian-vault")
DST = Path("/opt/obsidian-vault-en")

# Obsidian's own config folder: never mirrored into the public site.
EXCLUDE_DIRS = {".obsidian", ".trash", ".git", ".stfolder", ".stversions"}

# Frontmatter keys whose text is translated. `tags` are deliberately absent:
# they are identifiers used for filtering and must stay stable.
TRANSLATABLE_KEYS = {"title", "description", "summary", "excerpt"}

# Everything else (tags, aliases, date, cssclasses, publish, ...) is passed
# through untouched: tags are identifiers and must stay stable.

PROVIDERS = {
    "deepseek": {
        "url": "https://api.deepseek.com/chat/completions",
        "model": "deepseek-chat",
        "key_env": "DEEPSEEK_API_KEY",
    },
    "openrouter": {
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "model": "deepseek/deepseek-chat",
        "key_env": "OPENROUTER_API_KEY",
    },
}

HERMES_ENVS = (
    Path("/home/hermes/.hermes/profiles/webdev/.env"),
    Path("/home/hermes/.hermes/.env"),
)
MANIFEST_NAME = ".translate-manifest.json"

FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)

# Images are copied flat into the Astro project's public folder.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_IMAGES_DIR = PROJECT_ROOT / "public" / "wiki-images"

IMAGE_EXTENSIONS = {
    ".avif",
    ".bmp",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".png",
    ".svg",
    ".tif",
    ".tiff",
    ".webp",
}

OBSIDIAN_IMAGE_RE = re.compile(r"!\[\[([^\]]+)\]\]")
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]*)\)")

# Language checks — ordered most-specific first. A note is "Spanish" when it
# contains Spanish function words that are absent from English, and its
# Spanish signal beats its English signal. No extra dependency needed.
SPANISH_MARKERS = re.compile(
    r"\b(?:el|la|los|las|un|una|unos|unas|de|del|que|y|o|para|por|con|sin|"
    r"es|son|está|están|ser|tiene|tienen|más|también|pero|como|desde|hasta|"
    r"cuando|donde|porque|muy|este|esta|estos|estas|se|su|sus|al|lo|"
    r"puedes|puede|debemos|hay)\b",
    re.I,
)
SPANISH_CHARS = re.compile(r"[ñáéíóúüÑÁÉÍÓÚÜ¿¡]")
ENGLISH_MARKERS = re.compile(
    r"\b(?:the|and|of|to|is|are|with|for|from|that|this|when|where|because|"
    r"but|also|you|can|should|will|has|have|not|there|which|into|about)\b",
    re.I,
)


# --------------------------------------------------------------------------
# Small utilities
# --------------------------------------------------------------------------


def die(msg: str) -> NoReturn:
    print(f"translate-wiki: {msg}", file=sys.stderr)
    sys.exit(1)


def read_key(provider: str) -> str | None:
    """Env var first, then the Hermes .env file. Never echoes the value.

    Keys are provider-specific: a DeepSeek key must never be sent to
    OpenRouter (or vice versa).
    """
    env_name = PROVIDERS[provider]["key_env"]
    candidates = {env_name, f"HERMES_{env_name}"}
    for candidate in sorted(candidates):
        value = os.environ.get(candidate)
        if value:
            return value.strip()
    for env_file in HERMES_ENVS:
        if not env_file.is_file():
            continue
        for line in env_file.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            key, _, raw = line.partition("=")
            if key.strip() in candidates:
                value = raw.strip().strip('"').strip("'")
                if value:
                    return value
    return None


def split_frontmatter(text: str) -> tuple[dict[str, Any] | None, str, str]:
    """Return (frontmatter_dict, raw_frontmatter, body).

    `raw_frontmatter` is the text between the --- delimiters, so translated
    values can be spliced back without reformatting the rest of the block.
    """
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, "", text
    raw = match.group(1)
    data = yaml.safe_load(raw)
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data, raw, text[match.end() :]


def _split_comment(text: str) -> tuple[str, str]:
    """Split `value  # comment` while respecting quoted strings."""
    quote: str | None = None
    for idx, char in enumerate(text):
        if quote:
            if char == quote and (idx == 0 or text[idx - 1] != "\\"):
                quote = None
        elif char in "\"'":
            quote = char
        elif char == "#" and idx > 0 and text[idx - 1] in " \t":
            return text[:idx], text[idx:]
    return text, ""


def _format_scalar(original: str, value: str) -> str:
    """Render a translated value, keeping the original quoting style."""
    stripped = original.strip()
    if stripped.startswith('"') and stripped.endswith('"'):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if stripped.startswith("'") and stripped.endswith("'"):
        return "'" + value.replace("'", "''") + "'"
    if (
        not value
        or value[0] in "-?:,[]{}#&*!|>'\"%@`"
        or ": " in value
        or " #" in value
        or value != value.strip()
    ):
        return json.dumps(value, ensure_ascii=False)
    return value


def render_frontmatter(raw: str, translated: dict[str, str]) -> str:
    """Splice translated values into the original YAML, preserving layout."""
    lines = raw.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip("\r\n")
        eol = line[len(stripped) :]
        match = re.match(r"^([A-Za-z0-9_-]+):(.*)$", stripped)
        if not match or match.group(1) not in translated:
            out.append(line)
            i += 1
            continue

        key, rest = match.group(1), match.group(2)
        value = translated[key]
        if not value.strip():
            # An empty translation must not destroy the original value.
            out.append(line)
            i += 1
            continue

        # Block scalars (title: > / description: |) keep their header.
        if rest.strip() in ("|", ">", "|-", ">-", "|+", ">+"):
            header = rest.strip()
            block: list[str] = []
            j = i + 1
            while j < len(lines) and (lines[j].startswith((" ", "\t")) or not lines[j].strip()):
                block.append(lines[j])
                j += 1
            indent = "  "
            for candidate in block:
                if candidate.strip():
                    indent = candidate[: len(candidate) - len(candidate.lstrip())]
                    break
            out.append(f"{key}: {header}{eol}")
            for text_line in value.splitlines():
                out.append(f"{indent}{text_line}{eol}")
            i = j
            continue

        value_part, comment = _split_comment(rest)
        out.append(f"{key}: {_format_scalar(value_part, value)}{comment}{eol}")
        i += 1
    return "".join(out)


def strip_code(text: str) -> str:
    """Remove fenced/inline code so its identifiers don't skew detection."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return re.sub(r"`[^`]*`", " ", text)


# --------------------------------------------------------------------------
# Language detection
# --------------------------------------------------------------------------


@dataclass
class LanguageVerdict:
    language: str  # "es" | "en" | "unknown"
    es_score: int
    en_score: int
    reason: str


def detect_language(text: str, path: Path) -> LanguageVerdict:
    prose = strip_code(text)
    words = re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", prose)
    if len(words) < 12:
        return LanguageVerdict("unknown", 0, 0, "too little prose to judge")

    es_score = len(SPANISH_MARKERS.findall(prose)) + 3 * len(SPANISH_CHARS.findall(prose))
    en_score = len(ENGLISH_MARKERS.findall(prose))

    # Filename hint: "git-básico.md" is a strong, cheap signal. Check the raw
    # stem — accent-stripping would hide exactly what we are looking for.
    if any(c in path.stem for c in "ñáéíóúüÑÁÉÍÓÚÜ"):
        es_score += 2

    if es_score >= 3 and es_score > en_score:
        return LanguageVerdict("es", es_score, en_score, f"es={es_score} en={en_score}")
    if en_score >= 3 and es_score == 0:
        return LanguageVerdict("en", es_score, en_score, f"es={es_score} en={en_score}")
    return LanguageVerdict("unknown", es_score, en_score, f"es={es_score} en={en_score} (ambiguous)")


# --------------------------------------------------------------------------
# LLM client (DeepSeek, OpenAI-compatible)
# --------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a technical translator for a cybersecurity engineer's public notes.
Translate the user's Markdown note from Spanish into English.

Rules:
- Professional, precise, technical English. Keep the author's voice: direct and
  concrete. No marketing tone, no filler, no added commentary.
- Output ONLY the translated Markdown. No preamble, no code fences around the
  whole answer, no explanations.
- Preserve the document structure exactly: heading levels, list markers, tables,
  blockquotes, horizontal rules, blank lines and paragraph breaks.
- Leave these verbatim: fenced code blocks and their contents, inline code,
  URLs, image paths, HTML tags, Obsidian [[Wikilinks]] and ![[embeds]],
  callout markers (e.g. "> [!warning]"), math, and filenames.
- Never rewrite, reorder or drop image embeds (`![[...]]`) or Markdown
  images (`![...](...)`); keep the image syntax exactly as written.
- Do not translate the filename; filenames are never changed.
- Domain terms: when the standard English term is well known (e.g. "keylogger",
  "phishing", "payload", "shell"), use it. Otherwise translate plainly."""

FIELD_PROMPT = """Translate the string values in this JSON object from Spanish to English.
Return ONLY a JSON object with the same keys and translated values:
%s
Rules: professional, technical English. Keep the author's meaning and any
product names, commands or proper nouns. Do not add, remove or rename keys.
Return valid JSON only."""


class LLMError(RuntimeError):
    pass


class DeepSeekClient:
    def __init__(self, provider: str, api_key: str, timeout: int = 180, model: str | None = None):
        cfg = PROVIDERS[provider]
        self.provider = provider
        self.url = cfg["url"]
        self.model = model or cfg["model"]
        self.api_key = api_key
        self.timeout = timeout
        self.calls = 0

    def _post(self, payload: dict[str, Any], retries: int = 4) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.provider == "openrouter":
            headers["HTTP-Referer"] = "https://github.com/snc4377"
            headers["X-Title"] = "VaultSite translate-wiki"
        data = json.dumps(payload).encode("utf-8")

        for attempt in range(1, retries + 1):
            req = urllib.request.Request(self.url, data=data, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                self.calls += 1
                return body["choices"][0]["message"]["content"]
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", "replace")[:400]
                if exc.code in (429, 500, 502, 503, 504) and attempt < retries:
                    wait = 2**attempt
                    print(f"    retry {attempt}/{retries - 1} after HTTP {exc.code} in {wait}s", file=sys.stderr)
                    time.sleep(wait)
                    continue
                raise LLMError(f"HTTP {exc.code}: {detail}") from exc
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt < retries:
                    wait = 2**attempt
                    print(f"    retry {attempt}/{retries - 1} after network error in {wait}s", file=sys.stderr)
                    time.sleep(wait)
                    continue
                raise LLMError(f"network error: {exc}") from exc
        raise LLMError("exhausted retries")

    def translate_markdown(self, markdown: str, title: str) -> str:
        payload = {
            "model": self.model,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Note title: {title}\n\n{markdown}"},
            ],
        }
        return self._post(payload).strip()

    def translate_frontmatter(self, fields: dict[str, Any]) -> dict[str, Any]:
        schema = json.dumps(fields, ensure_ascii=False, indent=2)
        payload = {
            "model": self.model,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": FIELD_PROMPT % schema},
                {"role": "user", "content": "Translate these values now."},
            ],
        }
        raw = self._post(payload)
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMError(f"frontmatter translation was not JSON: {raw[:200]}") from exc
        if not isinstance(parsed, dict):
            raise LLMError("frontmatter translation was not a JSON object")
        return parsed


# --------------------------------------------------------------------------
# Pipeline
# --------------------------------------------------------------------------


@dataclass
class Job:
    src: Path
    rel: Path
    text: str
    sha: str
    verdict: LanguageVerdict
    front: dict[str, Any] | None = None
    body: str = ""
    error: str | None = None


@dataclass
class RunStats:
    translated: list[str] = field(default_factory=list)
    copied: list[str] = field(default_factory=list)
    refreshed: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)


def iter_markdown(root: Path) -> list[Path]:
    """All .md files, skipping hidden directories (Obsidian internals)."""
    files: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        parts = path.relative_to(root).parts
        if any(part.startswith(".") or part in EXCLUDE_DIRS for part in parts):
            continue
        if path.is_file():
            files.append(path)
    return files


FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})")
MAX_CHUNK = 9000


def split_fences(body: str) -> list[tuple[bool, str]]:
    """Split Markdown into [(is_code, text)] so fenced code is never translated."""
    segments: list[tuple[bool, str]] = []
    buffer: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0

    for line in body.splitlines(keepends=True):
        match = FENCE_RE.match(line)
        if not in_fence and match:
            if buffer:
                segments.append((False, "".join(buffer)))
                buffer = []
            in_fence = True
            fence_char = match.group(1)[0]
            fence_len = len(match.group(1))
            buffer.append(line)
        elif in_fence:
            buffer.append(line)
            if (
                match
                and match.group(1)[0] == fence_char
                and len(match.group(1)) >= fence_len
            ):
                segments.append((True, "".join(buffer)))
                buffer = []
                in_fence = False
        else:
            buffer.append(line)

    if buffer:
        segments.append((in_fence, "".join(buffer)))
    return segments


def chunk_text(text: str, limit: int = MAX_CHUNK) -> list[str]:
    """Group paragraphs under `limit`, hard-splitting oversized blocks."""
    chunks: list[str] = []
    current = ""
    for block in re.split(r"(\n\s*\n)", text):
        if len(current) + len(block) <= limit:
            current += block
            continue
        if current.strip():
            chunks.append(current)
        current = ""
        if len(block) <= limit:
            current = block
            continue
        for line in block.splitlines(keepends=True):
            if len(current) + len(line) > limit and current.strip():
                chunks.append(current)
                current = ""
            current += line
    if current.strip():
        chunks.append(current)
    return chunks or [text]


class ImageHandler:
    """Copy referenced vault images into public/wiki-images and rewrite links."""

    def __init__(
        self,
        src: Path,
        images_dir: Path,
        public_base: str = "",
        dry_run: bool = False,
    ) -> None:
        self.src = src
        self.images_dir = images_dir
        self.public_base = public_base.rstrip("/")
        self.dry_run = dry_run
        self.index = self._index_images()
        self.planned: dict[str, Path] = {}
        self.copied = 0
        self.skipped = 0
        self.rewritten = 0
        self.missing: set[str] = set()

    def _index_images(self) -> dict[str, list[Path]]:
        """Basename -> candidate files, shortest path first."""
        index: dict[str, list[Path]] = {}
        for path in self.src.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            rel = path.relative_to(self.src)
            if any(part.startswith(".") or part in EXCLUDE_DIRS for part in rel.parts):
                continue
            index.setdefault(path.name.casefold(), []).append(path)

        for candidates in index.values():
            candidates.sort(
                key=lambda path: (
                    len(path.relative_to(self.src).parts),
                    path.relative_to(self.src).as_posix(),
                )
            )
        return index

    def _closeness(self, candidate: Path, note_rel: Path) -> tuple[int, int, str]:
        """Prefer images in the note's folder or its nearest ancestor."""
        candidate_dir = candidate.relative_to(self.src).parts[:-1]
        note_dir = note_rel.parent.parts
        common = 0
        for left, right in zip(candidate_dir, note_dir):
            if left.casefold() != right.casefold():
                break
            common += 1
        return (-common, len(candidate_dir), candidate.relative_to(self.src).as_posix())

    def resolve(self, target: str, note_rel: Path) -> Path | None:
        """Find one referenced image in the source vault, or None."""
        target = unquote(target.strip()).replace("\\", "/")
        target = target.split("|", 1)[0].split("#", 1)[0].strip()
        if not target or target.startswith(
            ("http://", "https://", "//", "data:", "obsidian:")
        ):
            return None
        target = target.removeprefix("./")

        def inside(path: Path) -> Path | None:
            try:
                resolved = path.resolve()
            except OSError:
                return None
            return resolved if resolved.is_relative_to(self.src) else None

        root_candidate = inside(self.src / target)
        note_candidate = inside(self.src / note_rel.parent / target)
        exact = [path for path in (root_candidate, note_candidate) if path and path.is_file()]

        # An explicit path should win over a same-named file elsewhere.
        if "/" in target.strip("/") and exact:
            return exact[0]

        name = Path(target).name.casefold()
        pool = [path for path in self.index.get(name, []) if path.is_file()]
        pool.extend(exact)
        if not pool:
            return None
        pool.sort(key=lambda path: self._closeness(path, note_rel))
        return pool[0]

    @staticmethod
    def _same_file(left: Path, right: Path) -> bool:
        try:
            if left.stat().st_size != right.stat().st_size:
                return False
            return (
                hashlib.sha256(left.read_bytes()).hexdigest()
                == hashlib.sha256(right.read_bytes()).hexdigest()
            )
        except OSError:
            return False

    def _unique_name(self, source: Path) -> str:
        digest = hashlib.sha256(str(source).encode("utf-8")).hexdigest()[:8]
        stem = f"{source.stem}-{digest}"
        suffix = source.suffix.lower()
        counter = 0
        while True:
            name = f"{stem}{suffix}" if counter == 0 else f"{stem}-{counter}{suffix}"
            planned = self.planned.get(name)
            if planned is not None and planned != source:
                counter += 1
                continue
            dest = self.images_dir / name
            if dest.exists() and not self._same_file(dest, source):
                counter += 1
                continue
            return name

    def copy(self, source: Path) -> str:
        """Copy one image once; return its filename inside wiki-images."""
        name = source.name
        dest = self.images_dir / name

        if name in self.planned:
            if self.planned[name] == source:
                return name
            name = self._unique_name(source)
        elif dest.exists():
            if self._same_file(dest, source):
                self.planned[name] = source
                self.skipped += 1
                return name
            name = self._unique_name(source)

        dest = self.images_dir / name
        if dest.exists() and self._same_file(dest, source):
            self.planned[name] = source
            self.skipped += 1
            return name

        self.planned[name] = source
        if not self.dry_run:
            self.images_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
        self.copied += 1
        return name

    def _public_url(self, name: str) -> str:
        prefix = f"{self.public_base}/wiki-images" if self.public_base else "/wiki-images"
        return f"{prefix}/{quote(name)}"

    @staticmethod
    def _alt(alt: str, target: str) -> str:
        alt = alt.split("|", 1)[0].strip()
        if not alt:
            alt = Path(target).stem
        return alt.replace("[", "").replace("]", "")

    def _rewrite_text(self, text: str, note_rel: Path, warnings: list[str]) -> str:
        def standard(match: re.Match[str]) -> str:
            alt, inner = match.group(1), match.group(2).strip()
            if inner.startswith("<") and ">" in inner:
                target = inner[1 : inner.index(">")].strip()
            else:
                target = re.split(r"\s+[\"']", inner, maxsplit=1)[0].strip()
            if not target or target.startswith(
                ("http://", "https://", "//", "data:")
            ):
                return match.group(0)
            if "/wiki-images/" in target or target.startswith("wiki-images/"):
                return match.group(0)

            source = self.resolve(target, note_rel)
            if source is None:
                warnings.append(f"missing image '{target}' in {note_rel.as_posix()}")
                self.missing.add(target)
                return match.group(0)

            self.rewritten += 1
            name = self.copy(source)
            return f"![{self._alt(alt, target)}]({self._public_url(name)})"

        def obsidian(match: re.Match[str]) -> str:
            raw = match.group(1)
            target = raw.split("|", 1)[0].split("#", 1)[0].strip()
            if not target or target.startswith(
                ("http://", "https://", "//", "data:", "obsidian:")
            ):
                return match.group(0)
            if Path(target).suffix.lower() not in IMAGE_EXTENSIONS:
                return match.group(0)

            source = self.resolve(target, note_rel)
            if source is None:
                warnings.append(f"missing image '{target}' in {note_rel.as_posix()}")
                self.missing.add(target)
                return match.group(0)

            self.rewritten += 1
            name = self.copy(source)
            return f"![{self._alt('', target)}]({self._public_url(name)})"

        # Standard Markdown first, then Obsidian embeds: rewritten standard
        # images contain `](`, so the Obsidian regex cannot touch them.
        text = MARKDOWN_IMAGE_RE.sub(standard, text)
        return OBSIDIAN_IMAGE_RE.sub(obsidian, text)

    def _rewrite_body(self, body: str, note_rel: Path, warnings: list[str]) -> str:
        out: list[str] = []
        for is_code, segment in split_fences(body):
            out.append(
                segment if is_code else self._rewrite_text(segment, note_rel, warnings)
            )
        return "".join(out)

    def rewrite(self, text: str, note_rel: Path) -> tuple[str, list[str]]:
        """Rewrite image references in the body, leaving valid frontmatter alone."""
        warnings: list[str] = []
        match = FRONTMATTER_RE.match(text)
        if match:
            raw = match.group(1)
            try:
                data = yaml.safe_load(raw)
            except yaml.YAMLError:
                data = object()
            if isinstance(data, dict) or (data is None and not raw.strip()):
                body = text[match.end() :]
                return (
                    text[: match.end()] + self._rewrite_body(body, note_rel, warnings),
                    warnings,
                )

        # No frontmatter, or a leading `---` block that is really content.
        return self._rewrite_body(text, note_rel, warnings), warnings


def translate_body(client: DeepSeekClient, body: str, title: str) -> str:
    """Translate prose only; reassemble with code fences and spacing intact."""
    out: list[str] = []
    for is_code, segment in split_fences(body):
        if is_code:
            out.append(segment)
            continue
        lead = segment[: len(segment) - len(segment.lstrip())]
        trail = segment[len(segment.rstrip()) :]
        core = segment.strip()
        if not core:
            out.append(segment)
            continue
        translated = "\n\n".join(
            client.translate_markdown(chunk, title) for chunk in chunk_text(core)
        )
        out.append(lead + translated + trail)
    return "".join(out)


def translate_note(job: Job, client: DeepSeekClient) -> str:
    """Return the translated document text for one Spanish note.

    Only translated values are spliced into the original YAML: tags, dates,
    comments, ordering and quoting survive untouched. Filenames are never
    changed, so [[Wikilinks]] keep resolving inside the output vault.
    """
    try:
        front, raw, body = split_frontmatter(job.text)
    except ValueError as exc:
        raise LLMError(f"unparseable frontmatter: {exc}") from exc

    title = "Untitled"
    if front:
        title = str(front.get("title") or title)

    translated_body = translate_body(client, body, title) if body.strip() else ""

    if not front:
        return translated_body

    # Translate text fields only; tags/aliases/date are never sent to the LLM.
    fields = {k: v for k, v in front.items() if k in TRANSLATABLE_KEYS and isinstance(v, str)}
    if not fields:
        return f"---\n{raw}\n---\n{translated_body}"

    try:
        translated_fields = client.translate_frontmatter(fields)
    except LLMError as exc:
        print(f"    frontmatter translation failed ({exc}); translating title only", file=sys.stderr)
        fallback = client.translate_markdown(title, title).strip()
        translated_fields = {"title": fallback.splitlines()[0] if fallback else title}

    clean = {
        key: value
        for key, value in translated_fields.items()
        if key in TRANSLATABLE_KEYS and isinstance(value, str)
    }
    return f"---\n{render_frontmatter(raw, clean)}\n---\n{translated_body}"


def backup_if_present(target: Path, backup_root: Path, rel: Path) -> None:
    """Keep the previous output outside the published vault, path-preserving."""
    if target.exists():
        dest = backup_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, dest)


def load_manifest(manifest_path: Path) -> dict[str, dict[str, str]]:
    """Per-file cache: {"rel/path.md": {"status": ..., "sha256": ...}}."""
    if manifest_path.is_file():
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        # Ignore entries from the old, hash-less manifest format.
        return {k: v for k, v in data.items() if isinstance(v, dict)}
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Translate the Obsidian vault into English for Astro.")
    parser.add_argument("--src", type=Path, default=SRC, help=f"source vault (default {SRC})")
    parser.add_argument("--dst", type=Path, default=DST, help=f"output vault (default {DST})")
    parser.add_argument("--check", action="store_true", help="report languages only; no API calls, no writes")
    parser.add_argument("--dry-run", action="store_true", help="plan the run; no API calls, no writes")
    parser.add_argument("--force", action="store_true", help="retranslate and rewrite every note, ignoring the manifest")
    parser.add_argument("--only", metavar="GLOB", help="limit to relative paths matching this glob, e.g. 'git/*.md'")
    parser.add_argument(
        "--provider",
        choices=[*sorted(PROVIDERS), "auto"],
        default="auto",
        help="API provider; 'auto' picks whichever key is configured",
    )
    parser.add_argument("--model", help="override the provider's default model")
    parser.add_argument(
        "--prune",
        action="store_true",
        help="remove outputs whose source note no longer exists (managed files only)",
    )
    parser.add_argument(
        "--images-dir",
        type=Path,
        default=DEFAULT_IMAGES_DIR,
        help=f"public image directory (default {DEFAULT_IMAGES_DIR})",
    )
    parser.add_argument(
        "--public-base",
        default="",
        help="URL prefix for public images, e.g. /VaultSite (default: none)",
    )
    args = parser.parse_args()

    src: Path = args.src.resolve()
    dst: Path = args.dst.resolve()

    if not src.is_dir():
        die(f"source vault not found: {src}")
    if dst == src or src in dst.parents or dst in src.parents:
        die("source and output vaults must be separate, non-nested directories")

    files = iter_markdown(src)
    if args.only:
        files = [f for f in files if f.relative_to(src).match(args.only)]
    if not files:
        die(f"no .md files found under {src}")

    jobs: list[Job] = []
    for path in files:
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig", errors="replace")
        verdict = detect_language(text, path)
        jobs.append(
            Job(
                src=path,
                rel=path.relative_to(src),
                text=text,
                sha=hashlib.sha256(raw).hexdigest(),
                verdict=verdict,
            )
        )

    counts = {"es": 0, "en": 0, "unknown": 0}
    for job in jobs:
        counts[job.verdict.language] += 1

    print(f"source: {src}")
    print(f"output: {dst}")
    print(f"notes:  {len(jobs)}  ({counts['es']} es, {counts['en']} en, {counts['unknown']} unknown)\n")

    if args.check:
        for job in jobs:
            tag = {"es": "ES", "en": "EN", "unknown": "??"}[job.verdict.language]
            print(f"  [{tag}] {job.rel}  ({job.verdict.reason})")
        return 0

    images_dir: Path = args.images_dir.expanduser().resolve()
    public_base = args.public_base.rstrip("/")

    if args.dry_run:
        images = ImageHandler(src, images_dir, public_base=public_base, dry_run=True)
        print(
            f"images:  {images_dir}"
            f"{'' if images_dir.is_dir() else ' (will be created)'}\n"
        )
        manifest = {} if args.force else load_manifest(dst / MANIFEST_NAME)
        for job in jobs:
            target = dst / job.rel
            cached = manifest.get(str(job.rel)) or {}
            fresh = cached.get("sha256") == job.sha and target.exists()
            action = "unchanged" if fresh else {
                "es": "translate",
                "en": "copy",
                "unknown": "skip",
            }[job.verdict.language]
            print(f"  {action:<9} {job.rel}")
            image_warnings: list[str] = []
            if action in {"translate", "copy"}:
                _, image_warnings = images.rewrite(job.text, job.rel)
            elif action == "unchanged":
                existing = target.read_text(encoding="utf-8")
                refreshed, image_warnings = images.rewrite(existing, job.rel)
                if refreshed != existing:
                    print(f"  images    {job.rel}")
            for warning in image_warnings:
                print(f"    image: {warning}", file=sys.stderr)
        print(
            f"\nimages: {images.copied} to copy, {images.skipped} already present, "
            f"{len(images.missing)} missing"
        )
        print("dry run: no API calls, no files written")
        return 0

    provider = args.provider
    if provider == "auto":
        for candidate in ("deepseek", "openrouter"):
            if read_key(candidate):
                provider = candidate
                break
        else:
            die(
                "no API key found. Set DEEPSEEK_API_KEY or OPENROUTER_API_KEY "
                f"(or add it to {HERMES_ENVS[0]}), or run with --check/--dry-run."
            )

    manifest_path = dst / MANIFEST_NAME
    manifest = {} if args.force else load_manifest(manifest_path)

    # Backups live beside the published vault, never inside it: anything under
    # the glob base would be picked up as a wiki note.
    backup_root = dst.parent / f"{dst.name}-backups"

    for directory in (dst, backup_root):
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            die(
                f"cannot create {directory} — /opt is root-owned. Run:\n"
                f"  sudo mkdir -p {dst} {backup_root}\n"
                f"  sudo chown -R \"$(id -u):$(id -g)\" {dst} {backup_root}"
            )
        if not os.access(directory, os.W_OK):
            die(f"directory is not writable: {directory}")

    if images_dir == src or src in images_dir.parents or images_dir in src.parents:
        die("image directory must live outside the source vault")
    try:
        images_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        die(f"cannot create image directory: {images_dir}")
    if not os.access(images_dir, os.W_OK):
        die(f"image directory is not writable: {images_dir}")

    images = ImageHandler(src, images_dir, public_base=public_base, dry_run=False)
    print(f"images:  {images_dir}\n")

    client: DeepSeekClient | None = None
    needs_llm = any(j.verdict.language == "es" for j in jobs)
    if needs_llm:
        key = read_key(provider)
        if not key:
            die(f"no API key found for provider '{provider}'.")
        client = DeepSeekClient(provider, key, model=args.model)
        print(f"translating with {provider} ({client.model})\n")

    stats = RunStats()

    def refresh_existing(target_path: Path, rel: Path, key: str) -> bool:
        """Rewrite images in an already-translated output without an LLM call."""
        existing = target_path.read_text(encoding="utf-8")
        refreshed, image_warnings = images.rewrite(existing, rel)
        for warning in image_warnings:
            print(f"    image: {warning}", file=sys.stderr)
        if refreshed == existing:
            return False
        backup_if_present(target_path, backup_root, rel)
        target_path.write_text(refreshed, encoding="utf-8")
        stats.refreshed.append(key)
        print(f"  images    {key}")
        return True

    for job in jobs:
        target = dst / job.rel
        target.parent.mkdir(parents=True, exist_ok=True)
        key = str(job.rel)
        cached = manifest.get(key) or {}
        fresh = bool(cached.get("sha256") == job.sha and target.exists())

        try:
            if job.verdict.language == "en":
                if fresh and cached.get("status") == "copied":
                    if not refresh_existing(target, job.rel, key):
                        stats.unchanged.append(key)
                        print(f"  unchanged {key}")
                    continue
                backup_if_present(target, backup_root, job.rel)
                text, image_warnings = images.rewrite(job.text, job.rel)
                for warning in image_warnings:
                    print(f"    image: {warning}", file=sys.stderr)
                target.write_text(text, encoding="utf-8")
                manifest[key] = {"status": "copied", "sha256": job.sha}
                stats.copied.append(key)
                print(f"  copy      {key}")
                continue

            if job.verdict.language == "unknown":
                manifest[key] = {"status": "unknown", "sha256": job.sha}
                stats.unknown.append(key)
                print(f"  SKIP      {key}  ({job.verdict.reason})", file=sys.stderr)
                continue

            # Spanish: skip only when the source hash is unchanged.
            if fresh and cached.get("status") == "translated":
                if not refresh_existing(target, job.rel, key):
                    stats.unchanged.append(key)
                    print(f"  unchanged {key}")
                continue

            assert client is not None
            print(f"  translate {key}")
            translated = translate_note(job, client)
            translated, image_warnings = images.rewrite(translated, job.rel)
            for warning in image_warnings:
                print(f"    image: {warning}", file=sys.stderr)
            backup_if_present(target, backup_root, job.rel)
            target.write_text(translated, encoding="utf-8")
            manifest[key] = {
                "status": "translated",
                "sha256": job.sha,
                "model": client.model,
            }
            stats.translated.append(key)
        except LLMError as exc:
            job.error = str(exc)
            stats.failed.append(key)
            print(f"  FAILED    {key}: {exc}", file=sys.stderr)

    if args.prune:
        expected = {str(j.rel) for j in jobs}
        for stale_key in [k for k in manifest if k not in expected]:
            stale = dst / stale_key
            if stale.is_file():
                backup_if_present(stale, backup_root, Path(stale_key))
                stale.unlink()
                print(f"  prune     {stale_key}")
            del manifest[stale_key]

    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(
        f"\ndone: {len(stats.translated)} translated, {len(stats.copied)} copied, "
        f"{len(stats.refreshed)} image-refreshed, {len(stats.unchanged)} unchanged, "
        f"{len(stats.unknown)} unknown, {len(stats.failed)} failed"
    )
    print(
        f"images: {images.copied} copied, {images.skipped} already present, "
        f"{len(images.missing)} missing"
    )
    if client:
        print(f"LLM calls: {client.calls}")
    if stats.failed:
        print("failed notes:", ", ".join(stats.failed), file=sys.stderr)
        return 1
    if stats.unknown:
        print(
            "unknown-language notes were not published — add a language hint or "
            "translate them by hand: " + ", ".join(stats.unknown),
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
