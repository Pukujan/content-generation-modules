---
name: content-context
description: Build an evidence-bounded project brief from a repository so generated README, marketing, UX, visual, and HTML content describes what the project actually does.
---

# Content context

Use this module whenever the agent is entering a new repository or the product story has changed.

## Workflow

1. Read the repository's project contract and current checkpoint.
2. Identify the real user, job, problem, solution, mechanism, proof, limitations, and candidate boundaries.
3. Record exact file paths for evidence.
4. Mark each claim as shipped, experimentally supported, planned, or unknown.
5. Resolve scope conflicts before drafting: pinned implementation/tests establish shipped behavior; the narrowest current acceptance contract controls a planned release; broad epics describe direction; older documents are historical. Explicit exclusions and “not frozen” terms override broad roadmap paths. Record unresolved conflicts as unknown.
6. For each material claim, record what its evidence supports, what it does not establish, an exact source revision/locator or direct external citation, and timezone-aware `recorded_at` time.
7. For claims that apply only during a known period, add `valid_time` bounds and keep them separate from source event dates and record time.
8. Record technical terms that need plain-language translation.
9. Build the boundary inventory exhaustively from source-backed exclusions, explicit non-goals, not-implemented or deferred status, and owner or private-data limits. Keep each boundary concise, traceable to its source, and in `boundaries`; do not treat `must_preserve` as a replacement for that inventory.
10. Store the result in `project-brief.json` using the schema version pinned by the target adapter. For helper `0.4.x`, use project-brief v2. For `0.4.1` and later, every declared boundary must be copied verbatim into the README, and `must_preserve` may select one to eight entries only when each exactly matches a declared boundary.
11. For helper `0.4.2` and later, keep full pinned source URLs in Markdown destinations and use concise descriptive link labels in visible copy. Do not print raw web URLs in the README.
12. Create `.content-system/system-version.json` from the pinned helper's `templates/system-version.json`. Set `schema_version`, the exact helper repository/version/full commit, and the module list. Do not copy the helper repository's root `system-version.json` into the target adapter; it has a different purpose and shape.
13. Create the remaining adapter files from their matching templates, then run the pinned validator against the actual output directory before delivery.

## Output rule

The project brief is a source map, not marketing copy. It should be useful to a fresh agent and easy for a human maintainer to correct. Never let a citation upgrade an inference into an observed fact. The deterministic boundary check can verify that declared strings reach the README and that `must_preserve` entries belong to the inventory; it cannot prove that source extraction found every real exclusion or owner/private-data limit. Independent factual review remains required.
