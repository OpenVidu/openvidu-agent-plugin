# Vendored Agent Plugins schemas

Verbatim copies of the Agent Plugins 1.0.0 schemas, downloaded from:

- <https://agent-plugins.org/schemas/1.0.0/plugin.schema.json>
- <https://agent-plugins.org/schemas/1.0.0/mcp.schema.json>

They are vendored so `dev/build_plugin.py` and the test suite can validate
this package **offline** — the tests in this repository never touch the network.
The specification itself tells clients not to fetch schemas at load time, so
this is also what a conformant loader does.

Published canonical schema identifiers are immutable ("Published canonical
schema identifiers MUST NOT be reassigned to different schema contents",
§10.1), so these files only change when the plugin targets a new Agent Plugins
version — in which case add the new files alongside and update
`AGENT_PLUGINS_VERSION` in `dev/build_plugin.py`.
