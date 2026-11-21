---
title: "Environment setup"
date: 2026-11-18
tags: ["basics", "linux"]
description: "The shell, the package list and the aliases every rebuild starts with."
---

Every machine I rebuild starts here: a shell that behaves, a package list I can
replay, and notes short enough to actually read.

## Shell

zsh with a minimal prompt, tmux for anything long-running, and `fzf` bound to
history search. Nothing that needs a plugin manager to survive an update.

```bash
# default shell + the essentials
sudo apt install -y zsh tmux fzf ripgrep
chsh -s "$(which zsh)"
exec zsh
```

## Packages

Installed from a single list so a rebuild takes minutes, not an evening. The
list lives in the repo; this page only explains why each entry is there.

> note: keep the package list in version control — a wiki you cannot replay is
> just a diary.
