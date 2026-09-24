# Validation

Date: 2026-09-23

## Exact repository pins

| Repository | Origin | Full HEAD | Result |
| --- | --- | --- | --- |
| Target | `https://github.com/Pukujan/automated-agents` | `f2a542858f6b84923b61b710b6a775c0a050b785` | exact match |
| Helper | `https://github.com/Pukujan/content-generation-modules` | `8d4f041e8b82f007000b3a1b83d08c39616cc8c7` | exact match |

The target and helper were cloned, detached at the exact requested commits, and verified before reading their instructions. The target adapter records the same pins in [`.content-system/system-version.json`](.content-system/system-version.json).

## Validator

Command run exactly as requested:

```text
python work/cgm/scripts/validate_content_system.py --root work/cgm --adapter outputs/.content-system --project-root outputs
```

Full output:

```text
VALID: content-generation-modules contract and target adapter
```

Exit code: `0`.

## Direct image link and hash checks

The README contains direct local references to both required raster assets, and both files exist under `outputs/`:

- [`assets/automated-agents-hero.png`](assets/automated-agents-hero.png) — exists; PNG dimensions `1536x1024`; manifest SHA-256 `e17f69f3d68a88c9bad024455d89ca230251dbfb3da8d069b732402054496330`; computed hash matches.
- [`assets/automated-agents-boundaries.png`](assets/automated-agents-boundaries.png) — exists; PNG dimensions `1536x1024`; manifest SHA-256 `0a42af1711eac093ad800ea080c2d079e8c3b6565d4573b73fcec463d1abe686`; computed hash matches.

There are exactly two distinct raster image files in the output package. The hero and supporting image were generated as separate built-in `image_gen` calls, reviewed at full size, and recorded in [`.content-system/image-prompts.md`](.content-system/image-prompts.md).

## Source cleanliness

- Target source checkout: `git status --short` is empty.
- Helper source checkout: `git status --short` is empty.
- No target or helper source files were changed.
- All package files were written under `outputs/`; checkout material and intermediate inspection remain under `work/`.

## Package-level result

**PASS for the requested README and pinned CGM adapter package.** The deterministic validator passes, direct links and hashes match, and the source checkouts remain clean.

This pass does not upgrade the target’s implementation status. The pinned target remains design-only: its browser crawler, live viewer, scheduled runs, and production FOSSIL adapter are not implemented; early JSON contracts are not runtime enforcement; and `docs/PLAN.md` is still a placeholder containing a missing-file error. Those limitations are stated in the README and adapter rather than treated as completed work.

## Exact output file list

```text
outputs/README.md
outputs/VALIDATION.md
outputs/.content-system/asset-manifest.json
outputs/.content-system/brand-language.json
outputs/.content-system/image-prompts.md
outputs/.content-system/project-brief.json
outputs/.content-system/review-rubric.json
outputs/.content-system/system-version.json
outputs/.content-system/visual-style.json
outputs/assets/automated-agents-boundaries.png
outputs/assets/automated-agents-hero.png
```
