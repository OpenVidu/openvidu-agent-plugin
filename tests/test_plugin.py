"""The Agent Plugins package this repository publishes.

A plugin is only ever exercised by someone else's client, so these tests are
the only feedback loop before publishing: they validate the package against
the official Agent Plugins 1.0.0 schemas (vendored in scripts/schemas/, so the
suite stays offline), check the skill against the Agent Skills rules clients
enforce, and make sure the generated Claude Code files and the documentation
still agree on the endpoint.
"""

import json
from pathlib import Path

import pytest

import build_plugin as bp

REPO_ROOT = Path(__file__).resolve().parent.parent
# The repository root is the plugin root.
PLUGIN_DIR = REPO_ROOT


def read(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def manifest() -> dict:
    return read(PLUGIN_DIR / "plugin.json")


@pytest.fixture
def mcp() -> dict:
    return read(PLUGIN_DIR / "mcp.json")


# ---------------------------------------------------------------------------
# Conformance with Agent Plugins 1.0.0
# ---------------------------------------------------------------------------

def test_manifest_matches_the_official_schema(manifest):
    """The manifest schema is closed: an unknown field or a bad name is fatal
    to the whole plugin, not just to one component."""
    pytest.importorskip("jsonschema")
    bp.validate(manifest, "plugin", PLUGIN_DIR / "plugin.json")


def test_mcp_config_matches_the_official_schema(mcp):
    pytest.importorskip("jsonschema")
    bp.validate(mcp, "mcp", PLUGIN_DIR / "mcp.json")


def test_both_documents_target_the_same_spec_version(manifest, mcp):
    """§10.1: a version mismatch between the two invalidates the MCP half."""
    assert manifest["$schema"] == f"{bp.SCHEMA_BASE}/plugin.schema.json"
    assert mcp["$schema"] == f"{bp.SCHEMA_BASE}/mcp.schema.json"


def test_the_server_is_remote_and_encrypted(mcp):
    """Non-loopback endpoints MUST be HTTPS, and v1 has no portable secret
    mechanism: headers must not carry credentials."""
    for name, server in mcp["mcpServers"].items():
        assert server["type"] == "streamable-http", name
        assert server["url"].startswith("https://"), name
        assert "headers" not in server, f"{name}: no credentials belong in the package"


def test_skills_follow_the_agent_skills_rules():
    """Frontmatter `name` must equal the directory name, or clients skip the
    skill; description is capped at 1024 characters."""
    assert bp.check_skills() == ["openvidu-version-edition-product"]


@pytest.mark.parametrize("skill", ["openvidu-version-edition-product"])
def test_skill_description_says_when_to_use_it(skill):
    """The description is the only thing loaded before activation: it is what
    makes the model reach for the skill at the right moment."""
    front = bp.parse_frontmatter(PLUGIN_DIR / "skills" / skill / "SKILL.md")
    assert "use" in front["description"].lower()


def test_no_stray_component_locations():
    """`skills/` and `mcp.json` are fixed locations; a file where a directory
    is expected makes the client treat that component type as invalid."""
    assert (PLUGIN_DIR / "skills").is_dir()
    assert (PLUGIN_DIR / "mcp.json").is_file()
    assert (PLUGIN_DIR / "plugin.json").is_file()


# ---------------------------------------------------------------------------
# The generated Claude Code files
# ---------------------------------------------------------------------------

def test_generated_files_are_up_to_date():
    """Claude Code does not read the portable files, so these are generated.
    If this fails, run: python scripts/build_plugin.py"""
    bp.build(check_only=True)


def test_claude_transport_is_translated(mcp):
    """Claude Code spells Streamable HTTP `http`; shipping the portable
    `streamable-http` would leave the server silently unusable there."""
    generated = read(PLUGIN_DIR / ".mcp.json")
    for name, server in mcp["mcpServers"].items():
        assert generated["mcpServers"][name]["type"] == "http"
        assert generated["mcpServers"][name]["url"] == server["url"]


def test_claude_manifest_is_not_an_agent_plugins_document(manifest):
    generated = read(PLUGIN_DIR / ".claude-plugin" / "plugin.json")
    assert "$schema" not in generated, "Claude Code's manifest is its own format"
    assert generated["name"] == manifest["name"]
    assert generated["version"] == manifest["version"]


def test_marketplace_points_at_the_published_repository(manifest):
    catalog = read(PLUGIN_DIR / ".claude-plugin" / "marketplace.json")
    assert catalog["name"] == bp.MARKETPLACE_NAME
    entry, = catalog["plugins"]
    assert entry["name"] == manifest["name"]
    # A GitHub source rather than a relative path: relative paths do not
    # resolve when a marketplace is added by URL.
    assert entry["source"] == {"source": "github", "repo": "OpenVidu/openvidu-agent-plugin"}
    assert manifest["repository"].endswith(entry["source"]["repo"])


# ---------------------------------------------------------------------------
# Agreement with the documentation
# ---------------------------------------------------------------------------

DOCS_QUOTING_THE_ENDPOINT = [
    "README.md",
    "CLAUDE.md",
]


@pytest.mark.parametrize("doc", DOCS_QUOTING_THE_ENDPOINT)
def test_docs_quote_the_endpoint_the_plugin_ships(doc, mcp):
    """One wrong URL in one document sends users to a server that isn't there."""
    url = mcp["mcpServers"]["openvidu-docs"]["url"]
    text = (REPO_ROOT / doc).read_text(encoding="utf-8")
    assert url in text, f"{doc} does not mention {url}"


def test_install_commands_name_the_real_marketplace_and_plugin(manifest):
    """The two Claude Code commands in the docs have to match what the
    generated marketplace actually declares."""
    command = f"/plugin install {manifest['name']}@{bp.MARKETPLACE_NAME}"
    assert command in (REPO_ROOT / "README.md").read_text(encoding="utf-8")
