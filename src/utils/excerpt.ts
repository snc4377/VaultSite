/**
 * Plain-text preview of a Markdown note body.
 *
 * Vault notes are working documents: full of headings, image embeds, code
 * fences, callouts and bullet lists. A card excerpt has to read like prose, so
 * non-prose constructs are dropped, list items are joined with " · " (instead
 * of running together), and the first ~25 words are kept.
 */
export function excerpt(body: string | undefined, max = 150): string {
  if (!body) return "";

  const blocks = body
    .replace(/```[\s\S]*?```/g, "\n\n")
    .replace(/~~~[\s\S]*?~~~/g, "\n\n")
    .replace(/!\[\[[^\]]*\]\]/g, "")
    .replace(/!\[[^\]]*\]\([^)]*\)/g, "")
    .replace(/^\s{0,3}#{1,6}\s+.*$/gm, "")
    .replace(/^\s{0,3}>\s?\[![^\]]*\][+-]?.*$/gm, "")
    .split(/\n\s*\n/)
    .map((block) =>
      block
        .split("\n")
        .map((line) =>
          toPlainText(
            line
              .trim()
              .replace(/^>\s?/, "")
              .replace(/^(?:[-*+]\s*|\d+\.\s+)/, ""),
          ),
        )
        .filter(Boolean)
        .join(" · "),
    )
    .filter(Boolean);

  let out = "";
  for (const block of blocks) {
    if (!out) {
      out = block;
      continue;
    }
    // Stop once the excerpt is long enough; a very short first block still
    // gets one neighbour for context.
    if (out.length >= max * 0.6) break;
    out += ` ${block}`;
  }

  if (out.length <= max) return out;

  // Cut on a word boundary so the excerpt never ends mid-token.
  return `${out.slice(0, max).replace(/\s+\S*$/, "")}…`;
}

/** Strip inline Markdown from one paragraph-sized string. */
function toPlainText(value: string): string {
  return value
    .replace(/`([^`]*)`/g, "$1")
    .replace(/\[\[([^|\]]*\|)?([^\]]*)\]\]/g, "$2")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/<\/?[^>]+>/g, " ")
    .replace(/[*_~]{1,3}/g, "")
    .replace(/\s+/g, " ")
    .replace(/^[·\s]+|[·\s]+$/g, "")
    .trim();
}
