# Load into Claude Code / Claude Desktop

This repo **is** a plugin marketplace: `.claude-plugin/marketplace.json` at the root lists all
four plugins. Three ways in, cheapest first.

## 1. From GitHub (recommended — updates with `git pull`)

```bash
claude
```

Then inside Claude Code:

```
/plugin marketplace add <your-github-user>/shin-skillpack
/plugin install productivity@shin-skillpack
/plugin install product-management@shin-skillpack
/plugin install operations@shin-skillpack
/plugin install artifact-toolkit@shin-skillpack
```

Update later with `/plugin marketplace update shin-skillpack`.

## 2. From a local clone or the unzipped folder

```
/plugin marketplace add D:/path/to/shin-skillpack
/plugin install operations@shin-skillpack
```

Use a forward-slash path on Windows; a local marketplace points at the folder containing
`.claude-plugin/marketplace.json`.

## 3. Skills only, no plugin system

Copy the skill folders straight into a skills directory:

```powershell
# user-level: available in every project
Copy-Item -Recurse plugins\operations\skills\*        $HOME\.claude\skills\
Copy-Item -Recurse plugins\product-management\skills\* $HOME\.claude\skills\
Copy-Item -Recurse plugins\productivity\skills\*       $HOME\.claude\skills\
Copy-Item -Recurse plugins\artifact-toolkit\skills\*   $HOME\.claude\skills\

# or project-level: committed with the repo it serves
Copy-Item -Recurse plugins\operations\skills\* .\.claude\skills\
```

Note `plugins/productivity/skills/dashboard.html` sits *beside* the skill folders, not inside
one — copy it too if you want `/productivity:start` to open the board.

You lose two things this way: the `/plugin` update path, and the `.mcp.json` connector
pre-configuration.

## Connectors

Each plugin ships a `.mcp.json` listing the MCP servers its skills expect (Slack, Notion,
Asana, Linear, Jira, Figma, Amplitude, Gmail, Google Calendar, …). Installing the plugin
registers them; **each still needs its own OAuth** before its tools work. Authorize with
`/mcp` in an interactive `claude` session, or via claude.ai connector settings for claude.ai
connectors.

The skills are tool-agnostic by design: they speak in `~~category` placeholders
(`~~project tracker`, `~~chat`, …), so any MCP server in that category works. Read each
plugin's `CONNECTORS.md` for the category → server mapping.

## Verify

```
/help
```

The four plugins' commands should appear — `/status-report`, `/write-spec`, `/task-management`,
and so on. If a name collides with something you already have, Claude Code namespaces it as
`/operations:status-report`.
