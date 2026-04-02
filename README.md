# vaultbridge

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![MCP](https://img.shields.io/badge/MCP-compatible-purple)
![Version](https://img.shields.io/badge/version-1.1.0-orange)

A lightweight Python MCP server that bridges Claude and Obsidian — giving Claude full read/write/search/list/delete access to any Obsidian vault on your machine. Claude Desktop auto-starts it in the background, no manual server startup needed.

## Tools

| Tool | Description |
|---|---|
| `obsidian_list` | List all notes in a vault, or list all available vaults |
| `obsidian_read` | Read a note's full content, or a specific section by heading |
| `obsidian_write` | Write/append/prepend/section-update content to a note |
| `obsidian_search` | Full-text search across all notes in a vault |
| `obsidian_delete` | Delete a note (requires `confirm=true`) |

---

## Quick Setup

```bash
git clone https://github.com/k41r0s3/vaultbridge.git ~/vaultbridge
cd ~/vaultbridge
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Add to your Claude Desktop config file:

| OS | Config path |
|---|---|
| Linux / Kali | `~/.config/Claude/claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

```json
"vaultbridge": {
  "command": "/home/YOUR_USER/vaultbridge/.venv/bin/python",
  "args": ["/home/YOUR_USER/vaultbridge/server.py"],
  "env": {
    "OBSIDIAN_BASE": "/home/YOUR_USER/path/to/your/Obsidian"
  }
}
```

> macOS users: replace `/home/YOUR_USER` with `/Users/YOUR_USER`

Restart Claude Desktop — done.

---

## Updating

```bash
cd ~/vaultbridge
git pull origin main
```

Restart Claude Desktop. That's it.

---

## Documentation

| Doc | Description |
|---|---|
| [Getting Started](docs/01-getting-started.md) | Installation, setup, updating, troubleshooting |
| [Tools Reference](docs/02-tools-reference.md) | Full reference for all 5 tools |
| [Configuration](docs/03-configuration.md) | Environment variables and config options |
| [Use Cases](docs/04-use-cases.md) | Practical examples and workflows |
| [Changelog](docs/05-changelog.md) | Version history |

---

## License

MIT — see [LICENSE](LICENSE) for details.
