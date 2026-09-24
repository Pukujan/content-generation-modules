# Automated Agents

> A bounded career research system turns uncertainty into evidence and a next proposal.

![A thoughtful researcher and friendly story-guide companion move from a target role and profile evidence to a labeled next proposal.](assets/automated-agents-hero.png)

## Why this exists

You can have a target role, a profile, and a promising direction—and still not know what to investigate next. A broad assistant conversation can turn that uncertainty into confident-sounding advice before anyone has checked the role requirements, the available evidence, or the boundaries around personal material.

**The hard part is choosing a careful next question.** Automated Agents is shaped around a smaller move: gather only the evidence needed for one bounded career or positioning question, keep the proposal separate from proof, and leave external action with the owner. The repository records that intent in its [policy](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/policy.md) and [storage boundary](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/storage.md).

![A researcher and companion review a bounded path from task packet through role and profile, focused research, and a proposal beside an out-of-scope stop boundary.](assets/automated-agents-boundaries.png)

## What this project is

Automated Agents is a **person-agnostic design and instruction repository** for personal-brand and career research. It describes agents that investigate, assess role fit, propose positioning, and recommend campaigns for one owner while keeping observed evidence, model interpretations, proposals, and decisions distinct.

The pinned repository currently ships versioned design documents, module instructions, a communication manifest, a policy, and storage guidance. It does not claim to be a running crawler, live viewer, scheduler, or production FOSSIL adapter; the target README explicitly marks those components as unimplemented, and its early JSON contracts are not enforced runtime boundaries.

Personal evidence and proposals belong in a **private FOSSIL pack**, outside this public repository. Queues, checkpoints, retries, and other operational state stay local. That separation is part of the project’s trust model, not a promise that the current checkout enforces it at runtime.

## What you can make or use

The useful unit is a short task packet for one research question. The active hiring-coach instruction can shape that packet into five proposed outputs:

- a role assessment with demonstrated, transferable, unproven, and unknown labels;
- a targeted collection task with pages, relationships, budgets, and stop conditions;
- a network plan that distinguishes observed relationships from unknowns;
- a profile and positioning plan with evidence needed before making a claim;
- one prioritized next proposal with assumptions, missing data, confidence, and a review date.

These are **proposed artifacts**, not approved identity changes or instructions to contact, connect, apply, publish, or edit a profile. The [active hiring-coach contract](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/modules/hiring-coach/instructions.md) is the source for this shape.

## How it works

The mechanism is intentionally small before it becomes architectural:

1. Start with one question, target role, owner constraints, and the evidence already available.
2. Ask for focused observations rather than a broad crawl; keep the page, depth, comment-expansion, and time budgets explicit.
3. Separate observed facts, owner-approved facts, interpretations, hypotheses, and missing data.
4. Preserve evidence references and a proposal separately, then ask the owner to decide what—if anything—should be tested or adopted.

The repository’s [communication manifest](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/config/communication-manifest.yaml) names the intended handoffs from collector to research to hiring coach and onward to brand, strategy, planning, writing, and review. It is a design manifest with `status: design_only`; it does not wire those modules into a live runtime.

## Evidence and boundaries

The claims below use four status labels so a reader can tell what the checkout actually supports.

