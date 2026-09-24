# Automated Agents image prompt record

Generated with the built-in ChatGPT `image_gen` workflow on 2026-09-23. The provider did not expose a stable seed or model version, so this record captures reproducible intent, exact copy, review conditions, and the final file hashes rather than claiming pixel-identical regeneration.

The target repository has no stronger visual contract. The adapter therefore uses the pinned helper’s explicitly labeled fallback from `docs/BRAND_DIRECTION.md`: original anime-inspired editorial scenes, a human and friendly companion, blue-violet evening light, warm accents, and one clear explanatory idea per asset. The characters and compositions are target-specific; helper characters, logos, and scenes were not copied.

## Shared exact copy

- Title: `Automated Agents`
- Subtitle: `A bounded career research system turns uncertainty into evidence and a next proposal.`
- Provider: `built-in image_gen`
- Output format: PNG raster
- Target dimensions: `1536x1024` for both committed assets
- Accessibility rule: nearby Markdown and alt text carry the full explanation if images fail to load; image text is orientation copy, not the sole source of meaning.

## `assets/automated-agents-hero.png`

- Role: wide README hero; introduce why a bounded career research proposal matters.
- Reader question: Why should I care about this project?
- Dominant message: A person with a real career question can move from scattered role and profile material toward one bounded, inspectable next proposal.
- Prompt:

  ```text
  Use case: illustration-story
  Asset type: wide README hero
  Reader question: Why should I care about this project?
  Dominant message: A person with a real career question can move from scattered profile and role material toward one bounded, inspectable next proposal.
  Audience: Maintainers, agents, researchers, and engineers who need a careful career or positioning decision.
  Scene/backdrop: An original anime-inspired editorial evening workspace with a repository of career notes, a role brief, profile evidence, and a calm open page; no branded logos or copied characters.
  Subject and relationship: A thoughtful human career researcher at a desk with a small friendly story-guide companion, collaborating over a clear path from role, profile, and bounded research to a next proposal; keep both subjects visible and make their relationship accountable rather than magical.
  Style/medium: polished editorial anime-inspired illustration, warm desk light against deep blue-violet evening light, rounded paper and glass cards, gentle cyan connector lines, coral and gold accents.
  Composition/framing: 1536x1024 landscape wide hero; reserve calm negative space in the upper-left for a quiet copy panel; place the human and companion center-right; show one simple readable three-stage path in the scene: role, evidence, proposal; keep the title panel and subjects crop-safe on narrow screens.
  Lighting/mood: clear, welcoming, focused, cautiously optimistic.
  Color palette: night ink #111B4D, violet #8F7CFF, cyan #63D9FF, coral #FF8A70, warm cream #F4F1FF, mint #94E3CB, gold #FFD28A.
  Materials/textures: paper notes, translucent evidence cards, soft glass panel, readable but minimal artifacts.
  Text (verbatim): "Automated Agents" / "A bounded career research system turns uncertainty into evidence and a next proposal."
  Constraints: Render the exact title and subtitle once in a quiet panel, with clean spelling and no extra slogans. The image must communicate a bounded research-to-proposal workflow, not an autonomous or magical agent. Keep the human and companion unobstructed.
  Avoid: generic cyberpunk, dashboards, fake metrics, dense UI, extra labels, pseudo-text, logos, watermark, publication or outreach imagery, unsupported claims, copied characters or compositions.
  ```

- Alt text: `A thoughtful researcher and friendly story-guide companion move from a target role and profile evidence to a labeled next proposal.`
- Use: Place directly below the README title and subtitle as the wide story introduction.
- Crop behavior: Keep the title panel, researcher, companion, and role-evidence-proposal path visible on wide, tablet, and narrow crops.
- Rejection checks: Reject a candidate with changed or unreadable copy, an unclear human/companion relationship, a hidden path, autonomous-action implications, fake metrics, generic cyberpunk, or a dense dashboard.
- Review decision: Accepted after full-size inspection; exact copy is readable and the role-to-evidence-to-proposal path is visible without claiming a running system.
- Final dimensions: `1536x1024`.
- Final SHA-256: `e17f69f3d68a88c9bad024455d89ca230251dbfb3da8d069b732402054496330`.

