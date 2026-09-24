# Automated Agents

> A research-first design for bounded career and positioning proposals.

<p align="center">
  <img src="assets/readme/hero.png" alt="A career researcher and a small companion organize scattered evidence into a bounded next proposal." width="100%">
</p>

If you are trying to decide whether a role, audience, or positioning idea deserves your next hour, the raw material rarely arrives as one clean brief. It arrives as a job description, a profile, a few public observations, and several assumptions that sound more certain than they are. **The cost is a confident next step built on the wrong evidence.**

## Why this exists: turn a career question into a bounded next step

The repository's active slice starts with one explicit research question: a target company or job, a connection-list filter, or a topic search. The intended run chooses a small seed set, sets page/time/depth budgets, explores visibly, checkpoints each page, and produces an evidence brief plus a provisional strategy recommendation. See the [first-slice brief](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/first-slice.md#L5-L16).

That shape matters because a visible profile, a proposed project, and an agent interpretation are not interchangeable proof. The system is designed to keep observations, gaps, and proposals separate long enough for a person to decide what is worth testing. **Bounded research comes before broad activity.**

The target repository records a partial supervised path through a logged-in browser, but it also says that the repository still contains design documents and instructions rather than a running crawler or browser automation. That record is useful continuation context, not a claim that the public repository ships a browser product. See the [current handoff](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/handoff.md#L3-L15).

## What this project is: a person-agnostic research and positioning design

Automated Agents is a **personal-brand and career research system built in usable slices**. It gives a fresh task a way to inspect supplied role, profile, and research material; ask for targeted collection; and form a calibrated next proposal without turning a recommendation into an approved identity or external action.

The current operational center is the hiring coach contract. It defines a role assessment, a targeted crawler task, a network plan, a LinkedIn plan, and one prioritized next proposal. The contract also says that collection is read-only and that the coach cannot contact, connect, follow, react, apply, publish, edit a profile, bypass access controls, or expand beyond the task budget. Read the [hiring coach instructions](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/modules/hiring-coach/instructions.md#L1-L17).

This is a design-and-instructions repository today. **It does not claim a running agent runtime, browser crawler, scheduler, viewer, or production persistence adapter.** The root README and the communication manifest both mark the workflow as design-only, and the existing JSON contracts are early drafts rather than enforced runtime boundaries. See the [pinned repository README](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/README.md#L3-L11) and [communication manifest](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/config/communication-manifest.yaml#L1-L4).

## What you can make or use: evidence-aware proposals, not automatic outreach

The documented workflow is meant to produce small, inspectable artifacts:

- a structured capture batch with provenance, missing data, and coverage limits;
- a research brief that separates observations from interpretations;
- a role-fit assessment with demonstrated, transferable, unproven, and unknown labels;
- a targeted next research task with page, depth, selection, and stop conditions;
- positioning, campaign, or post proposals that retain assumptions and evidence references;
- a handoff that records owners, revisions, evidence references, state, open questions, and the next action.

These are **documented outputs and proposed interfaces** in the pinned revision. They are useful as a shape for the next slice, but they are not evidence that a production runner already creates or persists them.

## How it works: ask narrowly, observe visibly, propose carefully

The intended path is small enough to review by hand:

1. **Choose one question and seed set.** Start from a target role/company, a connection-list filter, or a topic search rather than asking for an unbounded crawl.
2. **Set limits before collection.** Record page, time, depth, comment-expansion, and stop budgets, then explore only visible, allowed sources.
3. **Checkpoint what was actually observed.** Preserve provenance, partial capture, missing values, sample limits, and model annotations as separate pieces of the record.
4. **Ask the right role for the next proposal.** Research ranks relevant evidence; the hiring coach turns role and research gaps into a next action; brand and strategy keep positioning and campaign decisions as proposals.
5. **Keep decisions and storage separate.** The public repository holds generic design and policy, private FOSSIL is the intended home for personal evidence and hypotheses, and local state holds queues and checkpoints.

<p align="center">
  <img src="assets/readme/problem-mechanism.png" alt="A researcher and companion separate public design, private evidence, and local checkpoints before forming a bounded proposal." width="100%">
</p>

The visual shows the mechanism as a boundary map, not a software screenshot: mixed notes are separated before a proposal is reviewed. The [storage boundary](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/storage.md#L3-L17) defines the intended authorities, while the [shared policy](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/policy.md#L3-L31) defines decision ownership, untrusted inputs, recovery, and the fact that runtime enforcement is not yet implemented.

## Evidence and boundaries: what the pinned revision supports

The table below treats repository artifacts as traceable evidence, not as a substitute for runtime proof. **A citation shows where to inspect the claim; it does not make the claim true by itself.**

| Claim | Status | What the evidence supports | What it does not establish | Source |
| --- | --- | --- | --- | --- |
| The repository is a versioned design and instruction set for personal-brand and career research. | shipped | The root README states the project category and current state. | It does not establish a working runtime or user outcomes. | [README.md](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/README.md#L1-L11) |
| The communication workflow is marked design-only and assigns roles, inputs, outputs, and prohibitions. | shipped | The manifest names the research-to-strategy-proposal workflow and module boundaries. | It does not prove that any controller, collector, or handoff dispatcher executes those rules. | [config/communication-manifest.yaml](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/config/communication-manifest.yaml#L1-L55) |
| The first slice is bounded visible research followed by evidence and a provisional proposal. | planned | The slice document specifies the question, budgets, visible exploration, checkpointing, report, and proposal steps. | It does not establish that the browser bridge, persistence path, or scheduler exists. | [docs/first-slice.md](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/first-slice.md#L5-L27) |
| The hiring coach has an active v1 role contract with five output sections and explicit action limits. | shipped | The instructions define the sections and prohibit contact, applications, publishing, profile edits, access-control bypasses, and budget expansion. | The file is an instruction contract, not a running agent. | [modules/hiring-coach/instructions.md](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/modules/hiring-coach/instructions.md#L1-L17) |
| Strategy, brand, research, planner, writer, and editor responsibilities remain separate proposals or review artifacts. | shipped | The policy and module instructions assign ownership and preserve evidence, alternatives, and user decisions. | They do not prove that every proposed module has an implemented executor. | [policy.md](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/policy.md#L3-L7), [modules/strategy/instructions.md](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/modules/strategy/instructions.md#L1-L9) |
| Personal evidence, hypotheses, decisions, and outcome lineage are intended for a private FOSSIL pack, while public Git holds generic design and local state holds operations. | shipped | The storage document names one authority per kind of information and separates evidence from execution approval. | It does not establish a production FOSSIL adapter, encryption, or off-device backup. | [docs/storage.md](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/storage.md#L3-L27) |
| A partial supervised browser path is recorded as continuation context. | experimentally_supported | The handoff records what the owner manually verified and says what should be explored next. | It is not a reproducible public capture, a population sample, or evidence of a running crawler. | [docs/handoff.md](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/handoff.md#L3-L19) |
| The planner contract is explicitly a legacy draft pending revision before wiring. | shipped | The planner instructions qualify the initial JSON contract and keep final posts, profile changes, and publication outside its role. | This does not establish a replacement contract or runtime wiring. | [modules/planner/instructions.md](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/modules/planner/instructions.md#L1-L7) |
| The durable plan referenced by the repository is not recoverable as a plan in this pinned revision. | unknown | `docs/PLAN.md` contains a missing-file note rather than roadmap content. | No broader roadmap, approved budgets, or future scope should be inferred from that reference. | [docs/PLAN.md](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/PLAN.md) |

The following boundaries are intentionally repeated because they change how a reader should interpret every other section:

- The browser crawler, live viewer, scheduled runs, and production FOSSIL adapter are not implemented.
- Personal evidence and proposals belong in a private FOSSIL pack.
- Existing JSON contracts are early drafts, not enforced runtime boundaries.
- No publication, outreach, or brand-profile adoption is implied.

Unknowns remain open: the browser bridge, actual runtime, first research seeds, profile inputs, unattended execution, backup destination, and the broader durable plan are not frozen in this revision. The [handoff open choices](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/handoff.md#L17-L19) are the honest next questions.

## Image generation and use: two visuals with two explanatory jobs

The target revision did not define its own accepted visual system, so this package uses the pinned CGM fallback direction: original anime-inspired editorial scenes, one recurring researcher-and-companion relationship, blue-violet evening light, warm accents, and one idea per asset. The exact prompts, rejected candidates, copy, crop notes, accessibility text, review decisions, and hashes are in [`assets/readme/IMAGE_NOTES.md`](assets/readme/IMAGE_NOTES.md) and the pinned [docs/IMAGE_GUIDE.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/IMAGE_GUIDE.md).

| Asset | Role and use | Exact copy | Dimensions and crop | Review decision |
| --- | --- | --- | --- | --- |
| [`assets/readme/hero.png`](assets/readme/hero.png) | README hero; introduces the movement from a question to a bounded proposal. | `Automated Agents` / `A research-first design for bounded career and positioning proposals.` | 1672×941 PNG; wide 16:9 role with central crop-safe subjects and left copy panel. | Accepted after rejecting a first candidate for extra labels and dense pseudo-UI. SHA-256: `362675af87ffcef887839884258d4f4feb25b38031c8aee17d33454a18c6b13a`. |
| [`assets/readme/problem-mechanism.png`](assets/readme/problem-mechanism.png) | Supporting problem/mechanism visual; explains separation between public design, private evidence, and local checkpoints. | `Automated Agents` / `A research-first design for bounded career and positioning proposals.` | 1672×941 PNG; wide 16:9 role with three visible lanes and narrow-crop-safe center. | Accepted after rejecting a first candidate for decorative pseudo-text in cards. SHA-256: `e4cb99dc1c1c31d700be6aa9aac0bb2bf4b39de601376ced6bb5414dc648873c`. |

Both are raster assets generated with the built-in `image_gen` provider. The README copy and alt text still carry the explanation if images fail to load; the images do not imply a crawler, scheduler, FOSSIL implementation, publication, outreach, or profile editing.

## Templates and guides: follow the source trail in order

For this target, begin with the local [`.content-system/system-version.json`](.content-system/system-version.json), [project brief](.content-system/project-brief.json), [brand language](.content-system/brand-language.json), [visual style](.content-system/visual-style.json), [asset manifest](.content-system/asset-manifest.json), and [review rubric](.content-system/review-rubric.json). Then read the target's [first-slice brief](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/first-slice.md), [current handoff](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/handoff.md), [storage boundary](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/storage.md), [policy](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/policy.md), and [communication manifest](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/config/communication-manifest.yaml).

The pinned CGM source trail used for this package is:

- [docs/CONTENT_RESEARCH.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/CONTENT_RESEARCH.md)
- [docs/BRAND_DIRECTION.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/BRAND_DIRECTION.md)
- [docs/README_PLAYBOOK.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/README_PLAYBOOK.md)
- [docs/IMAGE_GUIDE.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/IMAGE_GUIDE.md)
- [docs/PRIOR_WORK.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/PRIOR_WORK.md)
- [docs/HOLDOUT_EVALUATION.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/HOLDOUT_EVALUATION.md)
- [docs/MIGRATING_TO_0.2.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/MIGRATING_TO_0.2.md)
- [docs/MIGRATING_TO_0.3.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/MIGRATING_TO_0.3.md)
- [docs/MIGRATING_TO_0.4.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/MIGRATING_TO_0.4.md)
- [docs/README_QUALITY_PDD.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/README_QUALITY_PDD.md)
- [docs/README_QUALITY_SDD.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/README_QUALITY_SDD.md)
- [docs/README_QUALITY_TDD.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/README_QUALITY_TDD.md)
- [docs/PROVENANCE_AND_CITATION.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/PROVENANCE_AND_CITATION.md)
- [docs/REVERSE_ANALYSIS_PCM_AND_ADOPTERS.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/REVERSE_ANALYSIS_PCM_AND_ADOPTERS.md)
- [templates/README.template.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/templates/README.template.md)

The helper's module entry points used here are [brand-foundation](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/modules/brand-foundation/SKILL.md), [content-context](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/modules/content-context/SKILL.md), [writing-direction](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/modules/writing-direction/SKILL.md), [visual-direction](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/modules/visual-direction/SKILL.md), [image-generation](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/modules/image-generation/SKILL.md), and [html-demo](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/modules/html-demo/SKILL.md).

## Prior work and references: carry forward the method, not the story

The pinned helper records prior reviewed README work from [Eval Lab](https://github.com/Pukujan/Eval-lab), [Harness on Steroids](https://github.com/Pukujan/harness-on-steroids), [Custom Extensions](https://github.com/Pukujan/custom-extensions), and [Hades Product](https://github.com/Pukujan/hades-product). Those examples contributed the pattern of a human problem first, technical detail second, distinct visuals for distinct questions, explicit boundaries, and a human review decision. This package keeps that method but uses the target's own evidence and a target-specific research story.

## Try it: choose one question before adding machinery

The smallest useful action is to read the [first-slice brief](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/first-slice.md), choose one seed set, and write a private handoff with the question, owner, actual budget, evidence references, coverage, state, and proposed next action. The next documented slice is tracked in [GitHub issue #1](https://github.com/Pukujan/automated-agents/issues/1).

For a developer or researcher, inspect the pinned revision and its contracts before implementing anything. The repository's own working agreement says to keep the public tree person-agnostic, use fresh scoped context, and implement only what the next useful run needs; do not install an orchestration framework merely to begin. The [working agreement](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/AGENTS.md#L1-L13) is the right implementation starting point.

### Scan test

Read only the headings, bold phrases, and link text. They should recover the situation, bounded proposal, mechanism, evidence boundary, visual explanation, and next action. The pinned [docs/CONTENT_RESEARCH.md](https://github.com/Pukujan/content-generation-modules/blob/865199f63ac33154bc521eb5211d10156827cad1/docs/CONTENT_RESEARCH.md) explains the scan-first rule; removing bold styling should not make this README inaccurate.
