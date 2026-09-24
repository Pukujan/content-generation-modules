# Provenance record

## Source pins

| Role | Repository/version | Immutable source |
| --- | --- | --- |
| README target | `Pukujan/automated-agents` | `f2a542858f6b84923b61b710b6a775c0a050b785` |
| Baseline generator | CGM `0.3.1` | `8d4f041e8b82f007000b3a1b83d08c39616cc8c7` |
| Candidate generator | CGM `0.4.1` | `865199f63ac33154bc521eb5211d10156827cad1` |
| Guardrail revision being reviewed | CGM PR #10 | `3cb4aca892b5f8ccbbad6dcd1dfeb75d4efa6c03` |

The target README and the two generated output packages are retained in sibling folders. The adapter packages record their declared helper version and project-specific image prompt/review details. The source pins above identify the commits used for the comparison.

## Public-copy sanitization

The candidate `VALIDATION.md` originally included local checkout path strings. They were replaced with `[local CGM checkout]` before being copied into this public evidence package. The original file SHA-256 was `976877f20963afef8ac5e6f1fc746484e636032ebb4e1f0c1591a655cc07d5f7`; the sanitized file SHA-256 is `f521377258c68bd330fd96e40d2ec13fd209d888244578f2e04aa17be73d6860`.

No other workstation paths were found in the copied public package during the recorded scan. The package-level checksum list is `SHA256SUMS.txt`.

## Evaluation provenance

The scores and caveats in [`README.md`](README.md) summarize the recorded paired blind review and source-order metamorphic review. The sample is one target per generator version. Reviewer scoring and human image inspection are judgments, not instrumented user research. The mobile-render check for the candidate remained pending at the time of the review.

The publicly tracked follow-up and guardrail record is [issue #6](https://github.com/Pukujan/content-generation-modules/issues/6); the implementation and evidence-versioning change is [PR #10](https://github.com/Pukujan/content-generation-modules/pull/10).
