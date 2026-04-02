#!/usr/bin/env python3
"""
vaultbridge
A lightweight MCP server that bridges Claude and Obsidian.
Gives Claude full read/write/search/list access to any Obsidian vault.
Claude Desktop auto-starts this via stdio — no manual server startup needed.
"""

import os
import re
import logging
from pathlib import Path
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ── Configuration ─────────────────────────────────────────────────────────────
VAULTS_BASE   = Path(os.environ.get("OBSIDIAN_BASE", "/home/user/Obsidian")).resolve()
LOG_FILE      = Path(os.environ.get("VAULTBRIDGE_LOG", str(Path.home() / ".vaultbridge.log")))
READ_ONLY     = os.environ.get("VAULTBRIDGE_READONLY", "").lower() in ("1", "true", "yes")
REDACT_PATHS  = os.environ.get("VAULTBRIDGE_REDACT_PATHS", "1").lower() not in ("0", "false", "no")

# ── Audit Logging ─────────────────────────────────────────────────────────────
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def audit(action: str, vault: str, note: str = "", extra: str = ""):
    msg = f"action={action} vault={vault}"
    if note:
        msg += f" note={note}"
    if extra:
        msg += f" {extra}"
    logging.info(msg)


# ── Path Safety ───────────────────────────────────────────────────────────────
def safe_display(path: Path) -> str:
    """Return a redacted display path if REDACT_PATHS is enabled."""
    try:
        rel = path.relative_to(VAULTS_BASE)
        return str(rel)
    except ValueError:
        return "<redacted>"


def resolve_vault(vault_name: str) -> Path:
    """Resolve vault name, guarding against path traversal."""
    vault_name = vault_name.strip().lstrip("/")
    resolved   = (VAULTS_BASE / vault_name).resolve()

    if not str(resolved).startswith(str(VAULTS_BASE)):
        raise PermissionError("Access denied: path traversal detected.")

    if not resolved.exists():
        raise FileNotFoundError(f"Vault '{vault_name}' not found.")

    return resolved


def resolve_note(vault_path: Path, note: str) -> Path:
    """Resolve note path, guarding against path traversal."""
    note = note.strip().lstrip("/")
    if not note.endswith(".md"):
        note += ".md"

    resolved = (vault_path / note).resolve()

    if not str(resolved).startswith(str(vault_path.resolve())):
        raise PermissionError("Access denied: path traversal detected.")

    return resolved


# ── Helpers ───────────────────────────────────────────────────────────────────
def list_vault_tree(vault_path: Path) -> dict:
    tree = {}
    for md_file in sorted(vault_path.rglob("*.md")):
        if any(part.startswith(".") for part in md_file.parts):
            continue
        rel   = md_file.relative_to(vault_path)
        parts = list(rel.parts)
        node  = tree
        for part in parts[:-1]:
            node = node.setdefault(part + "/", {})
        node[parts[-1]] = str(rel)
    return tree


def tree_to_string(tree: dict, indent: int = 0) -> str:
    lines = []
    for key, val in tree.items():
        prefix = "  " * indent
        if isinstance(val, dict):
            lines.append(f"{prefix}📁 {key}")
            lines.append(tree_to_string(val, indent + 1))
        else:
            lines.append(f"{prefix}  • {key}")
    return "\n".join(lines)


def search_in_vault(vault_path: Path, query: str, case_sensitive: bool = False) -> list[dict]:
    results = []
    flags   = 0 if case_sensitive else re.IGNORECASE
    pattern = re.compile(re.escape(query), flags)

    for md_file in sorted(vault_path.rglob("*.md")):
        if any(part.startswith(".") for part in md_file.parts):
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        matches = []
        for i, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                matches.append({"line": i, "text": line.strip()})

        if matches:
            results.append({
                "file":          str(md_file.relative_to(vault_path)),
                "matches":       matches[:10],
                "total_matches": len(matches),
            })

    return results


def read_section(content: str, heading: str) -> str | None:
    """Extract content under a specific markdown heading."""
    lines   = content.splitlines()
    capture = False
    section = []
    target  = heading.lstrip("#").strip().lower()

    for line in lines:
        if line.startswith("#"):
            current = line.lstrip("#").strip().lower()
            if current == target:
                capture = True
                section.append(line)
                continue
            elif capture:
                break
        if capture:
            section.append(line)

    return "\n".join(section) if section else None


def write_section(content: str, heading: str, new_content: str) -> str | None:
    """Replace content under a specific heading."""
    lines       = content.splitlines()
    target      = heading.lstrip("#").strip().lower()
    start_idx   = None
    end_idx     = None
    heading_lvl = None

    for i, line in enumerate(lines):
        if line.startswith("#"):
            current = line.lstrip("#").strip().lower()
            lvl     = len(line) - len(line.lstrip("#"))
            if current == target and start_idx is None:
                start_idx   = i
                heading_lvl = lvl
            elif start_idx is not None and lvl <= heading_lvl:
                end_idx = i
                break

    if start_idx is None:
        return None

    end_idx   = end_idx or len(lines)
    new_lines = lines[:start_idx + 1] + [new_content] + lines[end_idx:]
    return "\n".join(new_lines)


