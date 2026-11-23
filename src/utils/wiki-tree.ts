import type { CollectionEntry } from "astro:content";
import { noteTitle } from "./note";

export type WikiNote = CollectionEntry<"wiki">;

export interface WikiFolder {
  name: string;
  folders: WikiFolder[];
  notes: WikiNote[];
  /** Number of notes in this folder and all descendants. */
  noteCount: number;
  /** Ids of every note in this subtree, used to open the active path. */
  noteIds: Set<string>;
}

export const UNCATEGORIZED = "Uncategorized";

const collator = (a: string, b: string) =>
  a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" });

/** Trimmed frontmatter path; empty or missing becomes the Uncategorized root. */
export function categoryPath(note: WikiNote): string[] {
  const parts = (note.data.category ?? [])
    .map((part) => part.trim())
    .filter(Boolean);
  return parts.length > 0 ? parts : [UNCATEGORIZED];
}

/**
 * Turn the flat collection into a folder tree ordered like a file explorer:
 * folders first, then notes, both case-insensitively alphabetical.
 */
export function buildWikiTree(notes: WikiNote[]): WikiFolder {
  const root: WikiFolder = {
    name: "",
    folders: [],
    notes: [],
    noteCount: 0,
    noteIds: new Set(),
  };

  for (const note of notes) {
    let folder = root;
    for (const name of categoryPath(note)) {
      const key = name.toLowerCase();
      let child = folder.folders.find(
        (candidate) => candidate.name.toLowerCase() === key,
      );
      if (!child) {
        child = {
          name,
          folders: [],
          notes: [],
          noteCount: 0,
          noteIds: new Set(),
        };
        folder.folders.push(child);
      }
      folder = child;
    }
    folder.notes.push(note);
    folder.noteIds.add(note.id);
  }

  const finalize = (folder: WikiFolder): number => {
    folder.folders.sort((a, b) => collator(a.name, b.name));
    folder.notes.sort((a, b) => collator(noteTitle(a), noteTitle(b)));

    let total = folder.notes.length;
    for (const child of folder.folders) {
      total += finalize(child);
      for (const id of child.noteIds) folder.noteIds.add(id);
    }
    folder.noteCount = total;
    return total;
  };

  finalize(root);
  return root;
}
