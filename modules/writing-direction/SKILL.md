---
name: writing-direction
description: Produce human-oriented README, marketing, UX, and product language from a project brief and brand foundation with concrete narrative structure and selective emphasis.
---

# Writing direction

## Story order

Use this sequence unless the format has a strong reason not to:

1. recognizable human situation;
2. concrete example of the problem and consequence;
3. what the project is;
4. how it works;
5. evidence and examples;
6. limitations and trust boundaries;
7. next action.

## README deliverable contract

Treat a repository README as a welcoming product entry point before treating it as a technical manual. Use the repository's `templates/readme-contract.json` and `docs/README_PLAYBOOK.md` as the acceptance source.

The README must make these questions easy to answer in order:

1. What human situation brings the reader here?
2. What becomes difficult, costly, risky, or confusing?
3. Why does this project exist, and who is it for?
4. What can the reader make, use, or understand with it?
5. How does it work at the reader's altitude?
6. What evidence supports the story, and where does the project stop?
7. What should the reader do next?

Place architecture, commands, schemas, and implementation vocabulary after the first human explanation. When the target repository has a visual contract or committed assets, the README should use a meaningful hero or lead visual and link to the image-generation/use guide and asset record.

## Paragraph recipe

Each important paragraph should contain:

- a concrete situation or claim;
- an interpretation that explains why it matters;
- evidence, example, or boundary.

At least one early example should show the problem unfolding for the target reader. Ground it in target-repository evidence or label it clearly as hypothetical. A section heading and a list of capabilities do not replace the explanation.

## Human-language rules

- prefer active verbs and concrete nouns;
- vary sentence length naturally;
- remove filler introductions and abstract adjective stacks;
- explain technical terms at the moment they matter;
- use one main idea per paragraph;
- bold the phrase a skimming reader should retain;
- italicize a short qualification, contrast, or human note;
- do not bold entire paragraphs;
- do not claim that a system “understands,” “guarantees,” or “solves” something without evidence.

## Scan-first formatting

Use [`docs/CONTENT_RESEARCH.md`](../../docs/CONTENT_RESEARCH.md) as the research source for this contract.

- Make the heading tell the reader what they will learn or gain.
- Put the main point early in the section and keep one idea per paragraph.
- Use bullets for parallel benefits, steps, options, and requirements.
- Bold one short phrase when it gives a skimming reader a useful anchor. Prefer a problem, outcome, mechanism, proof, or boundary.
- Treat one short bold phrase per paragraph, often 2–8 words, as a practical heuristic rather than a universal rule.
- Read headings and bold phrases alone. They should form a useful second story about the project.
- Do not use bold as a replacement for semantic headings or descriptive links.
- For helper `0.4.2` and later, keep full pinned URLs in Markdown destinations and use concise descriptive visible labels; do not print raw web URLs in the README.
- If the sentence becomes inaccurate or unclear when bold is removed, fix the sentence instead of depending on styling.

## Final review

Ask what a first-time reader can repeat after twenty seconds. If the answer is only a category (“an AI-powered evaluation platform”), the copy needs a more concrete situation and mechanism.

For helper `0.4.x`, also ask: does each material claim explain what its cited source supports, what remains unproven, which exact revision was inspected, and when this evidence record was recorded? Keep valid-time bounds separate for claims that only apply during a known period. Put direct citations beside important public claims. A citation provides traceability, not a truth guarantee.

For helper `0.4.2` and later, verify that citation labels are readable and that the page does not expose long raw URLs that force horizontal scrolling at narrow widths.

When a target brief contains a boundary inventory, include every `boundaries` sentence verbatim in the README and keep it beside the related citation. Treat `must_preserve` as a subset of those declared boundaries, never as the complete inventory. Review the rendered images against the same boundaries: captions, labels, portable objects, and interface cues can imply capabilities the prose carefully excludes. Do not turn a roadmap or epic into current scope when a narrower acceptance contract excludes or defers that behavior. The deterministic check cannot prove that source extraction was complete, so independent factual review remains required.

Also ask: can the reader find why the project exists, see one visual idea, understand how that visual was generated and should be used, find prior reviewed examples, and reach a useful next action without reading the technical appendix?

## Deterministic delivery gate

Before calling the README package complete, run the validator from the pinned helper checkout against the actual output adapter and README:

```bash
python path/to/content-generation-modules/scripts/validate_content_system.py \
  --root path/to/content-generation-modules \
  --adapter path/to/target/.content-system \
  --project-root path/to/target
```

Use the real paths for the task workspace. Fix every `INVALID` result and rerun the same command. In the handoff, report the command and its exact `VALID` result; never infer success from generated files or from a validator run against a different directory.
