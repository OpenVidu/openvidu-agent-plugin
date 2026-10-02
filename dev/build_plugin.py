"""
Generates the client-specific files of the Agent Plugin from the portable ones.

This repository IS the Agent Plugins 1.0 package: `plugin.json`, `mcp.json`,
and `skills/` sit at its root, which is what every client on
https://agent-plugins.org/compatible-clients reads directly.

Claude Code does NOT implement Agent Plugins: it reads the manifest at
`.claude-plugin/plugin.json` and MCP servers at `.mcp.json`, and ignores the
root `mcp.json`. It accepts `streamable-http` as an alias of `http` there, but
Anthropic's plugin directory accepts only `http`, `sse` and `ws` for a remote
server, so the generated file spells it `http`. Rather than ask OpenVidu users
on Claude Code to configure the server by hand, the package ships those files
too, GENERATED from the portable pair so the endpoint URL and the version exist
in exactly one place.

The generated manifest also carries the listing fields Anthropic's directory
shows (display name, icon, documentation, support and privacy URLs), which the
portable manifest's closed schema has no room for. The same generation writes
`.claude-plugin/marketplace.json`, which turns this repository into a
one-command install for Claude Code.

Deliberate deviation: §8 of the specification says client-specific files
belong under a reverse-domain directory (`com.anthropic.claude-code/`). Claude
Code only looks at the root, so the generated files sit at the root. No
Agent Plugins client rejects extra files, and the portable trio is untouched.

Usage, from the dev/ directory:
    python build_plugin.py            # validate and regenerate
    python build_plugin.py --check    # fail if anything is stale
"""

import argparse
import json
import re
import sys
from pathlib import Path

# dev/build_plugin.py -> the repository root.
REPO_ROOT = Path(__file__).resolve().parent.parent
# The repository root is the plugin root: every client installs an Agent Plugin
# from a location whose ROOT is the package.
PLUGIN_DIR = REPO_ROOT
SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"

AGENT_PLUGINS_VERSION = "1.0.0"
SCHEMA_BASE = f"https://agent-plugins.org/schemas/{AGENT_PLUGINS_VERSION}"

# Name of the Claude Code marketplace users add. Public-facing: it is the part
# after the '@' in `/plugin install openvidu@openvidu`.
MARKETPLACE_NAME = "openvidu"

# The generated files carry no "do not edit" comment: Claude Code's manifest
# and marketplace schemas are validated field by field, and an unrecognized key
# shows up as a validation warning. `--check` (wired into the test suite) is
# what actually stops a hand edit from surviving.

# Claude Code's listing fields. The URLs derive from `homepage` and
# `repository`; a marketplace entry must not carry any of them.
DISPLAY_NAME = "OpenVidu"
ICON = "assets/icon.png"

# Portable transport -> Claude Code transport.
TRANSPORT_MAP = {"streamable-http": "http", "sse": "sse"}


class PluginError(Exception):
    """A problem with the plugin package, reported as a message."""


# ---------------------------------------------------------------------------
# Validation against the vendored schemas
# ---------------------------------------------------------------------------

def load_schema(kind: str) -> dict:
    path = SCHEMA_DIR / f"{kind}-{AGENT_PLUGINS_VERSION}.schema.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate(document: dict, kind: str, source: Path) -> None:
    """Validates against the vendored copy of the official schema.

    Vendored, not fetched: the tests run without network, and the
    specification tells clients not to retrieve schemas while loading a
    plugin either.
    """
    try:
        import jsonschema  # noqa: PLC0415 - optional, only needed at build time
    except ImportError:
        print("  (jsonschema not installed: skipping schema validation)")
        return
    errors = sorted(
        jsonschema.Draft202012Validator(load_schema(kind)).iter_errors(document),
        key=lambda e: list(e.path),
    )
    if errors:
        detail = "\n".join(
            f"  - {'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}"
            for e in errors
        )
        raise PluginError(f"{source.name} does not satisfy the {kind} schema:\n{detail}")


def read_portable() -> tuple[dict, dict]:
    """Reads and validates plugin.json and mcp.json."""
    manifest_path, mcp_path = PLUGIN_DIR / "plugin.json", PLUGIN_DIR / "mcp.json"
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)
    with open(mcp_path, encoding="utf-8") as f:
        mcp = json.load(f)

    validate(manifest, "plugin", manifest_path)
    validate(mcp, "mcp", mcp_path)

    # §10.1: the two documents must target the same Agent Plugins version.
    if manifest["$schema"] != f"{SCHEMA_BASE}/plugin.schema.json":
        raise PluginError(f"plugin.json targets an unexpected schema: {manifest['$schema']}")
    if mcp["$schema"] != f"{SCHEMA_BASE}/mcp.schema.json":
        raise PluginError(f"mcp.json targets an unexpected schema: {mcp['$schema']}")
    return manifest, mcp


def check_skills() -> list[str]:
    """Checks each skill against the Agent Skills rules that clients enforce."""
    skills_dir = PLUGIN_DIR / "skills"
    if not skills_dir.is_dir():
        return []
    found = []
    for child in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            raise PluginError(f"skills/{child.name}/ has no SKILL.md")
        front = parse_frontmatter(skill_md)
        if front.get("name") != child.name:
            raise PluginError(
                f"skills/{child.name}/SKILL.md declares name "
                f"'{front.get('name')}': it must match the directory name"
            )
        description = front.get("description", "")
        if not 1 <= len(description) <= 1024:
            raise PluginError(
                f"skills/{child.name}: description must be 1-1024 characters "
                f"(it is {len(description)})"
            )
        found.append(child.name)
    return found


