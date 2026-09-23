# Test design: readable, traceable, repeatable output

Status: acceptance plan for Content Generation Modules `0.4.1`.

## Behavior contract: a fresh agent serves a first-time reader

This is the BDD-style acceptance example for the product. PDD defines the reader's problem and desired outcome; SDD describes the story and evidence flow; TDD turns the observable requirements into deterministic and metamorphic checks. They are complementary design artifacts, not three extra test frameworks.

```text
Given an unseen target repository at a pinned revision, its own relevant context,
and one pinned CGM contract,
When a clean independent agent is asked to prepare a README and the required visuals,
Then a first-time reader can recognize the human situation and consequence,
     understand the project's useful response before technical internals,
     scan the headings and selective bold anchors as a coherent second story,
     distinguish shipped facts, plans, unknowns, and evidence limits,
     see every evidence-backed `must_preserve` boundary stated plainly,
     follow citations back to immutable sources,
     find a concrete next action,
     and use two distinct, target-appropriate generated raster visuals with
     the required copy, accessibility, crop, review, prompt, and hash records.
And the generated package passes the pinned deterministic validator.
```

Treat this as an observable behavior contract, not an instruction to imitate PCM's wording or headings. Run the candidate without the diagnosis or scoring key; keep the evaluator key outside the candidate's checkout and prompt.

## What each test layer answers

| Layer | Question it answers | Appropriate evidence |
| --- | --- | --- |
| Deterministic regression | Are required records, links, image roles, hashes, and file formats structurally valid? | Validator result and a specific failing fixture. |
| Metamorphic | Does meaning change only when an input fact that supports it changes? | Paired runs over a controlled source transformation and a stated relation. |
| Differential | Does the candidate contract improve on the same inputs compared with the prior contract? | Blinded, paired baseline/candidate runs using the same target, task, model, and image request. |
| Fresh-session holdout | Can an agent transfer the method to an unseen repository without the diagnosis? | Clean sessions, sealed key, independent evaluation, repeated runs. |
| Reader task | Can a person explain the problem, promise, evidence boundary, and next action? | Comprehension, source resolution, errors, and time where practical. |

BDD is the discovery and formulation of shared, user-visible behavior; it is not another score or a synonym for Gherkin. TDD is a development cycle for implementing deterministic checks. Neither replaces the black-box holdout when the claim is that a fresh agent can transfer the method.

## Why these layers are separate

These methods answer different questions, so use the smallest set that covers the risk:

