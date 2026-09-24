# Citation readability holdout finding

- Review date: 2026-09-24
- Candidate helper: CGM `0.4.1`, pinned to `d754a3b8cba72449f4662843cc74638c3cbd3b30`.
- Generator: fresh context-isolated GPT-6-Luna agent with access only to the pinned helper and one pinned target snapshot.
- Privacy: target identity, source pin, README, adapter, and generated images remain in the local holdout package. This public record omits them.

## Observed behavior

The run produced a story-led README, a target adapter, and three ChatGPT-generated raster illustrations. The pinned `0.4.1` validator passed; all five README-local destinations resolved, and the manifest hashes and dimensions matched the image files.

An independent rendered review found that the images themselves fit at desktop (1440px), tablet (768px), and narrow (390px) widths. The page text did not: the README printed fifteen full helper permalinks as visible text in its source/reference list. At a 390px viewport, Chromium measured a 918px document width; the long source URLs caused horizontal overflow. This is a concrete human-readability failure that the `0.4.1` structural validator did not detect.

## Versioned response

CGM `0.4.2` introduces a citation-presentation rule: keep immutable revisions in Markdown link destinations and show concise descriptive link labels. Its validator rejects raw unlinked web URLs in README prose while allowing URLs in Markdown destinations, HTML attributes, fenced code, and inline code. The check is covered by regression tests.

The generation rules do not change the image workflow, brand direction, exact title/subtitle requirements, raster requirement, or visual-review policy. The owner’s separate nine-image preference review is recorded in [`2026-09-24-owner-image-review.md`](2026-09-24-owner-image-review.md).

## Verification and remaining work

- The new `0.4.2` validator flags all fifteen visible raw URLs in the saved `0.4.1` package.
- CGM’s test suite passes 27 tests, including coverage that permits descriptive Markdown links and URLs in code examples.
- The CGM root contract validator returns `VALID`.
- A fresh blind generation using the pinned `0.4.2` helper is still required to verify that an independent agent follows the new rule in a completed README package.
- The separate M-01 source-order metamorphic acceptance gate also remains unresolved; this finding does not clear it.

Issue [#6](https://github.com/Pukujan/content-generation-modules/issues/6) owns this evaluation, and draft [PR #10](https://github.com/Pukujan/content-generation-modules/pull/10) contains the versioned policy and validator change.
