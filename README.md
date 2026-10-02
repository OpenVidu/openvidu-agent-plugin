# OpenVidu Agent Plugin

[OpenVidu](https://openvidu.io) is an open-source, self-hosted platform for
building real-time video conferencing and WebRTC applications, built on top
of [LiveKit](https://livekit.io) and mediasoup.

This plugin gives your coding agent the official OpenVidu documentation:
instead of guessing from whatever it memorised during training, it searches
and reads the real pages, **for the OpenVidu deployment you are actually
running**: the right version, read for the right edition and the right
product.

It is both an [Agent Plugins 1.0](https://agent-plugins.org) package and a
[Claude Code plugin](https://code.claude.com/docs/en/plugins). It needs no
account, API key or login.

**Documentation: <https://openvidu.io/latest/docs/coding-agents/agent-plugin/>**,
with updates, setting it up by hand, and troubleshooting.

## Install

| Client | |
|---|---|
| Claude Code | `/plugin marketplace add OpenVidu/openvidu-agent-plugin`, then `/plugin install openvidu@openvidu` |
| VS Code | **Chat: Install Plugin From Source**, with `https://github.com/OpenVidu/openvidu-agent-plugin` |
| GitHub Copilot CLI | `copilot plugin install OpenVidu/openvidu-agent-plugin` |
| Codex CLI | `codex plugin marketplace add OpenVidu/openvidu-agent-plugin`, then `codex plugin add openvidu@openvidu` |
| Cursor | `git clone https://github.com/OpenVidu/openvidu-agent-plugin ~/.cursor/plugins/local/openvidu` |
| Kiro | **Powers → Add Custom Power → Import power from GitHub**, with the repository URL |

Claude Code leaves automatic updates off for marketplaces other than
Anthropic's: turn them on in `/plugin` → **Marketplaces** → `openvidu` →
**Enable auto-update**. How every other client updates, and how to configure
the server and the skill without a plugin, is on the
[documentation page](https://openvidu.io/latest/docs/coding-agents/agent-plugin/#install).

## What you get

| Component | What it is |
|---|---|
| `openvidu-docs` MCP server | OpenVidu's documentation, per version, at `https://docs-mcp.openvidu.io/mcp`. Its instructions also tell the agent when to read LiveKit's documentation for SDK detail, and what never to take from it |
| `openvidu-version-edition-product` skill | Establishes the version, edition and product your project targets when an answer depends on them, and pins them in `AGENTS.md` / `CLAUDE.md` |

What each tool does, and how LiveKit's documentation fits in:
[What's inside](https://openvidu.io/latest/docs/coding-agents/agent-plugin/#whats-inside).

## Try it

- "Using the OpenVidu docs, how do I record a room with individual tracks?"
- "Work out which OpenVidu version, edition and product this project uses, and
  write them into AGENTS.md."
- "Add a backend endpoint that creates an OpenVidu Meet room and returns the
  URL our frontend passes to the web component. Check the docs for our
  version."
- "Does the Egress service need S3 credentials, and how are they configured?"

## Data and privacy

The skill runs in your agent; only the MCP server is remote. Each request your
agent makes to it is logged as one line: the tool, what it asked for (for a
search, the search terms), the documentation version, the outcome and the
agent's name and version. What was asked is kept to learn what developers look
for and what the documentation is missing. Your conversation, your prompts and your code are
never sent. The IP address is used only to group a client's requests into a
visit and is never stored; logs are deleted after 7 days, and the archive,
which holds no addresses, after 395 days. Nothing is shared with third parties.
The details are in the
[privacy section](https://openvidu.io/latest/docs/coding-agents/agent-plugin/#privacy).

## Support

Report problems with the plugin, its skill or its server configuration in
[this repository's issues](https://github.com/OpenVidu/openvidu-agent-plugin/issues).
For help with OpenVidu itself, see [OpenVidu support](https://openvidu.io/support/).

## What's in the package

```text
plugin.json                     Agent Plugins 1.0 manifest
mcp.json                        the documentation MCP server (Streamable HTTP)
skills/                         one directory per skill, each with a SKILL.md
.claude-plugin/plugin.json      Claude Code manifest
.claude-plugin/marketplace.json Claude Code marketplace
.mcp.json                       Claude Code MCP config
assets/icon.png                 the plugin's icon
CHANGELOG.md                    what each version changed
LICENSE                         Apache 2.0
dev/                            not part of the plugin: how it is built,
                                validated and published
```

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
