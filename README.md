# vaultbridge

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![MCP](https://img.shields.io/badge/MCP-compatible-purple)

A lightweight Python MCP server that bridges Claude and Obsidian — giving Claude full read/write/search/list access to any Obsidian vault on your machine. Claude Desktop auto-starts it in the background, no manual server startup needed.

## Tools

| Tool | Description |
|---|---|
| `obsidian_list` | List all notes in a vault, or list all available vaults |
| `obsidian_read` | Read a note's full content |
| `obsidian_write` | Write/append/prepend content to a note |
| `obsidian_search` | Full-text search across all notes in a vault |

---

## Quick Setup

```bash
git clone https://github.com/k41r0s3/vaultbridge.git ~/vaultbridge
cd ~/vaultbridge
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Add to `~/.config/Claude/claude_desktop_config.json`:

```json
"vaultbridge": {
  "command": "/home/YOUR_USER/vaultbridge/.venv/bin/python",
  "args": ["/home/YOUR_USER/vaultbridge/server.py"],
  "env": {
    "OBSIDIAN_BASE": "/home/YOUR_USER/path/to/your/Obsidian"
  }
}
```

Restart Claude Desktop — done.

---

## Documentation

| Doc | Description |
|---|---|
| [Getting Started](docs/01-getting-started.md) | Installation, setup, troubleshooting |
| [Tools Reference](docs/02-tools-reference.md) | Full reference for all 4 tools |
| [Configuration](docs/03-configuration.md) | Environment variables and config options |
| [Use Cases](docs/04-use-cases.md) | Practical examples and workflows |
| [Changelog](docs/05-changelog.md) | Version history |

---

## License

MIT — see [LICENSE](LICENSE) for details.
