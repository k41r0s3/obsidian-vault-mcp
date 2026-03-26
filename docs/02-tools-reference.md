# Tools Reference

Vaultbridge exposes 4 tools to Claude. Once registered, you call them naturally through conversation — no special syntax needed.

---

## obsidian_list

List all notes inside a vault, or list all available vaults.

**Parameters**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `vault_name` | string | No | `.` | Vault folder name. Leave blank or use `.` to list all vaults. |

**Examples**

```
"List all my Obsidian vaults"
→ lists every vault folder under OBSIDIAN_BASE

"List all notes in my Resume Builder vault"
→ returns a tree of all .md files in the vault
```

---

## obsidian_read

Read the full content of a note.

**Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `vault_name` | string | Yes | Vault folder name, e.g. `Resume Builder` |
| `note` | string | Yes | Note name with or without `.md`, e.g. `profile` or `subfolder/note` |

**Examples**

```
"Read the skills note from my Resume Builder vault"
→ returns full markdown content of skills.md

"Read subfolder/note from my vault"
→ supports nested notes inside subfolders
```

---

## obsidian_write

Write content to a note. Creates the note and any missing parent folders automatically.

**Parameters**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `vault_name` | string | Yes | — | Vault folder name |
| `note` | string | Yes | — | Note name, e.g. `profile` or `subfolder/note` |
| `content` | string | Yes | — | Markdown content to write |
| `mode` | string | No | `overwrite` | `overwrite` \| `append` \| `prepend` |

**Modes**

- `overwrite` — replaces the entire note content (default)
- `append` — adds content to the bottom of the note
- `prepend` — adds content to the top of the note

**Examples**

```
"Update my profile note in Resume Builder with this new objective: ..."
→ overwrites profile.md with new content

"Append this new project to my projects note in Resume Builder: ..."
→ adds to the bottom of projects.md without touching existing content

"Add this to the top of my certifications note: ..."
→ prepends to certifications.md
```

---

## obsidian_search

Full-text search across all notes in a vault. Returns matching files with line numbers and context snippets.

**Parameters**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `vault_name` | string | Yes | — | Vault folder name to search in |
| `query` | string | Yes | — | Search term or phrase |
| `case_sensitive` | boolean | No | `false` | Whether to match case exactly |

**Examples**

```
"Search for 'Burp Suite' in my Resume Builder vault"
→ returns every note and line that mentions Burp Suite

"Search for 'KPMG' in my Resume Builder vault"
→ useful for finding where a specific experience is referenced
```
