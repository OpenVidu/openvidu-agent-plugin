# Working on this repository

This repository **is** an [Agent Plugins 1.0](https://agent-plugins.org)
package: its root is the plugin root, because that is the location every
client installs from. It holds the package and nothing else. The tooling that
builds and validates it is kept by the OpenVidu team outside this repository,
because Anthropic's directory refuses a plugin folder that carries anything
other than documents, data and images.

Portable first: this file is the one agents read, Claude Code included (it
reads `AGENTS.md` when there is no `CLAUDE.md`). There is deliberately no
`CLAUDE.md`: at the plugin root it also fails `claude plugin validate
--strict`, since a plugin's context ships in skills, not there. For the same
reason the package ships portable `plugin.json` + `mcp.json` and *generates*
Claude Code's files from them.

Five invariants that are load-bearing:

- **Never hand-edit `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json` or `.mcp.json`.** Claude Code does not
  implement Agent Plugins and reads only those paths, so they are generated
  from `plugin.json` and `mcp.json`, which hold the version and the endpoint.
  Change the portable files; the generated ones are regenerated from them.
- **Bump `version` in `plugin.json` for any change to the package**, and add
  its entry to `CHANGELOG.md`. Clients use the version to decide whether an
  update exists, so a change published without a bump reaches nobody.
- **Only package files in this repository**: Markdown, plain text, JSON, YAML
  and PNG, JPEG, GIF, WebP or ICO images. No scripts, tests, build or package
  manager configuration: Anthropic's directory refuses the whole version over
  one such file.
- **A skill is `skills/<name>/SKILL.md`**, with a frontmatter `name` equal to
  the directory name and a `description` that says when to use it.
- **The endpoint in `mcp.json` is not this repository's.** It is the
  documentation server the OpenVidu team operates. Changing it is a major
  version bump, and breaks every existing install until the new version
  reaches it.

The documentation for users is on openvidu.io, at
<https://openvidu.io/latest/docs/building-with-ai/agent-plugin/>, which is
what `plugin.json`'s `homepage` points at. A change to `mcp.json` or `skills/`
has a second half there, and `README.md` must keep quoting the endpoint and
the Claude Code install command.
