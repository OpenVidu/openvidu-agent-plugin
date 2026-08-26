---
name: openvidu-livekit-sdk-docs
description: Decide whether an answer comes from OpenVidu's documentation or from LiveKit's, and never mix them up. Use whenever a question about an OpenVidu project touches the client or server SDKs, the Agents framework, rooms, tracks, tokens, data messages, RPC, encryption or WebRTC transport — and before reading anything from docs.livekit.io.
---

# Two documentation sets, one of them authoritative

OpenVidu Platform is a fork of LiveKit and exposes **LiveKit-compatible
SDKs**: an OpenVidu app imports `livekit-client`, `livekit-server-sdk` and
their siblings. LiveKit documents those SDKs in far more depth than
openvidu.io does, so both servers are installed:

| Server | What it is |
|---|---|
| `openvidu-docs` | OpenVidu's own documentation, matched to the deployment's version, edition and product. **Authoritative.** |
| `livekit-docs` | LiveKit's documentation, operated by LiveKit. Deeper on SDK surface, wrong about everything else, and not versioned. |

## 1. Start with `openvidu-docs`. Always.

Search `openvidu-docs` first. Its `search_docs` may return a `livekit` block
naming the exact LiveKit page for the question, and that block carries the
version caveat — so going there first is also the fastest route to LiveKit
when LiveKit is the right answer.

## 2. `openvidu-docs` is the only authority on these

Do not answer from LiveKit's documentation, even if it looks similar, and do
not "confirm" an OpenVidu answer against it:

- **deployment and installation** — single node, elastic, high availability,
  Kubernetes, ports, TLS, scaling
- **configuration** — every setting, environment variable and config file
- **editions** — what COMMUNITY has and PRO does not, and licensing
- **OpenVidu Meet** — its REST API and the `<openvidu-meet>` component
- **recording, Egress and Ingress operations** as OpenVidu ships them
- **pricing** — `openvidu-docs` has `get_pricing_info`; LiveKit's tool of the
  same name returns **LiveKit Cloud** plans, which do not exist here
- **observability, dashboards, troubleshooting**

## 3. Use `livekit-docs` for SDK surface and self-hostable components

Reach for it when `openvidu-docs` does not cover the detail and the question
is about code the app writes, or about a LiveKit component the user can run
themselves:

- client SDK API reference — classes, enums, options, events
- server SDK API reference — token minting, room service calls
- the Agents framework — sessions, tools, turn detection, pipelines, plugins
- WebRTC transport concepts — data messages, RPC, byte streams, encryption,
  frame metadata, simulcast, adaptive stream
- **telephony and SIP** — trunks, dispatch rules, DTMF, transfers, the SIP
  APIs, and the per-provider trunk guides. `livekit/sip` is Apache-2.0 and
  self-hostable, and **OpenVidu ships no SIP service**, so running it yourself
  is the only route to telephony. `/transport/self-hosting/sip-server` is how.
- **the `lk` CLI** — Apache-2.0, and it works against a self-hosted server: a
  CLI "project" is just a URL, API key and secret. Useful well beyond Cloud
  management — room and token commands, SIP configuration, load testing, app
  templates, and `lk docs` for reading the docs from a shell.
- **the agent tooling** — the Agent Console debugs agents "running anywhere,
  including self-hosted and local"; the Agent Builder emits portable Agents
  SDK code; and `/deploy/custom/deployments` covers running agent workers on
  your own infrastructure.
- **LiveKit Portal** — its API "works with any robotics stack".

## 4. Never bring these back from LiveKit

These describe a service the user is not paying for and cannot run:

- **LiveKit Cloud itself** — `cloud.livekit.io`, the Cloud dashboard, Cloud
  projects, `lk cloud` authentication, sandbox tokens, billing, quotas,
  regions, and LiveKit's `get_pricing_info`
- **LiveKit Inference** — their managed model hosting. On a provider page, the
  "LiveKit Inference" section does not apply; the "Plugin" section, where you
  supply your own API key, does.
- **Cloud agent hosting** — deploying an agent *to* LiveKit Cloud with
  `lk agent deploy`, and the Cloud builds, logs and insights around it. Use
  the self-hosted deployment page instead.
- **LiveKit Phone Numbers** — numbers bought from LiveKit. Bring your own SIP
  trunk provider instead.
- **deploying the LiveKit media server** — `/transport/self-hosting/*` other
  than the SIP server: Kubernetes, VMs, ports, benchmarking. OpenVidu's
  deployment documentation replaces all of it.

The distinction to hold on to: **can the user run this themselves?** SIP, the
CLI, Portal and the agent framework all pass that test even though their pages
mention Cloud constantly. Managed inference, hosted agents and bought phone
numbers do not.

If a LiveKit page mentions a `LIVEKIT_URL` on `*.livekit.cloud`, substitute
the user's own OpenVidu URL and say you did.

## 5. Check the version before you promise a feature

**LiveKit's documentation is not versioned**: it describes LiveKit's current
release. An OpenVidu deployment runs the LiveKit its release bundled — 1.12.0
on OpenVidu 3.8.0, older further back.

- Establish the deployment first: see the
  `openvidu-version-edition-product` skill and
  `resolve_openvidu_version_edition_product`. That tool also maps a LiveKit
  Server version to OpenVidu versions and back.
- **Client SDK surface** is stable across these versions and generally applies
  as written.
- **Server behaviour** may not: new `RoomService` options, configuration
  flags, webhook fields, Egress and Ingress capabilities. Say a feature "is
  documented by LiveKit for a newer server than this deployment bundles"
  rather than presenting it as available.

## 6. Attribute it

When an answer comes from LiveKit's documentation, say so and link the page.
It is LiveKit's documentation about LiveKit, offered because the SDKs are
compatible — not an OpenVidu guarantee. `livekit-docs` is operated by LiveKit,
not by OpenVidu, and its terms and availability are theirs.
