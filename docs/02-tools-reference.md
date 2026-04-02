# Tools Reference

Vaultbridge exposes 5 tools to Claude. Once registered, you call them naturally through conversation — no special syntax needed.

---

## obsidian_list

List all notes inside a vault, or list all available vaults.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `vault_name` | string | No | `.` | Vault folder name. Leave blank to list all vaults. |

**Examples**
```
"List all my Obsidian vaults"
"List all notes in my Resume Builder vault"
```

---

## obsidian_read

Read the full content of a note, or extract a specific section by heading.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `vault_name` | string | Yes | Vault folder name |
| `note` | string | Yes | Note name with or without `.md`, supports subfolders e.g. `folder/note` |
| `section` | string | No | Heading to extract e.g. `## Skills` — returns only that section |

**Examples**
```
"Read the skills note from my Resume Builder vault"
"Read only the ## Work Experience section from my experience note"
```

---

## obsidian_write

Write content to a note. Creates the note and any missing parent folders automatically.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `vault_name` | string | Yes | — | Vault folder name |
| `note` | string | Yes | — | Note name, supports subfolders |
| `content` | string | Yes | — | Markdown content to write |
| `mode` | string | No | `overwrite` | `overwrite` \| `append` \| `prepend` \| `section` |
| `section` | string | No* | — | Required when `mode=section` — heading to update e.g. `## Skills` |

**Modes**

| Mode | What it does |
|---|---|
| `overwrite` | Replaces the entire note (default) |
| `append` | Adds content to the bottom |
| `prepend` | Adds content to the top |
| `section` | Replaces only the content under a specific heading, leaving the rest untouched |

**Examples**
```
"Update my profile note in Resume Builder with this new objective: ..."
"Append this new cert to my certifications note: ..."
"Update only the ## KPMG section in my experience note with: ..."
```

---

## obsidian_search

Full-text search across all notes in a vault.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `vault_name` | string | Yes | — | Vault folder name |
| `query` | string | Yes | — | Search term or phrase |
| `case_sensitive` | boolean | No | `false` | Exact case match |

**Examples**
```
"Search for 'Burp Suite' in my Resume Builder vault"
"Search for 'KPMG' in my Resume Builder vault"
```

---

## obsidian_delete

Delete a note from a vault. Requires explicit confirmation to prevent accidental deletion.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `vault_name` | string | Yes | — | Vault folder name |
| `note` | string | Yes | — | Note name to delete |
| `confirm` | boolean | No | `false` | Must be `true` to actually delete |

- Without `confirm=true` — **dry-run preview** only, nothing is changed
- With `confirm=true` — permanently deletes the note

**Examples**
```
"Delete the old-draft note from my Resume Builder vault"
→ dry-run: shows what would be deleted

"Delete old-draft from Resume Builder, confirm=true"
→ permanently deletes the note
```

> ⚠️ Deletion is permanent. Enable Obsidian's File Recovery plugin as a safety net.
