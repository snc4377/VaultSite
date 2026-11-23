#!/usr/bin/env node
/**
 * Mirror the translated Obsidian vault into src/content/wiki.
 *
 * Why: GitHub Actions runs on a clean runner without /opt/obsidian-vault-en.
 * The repo therefore carries a snapshot of the translated notes. This script
 * refreshes that snapshot from the live vault when it is present (local), and
 * is a no-op when it is not (GitHub-hosted runners), so CI builds what was
 * committed.
 *
 * Sanitization: some Obsidian notes start with blank lines and a `---`
 * horizontal rule. Astro parses that as YAML frontmatter and fails the build.
 * Any leading `---` block that is not a YAML mapping is demoted to a Markdown
 * rule (`***`) while copying. The source vault is never modified.
 *
 * Attachments: Obsidian writes vault-root-relative image paths, but Astro
 * resolves Markdown images relative to the note. Referenced local images are
 * copied out of WIKI_ASSETS (the source vault) and their URLs rewritten to be
 * note-relative. Missing images are reported, not silently dropped.
 *
 * Usage:
 *   npm run sync:wiki
 *   WIKI_SRC=/path/to/vault WIKI_ASSETS=/path/to/source npm run sync:wiki
 */
import {
  copyFile,
  mkdir,
  readdir,
  readFile,
  rm,
  stat,
  writeFile,
} from "node:fs/promises";
import { dirname, join, posix, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { parse } from "yaml";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const SRC = process.env.WIKI_SRC ?? "/opt/obsidian-vault-en";
const ASSET_SRC = process.env.WIKI_ASSETS ?? "/opt/obsidian-vault";
const DEST = join(ROOT, "src/content/wiki");

const LEADING_FRONTMATTER = /^(\s*)---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?=\r?\n|$)/;
const IMAGE = /!\[([^\]]*)\]\(\s*(?:<([^>]+)>|([^)\s]+))\s*\)/g;
const REMOTE = /^(?:[a-z][a-z0-9+.-]*:|#)/i;

const toPosix = (path) => path.split(sep).join("/");
const isMarkdown = (name) => name.toLowerCase().endsWith(".md");

function sanitize(text) {
  const match = LEADING_FRONTMATTER.exec(text);
  if (!match) return { text, changed: false };

  const [, leading, body] = match;
  let data;
  try {
    data = parse(body);
  } catch {
    data = undefined;
  }

  const isMapping =
    data !== null && typeof data === "object" && !Array.isArray(data);
  const isEmpty = data === null && body.trim() === "";
  if (isMapping || isEmpty) return { text, changed: false };

  // Not frontmatter: turn the opening delimiter into a Markdown rule.
  const at = match.index + leading.length;
  return {
    text: `${text.slice(0, at)}***${text.slice(at + 3)}`,
    changed: true,
  };
}

async function isFile(path) {
  try {
    return (await stat(path)).isFile();
  } catch {
    return false;
  }
}

async function isDir(path) {
  try {
    return (await stat(path)).isDirectory();
  } catch {
    return false;
  }
}

function safeAssetPath(path) {
  const normalized = posix.normalize(path);
  if (
    normalized === "." ||
    normalized === ".." ||
    normalized.startsWith("../") ||
    posix.isAbsolute(normalized)
  ) {
    return null;
  }
  return normalized;
}

function encodePath(path) {
  return path.split("/").map((part) => encodeURIComponent(part)).join("/");
}

async function walk(dir, filter = () => true) {
  const out = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    if (entry.name.startsWith(".")) continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...(await walk(full, filter)));
    else if (entry.isFile() && filter(entry.name)) out.push(full);
  }
  return out;
}

