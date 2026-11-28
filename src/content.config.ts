import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

/**
 * Blog posts are written by n8n straight into src/content/blog/ as Markdown.
 * Keep this schema in sync with the frontmatter that workflow emits:
 *   title: string
 *   date:  YYYY-MM-DD
 *   tags:  string[]
 */
const blog = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    description: z.string().optional(),
  }),
});

/**
 * One frontmatter contract for every vault-backed collection — the translate
 * pipeline writes the same shape into both output vaults.
 *
 * Vault notes often ship with no frontmatter at all; the glob loader rejects an
 * entry whose required fields are missing, so both `title` and `date` are
 * optional. Pages derive a title from the entry id.
 */
const noteSchema = z.object({
  title: z.string().optional(),
  date: z.coerce.date().optional(),
  // Ordered category path, e.g. ["Recopilación", "Activa", "Nmap"].
  // Missing or empty falls back to the "Uncategorized" root in the sidebar.
  category: z.array(z.string()).default([]),
  tags: z.array(z.string()).default([]),
  description: z.string().optional(),
});

/**
 * Wiki notes are hand-written (or later automated) Markdown. `date` is used
 * rather than `pubDate` so every collection shares one frontmatter contract.
 *
 * Source is the English output of scripts/translate-wiki.py, mirrored into
 * src/content/wiki by scripts/sync-wiki.mjs. The repo snapshot is what CI
 * builds — GitHub Actions has no /opt volume. Refresh it with `npm run
 * sync:wiki` after translating the vault; prebuild/predev do it automatically
 * when /opt/obsidian-vault-en exists.
 */
const wiki = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/wiki" }),
  schema: noteSchema,
});

/**
 * Portfolio = HTB machine write-ups. translate-wiki.py routes every note whose
 * vault path runs through `HTB/Machines/` to /opt/obsidian-portfolio-en (with
 * that prefix stripped), and sync-wiki.mjs mirrors that output into
 * src/content/portfolio. Keeping the glob base on the committed snapshot is
 * deliberate: CI has no /opt, and a collection pointing at a missing directory
 * builds green with zero entries — an empty portfolio on the deployed site.
 */
const portfolio = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/portfolio" }),
  schema: noteSchema,
});

export const collections = { blog, wiki, portfolio };
