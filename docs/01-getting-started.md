# Getting Started

## Prerequisites

- Python 3.10+
- [Claude Desktop](https://claude.ai/download) installed
- [Obsidian](https://obsidian.md) installed with at least one vault

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/k41r0s3/vaultbridge.git ~/vaultbridge
cd ~/vaultbridge
```

### 2. Create the virtual environment

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 3. Register with Claude Desktop

Edit `~/.config/Claude/claude_desktop_config.json` and add this inside the `"mcpServers"` block:

```json
"vaultbridge": {
  "command": "/home/YOUR_USER/vaultbridge/.venv/bin/python",
  "args": ["/home/YOUR_USER/vaultbridge/server.py"],
  "env": {
    "OBSIDIAN_BASE": "/home/YOUR_USER/path/to/your/Obsidian"
  }
}
```

Replace `YOUR_USER` with your username and `OBSIDIAN_BASE` with the path to the folder that contains all your Obsidian vaults.

### 4. Restart Claude Desktop

Close and reopen Claude Desktop. Vaultbridge starts automatically in the background — no manual startup needed.

---

## Verify it works

Once Claude Desktop restarts, open a new chat and say:

> "List all my Obsidian vaults"

Claude should respond with the vaults found under your `OBSIDIAN_BASE` path. If it does — you're good to go.

---

## Troubleshooting

**Tools not showing up after restart**

Check your config is valid JSON:
```bash
cat ~/.config/Claude/claude_desktop_config.json | python3 -m json.tool
```

Check the venv python exists:
```bash
ls ~/vaultbridge/.venv/bin/python
```

Test the server runs without errors:
```bash
~/vaultbridge/.venv/bin/python ~/vaultbridge/server.py
```
It should hang silently. Press `Ctrl+C` to exit. If it throws an error, the dependency install failed — re-run:
```bash
rm -rf .venv
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Check Claude Desktop logs for errors:
```bash
cat ~/.config/Claude/logs/main.log | grep -i "vaultbridge" | tail -20
```
