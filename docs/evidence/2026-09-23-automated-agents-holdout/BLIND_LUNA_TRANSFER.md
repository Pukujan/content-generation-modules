# Blind Luna transfer record

- Run date: 2026-09-24
- Generator: GPT-5.6 Luna in a fresh, context-isolated task
- CGM source: `3cb4aca892b5f8ccbbad6dcd1dfeb75d4efa6c03` (`0.4.1`)

## What was tested

A new agent task received the private target repository and the pinned CGM repository as its only project references. It was asked to inspect the target, follow CGM, and produce a human-facing README, target adapter, and generated narrative images. It had no access to the earlier review conversation or its diagnoses. The target repository and exact target pin remain in the private local source record; the target checkout was read-only.

The raw README, adapter, image prompts, generation history, validation output, and two raster files remain in the owner’s local holdout package. This public report intentionally records their hashes and aggregate results without reproducing private target material. [`blind-luna-SHA256SUMS.txt`](blind-luna-SHA256SUMS.txt) contains the package’s relative file names and SHA-256 digests. The digest for the private source-pin record is included there so the owner can verify which local record produced this result.

## Result

The blind run produced a complete README with a reader problem up front, a plain-language explanation of the retrieval/evidence distinction, source-backed claims and limits, a small first action, and an image-generation/use section. It also produced a target adapter and two original ChatGPT image-generation outputs: a wide hero and a square mechanism visual, both using an anime-inspired researcher-and-companion scene tied to the target’s research work. One hero candidate was rejected for extra readable copy and regenerated. The final output records exact prompts, rejected-candidate reasoning, alt text, placement and crop instructions, dimensions, and hashes.

The package passed CGM’s deterministic adapter validator, and every local link in the completed README resolves. Independent inspection found the images relevant to the project and their declared copy legible at full size. The exact output hashes are in the checksum file; the principal artifacts are:

| Artifact | SHA-256 |
| --- | --- |
| Generated README | `2cbcd8074a475ee992a9e11f94a6403eb84cd210ec7b633c1cd631b70768d374` |
| Wide generated hero | `cbf6fe0dee8ba9c62a8d3d8ef8bb9e46cc117764676e2a782832aa740daa7244` |
| Square generated mechanism image | `92cebe8fec85f216ed3d9f3a9b8592269f98ab072c757affbe25cae826bd5989` |
| Private source-pin record | `7e769fbc906c6f590b1113e76c3776cd572f3f1467dd620c0c678403b038c4a1` |

## Limits and decision

This is **one successful transfer run**, not a repeatability result, a causal comparison, or evidence of user preference. The target-specific README has not been published to its target repository. Desktop, tablet, and narrow-width rendering, source-by-source fact confirmation, and owner approval of the visual direction remain human review items. The pass shows that a fresh Luna task can follow this pinned CGM contract on this case; it does not show that every fresh agent will do so.

The full before-and-after public evidence set and this safe transfer record are versioned in CGM. Private target output stays local. Issue [#6](https://github.com/Pukujan/content-generation-modules/issues/6) owns the evaluation log, and PR [#10](https://github.com/Pukujan/content-generation-modules/pull/10) contains the guardrail and evidence changes. The PR remains draft while the independent source-order/metamorphic acceptance gate is still unresolved.
