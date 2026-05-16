◰ Filebase docs

Getting started

Quickstart
Concepts
Authentication

Sync engine

Block-level deltas
Conflict resolution
Resumable uploads

CLI

Install
Configuration
Subcommands

Docs › Getting started › Quickstart

# Quickstart

Sync your first folder in under five minutes. The CLI is the fastest path; the desktop app and the API client all wrap the same engine.

## 1. Install the CLI

The CLI is distributed as a single binary for macOS, Linux, and Windows.

```
# macOS · Homebrew
brew install filebase

# Linux · curl
curl -fsSL https://get.filebase.dev | sh
```

Verify the install:

```
filebase --version
# filebase 0.6.4
```

## 2. Authenticate

Sign in with your Filebase account. The token is stored in `~/.config/filebase/credentials`.

```
filebase auth login
# → opens your browser
# ✓ Logged in as you@example.com
```

Note

On servers without a browser, use `filebase auth login --device` for a device-code flow.

## 3. Sync a folder

Pick a local directory and link it to a remote root. Filebase watches it for changes and pushes block-level diffs in the background.

```
cd ~/projects
filebase init my-team
filebase sync
```

### Excluding files

Add a `.filebaseignore` at the root of the synced folder. Same syntax as `.gitignore`:

```
node_modules/
*.log
build/
```

## 4. Where to go next

Read Conflict resolution to understand how Filebase merges concurrent edits, or skip to the CLI reference for the full subcommand list.

← PreviousConcepts
Next →Conflict resolution

On this page

[1. Install the CLI](#install)
[2. Authenticate](#auth)
[3. Sync a folder](#sync)
[4. Where to go next](#next)