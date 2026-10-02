# OpenVidu Agent Plugin

[OpenVidu](https://openvidu.io) is an open-source, self-hosted platform for
building real-time video conferencing and WebRTC applications, built on top
of [LiveKit](https://livekit.io) and mediasoup.

This plugin gives your coding agent the official OpenVidu documentation —
instead of guessing from whatever it memorised during training, it searches
and reads the real pages, **for the OpenVidu deployment you are actually
running**: the right version, read for the right edition and the right
product.

It is both an [Agent Plugins 1.0](https://agent-plugins.org) package and a
[Claude Code plugin](https://code.claude.com/docs/en/plugins).

**Documentation: <https://openvidu.io/docs/coding-agents/agent-plugin/>** —
installation in every client, updates, setting it up by hand, and
troubleshooting.

## Quick start

In Claude Code:

```
/plugin marketplace add OpenVidu/openvidu-agent-plugin
/plugin install openvidu@openvidu
```

Then turn on automatic updates for it, which Claude Code leaves off for
marketplaces other than Anthropic's: `/plugin` → **Marketplaces** →
`openvidu` → **Enable auto-update**.

VS Code, Cursor, GitHub Copilot, Codex, Kiro and any other client: see
[Install](https://openvidu.io/docs/coding-agents/agent-plugin/#install).

## What you get

| Component | What it is |
|---|---|
| `openvidu-docs` MCP server | OpenVidu's documentation, per version, at `https://docs-mcp.openvidu.io/mcp`. Its instructions also tell the agent when to read LiveKit's documentation for SDK detail, and what never to take from it |
| `openvidu-version-edition-product` skill | Establishes the version, edition and product your project targets when an answer depends on them, and pins them in `AGENTS.md` / `CLAUDE.md` |

What each tool does, and how LiveKit's documentation fits in:
[What's inside](https://openvidu.io/docs/coding-agents/agent-plugin/#whats-inside).

## What's in the package

```text
plugin.json                     Agent Plugins 1.0 manifest
mcp.json                        the documentation MCP server (Streamable HTTP)
skills/                         one directory per skill, each with a SKILL.md
.claude-plugin/plugin.json      Claude Code manifest
.claude-plugin/marketplace.json Claude Code marketplace
.mcp.json                       Claude Code MCP config
LICENSE                         Apache 2.0
dev/                            not part of the plugin: how it is built,
                                validated and published
```

## Source

This repository is what gets installed: the plugin manifest, the MCP server
configuration, and the skills. Report issues with any of those here. The
documentation server behind the MCP endpoint is maintained separately by the
OpenVidu team, and the user documentation lives on openvidu.io.

## Development

Everything about building, validating and publishing the package lives in
**[`dev/README.md`](dev/README.md)**: what is generated and why, how the
version numbers work, how to add a skill, and the checklist before a release.

```bash
cd dev
pip install -r requirements.txt
python build_plugin.py    # validate the package + regenerate the Claude Code files
pytest
```
