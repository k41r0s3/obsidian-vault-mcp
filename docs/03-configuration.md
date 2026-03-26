# Configuration

## Environment Variables

Vaultbridge is configured entirely through environment variables set in `claude_desktop_config.json`.

| Variable | Required | Description |
|---|---|---|
| `OBSIDIAN_BASE` | Yes | Absolute path to the folder containing all your Obsidian vaults |

**Example structure:**
```
/home/user/Obsidian/          ← this is OBSIDIAN_BASE
├── Resume Builder/           ← vault 1
├── Personal Notes/           ← vault 2
└── Work Notes/               ← vault 3
```

With `OBSIDIAN_BASE=/home/user/Obsidian`, all three vaults are auto-discovered. No config changes needed when you add new vaults.

---

## Claude Desktop Config

Full example `claude_desktop_config.json` with vaultbridge alongside other MCP servers:

```json
{
  "mcpServers": {
    "vaultbridge": {
      "command": "/home/YOUR_USER/vaultbridge/.venv/bin/python",
      "args": ["/home/YOUR_USER/vaultbridge/server.py"],
      "env": {
        "OBSIDIAN_BASE": "/home/YOUR_USER/Obsidian"
      }
    }
  }
}
```

Config file location by OS:

| OS | Path |
|---|---|
| Linux | `~/.config/Claude/claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

---

## Multiple Vaults

No extra config needed. As long as each vault is a subfolder under `OBSIDIAN_BASE`, vaultbridge finds it automatically.

---

## Changing OBSIDIAN_BASE

If you move your Obsidian vaults folder, update `OBSIDIAN_BASE` in `claude_desktop_config.json` and restart Claude Desktop.
