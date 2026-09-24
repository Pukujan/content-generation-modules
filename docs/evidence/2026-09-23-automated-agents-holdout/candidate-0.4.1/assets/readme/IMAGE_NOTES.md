# README image records

These records follow the pinned CGM `0.4.1` image contract. Both accepted files were generated with the built-in ChatGPT `image_gen` provider. The target repository had no stronger accepted visual contract, so the helper's explicitly labeled fallback direction was used: original anime-inspired editorial scenes, a recurring researcher-and-companion relationship, blue-violet evening light, warm accents, one dominant idea per asset, and exact title/subtitle copy.

Final README title: `Automated Agents`

Final README subtitle: `A research-first design for bounded career and positioning proposals.`

## Accepted asset: hero

- Path: `assets/readme/hero.png`
- Role: README hero
- Provider: built-in ChatGPT `image_gen`
- Dimensions: 1672×941 PNG, approximately 16:9
- Exact title: `Automated Agents`
- Exact subtitle: `A research-first design for bounded career and positioning proposals.`
- Alt text: A career researcher and a small companion organize scattered evidence into a bounded next proposal.
- Use: Directly below the README title and subtitle; introduces the movement from one question to a bounded proposal.
- Crop/use behavior: Wide role. Keep the left copy panel and the researcher/companion pair inside the central crop-safe area. Reuse only as the README hero.
- Accessibility: The nearby lead paragraph explains the human situation; the alt text names the transformation rather than the filename; no claim depends on the image loading.
- Rejection checks: reject if extra words or labels appear, if text is garbled or crowded, if the pair is covered, if the path implies autonomous execution, if the image becomes a generic dashboard, or if a narrow crop loses the title/pair.
- Review decision: accepted after local inspection at original size and wide/narrow-crop review. The exact copy is legible and the scene communicates question → evidence → proposal without extra labels.
- SHA-256: `362675af87ffcef887839884258d4f4feb25b38031c8aee17d33454a18c6b13a`

### Accepted hero prompt

```text
Use case: illustration-story
Asset type: README hero
Reader question: Why should I care about this project?
Dominant message: Scattered career questions become a careful, bounded path from research to a next proposal.
Audience: A first-time reader of a documentation-first career and positioning research project.
Scene/backdrop: A calm evening desk with a notebook, blank evidence cards, and a single glowing path moving from a question mark toward a small proposal card.
Subject and relationship: One thoughtful career researcher and one original friendly story-guide companion quietly sort blank cards together; the companion is a collaborator in organization, not an autonomous agent.
Style/medium: Anime-inspired editorial illustration with original characters, human-centered product storytelling, polished and warm.
Composition/framing: Wide 16:9 README hero, keep the human and companion fully visible near center-right, reserve a large quiet dark panel on the left for the only copy, keep all important subjects inside a crop-safe central area.
Lighting/mood: Deep blue-violet evening light, warm desk lamp, curious, welcoming, careful, accountable.
Color palette: Night ink #111B4D, violet #8F7CFF, cyan #63D9FF, coral #FF8A70, warm cream #F4F1FF, mint #94E3CB, gold #FFD28A.
Dimensions/aspect ratio: Wide README hero, 1600x900, 16:9.
Text (verbatim): "Automated Agents" / "A research-first design for bounded career and positioning proposals."
Alt text: A career researcher and a small companion organize scattered evidence into a bounded next proposal.
Constraints: The ONLY legible text anywhere in the image is the exact title and exact subtitle above, rendered verbatim in the left panel. All cards, notebook pages, screens, signs, books, and objects must be blank or use abstract marks and icons with no words or letters. Show a simple visual transition from question to evidence to proposal without labels. No capability beyond bounded research, evidence-aware proposals, and next-step planning.
Avoid: Any extra words, labels, captions, slogans, pseudo-text, fake metrics, dense UI, logos, watermarks, cyberpunk imagery, enterprise dashboard imagery, unsupported autonomous behavior, competing focal points, cropped subjects.
Use in README/HTML: Directly below the README title and subtitle as the hero image; wide role with central crop safety; reuse only as the README hero.
```

## Accepted asset: problem-mechanism

