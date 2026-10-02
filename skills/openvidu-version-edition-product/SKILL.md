---
name: openvidu-version-edition-product
description: Establish and record which OpenVidu deployment a project targets — version, edition (CE/PRO) and product (OpenVidu Platform or OpenVidu Meet) — in its AGENTS.md/CLAUDE.md, and use those three facts when answering. Use whenever the user asks about OpenVidu, or about rooms, tracks, recording, egress, ingress, webhooks, authentication or deployment in an OpenVidu project, and before stating any OpenVidu behaviour from memory.
compatibility: Requires the openvidu-docs MCP server (https://docs-mcp.openvidu.io/mcp) and network access.
---

# Answer OpenVidu questions against the right deployment

OpenVidu answers depend on three facts about the deployment the project talks
to, none of which are visible in the question itself:

- **version** — the documentation differs between releases (e.g. `3.9.0`).
- **edition** — `ce` or `pro`; PRO has features CE does not.
- **product** — **OpenVidu Platform** (the app uses the LiveKit SDKs) or
  **OpenVidu Meet** (REST API plus the `<openvidu-meet>` web component). Two
  different APIs.

Establish them **once** and write them down. Guessing produces confident
answers about a release the user isn't running, or about an edition they don't
have.

## 1. Look for them in the project first

Read `AGENTS.md`, `CLAUDE.md` and the README. If they are pinned there, use
them: no tool call needed.

## 2. Otherwise, find them only when the answer depends on them

Many answers are the same for every version, edition and product. Search with
the default version first: every response says which version answered and
whether the pages it returned change between versions.

When the answer does depend on them, call
**`resolve_openvidu_version_edition_product`** with no arguments. It returns the
current, complete procedure: how to tell Platform from Meet, where the
deployment URL and its credentials live, which endpoint reports version and
edition, what to do when that endpoint isn't available, and the security rules
to follow while doing it (credentials are never read or printed, remote hosts
are never contacted without asking). Follow that procedure — do not improvise
your own, and do not reproduce its steps here: the server is the single source
of truth for them. If you cannot follow it (no project, no deployment to query,
no user to ask), answer for the latest version and say which version, edition
and product you assumed.

## 3. Write them down

Once established, offer to pin them in `AGENTS.md` / `CLAUDE.md` so no future
session repeats the work. `resolve_openvidu_version_edition_product` returns
the block to paste (`agents_md_snippet`) — fill in whatever it left as a
placeholder. Record the three facts only: never a credential, and never a
secret's value.

## 4. Use them on every answer

Pass `version` explicitly to `search_docs`, `get_doc_page`,
`list_doc_sections` and `get_changelog` for the rest of the session. Pass the
release the deployment reports (`3.9.1`): documentation is published per minor,
so the server resolves it to `3.9` and says so. Read every result through the
edition and the product: a PRO-only feature does not
exist on CE, and Platform and Meet do the same thing through different APIs.
The index is versioned but knows nothing about edition or product, so that
part of the interpretation is yours — state which one you assumed whenever it
changes the answer.

If a version isn't indexed the tool fails and lists what is available. Say that
their release isn't indexed; answer from the closest indexed one only if you
label it as such.
