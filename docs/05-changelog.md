# Changelog

## [1.1.0] — 2026-03-27

### Security
- **Path traversal protection** — all vault and note paths resolved and validated to stay inside `OBSIDIAN_BASE`. Attempts using `../` or absolute paths are blocked
- **Filesystem path redaction** — tool responses no longer expose full system paths. Only relative paths shown. Controlled via `VAULTBRIDGE_REDACT_PATHS` env var
- **Hidden folder exclusion** — `.obsidian/` and other dotfolders skipped in list and search operations

### Added
- **Audit logging** — every read, write, search, list, and delete logged with timestamp to `~/.vaultbridge.log`. Path configurable via `VAULTBRIDGE_LOG`
- **Read-only mode** — set `VAULTBRIDGE_READONLY=1` to disable all writes and deletes globally
- **`obsidian_delete`** — delete a note with mandatory `confirm=true` flag. Without it, returns dry-run preview only
- **Section-level read** — `obsidian_read` now accepts optional `section` parameter to extract only a specific heading's content
- **Section-level write** — `obsidian_write` now supports `mode=section` to update a specific heading without touching the rest of the note

### Changed
- `obsidian_list` no longer exposes full filesystem base path in output
- `obsidian_read` response header now shows relative path only

---

## [1.0.0] — 2026-03-27

### Added
- `obsidian_list` — list all notes in a vault or list all vaults
- `obsidian_read` — read full note content
- `obsidian_write` — write/append/prepend to notes, auto-creates missing folders
- `obsidian_search` — full-text search with line numbers and context
- Isolated Python venv setup
- Configurable via `OBSIDIAN_BASE` environment variable
- Auto-discovered vaults — no config changes needed for new vaults
- Full documentation in `docs/`

---

<!-- Template for future releases:
## [x.y.z] — YYYY-MM-DD

### Security
-

### Added
-

### Changed
-

### Fixed
-

### Removed
-
-->
