# Configuration

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `OBSIDIAN_BASE` | Yes | — | Absolute path to the folder containing all your Obsidian vaults |
| `VAULTBRIDGE_READONLY` | No | `0` | Set to `1`, `true`, or `yes` to disable all writes and deletes globally |
| `VAULTBRIDGE_LOG` | No | `~/.vaultbridge.log` | Path to the audit log file |
| `VAULTBRIDGE_REDACT_PATHS` | No | `1` | Set to `0` or `false` to show full filesystem paths in responses |

---

## OBSIDIAN_BASE Structure

```
/home/user/Desktop/Obsidian/     ← OBSIDIAN_BASE
├── Resume Builder/              ← vault (auto-discovered)
├── Personal Notes/              ← vault (auto-discovered)
└── Work Notes/                  ← vault (auto-discovered)
```

Any new vault folder added here is automatically available — no config changes needed.

---

## Claude Desktop Config

Config file location by OS:

| OS | Path |
|---|---|
| Linux / Kali | `~/.config/Claude/claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

### Basic setup

```json
{
  "mcpServers": {
    "vaultbridge": {
      "command": "/home/YOUR_USER/vaultbridge/.venv/bin/python",
      "args": ["/home/YOUR_USER/vaultbridge/server.py"],
      "env": {
        "OBSIDIAN_BASE": "/home/YOUR_USER/Desktop/Obsidian"
      }
    }
  }
}
```

### With all options

```json
{
  "mcpServers": {
    "vaultbridge": {
      "command": "/home/YOUR_USER/vaultbridge/.venv/bin/python",
      "args": ["/home/YOUR_USER/vaultbridge/server.py"],
      "env": {
        "OBSIDIAN_BASE": "/home/YOUR_USER/Desktop/Obsidian",
        "VAULTBRIDGE_READONLY": "0",
        "VAULTBRIDGE_LOG": "/home/YOUR_USER/.vaultbridge.log",
        "VAULTBRIDGE_REDACT_PATHS": "1"
      }
    }
  }
}
```

> macOS users: replace `/home/YOUR_USER` with `/Users/YOUR_USER`

---

## Audit Log

Every tool call is logged to `~/.vaultbridge.log` by default:

```
2026-03-27 02:13:45 | INFO | action=read vault=Resume Builder note=profile section=full
2026-03-27 02:14:01 | INFO | action=write vault=Resume Builder note=experience mode=append
2026-03-27 02:14:22 | INFO | action=delete vault=Resume Builder note=old-draft
```

View recent activity:
```bash
tail -20 ~/.vaultbridge.log
```

---

## Read-Only Mode

Set `VAULTBRIDGE_READONLY=1` to allow Claude to read notes but never modify them. All write and delete operations are blocked at the server level.