def parse_frontmatter(path: Path) -> dict:
    """Reads the `key: value` YAML frontmatter of a SKILL.md.

    Deliberately minimal: the Agent Skills frontmatter this plugin uses is
    flat single-line fields, and this keeps the check dependency-free.
    """
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise PluginError(f"{path} does not start with YAML frontmatter")
    fields = {}
    for line in match.group(1).splitlines():
        if field := re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line):
            fields[field.group(1)] = field.group(2).strip()
    return fields


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def claude_manifest(manifest: dict) -> dict:
    """Claude Code's `.claude-plugin/plugin.json`.

    Same metadata as the portable manifest, plus the listing fields; `$schema`
    is dropped because Claude Code's manifest is not an Agent Plugins document.
    """
    if not (PLUGIN_DIR / ICON).is_file():
        raise PluginError(f"{ICON} is missing: the Claude Code manifest points at it")
    out = {"name": manifest["name"], "displayName": DISPLAY_NAME}
    for key in ("description", "version", "author", "homepage",
                "repository", "license", "keywords"):
        if key in manifest:
            out[key] = manifest[key]
    out["icon"] = f"./{ICON}"
    out["documentationUrl"] = manifest["homepage"]
    out["supportUrl"] = f"{manifest['repository']}/issues"
    out["privacyPolicyUrl"] = f"{manifest['homepage']}#privacy"
    return out


def claude_mcp(mcp: dict) -> dict:
    """Claude Code's `.mcp.json`, translated from the portable configuration."""
    servers = {}
    for name, server in mcp["mcpServers"].items():
        kind = server["type"]
        if kind in TRANSPORT_MAP:
            entry = {"type": TRANSPORT_MAP[kind], "url": server["url"]}
            if "headers" in server:
                entry["headers"] = server["headers"]
        elif kind == "stdio":
            entry = {k: v for k, v in server.items() if k != "type"}
            if json.dumps(entry).find("${PLUGIN_DATA}") != -1:
                raise PluginError(
                    f"server '{name}' uses ${{PLUGIN_DATA}}, which has no Claude Code "
                    "equivalent: translate it by hand before shipping"
                )
            # Claude Code spells the plugin root differently.
            entry = json.loads(
                json.dumps(entry).replace("${PLUGIN_ROOT}", "${CLAUDE_PLUGIN_ROOT}")
            )
        else:
            raise PluginError(f"server '{name}' has an unsupported type: {kind}")
        servers[name] = entry
    return {"mcpServers": servers}


def marketplace(manifest: dict) -> dict:
    """Claude Code marketplace catalog, so the published repository installs
    with two commands.

    The plugin source is the repository's **HTTPS clone URL**, not a relative
    path and not `{"source": "github"}`: relative paths don't resolve when a
    marketplace is added by URL, and the `github` form makes Claude Code clone
    over SSH (`git@github.com:`), which fails for anyone without a GitHub SSH
    key — most people installing a documentation plugin. Every entry in
    Anthropic's own marketplace uses an HTTPS URL or a path for this reason.
    """
    repo = manifest.get("repository", "")
    match = re.match(r"^https://github\.com/([^/]+/[^/.]+)", repo)
    if not match:
        raise PluginError(
            f"repository must be a github.com URL to build the marketplace entry: {repo!r}"
        )
    entry = {
        "name": manifest["name"],
        "source": {"source": "url", "url": f"https://github.com/{match.group(1)}.git"},
    }
    for key in ("description", "version", "author", "homepage", "repository",
                "license", "keywords"):
        if key in manifest:
            entry[key] = manifest[key]
    return {
        "name": MARKETPLACE_NAME,
        "owner": manifest.get("author", {"name": manifest["name"]}),
        "description": manifest.get("description", ""),
        "plugins": [entry],
    }


def generated_files(manifest: dict, mcp: dict) -> dict:
    return {
        PLUGIN_DIR / ".claude-plugin" / "plugin.json": claude_manifest(manifest),
        PLUGIN_DIR / ".mcp.json": claude_mcp(mcp),
        PLUGIN_DIR / ".claude-plugin" / "marketplace.json": marketplace(manifest),
    }


def serialize(document: dict) -> str:
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"


def build(check_only: bool = False) -> list[Path]:
    """Validates the package and writes the generated files.

    Returns the files that are (or would be) written.
    """
    manifest, mcp = read_portable()
    skills = check_skills()
    stale = []
    for path, document in generated_files(manifest, mcp).items():
        wanted = serialize(document)
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == wanted:
            continue
        stale.append(path)
        if not check_only:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(wanted, encoding="utf-8")

    if check_only and stale:
        names = ", ".join(p.relative_to(REPO_ROOT).as_posix() for p in stale)
        raise PluginError(
            f"generated files are out of date ({names}). "
            "Run, from dev/: python build_plugin.py"
        )

    print(f"Plugin '{manifest['name']}' v{manifest.get('version', '?')} "
          f"targeting Agent Plugins {AGENT_PLUGINS_VERSION}")
    print(f"  servers: {', '.join(mcp['mcpServers'])}")
    print(f"  skills:  {', '.join(skills) if skills else '(none)'}")
    for path in generated_files(manifest, mcp):
        mark = "written" if path in stale else "up to date"
        print(f"  {path.relative_to(REPO_ROOT).as_posix():42} {mark}")
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true",
                        help="fail instead of writing if the generated files are stale")
    args = parser.parse_args()
    try:
        build(check_only=args.check)
    except PluginError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
