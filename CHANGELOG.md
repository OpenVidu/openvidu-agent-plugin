# Changelog

## 1.0.1

- The plugin no longer carries its development tooling: the package holds
  only what clients load. The server and the skill are unchanged.

## 1.0.0

The first public release.

- The `openvidu-docs` MCP server, `https://docs-mcp.openvidu.io/mcp`: the
  OpenVidu documentation for every release from 3.4, matched to the version
  the project's deployment runs.
- The `openvidu-version-edition-product` skill: finds out which OpenVidu the
  project targets when an answer depends on it, and pins it in `AGENTS.md` or
  `CLAUDE.md`.
