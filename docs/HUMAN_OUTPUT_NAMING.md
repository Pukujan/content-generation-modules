# Human output naming

Contract for **generated artifact filenames**, **asset-manifest paths**, and
**committed media basenames**. Companion to the soft writing router: titles and
docs use **hsw**; filesystem names use **hon** (`human-output-naming`).

Machine-readable twin: [`docs/human-output-naming.json`](human-output-naming.json)
(`content-generation.human-output-naming.v1`). Skill:
[`modules/human-output-naming/SKILL.md`](../modules/human-output-naming/SKILL.md).
Python API: [`scripts/human_filename.py`](../scripts/human_filename.py).

## Why this exists

After HSW adoption, issue titles and docs became human-readable, but adopters
still emitted junk like `song_food-p0-00e86d.mp3` or
`generated/p+8/song_food__p0.mp3`. Pitch and speed collapsed into opaque `p0`
folklore. Humans cannot skim a folder without decoding agent-coded stems.

## Surfaces (MUST load `human-output-naming` / **hon**)

| Surface | Rule |
| --- | --- |
| Generated artifact filenames | Call `build_basename` (or equivalent) before write |
| asset-manifest `path` values (new entries) | Store the human path; keep `hash` as a field |
| Committed media basenames | Same labeled-segment shape in git |

Soft enforcement for *label prose*; structural basename shape **is** validated
for helper pins ≥ **0.5.5**.

## Before / after

| Before | After |
| --- | --- |
| `song_food-p0-00e86d.mp3` | `song-food_pitch-plus-8st_speed-0pct.mp3` |
| `song_food-p20-8eb807.mp3` | `song-food_pitch-plus-8st_speed-20pct.mp3` |
| `generated/p+8/song_food__p0.mp3` | `generated/song-food_pitch-plus-8st_speed-0pct.mp3` |

## Apply checklist

1. Identify the naming surface (artifact file, manifest path, committed media).
2. Collect **ordered** dimension labels for every varying axis that would collide
   if collapsed (e.g. line, pitch, speed).
3. **MUST** load `modules/human-output-naming/SKILL.md` and call
   `scripts/human_filename.build_basename` (or `build_relative_path`).
4. Write the file and record the human path in the manifest; keep content hash
   as a separate field (optional short hash **suffix** only after human labels).
5. Do not rewrite published blob history to rename old files unless a scoped
   migration says so.

## Short name

**hon** / **HON** is the official short name for `human-output-naming`. Agents
asked for "hon" load this module. The canonical module id and folder remain
`human-output-naming`.

## Validator / ACS

- Full helper check requires the 8th module `human-output-naming` and the
  importable `scripts/human_filename.py` API when this contract is claimed.
- Adapter smoke (helper ≥ 0.5.5): reject classic `name-pN-<6hex>.ext` basenames
  in asset-manifest paths. Hash may remain as an asset field.
- See [`docs/ACS_VERIFY.md`](ACS_VERIFY.md) and
  [`docs/WRITING_ROUTING.md`](WRITING_ROUTING.md).

## Non-goals

- No forced rewrite of already-published blobs.
- No PCM task/checkpoint path conventions (sibling ownership).
- No NLP grade of label wording in CI.
