import type { CollectionEntry } from "astro:content";
import { noteTitle } from "./note";

export type WikiNote = CollectionEntry<"wiki">;

export interface WikiNoteLeaf {
  id: string;
  label: string;
  note: WikiNote;
}

export interface WikiFolder {
  name: string;
  folders: WikiFolder[];
  notes: WikiNoteLeaf[];
  /** Number of notes in this folder and all descendants. */
  noteCount: number;
  /** Ids of every note in this subtree, used to open the active path. */
  noteIds: Set<string>;
}

export const UNCATEGORIZED = "Uncategorized";

const collator = (a: string, b: string) =>
  a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" });

const categoryParts = (note: WikiNote): string[] =>
  (note.data.category ?? []).map((part) => part.trim()).filter(Boolean);

/**
 * Folders are every category element except the last one. The final element
 * is the note itself, so it must not become another folder.
 *
 * Missing/empty category -> the "Uncategorized" root folder.
 */
export function folderPath(note: WikiNote): string[] {
  const parts = categoryParts(note);
  return parts.length > 0 ? parts.slice(0, -1) : [UNCATEGORIZED];
}

/** The note's label inside the tree: final category element, or its title. */
export function noteLabel(note: WikiNote): string {
  const parts = categoryParts(note);
  return parts.length > 0 ? parts[parts.length - 1] : noteTitle(note);
}

/**
 * Build the folder tree:
 *   S4VITAR -> fases -> Buffer Overflow -> [note leaf]
 *
 * Folders and notes are sorted case-insensitively, folders first.
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
    for (const name of folderPath(note)) {
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

    folder.notes.push({ id: note.id, label: noteLabel(note), note });
    folder.noteIds.add(note.id);
  }

  const finalize = (folder: WikiFolder): number => {
    folder.folders.sort((a, b) => collator(a.name, b.name));
    folder.notes.sort((a, b) => collator(a.label, b.label));

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
