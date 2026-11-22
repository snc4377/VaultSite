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
 * Wiki notes are hand-written (or later automated) Markdown. `date` is used
 * rather than `pubDate` so both collections share one frontmatter contract.
 *
 * Source is the English output of scripts/translate-wiki.py, mirrored into
 * src/content/wiki by scripts/sync-wiki.mjs. The repo snapshot is what CI
 * builds — GitHub Actions has no /opt volume. Refresh it with `npm run
 * sync:wiki` after translating the vault; prebuild/predev do it automatically
 * when /opt/obsidian-vault-en exists.
 */
const wiki = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/wiki" }),
  schema: z.object({
    // Vault notes often ship with no frontmatter at all; the glob loader
    // rejects an entry whose required fields are missing, so both `title`
    // and `date` are optional. Pages derive a title from the entry id.
    title: z.string().optional(),
    date: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    description: z.string().optional(),
  }),
});

export const collections = { blog, wiki };
