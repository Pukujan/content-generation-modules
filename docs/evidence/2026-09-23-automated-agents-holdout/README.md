# README generation holdout: Automated Agents

This folder preserves the before-and-after artifacts from a blind README-generation holdout. It makes the source inputs, helper versions, images, review findings, and limitations inspectable in CGM itself.

The target for this public holdout is [Automated Agents](https://github.com/Pukujan/automated-agents), pinned at commit [`f2a542858f6b84923b61b710b6a775c0a050b785`](https://github.com/Pukujan/automated-agents/tree/f2a542858f6b84923b61b710b6a775c0a050b785). The original README is preserved in [`target-original/README.md`](target-original/README.md). Both generated versions and their complete output packages are retained below.

The original README’s relative document links point into that pinned target checkout; the linked target documents are not copied into this comparison package. The generated baseline and candidate packages include their own required output files and assets.

## Before: CGM 0.3.1

The baseline starts with a project description and implementation limits, then sends the reader to three documents. It is accurate and compact, but offers little help for a first-time reader to understand the human problem, intended workflow, evidence boundaries, or visual identity.

[Read the complete baseline README](baseline-0.3.1/README.md) · [Inspect its adapter and image prompts](baseline-0.3.1/.content-system/) · [Baseline hero](baseline-0.3.1/assets/automated-agents-hero.png) · [Baseline supporting image](baseline-0.3.1/assets/automated-agents-boundaries.png)

![Baseline README hero generated for the 0.3.1 holdout](baseline-0.3.1/assets/automated-agents-hero.png)

## After: CGM 0.4.1

The candidate opens with the reader’s career-research uncertainty, then explains the bounded approach, what the repository actually contains, what it does not yet implement, the evidence status, and how a maintainer can continue. It keeps the original project’s limits explicit while giving readers a clearer path through the material.

[Read the complete candidate README](candidate-0.4.1/README.md) · [Inspect the candidate adapter](candidate-0.4.1/.content-system/) · [Read both image prompts and reviews](candidate-0.4.1/assets/readme/IMAGE_NOTES.md) · [Candidate validation record](candidate-0.4.1/VALIDATION.md)

![Candidate README hero generated for the 0.4.1 holdout](candidate-0.4.1/assets/readme/hero.png)

![Candidate supporting visual explaining the problem and mechanism](candidate-0.4.1/assets/readme/problem-mechanism.png)

The hero introduces the user situation; the supporting visual answers a different question about the project’s evidence and decision boundaries. The prompt records specify exact title and subtitle text, provider, composition, crop behavior, alt text, rejection criteria, review decision, and asset hash. The first hero candidate and first supporting candidate were rejected and regenerated; those decisions are recorded in the image notes.

## Holdout method and result

The same public target was generated once with helper version 0.3.1 and once with 0.4.1. An evaluator that did not author either candidate scored the outputs against the same five-part rubric. This is a paired, single-target blind holdout (`n=1`), not a repeatability study.

| Candidate | Score | Outcome | Recorded review |
| --- | ---: | --- | --- |
| CGM 0.3.1 baseline | 3.1 / 5 | Fail | Useful, but weaker human problem framing and information structure. |
| CGM 0.4.1 candidate | 4.6 / 5 | Pass with a pending check | Stronger problem framing, explanation, evidence boundaries, and scanability. A final mobile-render check remained pending. |

The score change is evidence that this one candidate improved under this rubric. It does **not** establish that CGM caused the change, that the result will repeat, that readers prefer it, or that all visual and responsive checks passed. Source-order metamorphic testing also found that protected-boundary coverage and provenance topology differed between runs; that failure remains open and is part of the follow-up work tracked in [CGM issue #6](https://github.com/Pukujan/content-generation-modules/issues/6).

The PR that versions the associated guardrail and evidence work is [CGM PR #10](https://github.com/Pukujan/content-generation-modules/pull/10). This snapshot records what was reviewed; it does not convert a pending or failed gate into a pass.

## Provenance and privacy

- Target source: public Automated Agents repository, pinned to `f2a542858f6b84923b61b710b6a775c0a050b785`.
- Baseline helper: CGM `0.3.1`, source commit `8d4f041e8b82f007000b3a1b83d08c39616cc8c7`.
- Candidate helper: CGM `0.4.1`, source commit `865199f63ac33154bc521eb5211d10156827cad1`.
- Follow-up guardrail under review: CGM PR #10 at `3cb4aca892b5f8ccbbad6dcd1dfeb75d4efa6c03`.
- A workstation-specific path in the candidate validation note was removed before this public copy. The source and sanitized file hashes are recorded in [`PROVENANCE.md`](PROVENANCE.md).
- [`SHA256SUMS.txt`](SHA256SUMS.txt) records hashes for the files in this evidence package, excluding the checksum list itself.

The copied target README is from a public, pinned repository. No private target material, credentials, or user-specific evidence belongs in this public evidence set. A separate transfer run against a private repository is evaluated independently and will be represented here only by a privacy-safe method, result summary, and output hashes; its full target-specific files remain local.

## What this evidence is for

Use the paired artifacts to inspect the actual writing and generated images, trace which helper version produced each package, and challenge the evaluation result. Use the holdout and metamorphic tests in [`docs/HOLDOUT_EVALUATION.md`](../../HOLDOUT_EVALUATION.md) and [`docs/README_QUALITY_TDD.md`](../../README_QUALITY_TDD.md) to guide the next validation. The privacy-safe report for the separate blind Luna transfer is in [`BLIND_LUNA_TRANSFER.md`](BLIND_LUNA_TRANSFER.md). Do not use these individual comparisons as a blanket claim that README quality or image quality is solved.

The owner's later preference review of nine supplied image candidates is recorded separately in [`2026-09-24-owner-image-review.md`](../2026-09-24-owner-image-review.md). It preserves the original list order and per-image hashes: positions 1–7 were preferred; positions 8–9 were not preferred. The record does not copy the supplied image files or identify their source project.

A separate `0.4.1` transfer exposed a citation-layout failure that the pinned validator missed. Its privacy-safe finding and the `0.4.2` response are in [`2026-09-24-citation-layout-holdout.md`](../2026-09-24-citation-layout-holdout.md); target-specific README and image files remain local.
