# AGENTS.md

## Environment

- **Package manager:** `uv` — use `uv run` and `uv sync`, not `pip`
- **Python version:** 3.12+ (pinned in `pyproject.toml` via `requires-python`)
- No required environment variables — the server makes unauthenticated requests only

## Commands

| Action | Command |
|---|---|
| Install dependencies | `uv sync` |
| Start server (stdio) | `uv run mcp-web-search` |
| Start server (HTTP) | `uv run mcp-web-search --transport streamable-http --host 127.0.0.1 --port 8000` |
| Build wheel | `uv build` |

There is no test suite and no lint step at this time.

## Tool contracts

Both tools always return a JSON string (never raise). The `success` field signals outcome.

**`search_list`**
- Returns up to 10 results from DuckDuckGo.
- Can fail with `DDGSException: Ratelimit` — this is a transient DuckDuckGo rate-limit, not a code bug.

**`access_site`**
- Downloads up to **2 MB** of raw bytes before cutting off.
- After HTML stripping, content is further capped at **20 000 characters**. If truncated, `"truncated": true` is set and the string ends with `[... content truncated ...]`.
- Non-HTML responses (JSON, plain text, etc.) are returned as-is up to the same character cap.
- The User-Agent is spoofed to a Chrome/Linux string — this is intentional to avoid bot-blocking.

## Boundaries

### Always
- Keep both tools returning JSON strings; never change them to raise exceptions.
- Verify the server starts cleanly (`uv run mcp-web-search`) before finishing any task.

### Ask First
- Adding any new dependency to `pyproject.toml`
- Adding a third tool — the two-tool surface is intentional
- Changing default transport, host, or port values

### Never
- Commit secrets, API keys, or `.env` files
- Remove the 2 MB download cap or the 20 000-character text cap without explicit instruction — they exist to protect Claude's context window
