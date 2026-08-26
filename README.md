# OpenVidu Agent Plugin

[OpenVidu](https://openvidu.io) is an open-source, self-hosted platform for
building real-time video conferencing and WebRTC applications, built on top
of [LiveKit](https://livekit.io) and mediasoup. It's developed by a team with
over a decade building WebRTC systems — see [About Us](https://openvidu.io/about-us/).

This plugin gives your coding agent direct access to the official OpenVidu
documentation (<https://openvidu.io/latest/docs/>) — instead of guessing from
whatever it memorised during training, it searches and reads the real pages,
**for the OpenVidu deployment you are actually running**: the right version,
read for the right edition and the right product.

It is both an [Agent Plugins 1.0](https://agent-plugins.org) package and a
[Claude Code plugin](https://code.claude.com/docs/en/plugins). What you get is
two kinds of component, and they are worth telling apart:

- **MCP servers** — where the documentation comes from: the agent searches
  them and reads pages out of them. `openvidu-docs` serves OpenVidu's own
  documentation for the version you are actually running; `livekit-docs` is
  LiveKit's own public server, included because OpenVidu Platform exposes
  LiveKit-compatible SDKs and LiveKit documents them in more depth. See
  [The documentation servers](#the-documentation-server) and
  [Why LiveKit's docs are here too](#why-livekits-docs-are-here-too).
- **skills** — procedures the agent loads when a task calls for one, so it
  works the way an OpenVidu project needs instead of improvising. See
  [The skills](#the-skills).

## Installation

Find your tool below. One caveat first:
[Agent Plugins 1.0](https://agent-plugins.org) was only published on 11 August
2026, so support for it is new everywhere — if the commands below do nothing,
update your client before assuming something is broken. Claude Code is the
exception: its plugin format is its own and predates the standard.

### Claude Code

```
/plugin marketplace add anthropics/claude-plugins-community
/plugin install openvidu@claude-community
```

Anthropic-maintained marketplaces auto-update by default, so that is the route
to prefer — see [Keeping the plugin updated](#keeping-the-plugin-updated).
If it isn't in
[the catalog](https://github.com/anthropics/claude-plugins-community/blob/main/.claude-plugin/marketplace.json)
yet, `/plugin marketplace add OpenVidu/openvidu-agent-plugin` and then
`/plugin install openvidu@openvidu` installs it straight from this repository,
without the auto-updates.

### VS Code

Enable plugins once (`"chat.plugins.enabled": true` in settings), then run
**Chat: Install Plugin From Source** from the Command Palette and paste:

```
https://github.com/OpenVidu/openvidu-agent-plugin
```

### Cursor

Clone the repository into Cursor's local plugin folder and restart:

```bash
git clone https://github.com/OpenVidu/openvidu-agent-plugin \
  ~/.cursor/plugins/local/openvidu
```

Teams can instead import the repository as a marketplace from
**Dashboard → Plugins → Add Marketplace → Import from Repo**, which makes it
installable from **Customize** in the sidebar.

### GitHub Copilot

Copilot installs plugins from a repository with `copilot plugin install` (or
the `/plugin install` slash command), and declaratively through the
`enabledPlugins` field of `~/.copilot/settings.json` or
`.github/copilot/settings.json`. See
[About plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
for the exact syntax in your Copilot version.

### Kiro

Install from the repository, or find it in **kiro.dev/powers** — Kiro loads
Agent Plugins packages as powers. See the
[Kiro powers documentation](https://kiro.dev/docs/powers/).

### ChatGPT & Codex

Codex loads Agent Plugins packages; follow
[the OpenAI plugin documentation](https://developers.openai.com/plugins) and
point it at this repository.

### Any other Agent Plugins client

Clone the repository and point the client at the directory. The
[compatible clients list](https://agent-plugins.org/compatible-clients) says
which clients implement the standard and which components each of them loads.

### Not there, or not installing anything

Configure the components yourself:
**[Setting it up without the plugin](docs/manual-setup.md)** — the same server
and skills, set up by hand. You can move to the plugin later.

## Keeping the plugin updated

An update carries whatever is inside the package — the skills, and the server
address. The server behind that address is versioned per documentation release
(see [The documentation server](#the-documentation-server)), not per plugin
release, so the endpoint itself never goes stale.

A [hand-configured setup](docs/manual-setup.md) behaves differently: copies do
not update, and nothing tells you when the originals move on. That page says
what to re-do.

How you get a new plugin version depends entirely on the client, and on
*how* you added it:

- **Claude Code.** Updates in the background after each session starts (up to
  a 10-minute random delay), because Anthropic-maintained marketplaces
  auto-update by default. A detected update needs `/reload-plugins` to take
  effect in a running session, or your next launch.
- **VS Code.** Run **Extensions: Check for Extension Updates** from the
  Command Palette, or let it happen automatically every 24 hours if
  `extensions.autoUpdate` is enabled — the same setting that governs regular
  extension updates, not something specific to this plugin.
- **Cursor.** A plugin cloned manually into
  `~/.cursor/plugins/local/openvidu` is never updated for you: `git pull`
  the clone yourself and restart Cursor. A plugin installed from a team
  marketplace updates on its own only if an admin turned on **Enable Auto
  Refresh** for that marketplace (push-based, so it lands within about 10
  minutes of a new commit); otherwise someone has to click **Refresh** in
  the marketplace dashboard.
- **GitHub Copilot.** `copilot plugin update openvidu` (or `--all` for
  everything installed). Automatic updates at the start of each session are
  a first-party-plugin behavior; for a plugin from a marketplace like ours,
  they only happen if that marketplace's own configuration sets
  `autoUpdate: true` — otherwise it's the manual command above, or
  `copilot plugin marketplace update` to refresh the catalog first.
- **Kiro.** Manual only: open the **Powers** panel, select the plugin, and
  run **Check for updates** → **Install updates**. Kiro doesn't poll for
  updates on its own.
- **ChatGPT & Codex.** `codex plugin marketplace upgrade` (or with a
  marketplace name, to target just this one).
- **Any other Agent Plugins client.** Pull the repository again and reload
  the client; whether it does this for you is client-specific — check the
  [compatible clients list](https://agent-plugins.org/compatible-clients).

## What's in the package

```text
plugin.json                     Agent Plugins 1.0 manifest
mcp.json                        the two documentation MCP servers (Streamable HTTP)
skills/                         one directory per skill, each with a SKILL.md
.claude-plugin/plugin.json      Claude Code manifest
.claude-plugin/marketplace.json Claude Code marketplace
.mcp.json                       Claude Code MCP config
LICENSE                         Apache 2.0
docs/manual-setup.md            setting the same components up by hand
dev/                            not part of the plugin: how it is built,
                                validated and published
```

## What OpenVidu are you developing your app for?

Every answer this package produces depends on it, and nothing in the package
can work it out alone: **a remote server cannot see your project**, and a skill
only knows what your repository tells it. Three facts have to come from your
side:

- **version** — the documentation differs between releases. It is what the
  documentation server indexes by.
- **edition** — CE or PRO; PRO has features CE does not.
- **product** — OpenVidu Platform (your app uses the LiveKit SDKs) or
  OpenVidu Meet (its REST API and the `<openvidu-meet>` web component). Two
  different APIs.

Without them the answers don't get vaguer, they get confidently wrong — right
documentation for a release you aren't running, or a feature that only exists
in the edition you don't have. It is also why this sits outside both
components rather than inside either: the documentation server indexes by
version and knows nothing at all about edition or product, and a skill can only
act on what it has been told. Establish the three, write them down, and
everything downstream is aimed at the same target.

### Finding them out

Ask your coding agent to work it out and it will.

**Do not read the version off your dependencies**, and don't let your coding
agent do it either. `livekit-client`, `livekit-server-sdk` and the web
components are *client* SDKs; their version numbers have no relationship with
the OpenVidu server's, and they say nothing about CE vs PRO. The server's tool
descriptions tell the model this explicitly, but it is worth knowing yourself.

### Write the version, edition and product in AGENTS.md

So you don't repeat it in every conversation, put this in your project's
`AGENTS.md` or `CLAUDE.md`:

```markdown
This project connects to an OpenVidu 3.9.0 pro deployment, using OpenVidu Meet.
When querying the OpenVidu documentation MCP, always pass version="3.9.0",
and read the answers for that edition and product.
```

Look before you write it, though: a coding agent asked to work the three out
will often have added them already. And facts only — never put credentials in
that file.

## The documentation server

This section is about `openvidu-docs`. For `livekit-docs`, see
[Why LiveKit's docs are here too](#why-livekits-docs-are-here-too).

Everything under this heading concerns one component: the `openvidu-docs` MCP
server, which is what carries the documentation. None of it applies to
[the skills](#the-skills).

### Server URL

```
https://docs-mcp.openvidu.io/mcp
```

Transport: **Streamable HTTP**. No API key, no login required.

### Available tools

| Tool | What it does |
|---|---|
| `search_docs` | Searches the documentation. Handles word variants (*record* finds *recording*) and OpenVidu vocabulary (*auth* finds *authentication*) |
| `get_doc_page` | Returns the full content of a page |
| `list_doc_sections` | The table of contents: which pages exist, grouped by section |
| `list_versions` | Which documentation versions this server has indexed, and which one it uses by default |
| `resolve_openvidu_version_edition_product` | How to find out which deployment your project talks to: version, edition (CE/PRO) and product (Platform/Meet). Also maps a LiveKit Server version to OpenVidu version(s) |
| `get_changelog` | The release notes for a version, without having to find the page first. Takes an optional product (*meet*, *platform*) |
| `get_pricing_info` | The pricing page: editions, plans, and the cost model. The same for every version |

You don't call these yourself — your coding agent does, when the conversation
needs them.

### How the server handles the version

- Every tool takes an optional `version`. Without it, the newest indexed
  version is used.
- Ask for a version that isn't indexed and it **fails, listing the ones it
  has**. It will never quietly answer with a different version — documentation
  for the wrong release is worse than none.
- Every answer says which version it used, and flags pages that actually
  differ between versions (pages identical across all of them say so, so the
  warning means something when it appears).

The version is what you pass to the server — the only one of the three the
index carries. The edition and the product guide the coding agent instead:
what to search for, and how to read what comes back. See
[What OpenVidu are you developing your app for?](#what-openvidu-are-you-developing-your-app-for).

### Example prompts

- "Using the OpenVidu docs MCP, how do I record a room with individual tracks?"
- "What does OpenVidu documentation say about deploying with fault tolerance?
  We're on 3.8.0."
- "Check the OpenVidu docs before answering: does the egress service need S3
  credentials, and how are they configured?"
- "Work out which OpenVidu version, edition and product this project uses, and
  write it into CLAUDE.md."
- "Our LiveKit server reports 1.9.8 — which OpenVidu version is that, and is
  the docs server carrying it?"
- "List the sections of the OpenVidu documentation so I can see what's there."

### Checking it works

With Claude Code:

```bash
claude mcp list          # openvidu-docs should appear as connected
```

If you installed the plugin, `/plugin` lists it as enabled and its **Errors**
tab is where a failed MCP connection shows up.

Or straight against the endpoint:

```bash
curl -s -X POST https://docs-mcp.openvidu.io/mcp \
  -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

You should get a JSON-RPC response listing the seven tools.

## The skills

A skill is instructions rather than tools: a directory with a `SKILL.md` that
the agent loads when its description matches what you asked. They live in
[`skills/`](skills/) in this repository, in the
[Agent Skills](https://agentskills.io) format.

| Skill | What it does |
|---|---|
| `openvidu-version-edition-product` | Establishes the three facts every OpenVidu answer depends on — version, edition and product — and writes them into your `AGENTS.md` / `CLAUDE.md`, so they are settled once instead of every session. The reasoning is in [What OpenVidu are you developing your app for?](#what-openvidu-are-you-developing-your-app-for) |
| `openvidu-livekit-sdk-docs` | Decides which of the two documentation servers answers a given question, so LiveKit's docs are used for SDK detail and never for deployment, configuration, editions or pricing. See [Why LiveKit's docs are here too](#why-livekits-docs-are-here-too) |

## Why LiveKit's docs are here too

OpenVidu Platform is a fork of LiveKit and your app imports the LiveKit
client and server SDKs directly — `livekit-client`, `livekit-server-sdk` and
their siblings. LiveKit's own documentation covers that SDK surface in far
more depth than openvidu.io does: the full API reference, the Agents
framework, the WebRTC transport details.

So the package pre-configures **LiveKit's own public MCP server**
(<https://docs.livekit.io/mcp>) alongside OpenVidu's. This is the same setup
LiveKit documents on its
[Coding agent support](https://docs.livekit.io/intro/coding-agents/) page —
your agent talks to LiveKit directly, and nothing of LiveKit's is copied,
cached or served by OpenVidu. That server is **operated by LiveKit, not by
OpenVidu**: its availability and its terms are theirs.

Two things to know, both of which the `openvidu-livekit-sdk-docs` skill
enforces so you do not have to:

**OpenVidu's documentation wins on anything that is not SDK surface.**
Deployment, installation, configuration, editions (COMMUNITY vs PRO),
OpenVidu Meet, recording as OpenVidu ships it, observability and pricing are
all answered by `openvidu-docs`, and LiveKit's documentation is wrong about
them here. Watch out for pricing in particular: **both servers expose a tool
called `get_pricing_info`**, and LiveKit's returns LiveKit Cloud plans, which
have nothing to do with a self-hosted OpenVidu.

The line is **"can you run this yourself?"**, not "does the page mention
Cloud". LiveKit Cloud itself, LiveKit Inference (their managed model hosting),
deploying an agent *to* Cloud, and phone numbers bought from LiveKit are all
out — you cannot run any of them. But **SIP telephony, the `lk` CLI, LiveKit
Portal and the agent tooling are all in**, because each works against a
self-hosted server even though its pages talk about Cloud throughout. SIP
matters especially: OpenVidu ships no SIP service, so running LiveKit's
Apache-2.0 [`livekit/sip`](https://github.com/livekit/sip) yourself is the
route to telephony, and LiveKit's docs are where that is written down.

**LiveKit's documentation is not versioned.** It always describes LiveKit's
current release, while your deployment runs the LiveKit its OpenVidu release
bundled — LiveKit Server 1.12.0 on OpenVidu 3.8.0, and older further back.
The client SDK surface is stable and generally applies as written; anything
that depends on server behaviour (new `RoomService` options, configuration
flags, webhook fields, Egress and Ingress capabilities) may not exist in your
version yet. `resolve_openvidu_version_edition_product` on `openvidu-docs`
maps between the two version numbers in both directions.

If you would rather not have LiveKit's server configured, remove the
`livekit-docs` entry from your client's MCP configuration; nothing else in the
package depends on it.

## Troubleshooting

**The plugin installed but no OpenVidu tools appear.** Not every client that
loads Agent Plugins loads every component: check that yours supports MCP
servers in plugins on the
[compatible clients list](https://agent-plugins.org/compatible-clients). If it
only loads skills, add the server by hand instead:
[Setting it up without the plugin](docs/manual-setup.md#the-mcp-server).

**A skill never activates.** If you installed the plugin, check the same
[compatible clients list](https://agent-plugins.org/compatible-clients) for
whether your client loads skills from plugins — several load MCP servers and
not skills. If you copied it in by hand, the two things that go wrong are the
directory name, which must equal the `name` in that skill's frontmatter or
clients skip it in silence, and the location; both are covered in
[Setting it up without the plugin](docs/manual-setup.md#the-skills). It is also
possible the skill loaded and had nothing to do — one whose work is already
done stays quiet, which is not a fault.

**The client shows the server as failed or offline.** Check the transport is
HTTP, not `sse` or `stdio`; this server is Streamable HTTP only. And the URL
ends in `/mcp`.

**Opening the URL in a browser gives an error.** That is expected: the server
only accepts `POST` and answers `405` to anything else. It is not a web page.
For the same reason a browser-based client won't work — there is no CORS
preflight.

**The answers are for the wrong version.** Pass `version` explicitly, or pin
it in `AGENTS.md`/`CLAUDE.md` as shown above. Ask your coding agent to run
`list_versions` to see what is indexed.

**A page you know exists isn't found.** The index covers what the OpenVidu
`llms.txt` lists, and it is rebuilt when the documentation changes, not
continuously — a page published minutes ago may not be there yet.

## Source

This repository is what gets installed: the plugin manifest, the MCP server
configuration, and the skills. Report issues with any of those here. The
documentation server behind the MCP endpoint is maintained separately by the
OpenVidu team.

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
