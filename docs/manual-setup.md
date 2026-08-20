# Setting it up without the plugin

Everything the [OpenVidu Agent Plugin](../README.md) installs can be configured
by hand instead. Use this when your client doesn't implement
[Agent Plugins 1.0](https://agent-plugins.org) yet, or when you would rather
not install anything.

The package has two kinds of component, and here they are independent: the
**MCP server**, which is where the documentation comes from, and the
**skills**, which are instructions the agent follows. Set up either, or both.
Nothing on this page updates itself — see
[Keeping a manual setup current](#keeping-a-manual-setup-current).

## The MCP server

The same server the plugin points at, configured directly. No account and no
API key; the endpoint is

```
https://docs-mcp.openvidu.io/mcp
```

and the transport is **Streamable HTTP**.

### Claude Code

```bash
claude mcp add --transport http openvidu-docs https://docs-mcp.openvidu.io/mcp
```

Add `--scope project` to share it with your team through `.mcp.json`, or
`--scope user` to have it in every project. Check it with `claude mcp list`.

### Cursor

Add it to `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (this project):

```json
{
  "mcpServers": {
    "openvidu-docs": {
      "url": "https://docs-mcp.openvidu.io/mcp"
    }
  }
}
```

### VS Code (GitHub Copilot)

Create `.vscode/mcp.json` in the workspace:

```json
{
  "servers": {
    "openvidu-docs": {
      "type": "http",
      "url": "https://docs-mcp.openvidu.io/mcp"
    }
  }
}
```

Or from the command line:

```bash
code --add-mcp '{"name":"openvidu-docs","type":"http","url":"https://docs-mcp.openvidu.io/mcp"}'
```

### Claude Desktop

*Settings → Connectors → Add custom connector*, then paste the server URL.

### Any other client

Anything that speaks MCP over Streamable HTTP works; it only needs the URL.
The usual shape of the configuration file is:

```json
{
  "mcpServers": {
    "openvidu-docs": {
      "type": "http",
      "url": "https://docs-mcp.openvidu.io/mcp"
    }
  }
}
```

Check your client's own documentation for where that file lives and whether it
calls the field `type`, `transport`, or nothing at all.

## The skills

A skill is a **directory** — a `SKILL.md`, plus whatever references, scripts or
templates it bundles — so installing one by hand means copying the whole
directory, not just the file. [`skills/`](../skills/) in the plugin repository
holds one directory per skill; take all of them, or pick the ones you want.

Two rules, and they are the two things that go wrong:

- **Keep the directory name.** It has to match the `name` in that skill's
  frontmatter, and a mismatch makes clients skip the skill in silence.
- **Use a location your client scans.** They differ:

| Client | For one project | For every project |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.agents/skills/`, `.cursor/skills/` | `~/.agents/skills/`, `~/.cursor/skills/` |
| VS Code (GitHub Copilot) | `.github/skills/`, `.agents/skills/` | `~/.copilot/skills/`, `~/.agents/skills/` |
| Codex | — | `~/.codex/skills/` (or `$CODEX_HOME/skills`) |
| Kiro | `.kiro/skills/` | `~/.kiro/skills/` |

For anything not listed, the
[client showcase](https://agentskills.io/clients) links each one's own
documentation, which is where the current paths live.

Two things are worth reading out of that table. Cursor and VS Code also accept
`.claude/skills/` and `~/.claude/skills/` for backward compatibility, which
makes **`.claude/skills/` the single project directory that covers Claude Code,
Cursor and Copilot at once** — the pragmatic choice for a repository shared
across a team today. And `.agents/skills/` is the vendor-neutral location the
ecosystem is converging on: Cursor and VS Code read it, Claude Code does not
yet.

### Copying them in

Clone once, copy what you want, throw the clone away. For every project, on
Claude Code:

```bash
git clone --depth 1 https://github.com/OpenVidu/openvidu-agent-plugin /tmp/openvidu-agent-plugin
mkdir -p ~/.claude/skills
cp -r /tmp/openvidu-agent-plugin/skills/. ~/.claude/skills/
```

For one project, shared with your team, use the project-level path from the
table instead and commit the result, so a checkout brings the skills with it:

```bash
mkdir -p .claude/skills
cp -r /tmp/openvidu-agent-plugin/skills/. .claude/skills/
```

To take a single skill rather than all of them, name its directory —
`ls /tmp/openvidu-agent-plugin/skills` lists what there is to choose from:

```bash
cp -r /tmp/openvidu-agent-plugin/skills/<skill-name> ~/.claude/skills/
```

Then `rm -rf /tmp/openvidu-agent-plugin` once you are done with the clone.

### Checking they loaded

Claude Code lists them in `/skills`, and picks up a newly added skill without a
restart — unless you created the top-level skills directory itself mid-session,
which needs one. In VS Code, type `/` in chat, or run **Chat: Open
Customizations** from the Command Palette. Elsewhere, each skill's name appears
wherever your client lists what it has loaded.

### Clients that take skills through settings, not a directory

Claude Desktop and claude.ai don't read a folder on your disk: skills are
enabled for your account, from **Customize** in the Desktop app sidebar or the
skill settings on claude.ai.

### Clients that don't do skills at all

You lose less than it sounds. A skill is only instructions, so you can do by
hand what it would have done: for the version, edition and product, that means
[writing them into your AGENTS.md](../README.md#write-the-version-edition-and-product-in-agentsmd)
once, after which the coding agent reads them in every session that follows.

## Keeping a manual setup current

The server asks nothing of you: the endpoint is stable, and the documentation
behind it is versioned per OpenVidu release rather than per plugin release, so
there is no client-side copy to refresh.

The skills are copies, and nothing tells you when the originals change. Re-run
the copy above to refresh them, or
[install the plugin](../README.md#installation) and let your client keep them
current.