| Status | What the pinned target supports | Evidence or boundary |
| --- | --- | --- |
| **Shipped** | Versioned policy, storage guidance, module instructions, a communication manifest, and the active hiring-coach role contract are present. | [Repository tree at the pinned commit](https://github.com/Pukujan/automated-agents/tree/f2a542858f6b84923b61b710b6a775c0a050b785) |
| **Experimentally supported** | A partial manual supervised run recorded the path profile → own post → post analytics → content analytics → older post → visible commenter profile. | [Current handoff](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/handoff.md); this is a recorded manual path, not a shipped browser implementation. |
| **Planned** | Bounded research exploration, structured capture, evidence brief, proposal preservation, and read-back through a future adapter. | [First-slice plan](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/first-slice.md) and [storage proposal](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/storage.md) |
| **Unknown** | The actual browser bridge, runtime, first research seeds, profile inputs, unattended execution, and backup destination are not established in the pinned checkout. | [Handoff open choices](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/handoff.md); `docs/PLAN.md` is currently a placeholder containing a missing-file error. |

The boundaries are deliberate:

- **Private FOSSIL owns personal evidence and proposals.** Public Git stores generic plans, policy, prompts, source, and contracts.
- **A saved proposal is not proof.** Persistence, evidential support, execution approval, and profile adoption remain separate decisions.
- **Collection is read-only by design.** The instructions prohibit messages, connection requests, follows, reactions, applications, publication, profile edits, bypassing access controls, and expansion beyond the task budget.
- **Early contracts do not enforce behavior.** The target’s JSON drafts and design manifest describe intended interfaces; they are not runtime boundaries in this commit.

## Image generation and use

These two images use the pinned helper’s explicitly labeled fallback direction because the target repository does not ship its own visual contract: original anime-inspired editorial scenes, a recurring human and friendly companion, blue-violet evening light, warm accents, and one clear explanatory idea per asset. They are target-specific illustrations, not a claim that the target runtime exists.

The complete prompts, exact copy, provider, dimensions, crop/accessibility guidance, rejection checks, review decisions, and SHA-256 hashes are recorded in [`.content-system/image-prompts.md`](.content-system/image-prompts.md). The reusable method is documented in the pinned helper’s [`docs/IMAGE_GUIDE.md`](https://github.com/Pukujan/content-generation-modules/blob/8d4f041e8b82f007000b3a1b83d08c39616cc8c7/docs/IMAGE_GUIDE.md).

| Asset | Reader question | Use |
| --- | --- | --- |
| [`assets/automated-agents-hero.png`](assets/automated-agents-hero.png) | Why should I care? | Wide hero below the title; introduces the move from role and evidence to a next proposal. |
| [`assets/automated-agents-boundaries.png`](assets/automated-agents-boundaries.png) | How does the work stay bounded? | Supporting visual after the opening problem; explains the task packet, focused research path, private evidence, proposal status, and stop boundary. |

## Templates and guides

For a maintainer continuing the work, start with the [target adapter in this package](.content-system/) and compare it with the exact pinned helper contract:

- [`system-version.json`](.content-system/system-version.json) pins helper version `0.3.1` and commit `8d4f041e8b82f007000b3a1b83d08c39616cc8c7`.
- [`project-brief.json`](.content-system/project-brief.json) maps users, problem, mechanism, evidence, and limits.
- [`brand-language.json`](.content-system/brand-language.json) keeps the voice careful and evidence-led.
- [`visual-style.json`](.content-system/visual-style.json) declares the fallback visual direction and crop roles.
- [`asset-manifest.json`](.content-system/asset-manifest.json) records the two raster assets and their hashes.
- [`review-rubric.json`](.content-system/review-rubric.json) keeps claim safety and human comprehension ahead of polish.

The helper’s required references are [`docs/CONTENT_RESEARCH.md`](https://github.com/Pukujan/content-generation-modules/blob/8d4f041e8b82f007000b3a1b83d08c39616cc8c7/docs/CONTENT_RESEARCH.md), [`docs/BRAND_DIRECTION.md`](https://github.com/Pukujan/content-generation-modules/blob/8d4f041e8b82f007000b3a1b83d08c39616cc8c7/docs/BRAND_DIRECTION.md), [`docs/README_PLAYBOOK.md`](https://github.com/Pukujan/content-generation-modules/blob/8d4f041e8b82f007000b3a1b83d08c39616cc8c7/docs/README_PLAYBOOK.md), [`docs/IMAGE_GUIDE.md`](https://github.com/Pukujan/content-generation-modules/blob/8d4f041e8b82f007000b3a1b83d08c39616cc8c7/docs/IMAGE_GUIDE.md), [`docs/PRIOR_WORK.md`](https://github.com/Pukujan/content-generation-modules/blob/8d4f041e8b82f007000b3a1b83d08c39616cc8c7/docs/PRIOR_WORK.md), [`docs/HOLDOUT_EVALUATION.md`](https://github.com/Pukujan/content-generation-modules/blob/8d4f041e8b82f007000b3a1b83d08c39616cc8c7/docs/HOLDOUT_EVALUATION.md), [`docs/MIGRATING_TO_0.3.md`](https://github.com/Pukujan/content-generation-modules/blob/8d4f041e8b82f007000b3a1b83d08c39616cc8c7/docs/MIGRATING_TO_0.3.md), [`docs/MIGRATING_TO_0.2.md`](https://github.com/Pukujan/content-generation-modules/blob/8d4f041e8b82f007000b3a1b83d08c39616cc8c7/docs/MIGRATING_TO_0.2.md), and [`templates/README.template.md`](https://github.com/Pukujan/content-generation-modules/blob/8d4f041e8b82f007000b3a1b83d08c39616cc8c7/templates/README.template.md).

## Prior work and references

This package carries forward the helper’s reviewed pattern rather than presenting it as newly invented here: [Eval Lab](https://github.com/Pukujan/Eval-lab), [Harness on Steroids](https://github.com/Pukujan/harness-on-steroids), [Custom Extensions](https://github.com/Pukujan/custom-extensions), and [Hades Product](https://github.com/Pukujan/hades-product) are named in the pinned helper’s [`docs/PRIOR_WORK.md`](https://github.com/Pukujan/content-generation-modules/blob/8d4f041e8b82f007000b3a1b83d08c39616cc8c7). Their contribution here is the method: human situation first, clear boundaries, a distinct supporting visual, exact prompt records, and a human review gate.

The target-specific story comes from the pinned Automated Agents checkout: the first slice is bounded research exploration, the active simple slice is the hiring coach, and personal evidence/proposals remain outside public Git. Because the target does not document a visual identity, the adapter labels the helper direction as a fallback and changes the subject to career research rather than copying helper characters, logos, or scenes.

## Try it

**Start with one explicit research question.** Read the [first-slice document](https://github.com/Pukujan/automated-agents/blob/f2a542858f6b84923b61b710b6a775c0a050b785/docs/first-slice.md), choose a target role, connection-list filter, or topic search, and keep the first run visible, bounded, and private. Do not treat this README package as evidence that the browser bridge or FOSSIL adapter is already implemented.

For the developer path, inspect the six files in [`.content-system/`](.content-system/), verify the pinned target and helper commits, then implement only the next useful run described by the repository’s handoff. Validate this package with:

```powershell
python work/cgm/scripts/validate_content_system.py --root work/cgm --adapter outputs/.content-system --project-root outputs
```

### Scan test

Read only the headings, bold phrases, and link text. They should communicate the problem, promise, mechanism, boundary, evidence status, and next action. The scanability rationale is in the pinned helper’s [`docs/CONTENT_RESEARCH.md`](https://github.com/Pukujan/content-generation-modules/blob/8d4f041e8b82f007000b3a1b83d08c39616cc8c7/docs/CONTENT_RESEARCH.md), and subjective quality still requires human review.
