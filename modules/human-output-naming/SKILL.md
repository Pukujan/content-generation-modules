---
name: human-output-naming
description: >-
  MUST load before writing generated artifact filenames, asset-manifest paths,
  or committed media basenames. Official short name: hon (also HON); canonical
  module id remains human-output-naming. Produces pronounceable, labeled
  dimension segments — never opaque p0 / short-hash stems. Use human-sounding
  writing (hsw) for label wording voice; this module owns the filesystem shape.
---

# Human output naming

Official short name: **hon** (also HON). Canonical module id remains
`human-output-naming`.

**MUST load** this module before naming any surface routed to it in
[`docs/WRITING_ROUTING.md`](../../docs/WRITING_ROUTING.md) /
[`docs/writing-routing.json`](../../docs/writing-routing.json) or the sibling
filename contract [`docs/HUMAN_OUTPUT_NAMING.md`](../../docs/HUMAN_OUTPUT_NAMING.md)
(`required_load: true`). Soft = no NLP CI grade of prose labels; the basename
shape **is** testable.

## When to use

- Generated artifact / output filenames (audio, images, video, demos)
- `asset-manifest.json` `path` values for **new** assets
- Committed media basenames humans skim in a folder

## When not to use

- Issue / PR / commit **titles** and docs prose → load `human-sounding-writing` (**hsw**)
- README / product entry story → load `writing-direction`
- PCM task / checkpoint path conventions (sibling ownership; not this module)

## Before / after

| Before (hashy junk) | After (human labels) |
| --- | --- |
| `song_food-p0-00e86d.mp3` | `song-food_pitch-plus-8st_speed-0pct.mp3` |
| `song_food-p20-8eb807.mp3` | `song-food_pitch-plus-8st_speed-20pct.mp3` |
| `generated/p+8/song_food__p0.mp3` | `generated/song-food_pitch-plus-8st_speed-0pct.mp3` |

Pitch and speed never share one opaque `p0` token. Hash stays an asset **field**
(or an optional suffix **after** human labels), never the basename itself.

## Python API

Importable helper: [`scripts/human_filename.py`](../../scripts/human_filename.py)

```python
from scripts.human_filename import build_basename, is_hashy_junk_basename

name = build_basename(
    [("line", "song-food"), ("pitch", "+8st"), ("speed", "0%")],
    "mp3",
)
# -> "song-food_pitch-plus-8st_speed-0pct.mp3"

assert is_hashy_junk_basename("song_food-p0-00e86d.mp3")
assert not is_hashy_junk_basename(name)
```

Optional kwargs: `disambiguator=`, `content_hash=` — appended only after the
human segments when a true collision remains.

## Operational rules

1. **List every colliding dimension** as its own labeled segment (`key-value`).
   Do not collapse pitch and speed into one folklore token.
2. **Sanitize** for the filesystem: lowercase; spaces → `-`; `+N` → `plus-N`;
   `%` → `pct`; strip other unsafe characters. Join segments with `_`.
3. **Stem keys** (`line`, `stem`, `name`, `title`, `base`): the first such key
   contributes its value alone as the leading segment.
4. **Determinism:** same ordered label set → same basename; different label
   sets → different basenames.
5. **Hash suffix last:** if two distinct configs somehow still collide, append a
   short content hash **after** the human labels — never instead of them.
6. **Manifest:** store the human path in `asset-manifest` / verifiable output
   records; keep `hash` as a separate field.
7. **Label voice:** prefer pronounceable words (HSW voice for *what* you call
   dimensions). Do not invent README-style bold rules for filenames.
8. **History:** do not rewrite published blob history. Stop emitting new hashy
   basenames on helper pins ≥ 0.5.5.

## Final review

- Can a newcomer read the basename aloud and know which dimensions vary?
- Would two pitch×speed settings that used to share `…-p0-….mp3` now differ?
- Is any short hex the *only* discriminator? If yes, fix — add human labels.
