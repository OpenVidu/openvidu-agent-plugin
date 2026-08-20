# Submitting the plugin to Anthropic's Claude Code marketplace

This is about getting this plugin (see [`README.md`](README.md)) listed
in one of the marketplaces Claude Code ships with, so a user doesn't have to
run
`/plugin marketplace add OpenVidu/openvidu-agent-plugin` themselves, and so
they get updates the same way they'd get updates for any Anthropic-maintained
plugin, instead of the auto-update-off-by-default behavior of a third-party
marketplace (see [Publishing](README.md#publishing)).

## Two marketplaces, and only one takes submissions

Claude Code registers two public marketplaces that Anthropic maintains:

| Marketplace | Install name | How a plugin gets listed |
| --- | --- | --- |
| `claude-plugins-official` | `claude-plugins-official` | Anthropic's own curation, at its sole discretion. **There is no application process** — the submission forms below do not add a plugin here. |
| `claude-plugins-community` | `claude-community` | Open: anyone can submit through a form; accepted plugins are pinned to a commit SHA in the catalog. |

So in practice, "submitting to Anthropic's marketplace" means the
**community marketplace** — that is the only one with an actual process.
Nothing below can get the plugin into the curated official list; that
isn't something that can be requested, and this doc doesn't try to.

## Prerequisites

- [ ] The plugin is already published at
      `OpenVidu/openvidu-agent-plugin` and installable directly from it (the
      ["Before the first publish" checklist](README.md#before-the-first-publish))
      — the community marketplace entry just points at that repository, so it
      has to work on its own first.
- [ ] `claude plugin validate .` passes locally, ideally with
      `--strict` (treats warnings as errors) since the review pipeline runs
      the same check plus automated safety screening on submission.

## Submitting

Two entry points, and they have different account requirements:

- **claude.ai** — `claude.ai/admin-settings/directory/submissions/plugins/new`.
  Requires a **Team or Enterprise organization** — claude.ai's paid
  organizational plans — plus directory management access within it
  (organization Owners have this by default; on Enterprise an Owner can
  delegate it to a custom role). A free or Pro individual account cannot use
  this form at all: there is no organization for it to submit from.
- **Console** — `platform.claude.com/plugins/submit`. Requires a
  **Developer, Admin, or Owner role on a Console organization** (the
  Anthropic API developer platform, separate from claude.ai's paid plans).
  Anyone can sign up for a Console organization; Anthropic's docs don't
  state that doing so, or submitting a plugin through it, costs anything by
  itself — it's the intended route for "individual authors who aren't part
  of a claude.ai Team or Enterprise organization", which is our case.

So **no, a paid claude.ai plan is not required** to submit this plugin: the
Console route is the one to use, and it doesn't require Team/Enterprise
billing. (Using an API key against Claude's models is billed separately and
isn't needed just to submit or maintain a directory listing.)

Anthropic's own documentation does not describe a review-time SLA.

## What happens after acceptance

- The plugin is pinned to a specific commit SHA inside the
  `anthropics/claude-plugins-community` catalog, not to a branch.
- **Anthropic's CI bumps that pin automatically** whenever new commits land
  on `OpenVidu/openvidu-agent-plugin`. There is no separate re-submission
  step for an ordinary update — pushing to this repository (see
  [Publishing](README.md#publishing)) is enough once the plugin has been
  accepted once.
- The public catalog (`marketplace.json` in
  [`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community))
  syncs from the review pipeline **nightly**, so there is a delay between a
  commit landing and it becoming installable from the community
  marketplace. Search the plugin's name in that repository's
  `marketplace.json` to confirm it is live before telling users it is.

## What if the submitting account goes away

**Not addressed anywhere in Anthropic's documentation.** There is no stated
policy for what happens to an already-listed plugin if the Console
organization (or the claude.ai Team/Enterprise organization, for the other
route) that submitted it is later cancelled, downgraded, or deleted, or if
the individual account holding the Developer/Admin/Owner role leaves. Don't
assume either outcome — that the listing survives untouched, or that it
gets pulled — until Anthropic documents it.

Two things reduce the practical risk regardless of what Anthropic does on
its side:

- **Anthropic's CI mirrors from the GitHub repository, not from the
  submitting account.** Since updates flow from new commits on
  `OpenVidu/openvidu-agent-plugin` (see "What happens after acceptance"
  above), the repository itself — not whoever's Console/claude.ai account
  did the one-time submission — is what has to keep existing.
- **Submit from an OpenVidu-owned account, not a personal one.** A Console
  organization (or claude.ai organization) under OpenVidu's control, with
  more than one person holding the Owner/Admin role, avoids the listing
  depending on any single person's account staying active.

## What users get from this

Once listed, a user adds the marketplace once —
`/plugin marketplace add anthropics/claude-plugins-community` — and installs
with `/plugin install openvidu@claude-community`, instead of pointing at our
own repository. See [`../README.md`](../README.md) for the commands as shown
to users, and its ["Keeping the plugin updated"](../README.md#keeping-the-plugin-updated)
section for how this changes what that means for someone using Claude Code
specifically.
