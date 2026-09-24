# README package validation

## Package result

**PASS for the requested deterministic package gate.** The pinned CGM validator passed, both required raster assets are linked and hash-checked, the adapter pins the requested revisions, and the source checkouts remained clean. This is not a claim that the target repository has a running crawler, scheduler, viewer, FOSSIL adapter, or hidden-holdout result; the README preserves those boundaries.

## Exact pins and origin checks

| Checkout | Origin | Full HEAD |
| --- | --- | --- |
| Target `work/target` | `https://github.com/Pukujan/automated-agents` | `f2a542858f6b84923b61b710b6a775c0a050b785` |
| Helper `work/cgm` | `https://github.com/Pukujan/content-generation-modules` | `865199f63ac33154bc521eb5211d10156827cad1` |
| Local helper source `[local CGM checkout]` | `https://github.com/Pukujan/content-generation-modules.git` (canonical URL with `.git`) | `865199f63ac33154bc521eb5211d10156827cad1` |

The adapter records helper version `0.4.1`, helper commit `865199f63ac33154bc521eb5211d10156827cad1`, target repository `Pukujan/automated-agents`, and target commit `f2a542858f6b84923b61b710b6a775c0a050b785` in `.content-system/system-version.json`.

## Validator command and full output

Command:

```text
python work/cgm/scripts/validate_content_system.py --root work/cgm --adapter outputs/.content-system --project-root outputs
```

Output:

```text
VALID: content-generation-modules contract and target adapter
```

## Direct image link and hash checks

The two local README links were checked against the files under `outputs/` and the hashes recorded in `.content-system/asset-manifest.json`.

| README path | README-linked | File exists | Dimensions | Manifest SHA-256 | Actual SHA-256 | Result |
| --- | --- | --- | --- | --- | --- | --- |
| `assets/readme/hero.png` | yes | yes | 1672×941 PNG | `362675af87ffcef887839884258d4f4feb25b38031c8aee17d33454a18c6b13a` | `362675af87ffcef887839884258d4f4feb25b38031c8aee17d33454a18c6b13a` | pass |
| `assets/readme/problem-mechanism.png` | yes | yes | 1672×941 PNG | `e4cb99dc1c1c31d700be6aa9aac0bb2bf4b39de601376ced6bb5414dc648873c` | `e4cb99dc1c1c31d700be6aa9aac0bb2bf4b39de601376ced6bb5414dc648873c` | pass |

The accepted images were visually inspected at original size. A hero candidate with extra labels and dense pseudo-UI was rejected; a supporting candidate with decorative pseudo-text was rejected. The accepted prompt, role, exact copy, provider, crop/use/accessibility guidance, rejection checks, review decision, rejected-candidate hashes, and final hashes are recorded in `assets/readme/IMAGE_NOTES.md`.

## Source cleanliness

- `work/target`: clean, detached at the requested full target commit.
- `work/cgm`: clean, detached at the requested full helper commit.
- `[local CGM checkout]`: inspected only; origin and full HEAD remained unchanged.
- No source repository files were changed after checkout.

## Exact deliverable file list

```text
.content-system/asset-manifest.json
.content-system/brand-language.json
.content-system/project-brief.json
.content-system/review-rubric.json
.content-system/system-version.json
.content-system/visual-style.json
assets/readme/hero.png
assets/readme/IMAGE_NOTES.md
assets/readme/problem-mechanism.png
README.md
VALIDATION.md
```

The package is complete for this README-generation task. Runtime implementation, private FOSSIL data, personal captures, and external actions remain outside the deliverable by design.
