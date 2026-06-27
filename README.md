# mcp-web-search

A local MCP server providing DuckDuckGo web search and site fetching tools for Claude Desktop.

## Tools

| Tool | Description |
|------|-------------|
| `search_list` | Search DuckDuckGo and return up to 10 ranked results |
| `access_site` | Fetch a URL (follows redirects) and return its text content |

---

## Setup

### 0. uv

if `uv` seems not to be available try this absolute path.

```bash
$HOME/.local/bin/uv
```

### 1. Install dependencies

```bash
uv sync
```

### 2. Test the server starts

```bash
uv run mcp-web-search
# Pass transport (optional) and host (optional) and port(optional) to start with streamable http protocol
uv run mcp-web-search --transport streamable-http --host 127.0.0.1 --port 8000
```

You should see the server waiting on stdin — that means it's working. Press Ctrl+C to stop.

---

## Connect to Claude Desktop

Add the following to your Claude Desktop config file.

**Config file location:**

| OS | Path |
|----|------|
| macOS | `$HOME/Library/Application\ Support/Claude/claude_desktop_config.json` |
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

Replace `/absolute/path/to/mcp-web-search` with the actual path to this folder.

Restart Claude Desktop — both tools will appear in the 🔌 menu.

---

## Tool Reference

### `search_list`

**Input:** `{ "query": "DocLang document specification" }`

**Output:**
```json
{
  "success": true,
  "query": "DocLang document specification",
  "results_count": 10,
  "results": [
    {
      "rank": 1,
      "title": "...",
      "url": "https://...",
      "snippet": "..."
    }
  ]
}
```

### `access_site`

**Input:** `{ "url": "https://doclang.org" }`

**Output:**
```json
{
  "success": true,
  "requested_url": "https://doclang.org",
  "final_url": "https://doclang.org/",
  "status_code": 200,
  "content_type": "text/html; charset=utf-8",
  "truncated": false,
  "content": "Page text content..."
}
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `uv sync` to install dependencies |
| Tools don't appear in Claude | Use an absolute path in the config; restart Claude Desktop |
| `DDGSException: Ratelimit` | DuckDuckGo rate-limited you; wait a moment and retry |