- **BDD behavior examples** define what a first-time reader should understand and do. Cucumber describes BDD as collaborative discovery, formulation, and automation around concrete examples; it is broader than a Given/When/Then file or a test runner. [Cucumber BDD guide](https://cucumber.io/docs/bdd/)
- **TDD and deterministic regression checks** make objective rules fail before implementation and stay repeatable afterward, such as schema shape, local image links, hashes, and evidence locators.
- **Metamorphic checks** test an expected relationship between runs when an exact output oracle is impractical. For example, removing the only source for a claim should weaken or remove that claim while leaving unrelated facts alone. This is a recognized response to the test-oracle problem; each transformation and expected relation must be stated before the run. [Systematic review of metamorphic-relation methods](https://psta.psiras.ru/en/2024/2_37-86)
- **Differential evaluation** compares two implementations or instruction versions on the same inputs and checks where their outputs disagree. It is useful for CGM baseline-versus-candidate comparisons, but a preference score alone does not establish that either output is correct. [McKeeman, “Differential Testing for Software”](https://www.cs.tufts.edu/comp/150FP/archive/bill-mckeeman/DifferentailTesting.pdf)
- **Fresh-session holdouts** test whether an agent can transfer the written contract without seeing the diagnosis or answer key. Keep the fixture and rubric private, but do not claim that secrecy proves the underlying public facts were absent from model training; benchmark-contamination research shows that hidden or newly collected examples can still be exposed or contaminated. [ACL research on benchmark data contamination](https://aclanthology.org/2023.emnlp-main.308/)

These layers are not a checklist to run for every documentation edit. Use deterministic regression for stable rules, a metamorphic relation when an input transformation should preserve or change a known part of the result, paired differential runs when comparing versions, and a fresh-session holdout when making a transfer claim. BDD keeps the expected human behavior clear across those checks.

## Product acceptance tasks

Give a fresh reader the README without the issue or conversation. Ask them to:

1. Explain who the project helps, what situation brings that person there, and what becomes difficult.
2. State what the project offers and describe the mechanism without repeating internal module names.
3. Distinguish shipped behavior from experimental, planned, and unknown work.
4. Find one piece of evidence for a material claim and explain its limitation.
5. Find the smallest useful next action; developers should also find the reproduce/build path.

Record task success, incorrect or missing answers, source-resolution success, and time where practical. Do not treat word count or a model-generated style score as a substitute for comprehension.

## Deterministic contract tests

- Required story-spine fields are present and specific enough to be reviewed.
- Every material claim has nonempty `claim`, `source`, `status`, `supports`, `limits`, and `source_revision` fields, plus a timezone-aware `recorded_at` timestamp.
- A time-bound claim records its `valid_time` interval separately from when its evidence record was recorded; intervals are ordered and corrections remain append-only in the issue/PR/commit history.
- Repository source revisions include an exact repository, full revision, path, locator, and immutable direct permalink.
- External source revisions include a direct URI and access date; publication date is recorded when available.
- Important public claims have a direct citation near the claim or in an immediately relevant evidence section.
- The source supports the stated status; a plan cannot be presented as shipped, and unknown claims remain explicitly unknown.
- No missing source, vague revision, invalid status, unsupported source type, or self-attestation as sole behavioral proof passes silently.
- `0.3.x` adapters remain valid under their pinned contract; `0.4.x` requires project-brief v2.
- A CGM change PR links an open issue with written acceptance/delivery criteria; CI validates this before it can satisfy branch protection.
- For helper `0.4.1` and later, the brief contains an exhaustive source-mapped boundary inventory, every declared boundary appears verbatim in the target README, and one to eight `must_preserve` sentences are exact members of that inventory.
- The deterministic boundary gate checks declared-string coverage and `must_preserve` membership only; independent factual review must still assess whether source extraction missed exclusions, non-goals, not-implemented status, or owner/private-data limits.
- Conflicting source scope is resolved before drafting: explicit non-goals and “not frozen” constraints are not overridden by a broad epic or a suggestive visual.
- Existing image tests still require the declared narrative raster generation path, exact title/subtitle, prompt record, hash, and review evidence.
- The target README itself is checked for linked, local narrative rasters; a source-map manifest cannot pass while the README omits those assets.
- An asset whose usage calls it a README hero or supporting narrative cannot escape the image contract by labeling its manifest role `diagram`.
- Markdown prompt-record anchors resolve to the underlying local file, while free-text descriptions do not count as file records.

Network resolution is an optional verification step. Offline validation checks identity and shape; an online verifier may additionally confirm that a permalink and line locator still resolve.

## Metamorphic tests

Run each transformation as a separate fresh generation against a fixed task packet and compare the generated brief and README against the same semantic rubric. A static review of unchanged outputs can assess the expected oracle, but it is not an executed metamorphic run and must be recorded as `not_run`.

- **M-01 Source-order invariance:** reorder equivalent source files; reader, story spine, claim status, and visual contract stay materially unchanged.
- **M-02 Irrelevant-context invariance:** add unrelated files or metadata; core claims and story do not change.
- **M-03 Locator relocation:** move a source while preserving its content and identity; supported claim meaning/status stays stable while its citation locator updates.
- **M-04 Evidence removal:** remove the sole source for a claim; the claim is removed, qualified, or marked unknown, never left confidently stated.
- **M-05 Evidence-status change:** change a source from planned to shipped or invalidate it; only dependent claim wording/status changes, with the new citation recorded.
- **M-06 Explanation boundary:** change only what the evidence establishes; `supports` and `limits` change accordingly, and public wording never becomes stronger than the source.
- **M-07 Paraphrase invariance:** paraphrase the user task without changing facts; the story and evidence mapping remain materially equivalent.
- **M-08 Visual independence:** change the target's visual adapter; the visual brief follows the new brand while the evidence-supported story remains stable.
- **M-09 Presentation independence:** remove bold styling or change heading wording; the text still explains the same story and citations remain available.
- **M-10 Protected-boundary preservation:** add an evidence-backed `must_preserve` sentence; the README includes it verbatim, and the generated visuals do not imply the excluded capability.
- **M-11 Temporal correction:** append a correction with a later `recorded_at` and changed `valid_time`; the previous record remains attributable, and current prose follows the active evidence.

Metamorphic equality is semantic, not byte-for-byte. Exact prose is not the oracle.

## Differential evaluation

Compare the pinned `0.3.1` contract and the candidate contract on the same task packet, target evidence, model family where practical, and image role. Keep the visual direction and image requirements constant so the comparison isolates writing and evidence improvements. Blind reviewers to the contract version. Report dimension-level results and disagreement, not only an aggregate score.

## Hidden holdout protocol

The hidden target, expected story/evidence map, failure labels, and scoring key must live outside the candidate agent's readable checkout and prompt. A benchmark designer freezes them before the run. A fresh candidate receives only its permitted target repository/context and the pinned CGM contract; an independent evaluator receives the frozen output and the key afterward. Record CGM commit, model/session identity, prompt, target revision, run ID, output hashes, deterministic results, reader tasks, and human review. Run each fixture at least three clean times before making a repeatability claim.

Reference repositories used to design the contract are training/development evidence, not holdouts. Do not call this acceptance suite a hidden-holdout pass unless a separate sealed target and independent run record exist. If the private fixture is unavailable, report the holdout as `not_run` and use visible contract/metamorphic tests only.

## Release gate

Reject a candidate for any missing or false required citation, unsupported shipped claim, image-generation regression, target-brand substitution, or hidden-test leakage. Require all deterministic tests to pass, reader tasks to improve or remain non-inferior on the preregistered dimensions, and independent review to accept the story and visuals. Human review remains the final decision for tone, honesty, and usefulness.