## `assets/automated-agents-boundaries.png`

- Role: wide README supporting mechanism and boundary image; explain how a task packet becomes focused research and a proposal.
- Reader question: How does this project keep a career recommendation bounded and inspectable?
- Dominant message: A short task packet moves through a target role, profile evidence, focused research, and a clearly labeled proposal while privacy and authority boundaries remain visible.
- Prompt:

  ```text
  Use case: infographic-diagram
  Asset type: wide README supporting problem/mechanism image
  Reader question: How does this project keep a career recommendation bounded and inspectable?
  Dominant message: A short task packet moves through a target role, profile evidence, focused research, and a clearly labeled proposal while privacy and authority boundaries remain visible.
  Audience: Maintainers, agents, researchers, and engineers who need to inspect a careful next step rather than trust an unbounded assistant.
  Scene/backdrop: A different original anime-inspired editorial evening workspace from the hero: a wall-mounted research board and desk with four large calm cards for question, role, evidence, and proposal; include a small locked private folder icon and a stop boundary line, but no logos.
  Subject and relationship: The same kind of thoughtful human career researcher and small friendly story-guide companion are reviewing the board together; the companion points to a narrow evidence path and the human checks a boundary card. The relationship must feel collaborative and accountable, not autonomous.
  Style/medium: polished editorial anime-inspired illustration with one simple visual metaphor, deep blue-violet background, warm desk light, cyan evidence connectors, coral action accents, cream cards, mint boundary markers.
  Composition/framing: 1536x1024 landscape wide supporting asset; reserve clear negative space on the left for a quiet copy panel; place the four-card path across the center-right in a distinct sequence: task packet -> role/profile -> focused research -> proposal; add a visible stop marker before any external action; keep subjects and the path crop-safe when stacked on narrow screens.
  Lighting/mood: calm, thoughtful, honest, practical.
  Color palette: night ink #111B4D, violet #8F7CFF, cyan #63D9FF, coral #FF8A70, warm cream #F4F1FF, mint #94E3CB, gold #FFD28A.
  Materials/textures: paper cards, soft glass board, notebook, modest evidence pins, no dense interface.
  Text (verbatim): "Automated Agents" / "A bounded career research system turns uncertainty into evidence and a next proposal."
  Constraints: Render the exact title and subtitle once in a quiet panel with clean spelling and no extra slogans. Make this a different explanatory image from the hero: emphasize bounded collection, private evidence, proposal status, and the stop boundary. Do not imply a running crawler, production FOSSIL adapter, autonomous outreach, publishing, or profile changes.
  Avoid: generic cyberpunk, a second hero composition, fake metrics, dense UI, extra labels, pseudo-text, logos, watermark, publication or outreach imagery, unsupported runtime claims, copied characters or compositions.
  ```

- Alt text: `A researcher and companion review a bounded path from task packet through role and profile, focused research, and a proposal beside an out-of-scope stop boundary.`
- Use: Place after the opening problem paragraph to explain the bounded mechanism and why external action remains out of scope.
- Crop behavior: Keep exact copy, four-stage path, private-evidence marker, and stop boundary visible when the image is stacked on narrow screens.
- Rejection checks: Reject a candidate with changed or unreadable copy, a missing path or stop boundary, dense fake UI, an unclear relationship, or implications of running crawler automation, outreach, publishing, or profile editing.
- Review decision: Accepted after full-size inspection; it is distinct from the hero and makes the mechanism and boundary visible. Functional stage annotations are retained because they explain the mechanism rather than act as decorative pseudo-text.
- Final dimensions: `1536x1024`.
- Final SHA-256: `0a42af1711eac093ad800ea080c2d079e8c3b6565d4573b73fcec463d1abe686`.

## Review and reuse

The README places each image beside the paragraph it clarifies and supplies useful alt text. The assets are wide and should be checked again at wide, tablet, and narrow rendered sizes before publication. Reuse the method—one reader question, exact copy, target-specific scene, crop rule, and review record—not these characters or compositions.
