/** Structural shape shared by every vault-backed collection. */
export type NoteLike = {
  id: string;
  filePath?: string;
  data: { title?: string };
};

type DatedNote = NoteLike & { data: { date?: Date } };

/**
 * Prefer the frontmatter title. Hand-written vault notes often have none, so
 * fall back to the original filename (preserving its casing), then to the
 * entry id ("la-biblia" -> "La Biblia") if no file path is available.
 */
export function noteTitle(note: NoteLike): string {
  const title = note.data.title?.trim();
  if (title) return title;

  const filename = note.filePath?.split("/").pop();
  if (filename) {
    const stem = filename.replace(/\.(md|mdx)$/i, "").trim();
    if (stem) return stem;
  }

  const segment = note.id.split("/").filter(Boolean).pop() ?? note.id;
  return titleCase(segment.replace(/-+/g, " ")) || note.id;
}

const SMALL_WORDS = new Set([
  "a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on",
  "or", "the", "to", "via", "vs",
]);

function titleCase(value: string): string {
  return value
    .split(/\s+/)
    .filter(Boolean)
    .map((word, index) =>
      index > 0 && SMALL_WORDS.has(word.toLowerCase())
        ? word.toLowerCase()
        : word.charAt(0).toUpperCase() + word.slice(1),
    )
    .join(" ");
}

/** `YYYY-MM-DD` for `<time datetime>`, or null when the note is undated. */
export function noteDate(note: DatedNote): string | null {
  return note.data.date ? note.data.date.toISOString().slice(0, 10) : null;
}

/** Newest first; undated notes last, alphabetically, so order stays stable. */
export function sortNotes<T extends DatedNote>(notes: T[]): T[] {
  return [...notes].sort((a, b) => {
    const aDate = a.data.date?.valueOf();
    const bDate = b.data.date?.valueOf();
    if (aDate !== undefined && bDate !== undefined) return bDate - aDate;
    if (aDate !== undefined) return -1;
    if (bDate !== undefined) return 1;
    return noteTitle(a).localeCompare(noteTitle(b));
  });
}
