# MCP Setup Guide

Guide for configuring Obsidian MCP server connectivity.

## Prerequisites

1. **Obsidian** installed and running
2. **Obsidian Local REST API plugin** installed and enabled
   - Install from Community Plugins: search "Local REST API"
   - Enable the plugin in Settings → Community Plugins
   - Generate an API key in the plugin settings
   - Default base URL: `http://127.0.0.1:27124`

## MCP Server Options

| Server | Focus | Tools | Best For |
|--------|-------|-------|----------|
| cyanheads/obsidian-mcp-server | Comprehensive | 8 tools (read, write, search, metadata, tags) | Full vault management |
| iansinnott/obsidian-claude-code-mcp | Claude Code specific | Optimized for CC workflow | Claude Code users |
| MarkusPfundstein/mcp-obsidian | Task-oriented | 7 tools + patch content | Task management vaults |

**Recommendation**: Start with `cyanheads/obsidian-mcp-server` for comprehensive coverage, or `iansinnott/obsidian-claude-code-mcp` if specifically using Claude Code.

The choice of MCP server is deferred to the user — present options with trade-offs and let them decide.

## Environment Variables

```bash
OBSIDIAN_API_KEY=<your-api-key-from-plugin-settings>
OBSIDIAN_BASE_URL=http://127.0.0.1:27124  # default, change if customized
```

**IMPORTANT**: Never commit API keys to git. Store in environment variables only.

## MCP Configuration

The user needs to add the MCP server to their Claude Code MCP configuration. The exact format depends on the chosen server — refer to the server's README for configuration syntax.

General pattern:
```json
{
  "mcpServers": {
    "obsidian": {
      "command": "<server-specific command>",
      "env": {
        "OBSIDIAN_API_KEY": "<key>",
        "OBSIDIAN_BASE_URL": "http://127.0.0.1:27124"
      }
    }
  }
}
```

## Connectivity Testing

After configuration, verify with these steps:

1. **List vault root**: Use MCP list/directory tool to enumerate root contents
2. **Read a note**: Use MCP read tool to read any existing note
3. **Search test**: Use MCP search tool to find a known term

If any test fails:
- Verify Obsidian is running
- Verify Local REST API plugin is enabled
- Check API key is correct
- Check base URL matches plugin settings
- Check firewall/antivirus isn't blocking localhost connections

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Connection refused | Obsidian not running or plugin disabled | Start Obsidian, enable plugin |
| 401 Unauthorized | Wrong API key | Regenerate key in plugin settings |
| Empty vault listing | Wrong vault path or base URL | Verify settings match the target vault |
| Timeout | Firewall blocking | Allow localhost:27124 through firewall |
| MCP server not found | Server not installed | Follow server-specific installation steps |

## Security Notes

- API key grants full read/write access to the vault — no granular permissions
- Only one vault per REST API instance
- Base URL defaults to localhost only — not exposed to network
- Never commit API keys to version control