# ── Server ────────────────────────────────────────────────────────────────────
app = Server("vaultbridge")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="obsidian_list",
            description=(
                "List all notes inside an Obsidian vault. "
                "Leave vault_name blank or use '.' to list all available vaults."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "vault_name": {
                        "type": "string",
                        "description": "Vault folder name. Leave blank to list all vaults.",
                        "default": ".",
                    }
                },
            },
        ),
        Tool(
            name="obsidian_read",
            description=(
                "Read the full content of a note, or a specific section by heading. "
                "Use section='## Skills' to read only that section."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "vault_name": {"type": "string", "description": "Vault folder name"},
                    "note":       {"type": "string", "description": "Note name e.g. 'profile' or 'folder/note'"},
                    "section":    {"type": "string", "description": "Optional heading to read e.g. '## Skills'"},
                },
                "required": ["vault_name", "note"],
            },
        ),
        Tool(
            name="obsidian_write",
            description=(
                "Write content to a note. "
                "mode='overwrite' replaces everything (default). "
                "mode='append' adds to the bottom. "
                "mode='prepend' adds to the top. "
                "mode='section' replaces content under a specific heading (requires section parameter). "
                "Creates the note and any missing parent folders automatically."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "vault_name": {"type": "string", "description": "Vault folder name"},
                    "note":       {"type": "string", "description": "Note name"},
                    "content":    {"type": "string", "description": "Markdown content to write"},
                    "mode":       {
                        "type": "string",
                        "enum": ["overwrite", "append", "prepend", "section"],
                        "default": "overwrite",
                        "description": "overwrite | append | prepend | section",
                    },
                    "section":    {"type": "string", "description": "Required for mode=section: heading to update e.g. '## Skills'"},
                },
                "required": ["vault_name", "note", "content"],
            },
        ),
        Tool(
            name="obsidian_search",
            description="Full-text search across all notes in a vault. Returns matching files with line numbers and context.",
            inputSchema={
                "type": "object",
                "properties": {
                    "vault_name":     {"type": "string", "description": "Vault folder name"},
                    "query":          {"type": "string", "description": "Search term or phrase"},
                    "case_sensitive": {"type": "boolean", "default": False},
                },
                "required": ["vault_name", "query"],
            },
        ),
        Tool(
            name="obsidian_delete",
            description=(
                "Delete a note from a vault. "
                "Requires confirm=true to execute. "
                "Without confirm=true, returns a dry-run preview only."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "vault_name": {"type": "string", "description": "Vault folder name"},
                    "note":       {"type": "string", "description": "Note name to delete"},
                    "confirm":    {"type": "boolean", "default": False, "description": "Must be true to actually delete"},
                },
                "required": ["vault_name", "note"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:

    # ── obsidian_list ─────────────────────────────────────────────────────────
    if name == "obsidian_list":
        vault_name = arguments.get("vault_name", ".").strip()
        audit("list", vault=vault_name)

        if vault_name in (".", "", "all"):
            try:
                vaults = [
                    d.name for d in sorted(VAULTS_BASE.iterdir())
                    if d.is_dir() and not d.name.startswith(".")
                ]
            except Exception:
                return [TextContent(type="text", text="❌ Could not read vaults directory.")]
            return [TextContent(type="text", text=f"📂 Vaults ({len(vaults)}):\n" + "\n".join(f"  • {v}" for v in vaults))]

        try:
            vault_path = resolve_vault(vault_name)
        except (PermissionError, FileNotFoundError) as e:
            return [TextContent(type="text", text=f"❌ {e}")]

        tree = list_vault_tree(vault_path)
        if not tree:
            return [TextContent(type="text", text=f"Vault '{vault_name}' is empty.")]

        return [TextContent(type="text", text=f"📂 {vault_name}\n\n" + tree_to_string(tree))]

    # ── obsidian_read ─────────────────────────────────────────────────────────
    elif name == "obsidian_read":
        vault_name = arguments.get("vault_name", "").strip()
        note_name  = arguments.get("note", "").strip()
        section    = arguments.get("section", "").strip()

        if not vault_name or not note_name:
            return [TextContent(type="text", text="❌ vault_name and note are required.")]

        try:
            vault_path = resolve_vault(vault_name)
            note_path  = resolve_note(vault_path, note_name)
        except (PermissionError, FileNotFoundError) as e:
            return [TextContent(type="text", text=f"❌ {e}")]

        if not note_path.exists():
            return [TextContent(type="text", text=f"❌ Note not found: {safe_display(note_path)}")]

        audit("read", vault=vault_name, note=note_name, extra=f"section={section or 'full'}")
        content = note_path.read_text(encoding="utf-8")

        if section:
            extracted = read_section(content, section)
            if not extracted:
                return [TextContent(type="text", text=f"❌ Section '{section}' not found in '{note_name}'.")]
            return [TextContent(type="text", text=f"📄 {note_name} › {section}\n\n{extracted}")]

        return [TextContent(type="text", text=f"📄 {safe_display(note_path)}\n\n{content}")]

    # ── obsidian_write ────────────────────────────────────────────────────────
    elif name == "obsidian_write":
        if READ_ONLY:
            return [TextContent(type="text", text="❌ vaultbridge is in read-only mode. Writes are disabled.")]

        vault_name = arguments.get("vault_name", "").strip()
        note_name  = arguments.get("note", "").strip()
        content    = arguments.get("content", "")
        mode       = arguments.get("mode", "overwrite")
        section    = arguments.get("section", "").strip()

        if not vault_name or not note_name:
            return [TextContent(type="text", text="❌ vault_name and note are required.")]

        if mode == "section" and not section:
            return [TextContent(type="text", text="❌ mode=section requires a section parameter e.g. '## Skills'")]

        try:
            vault_path = resolve_vault(vault_name)
            note_path  = resolve_note(vault_path, note_name)
        except (PermissionError, FileNotFoundError) as e:
            return [TextContent(type="text", text=f"❌ {e}")]

        note_path.parent.mkdir(parents=True, exist_ok=True)
        existed = note_path.exists()
        audit("write", vault=vault_name, note=note_name, extra=f"mode={mode}")

        if mode == "overwrite" or not existed:
            note_path.write_text(content, encoding="utf-8")
            action = "overwritten" if existed else "created"

        elif mode == "append":
            existing  = note_path.read_text(encoding="utf-8")
            separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
            note_path.write_text(existing + separator + content, encoding="utf-8")
            action = "appended"

        elif mode == "prepend":
            existing  = note_path.read_text(encoding="utf-8")
            separator = "\n\n" if existing else ""
            note_path.write_text(content + separator + existing, encoding="utf-8")
            action = "prepended"

        elif mode == "section":
            if not existed:
                return [TextContent(type="text", text=f"❌ Note '{note_name}' does not exist. Create it first with mode=overwrite.")]
            existing = note_path.read_text(encoding="utf-8")
            updated  = write_section(existing, section, content)
            if updated is None:
                return [TextContent(type="text", text=f"❌ Section '{section}' not found in '{note_name}'.")]
            note_path.write_text(updated, encoding="utf-8")
            action = f"section '{section}' updated"

        else:
            return [TextContent(type="text", text=f"❌ Unknown mode '{mode}'.")]

        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        return [TextContent(type="text", text=f"✅ {safe_display(note_path)} — {action} [{ts}]")]

    # ── obsidian_search ───────────────────────────────────────────────────────
    elif name == "obsidian_search":
        vault_name     = arguments.get("vault_name", "").strip()
        query          = arguments.get("query", "").strip()
        case_sensitive = arguments.get("case_sensitive", False)

        if not vault_name or not query:
            return [TextContent(type="text", text="❌ vault_name and query are required.")]

        try:
            vault_path = resolve_vault(vault_name)
        except (PermissionError, FileNotFoundError) as e:
            return [TextContent(type="text", text=f"❌ {e}")]

        audit("search", vault=vault_name, extra=f"query={query}")
        results = search_in_vault(vault_path, query, case_sensitive)

        if not results:
            return [TextContent(type="text", text=f"No results for '{query}' in '{vault_name}'.")]

        lines = [f"🔍 '{query}' in '{vault_name}' — {len(results)} file(s) matched\n"]
        for r in results:
            lines.append(f"\n📄 {r['file']}  ({r['total_matches']} match{'es' if r['total_matches']>1 else ''})")
            for m in r["matches"]:
                lines.append(f"   L{m['line']:>4}: {m['text'][:120]}")

        return [TextContent(type="text", text="\n".join(lines))]

    # ── obsidian_delete ───────────────────────────────────────────────────────
    elif name == "obsidian_delete":
        if READ_ONLY:
            return [TextContent(type="text", text="❌ vaultbridge is in read-only mode. Deletes are disabled.")]

        vault_name = arguments.get("vault_name", "").strip()
        note_name  = arguments.get("note", "").strip()
        confirm    = arguments.get("confirm", False)

        if not vault_name or not note_name:
            return [TextContent(type="text", text="❌ vault_name and note are required.")]

        try:
            vault_path = resolve_vault(vault_name)
            note_path  = resolve_note(vault_path, note_name)
        except (PermissionError, FileNotFoundError) as e:
            return [TextContent(type="text", text=f"❌ {e}")]

        if not note_path.exists():
            return [TextContent(type="text", text=f"❌ Note not found: {safe_display(note_path)}")]

        if not confirm:
            return [TextContent(type="text", text=(
                f"⚠️  Dry run — would delete: {safe_display(note_path)}\n"
                f"Call obsidian_delete again with confirm=true to proceed."
            ))]

        audit("delete", vault=vault_name, note=note_name)
        note_path.unlink()
        return [TextContent(type="text", text=f"🗑️  Deleted: {safe_display(note_path)}")]

    else:
        return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]


# ── Entry point ───────────────────────────────────────────────────────────────
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
