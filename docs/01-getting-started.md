# Getting Started

## Prerequisites

- Python 3.10+
- Claude Desktop installed
- Obsidian installed with at least one vault

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/k41r0s3/vaultbridge.git ~/vaultbridge
cd ~/vaultbridge
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 3. Register with Claude Desktop

Config file location by OS:

| OS | Path |
|---|---|
| Linux / Kali | `~/.config/Claude/claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

Add this inside the `"mcpServers"` block:

```json
"vaultbridge": {
  "command": "/home/YOUR_USER/vaultbridge/.venv/bin/python",
  "args": ["/home/YOUR_USER/vaultbridge/server.py"],
  "env": {
    "OBSIDIAN_BASE": "/home/YOUR_USER/Desktop/Obsidian"
  }
}
```

> macOS users: replace `/home/YOUR_USER` with `/Users/YOUR_USER`

### 4. Restart Claude Desktop

Close fully (check system tray) and reopen. vaultbridge starts automatically in the background.

### 5. Verify

Say: *"List all my Obsidian vaults"* — Claude should respond with your vault names.

---

## Updating

When a new version is released:

```bash
cd ~/vaultbridge
git pull origin main
```

Then restart Claude Desktop. If the new version adds packages:

```bash
.venv/bin/pip install -r requirements.txt
```

Check your current version:
```bash
git log --oneline -1
```

---

## Troubleshooting

**Tools not showing up after restart**
```bash
# Check config is valid JSON
cat ~/.config/Claude/claude_desktop_config.json | python3 -m json.tool

# Check venv python exists
ls ~/vaultbridge/.venv/bin/python

# Test server manually — should hang silently, Ctrl+C to exit
~/vaultbridge/.venv/bin/python ~/vaultbridge/server.py

# Check Claude Desktop logs
cat ~/.config/Claude/logs/main.log | grep -i "vaultbridge" | tail -20
```

**Venv broken after moving or renaming the folder**

The venv stores absolute paths internally — recreate it:
```bash
rm -rf ~/vaultbridge/.venv
python3 -m venv ~/vaultbridge/.venv
~/vaultbridge/.venv/bin/pip install -r ~/vaultbridge/requirements.txt
```

**Vault not found error**

`OBSIDIAN_BASE` must point to the **parent folder** containing your vaults, not a vault itself:
```
✅ OBSIDIAN_BASE=/home/user/Desktop/Obsidian     ← contains vault folders
❌ OBSIDIAN_BASE=/home/user/Desktop/Obsidian/My Vault  ← this IS a vault
```
