# Migrating to Content Generation Modules 0.4

Version `0.4.0` strengthened how a README explains its claims and source trail. Version `0.4.1` adds a required protected-boundary field for new target adapters and validates that its exact wording appears in the README. Both keep the existing human-first story order, brand ownership, visual direction, and image-generation requirements from `0.3.x`.

## What changes

For each material claim, project-brief v2 records:

- `claim`, `source`, and `status`, as before;
- `supports`: what the cited evidence establishes, in plain language;
- `limits`: what that evidence does not establish;
- `source_revision`: the kind of source, a stable reference, and enough identity to find the exact evidence again;
- `recorded_at`: when this version of the evidence record was entered, as a timezone-aware timestamp.

For claims that apply only during a known interval, add optional `valid_time.start` and `valid_time.end` bounds. These are separate from `recorded_at`: valid time says when the claim applies; record time says when the repository knew or recorded this version. Use the tracking issue for ownership and PR/commit history for append-only operational changes rather than maintaining a second log.

Repository evidence requires an owner/repository, full commit ID, repository-relative path, locator, and immutable permalink. External sources require a direct URL and access date. Owner observations, decisions, and searches that did not establish a fact carry an observation date. An unsuccessful search can support an `unknown` record; it cannot be the sole support for a shipped claim.

The validator checks the record structure and that requested citations appear in the target README. A human still checks whether the source is credible and actually supports the wording. A citation provides traceability, not proof of truth.

For helper `0.4.1` and later, `project-brief.json` must include one to eight concise `must_preserve` sentences. Select evidence-backed exclusions or qualifications that could materially mislead readers if omitted, cite their sources near the sentence, and include each sentence verbatim in the README. The validator checks presence; independent review still checks whether the chosen boundaries are complete and whether prose or images imply excluded behavior.

## Upgrade a target adapter

1. Keep the helper pinned to the intended `0.4.x` release and commit in `.content-system/system-version.json`.
2. Start `.content-system/system-version.json` from [`templates/system-version.json`](../templates/system-version.json). Replace every placeholder with the target repository, target commit, helper version, and full pinned helper commit. Do not copy the helper repository's root `system-version.json` into the target adapter.
3. Change `.content-system/project-brief.json` to schema version `content-generation.project-brief.v2`.
4. For every material evidence item, write what the source supports and leaves open, classify its source, and record a stable revision and locator.
5. Add direct citations beside important README claims. Set `cite_in_readme` to `true` for evidence that must appear in the README; the validator checks that link.
6. Revisit any claim whose source is missing, stale, private, or weaker than its wording. Qualify it or mark it `unknown`.
7. Run the pinned helper's validator against the actual README and adapter, then complete the target's reader, evidence, image, and human review checks. Do not report completion on an `INVALID` result.
8. For helper `0.4.1` and later, resolve conflicts between broad roadmap material and narrower current acceptance contracts, record the controlling source in the brief, and verify every `must_preserve` disclosure appears in the README.

The starter shape is in [`templates/project-brief.json`](../templates/project-brief.json); the machine-readable contract is [`schemas/project-brief.v2.schema.json`](../schemas/project-brief.v2.schema.json). See [`PROVENANCE_AND_CITATION.md`](PROVENANCE_AND_CITATION.md) for source-kind guidance and [`README_QUALITY_TDD.md`](README_QUALITY_TDD.md) for acceptance and metamorphic tests.

## Visual and image rules continue unchanged

Do not replace the target's visual identity with CGM's default brand. Continue following the target adapter and the existing [`IMAGE_GUIDE.md`](IMAGE_GUIDE.md): narrative images use the required image-generation workflow, exact title and subtitle context, raster outputs, prompt records, hashes, crop and accessibility guidance, and a recorded review decision. The v0.4 story and evidence changes do not waive or weaken those requirements.

## Compatibility

Targets pinned to `0.3.x` may keep project-brief v1 and their existing checks. A target that pins helper `0.4.0` or later must use project-brief v2. A target pinned to `0.4.1` or later must also provide `must_preserve` and repeat those boundaries in its README. Do not change a target adapter's version pin until its brief, README citations, boundary disclosures, and review are ready together.
