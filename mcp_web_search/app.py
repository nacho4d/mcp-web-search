"""
MCP Web Search Server
Provides two tools:
  - search_list: Search the web via DuckDuckGo
  - access_site: Fetch and return the contents of a URL
"""

import json
import re
import urllib.request
import urllib.error
from mcp.server.fastmcp import FastMCP
from ddgs import DDGS

mcp = FastMCP("web-search")


@mcp.tool()
def search_list(query: str) -> str:
    """
    Search the web using DuckDuckGo and return ranked results.

    Args:
        query: The search query string

    Returns:
        JSON with results including rank, title, url, and snippet
    """
    try:
        with DDGS() as ddgs:
            raw = list(ddgs.text(query, max_results=10))

        results = [
            {
                "rank": i + 1,
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
            }
            for i, r in enumerate(raw)
        ]

        return json.dumps({
            "success": True,
            "query": query,
            "results_count": len(results),
            "results": results,
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "query": query,
            "error": str(e),
        }, indent=2)


def _extract_text(html: str) -> str:
    """Strip HTML tags and collapse whitespace into readable plain text."""
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


@mcp.tool()
def access_site(url: str) -> str:
    """
    Fetch the contents of a URL, following redirects, and return as plain text.

    Args:
        url: The URL to fetch

    Returns:
        JSON with the page content and metadata
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
        }

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            final_url = resp.geturl()
            status = resp.status
            content_type = resp.headers.get("Content-Type", "")
            raw_bytes = resp.read(2 * 1024 * 1024)  # cap at 2 MB

        charset = "utf-8"
        if "charset=" in content_type:
            charset = content_type.split("charset=")[-1].split(";")[0].strip()
        try:
            raw_text = raw_bytes.decode(charset, errors="replace")
        except LookupError:
            raw_text = raw_bytes.decode("utf-8", errors="replace")

        if "html" in content_type.lower():
            content = _extract_text(raw_text)
        else:
            content = raw_text

        max_chars = 20_000
        truncated = len(content) > max_chars
        if truncated:
            content = content[:max_chars] + "\n\n[... content truncated ...]"

        return json.dumps({
            "success": True,
            "requested_url": url,
            "final_url": final_url,
            "status_code": status,
            "content_type": content_type,
            "truncated": truncated,
            "content": content,
        }, indent=2)

    except urllib.error.HTTPError as e:
        return json.dumps({
            "success": False,
            "requested_url": url,
            "error": f"HTTP {e.code}: {e.reason}",
        }, indent=2)
    except urllib.error.URLError as e:
        return json.dumps({
            "success": False,
            "requested_url": url,
            "error": f"URL error: {e.reason}",
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "requested_url": url,
            "error": str(e),
        }, indent=2)