async function rewriteImages(text, noteRel, expected, stats, hasAssets) {
  if (!hasAssets) return text;

  const noteDir = posix.dirname(noteRel) === "." ? "" : posix.dirname(noteRel);
  let out = "";
  let last = 0;

  for (const match of text.matchAll(IMAGE)) {
    const [full, alt, angled, plain] = match;
    out += text.slice(last, match.index);
    last = match.index + full.length;

    const raw = (angled ?? plain ?? "").trim();
    if (
      !raw ||
      REMOTE.test(raw) ||
      raw.includes("/wiki-images/") ||
      raw.startsWith("wiki-images/")
    ) {
      out += full;
      continue;
    }

    let decoded;
    try {
      decoded = decodeURIComponent(raw);
    } catch {
      decoded = raw;
    }
    decoded = decoded.replace(/^\.\//, "");

    // Obsidian usually writes paths from the vault root; fall back to
    // note-relative for notes that already use portable paths.
    const rootRel = safeAssetPath(decoded);
    const noteRelAsset = safeAssetPath(posix.join(noteDir, decoded));
    const fromRoot = rootRel && join(ASSET_SRC, rootRel);
    const fromNote = noteRelAsset && join(ASSET_SRC, noteRelAsset);

    let source;
    let assetRel;
    let replacement = full;
    if (fromRoot && (await isFile(fromRoot))) {
      source = fromRoot;
      assetRel = rootRel;
      const relativeUrl =
        posix.relative(noteDir, rootRel) || posix.basename(rootRel);
      replacement = `![${alt}](<${encodePath(relativeUrl)}>)`;
    } else if (fromNote && (await isFile(fromNote))) {
      source = fromNote;
      assetRel = noteRelAsset;
    } else {
      stats.missing.add(raw);
      out += full;
      continue;
    }

    const target = join(DEST, ...assetRel.split("/"));
    await mkdir(dirname(target), { recursive: true });
    await copyFile(source, target);
    expected.add(target);
    stats.assets.add(target);
    out += replacement;
  }

  return out + text.slice(last);
}

async function main() {
  if (!(await isDir(SRC))) {
    console.log(`sync-wiki: ${SRC} not found — keeping the committed snapshot`);
    return;
  }

  const files = (await walk(SRC, isMarkdown)).sort();
  if (files.length === 0) {
    console.error(`sync-wiki: no .md files under ${SRC} — snapshot left untouched`);
    process.exitCode = 1;
    return;
  }

  const hasAssets = await isDir(ASSET_SRC);
  if (!hasAssets) {
    console.warn(`sync-wiki: ${ASSET_SRC} not found — keeping existing assets`);
  }

  const expected = new Set();
  const stats = { sanitized: 0, assets: new Set(), missing: new Set() };

  for (const file of files) {
    const noteRel = toPosix(relative(SRC, file));
    const target = join(DEST, ...noteRel.split("/"));
    expected.add(target);

    let { text, changed } = sanitize(await readFile(file, "utf8"));
    if (changed) stats.sanitized += 1;
    text = await rewriteImages(text, noteRel, expected, stats, hasAssets);

    await mkdir(dirname(target), { recursive: true });
    await writeFile(target, text, "utf8");
  }

  // Prune only after every copy succeeded, so a failed run cannot empty the snapshot.
  let removed = 0;
  for (const file of await walk(DEST).catch(() => [])) {
    if (expected.has(file)) continue;
    if (!hasAssets && !isMarkdown(file)) continue;
    await rm(file, { force: true });
    removed += 1;
  }

  console.log(
    `sync-wiki: ${files.length} notes mirrored to src/content/wiki` +
      (stats.sanitized
        ? ` (${stats.sanitized} malformed leading blocks sanitized)`
        : "") +
      (stats.assets.size ? `, ${stats.assets.size} assets copied` : "") +
      (removed ? `, ${removed} stale files removed` : ""),
  );

  if (stats.missing.size) {
    console.warn(
      `sync-wiki: ${stats.missing.size} referenced image(s) not found:`,
    );
    for (const ref of [...stats.missing].slice(0, 10)) {
      console.warn(`  ${ref}`);
    }
  }
}

await main();