- Path: `assets/readme/problem-mechanism.png`
- Role: README supporting/problem-mechanism image
- Provider: built-in ChatGPT `image_gen`
- Dimensions: 1672×941 PNG, approximately 16:9
- Exact title: `Automated Agents`
- Exact subtitle: `A research-first design for bounded career and positioning proposals.`
- Alt text: A researcher and companion separate public design, private evidence, and local checkpoints before forming a bounded proposal.
- Use: Beside the mechanism and evidence-boundary section; explains why public design, private evidence, and local operational state are separate lanes.
- Crop/use behavior: Wide role with the three trays and proposal boundary visible. Preserve the center for narrow crops. Reuse only for storage and decision boundaries.
- Accessibility: The nearby storage paragraph names the three authorities; the alt text communicates the separation and proposal boundary; no label in the image is required to understand the mechanism.
- Rejection checks: reject if extra words or pseudo-text appear, if the visual repeats the hero, if the lanes collapse into a generic dashboard, if the image implies a running crawler or FOSSIL adapter, or if a narrow crop loses the researcher, companion, and boundary symbol.
- Review decision: accepted after local inspection at original size and wide/narrow-crop review. The replacement uses blank cards and globe/lock/checkpoint/shield symbols only; a first candidate was rejected for decorative pseudo-text.
- SHA-256: `e4cb99dc1c1c31d700be6aa9aac0bb2bf4b39de601376ced6bb5414dc648873c`

### Accepted problem-mechanism prompt

```text
Use case: illustration-story
Asset type: README supporting problem/mechanism image
Reader question: What problem does the project prevent, and how does its design respond?
Dominant message: A mixed pile of career notes becomes three deliberate lanes—public design, private evidence, and local checkpoints—before a proposal is reviewed.
Audience: A first-time maintainer or researcher deciding whether this repository is safe and useful to extend.
Scene/backdrop: A wide editorial workspace where one messy pile of colored papers is sorted into three distinct trays by a researcher and a small companion, then moves toward one simple shield-shaped proposal boundary. The public tray uses a globe icon, the private tray uses a lock icon, and the local tray uses a checkpoint dot icon.
Subject and relationship: The same original career researcher and friendly story-guide companion from the hero calmly review and sort the material; their posture shows human judgment and boundaries, not autonomous action.
Style/medium: Anime-inspired editorial illustration, original characters, polished human-centered product storytelling, simple visual metaphor rather than a software screenshot.
Composition/framing: Wide 16:9 supporting image with a left-to-right sort-and-review composition, human and companion centered, three trays visible, quiet dark title panel in upper-left, preserve all important shapes for narrow crops.
Lighting/mood: Deep blue-violet evening light with warm cream paper, cyan evidence connections, coral accents; careful, reassuring, explicit about boundaries.
Color palette: Night ink #111B4D, violet #8F7CFF, cyan #63D9FF, coral #FF8A70, warm cream #F4F1FF, mint #94E3CB, gold #FFD28A.
Dimensions/aspect ratio: Wide README supporting/problem image, 1600x900, 16:9.
Text (verbatim): "Automated Agents" / "A research-first design for bounded career and positioning proposals."
Alt text: A researcher and companion separate public design, private evidence, and local checkpoints before forming a bounded proposal.
Constraints: The ONLY legible text anywhere in the image is the exact title and exact subtitle above in a quiet upper-left panel. All papers, trays, folders, screens, books, and signs must be completely blank with no lines, letters, words, captions, or pseudo-text. Use only solid color cards, simple icons, arrows, and the lock/globe/checkpoint/shield symbols described above. Show separation, review, and a clear proposal boundary visually; do not imply a running crawler, scheduled runs, FOSSIL implementation, publishing, outreach, or profile editing.
Avoid: Any extra words, labels, captions, slogans, pseudo-text, fake metrics, dense fake UI, logos, watermarks, cyberpunk imagery, enterprise dashboard imagery, unsupported capabilities, competing focal points, cropped subjects, duplicated hero composition.
Use in README/HTML: Place beside the mechanism or evidence-boundary section as a distinct supporting/problem visual; preserve the wide crop; reuse only for explaining storage and decision boundaries.
```

## Rejected candidates

| Candidate | Provider and role | SHA-256 | Rejection reason | Review consequence |
| --- | --- | --- | --- | --- |
| `exec-b72384fe-bfda-4573-bc9a-386bb45590f7.png` | built-in ChatGPT `image_gen`; hero | `69255a6b12f2225fae8f89bce3cf20f11f8310eda355a78d9ba2d849f30ecd33` | Added readable labels and dense workflow cards beyond the exact title/subtitle. | Regenerated with a blank-card constraint; replacement accepted as `hero.png`. |
| `exec-985ae74d-209b-43d4-8a6b-4e2c8bc66597.png` | built-in ChatGPT `image_gen`; supporting/problem-mechanism | `a02b0196913a392c35b6b94c98ecc7e1483725f0c49dae1123327c2f93dcf81f` | Used decorative pseudo-text and line-heavy cards, weakening the boundary explanation. | Regenerated with blank cards and simple symbols only; replacement accepted as `problem-mechanism.png`. |
