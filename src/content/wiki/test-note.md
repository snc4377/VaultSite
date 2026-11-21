---
title: "Test note: aliases that earn their keep"
date: 2026-11-20
tags: ["basics", "shell"]
---

Placeholder note used to check the wiki layout, spacing and code rendering.
Replace it with a real entry — it exists so the collection has something to
render end to end.

## Why aliases

Short commands are not about saving keystrokes. They are about making the safe
option the fastest one, so you stop skipping the verbose flag that would have
told you what went wrong.

- `ll` — long listing, newest first
- `gst` — branch and status without the ceremony
- `..` — up one directory, because typing `cd ..` gets old

## A snippet

```bash
alias ll='ls -alFh --group-directories-first'
alias gst='git status --short --branch'
alias ..='cd ..'
```

> note: keep aliases in a versioned dotfile, not in your shell history — the
> whole point is that a rebuild takes minutes.
