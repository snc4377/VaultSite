#!/usr/bin/env node
/**
 * n8n writes posts as `post-YYYY-MM-DD-HHMM. md` — a space before the
 * extension. No glob loader matches that, and the post is silently dropped
 * from the build. Normalise the names before every build so a malformed
 * filename can never hide a post again.
 *
 * Fix the n8n filename template if you can; this is the safety net.
 */
import { readdir, rename } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const dir = fileURLToPath(new URL("../src/content/blog/", import.meta.url));

let renamed = 0;
let entries = [];

try {
  entries = await readdir(dir);
} catch {
  console.log("normalize-content: no src/content/blog directory yet");
  process.exit(0);
}

for (const name of entries) {
  // "slug. md" or "slug .md"
  const match = name.match(/^(.*?)\.\s+md$/i) ?? name.match(/^(.*?)\s+\.md$/i);
  if (!match) continue;

  const target = `${match[1]}.md`;
  if (target === name) continue;

  await rename(join(dir, name), join(dir, target));
  console.log(`normalize-content: ${JSON.stringify(name)} -> ${JSON.stringify(target)}`);
  renamed += 1;
}

if (renamed === 0) console.log("normalize-content: no malformed filenames");
