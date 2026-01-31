---
name: chrome-devtools-mcp
description: Use Chrome DevTools MCP to connect to a Chrome instance and perform DevTools actions (inspect pages, capture requests, read DOM, etc.). Use when the user asks to operate Chrome via the chrome-devtools-mcp tool.
---

# Chrome DevTools MCP

## Quick start

1. Ensure the MCP server is configured:
   - In Codex config: `chrome-devtools` with `npx -y chrome-devtools-mcp@latest`.
2. Start Chrome with remote debugging enabled (ask user for port if unsure):
   - Typical: `--remote-debugging-port=9222`
3. Connect to the target tab / page via the MCP tool.

## Requirements (from README)

- Node.js v20.19+ or latest maintenance LTS
- Chrome stable or newer
- npm

## Server config examples (from README)

Minimal config:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

Connect to an existing Chrome via browser URL (example):

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--browser-url=http://127.0.0.1:9222",
        "-y"
      ]
    }
  }
}
```

## Notes (from README)

- Use `chrome-devtools-mcp@latest` to stay current.
- Usage statistics are enabled by default; disable with `--no-usage-statistics`.
- This MCP exposes browser content to clients; avoid sensitive data.

## When to ask for info

If the user hasn't provided details, ask for:
- Chrome remote debugging port (default is usually 9222).
- The target tab URL or a brief description to identify the page.
- Whether Chrome is already running with remote debugging enabled.

## Workflow (high level)

- Confirm Chrome is running with a remote debugging port.
- Use the MCP tool to list available targets/pages.
- Select the target tab.
- Perform requested DevTools actions (network capture, DOM queries, screenshots, etc.).

## Notes

- If the user provides a README snippet or commands, follow those exactly.
- If behavior is unclear, request the minimal missing detail instead of guessing.
