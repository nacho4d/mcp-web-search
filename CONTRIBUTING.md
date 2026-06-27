# Contributing

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — if not in your `PATH`, try the absolute path: `$HOME/.local/bin/uv`

## Install dependencies

```bash
uv sync
```

## Verify the server starts

```bash
uv run mcp-web-search
```

You should see the server waiting on stdin — that means it's working. Press `Ctrl+C` to stop.

Optionally, start with streamable HTTP instead of stdio:

```bash
uv run mcp-web-search --transport streamable-http --host 127.0.0.1 --port 8000
```

## Connect to Claude Desktop

Add the following block to your Claude Desktop config file.

**Config file location:**

| OS | Path |
|----|------|
| macOS | `$HOME/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

```json
{
  "mcpServers": {
    "web-search": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/absolute/path/to/mcp-web-search",
        "mcp-web-search"
      ]
    }
  }
}
```

Replace `/absolute/path/to/mcp-web-search` with the actual absolute path to this folder, then restart Claude Desktop. Both tools will appear in the 🔌 menu.

## Making changes

- Keep changes minimal and focused — this is intentionally a small, two-tool server.
- There are no automated tests yet. Manually verify both tools work in Claude Desktop after any change.
- Run `uv run mcp-web-search` and confirm it starts cleanly before opening a PR.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `uv sync` to install dependencies |
| Tools don't appear in Claude | Use an absolute path in the config; restart Claude Desktop |
| `DDGSException: Ratelimit` | DuckDuckGo rate-limited you; wait a moment and retry |
