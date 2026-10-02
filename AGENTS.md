# Working on this repository

This repository **is** an [Agent Plugins 1.0](https://agent-plugins.org)
package: its root is the plugin root, because that is the location every
client installs from. The development documentation — layout, naming,
versioning, how to add a skill, how to publish — is
**[`dev/README.md`](dev/README.md)**. Read it before changing anything
structural.

Portable first: this file is the one agents read, Claude Code included (it
reads `AGENTS.md` when there is no `CLAUDE.md`). There is deliberately no
`CLAUDE.md`: at the plugin root it also fails `claude plugin validate
--strict`, since a plugin's context ships in skills, not there. For the same
reason the package ships portable `plugin.json` + `mcp.json` and *generates*
Claude Code's files from them.

Four invariants that are load-bearing. Everything else is in `dev/README.md`.

- **Never hand-edit `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json` or `.mcp.json`.** They are generated from
  `plugin.json` and `mcp.json` by `python build_plugin.py`, run from `dev/`,
  because Claude Code does not implement Agent Plugins: it reads only those
  paths. `build_plugin.py --check` runs in the test suite and will fail on a
  hand edit.
- **Bump `version` in `plugin.json` for any change to the package.** Clients
  use it to decide whether an update exists, so a change published without a
  bump reaches nobody.
- **Keep the root clean.** Package files at the root, tooling and development
  docs under `dev/` — and run the tooling from there, or `pytest` finds no
  configuration. A new skill goes in `skills/<name>/`, not under `dev/`.
- **The endpoint in `mcp.json` is not this repository's.** It is the
  documentation server the OpenVidu team operates. Changing it is a major
  version bump, and breaks every existing install until the new version
  reaches it.

```bash
cd dev
pip install -r requirements.txt
python build_plugin.py    # validate + regenerate
pytest
```
