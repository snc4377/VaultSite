import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

/**
 * Posts are written by n8n straight into src/content/blog/ as Markdown.
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

export const collections = { blog };
