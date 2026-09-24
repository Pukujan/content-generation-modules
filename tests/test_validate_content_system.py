import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_content_system import (
    check,
    check_adapter,
    check_narrative_assets,
    check_project_brief_v2,
    check_readme,
)


ROOT = Path(__file__).resolve().parents[1]
MODULES = sorted({"brand-foundation", "content-context", "writing-direction", "visual-direction", "image-generation", "html-demo"})
COMMIT = "a" * 40
SOURCE_URI = f"https://github.com/Pukujan/demo/blob/{COMMIT}/src/app.py#L2-L6"


def sample_evidence(**overrides):
    item = {
        "claim": "The command writes a report.",
        "source": "The command implementation and its test.",
        "status": "shipped",
        "supports": "The test confirms that this command writes a report for the sample input.",
        "limits": "The test does not establish performance or behavior for every input.",
        "recorded_at": "2026-09-23T12:00:00Z",
        "source_revision": {
            "kind": "repository_artifact",
            "reference": "Implementation and unit test",
            "repository": "Pukujan/demo",
            "commit": COMMIT,
            "path": "src/app.py",
            "locator": "lines 2-6",
            "uri": SOURCE_URI,
        },
        "cite_in_readme": False,
    }
    item.update(overrides)
    return item


def write_adapter(adapter: Path, brief_version="v2", helper_version="0.4.0"):
    project_schema = f"content-generation.project-brief.{brief_version}"
    evidence = sample_evidence()
    if brief_version == "v1":
        evidence = {"claim": evidence["claim"], "source": evidence["source"]}
    files = {
        "system-version.json": {
            "schema_version": "content-generation.adapter.v1",
            "helper_repository": "https://github.com/Pukujan/content-generation-modules",
            "helper_version": helper_version,
            "helper_commit": COMMIT,
            "modules": MODULES,
        },
        "project-brief.json": {
            "schema_version": project_schema,
            "project": "Demo",
            "audience": ["people"],
            "problem": "A concrete reader problem.",
            "solution": "A useful response.",
            "evidence": [evidence],
            "boundaries": ["One explicit limitation."],
        },
        "brand-language.json": {"schema_version": "content-generation.brand-language.v1", "name": "Demo", "personality": ["clear"], "promise": "A useful promise", "avoid": ["hype"]},
        "visual-style.json": {"schema_version": "content-generation.visual-style.v1", "reference_asset": "hero.png", "generation_workflow": "built-in image_gen", "narrative_roles": ["hero", "problem", "supporting"], "palette": {"background": "#000"}, "roles": {"hero": {}}, "reject_when": ["busy"]},
        "asset-manifest.json": {"schema_version": "content-generation.asset-manifest.v1", "system_version": helper_version, "assets": [{"path": "diagram.png", "role": "diagram"}]},
        "review-rubric.json": {"schema_version": "content-generation.review-rubric.v1", "dimensions": [{"id": "clarity", "question": "clear?"}], "decision_rule": "human review"},
    }
    for name, value in files.items():
        (adapter / name).write_text(json.dumps(value), encoding="utf-8")


class ContentSystemValidationTests(unittest.TestCase):
    def test_repository_contract_is_valid(self):
        self.assertEqual(check(ROOT), [])

    def test_repository_contract_requires_041_boundary_policy(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "helper"
            shutil.copytree(
                ROOT,
                target,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
            )
            version_path = target / "system-version.json"
            version = json.loads(version_path.read_text(encoding="utf-8"))
            del version["boundary_disclosure_contract"]
            version_path.write_text(json.dumps(version), encoding="utf-8")
            errors = check(target)
            self.assertTrue(any("must declare content-generation.must-preserve.v1" in error for error in errors), errors)

    def test_readme_gate_rejects_a_technical_only_readme(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "templates").mkdir()
            (target / "templates" / "readme-contract.json").write_bytes(
                (ROOT / "templates" / "readme-contract.json").read_bytes()
            )
            (target / "README.md").write_text("# Internal API\n\n## Setup\n", encoding="utf-8")
            errors = check_readme(target)
            self.assertTrue(any("README missing required section" in error for error in errors))
            self.assertTrue(any("local raster narrative image" in error for error in errors))

    def test_readme_gate_rejects_technical_details_before_the_human_story(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "templates").mkdir()
            (target / "templates" / "readme-contract.json").write_bytes(
                (ROOT / "templates" / "readme-contract.json").read_bytes()
            )
            (target / "README.md").write_text(
                "# Project\n\n```powershell\npython run.py\n```\n\n## Why this exists\n",
                encoding="utf-8",
            )
            errors = check_readme(target)
            self.assertTrue(any("technical code after the human situation" in error for error in errors))

    def test_readme_gate_requires_scan_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "templates").mkdir()
            (target / "templates" / "readme-contract.json").write_bytes(
                (ROOT / "templates" / "readme-contract.json").read_bytes()
            )
            (target / "README.md").write_text(
                "# Project\n\n## Why this exists\n\nA human situation.\n",
                encoding="utf-8",
            )
            errors = check_readme(target)
            self.assertTrue(any("bold scan anchor" in error for error in errors))

    def test_readme_gate_rejects_malformed_commit_pinned_github_blob_links(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "templates").mkdir()
            (target / "templates" / "readme-contract.json").write_bytes(
                (ROOT / "templates" / "readme-contract.json").read_bytes()
            )
            commit = "d" * 40
            (target / "README.md").write_text(
                "# Project\n\n"
                f"[Broken citation](https://github.com/Pukujan/demo/blob/{commit}#L14-L19)\n\n"
                "[Branch citation](https://github.com/Pukujan/demo/blob/main/README.md)\n",
                encoding="utf-8",
            )

            errors = check_readme(target)

            self.assertTrue(any("commit-pinned GitHub blob/tree link" in error for error in errors), errors)

    def test_readme_gate_rejects_absolute_local_paths_but_allows_code_examples(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "templates").mkdir()
            (target / "templates" / "readme-contract.json").write_bytes(
                (ROOT / "templates" / "readme-contract.json").read_bytes()
            )
            (target / "README.md").write_text(
                "# Project\n\n"
                "The generated handoff was written to C:\\Users\\pujan\\Documents\\handoff.md.\n\n"
                "```powershell\n"
                "Get-Content C:\\Users\\pujan\\Documents\\example.md\n"
                "```\n",
                encoding="utf-8",
            )

            errors = check_readme(target)

            self.assertTrue(any("absolute local path" in error for error in errors), errors)
            self.assertEqual(sum("absolute local path" in error for error in errors), 1, errors)

    def test_prompt_record_hash_must_match_manifest_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "assets").mkdir()
            image = project / "assets" / "hero.png"
            image.write_bytes(b"image bytes")
            actual_hash = hashlib.sha256(image.read_bytes()).hexdigest()
            wrong_hash = hashlib.sha256(b"different image bytes").hexdigest()
            short_hash = wrong_hash[:-1]
            (project / "assets" / "IMAGE_NOTES.md").write_text(
                f"# Hero\n\n- Output: `assets/hero.png`\n"
                f"- SHA-256: `{wrong_hash}`\n"
                f"- SHA-256: `{short_hash}`\n",
                encoding="utf-8",
            )
            asset = {
                "path": "assets/hero.png",
                "role": "hero",
                "orientation": "wide",
                "dimensions": "1600x900",
                "text_policy": "exact copy",
                "prompt_recipe": "Title / Subtitle",
                "exact_title": "Title",
                "exact_subtitle": "Subtitle",
                "alt_text": "A clear story",
                "usage": "README hero",
                "crop_behavior": "center-safe",
                "rejection_conditions": ["garbled copy"],
                "review_decision": "accepted",
                "provider": "built-in image_gen",
                "prompt_record": "assets/IMAGE_NOTES.md#hero",
                "hash": actual_hash,
            }
            visual = {"generation_workflow": "built-in image_gen", "narrative_roles": ["hero"]}

            errors = check_narrative_assets(visual, {"assets": [asset]}, project)

            self.assertTrue(any("prompt record hash does not match manifest" in error for error in errors), errors)
            self.assertTrue(any("prompt record hash must be a SHA-256 digest" in error for error in errors), errors)

    def test_missing_module_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for source in (ROOT / "system-version.json", ROOT / "CHATGPT_SETUP.md"):
                destination = target / source.name
                destination.write_bytes(source.read_bytes())
            errors = check(target)
            self.assertTrue(any("missing module" in error for error in errors))

    def test_adapter_requires_project_and_asset_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            adapter = Path(directory) / ".content-system"
            adapter.mkdir()
            files = {
                "system-version.json": {
                    "schema_version": "content-generation.adapter.v1",
                    "helper_repository": "https://example.invalid/helper",
                    "helper_version": "0.1.1",
                    "helper_commit": COMMIT,
                    "modules": sorted({"brand-foundation", "content-context", "writing-direction", "visual-direction", "image-generation", "html-demo"}),
                },
                "project-brief.json": {"schema_version": "content-generation.project-brief.v1", "project": "Demo", "audience": ["people"], "problem": "problem", "solution": "solution", "evidence": [{"claim": "claim", "source": "README.md"}], "boundaries": ["boundary"]},
                "brand-language.json": {"schema_version": "content-generation.brand-language.v1", "name": "Demo", "personality": ["clear"], "promise": "promise", "avoid": ["hype"]},
                "visual-style.json": {"schema_version": "content-generation.visual-style.v1", "reference_asset": "hero.png", "palette": {"background": "#000"}, "roles": {"hero": {}}, "reject_when": ["busy"]},
                "asset-manifest.json": {"schema_version": "content-generation.asset-manifest.v1", "system_version": "0.1.1", "assets": [{"path": "hero.png"}]},
                "review-rubric.json": {"schema_version": "content-generation.review-rubric.v1", "dimensions": [{"id": "clarity", "question": "clear?"}], "decision_rule": "human review"},
            }
            for name, value in files.items():
                (adapter / name).write_text(__import__("json").dumps(value), encoding="utf-8")
            project_root = Path(directory) / "project"
            project_root.mkdir()
            (project_root / "hero.png").write_bytes(b"placeholder")
            self.assertEqual(check_adapter(adapter, project_root), [])

    def test_03_adapter_rejects_svg_narrative_substitution(self):
        with tempfile.TemporaryDirectory() as directory:
            adapter = Path(directory) / ".content-system"
            adapter.mkdir()
            files = {
                "system-version.json": {
                    "schema_version": "content-generation.adapter.v1",
                    "helper_repository": "https://example.invalid/helper",
                    "helper_version": "0.3.1",
                    "helper_commit": "abc123",
                    "modules": sorted({"brand-foundation", "content-context", "writing-direction", "visual-direction", "image-generation", "html-demo"}),
                },
                "project-brief.json": {"schema_version": "content-generation.project-brief.v1", "project": "Demo", "audience": ["people"], "problem": "problem", "solution": "solution", "evidence": [{"claim": "claim", "source": "README.md"}], "boundaries": ["boundary"]},
                "brand-language.json": {"schema_version": "content-generation.brand-language.v1", "name": "Demo", "personality": ["clear"], "promise": "promise", "avoid": ["hype"]},
                "visual-style.json": {"schema_version": "content-generation.visual-style.v1", "reference_asset": "hero.svg", "generation_workflow": "built-in image_gen", "narrative_roles": ["hero"], "palette": {"background": "#000"}, "roles": {"hero": {}}, "reject_when": ["busy"]},
                "asset-manifest.json": {"schema_version": "content-generation.asset-manifest.v1", "system_version": "0.3.1", "assets": [{"path": "hero.svg", "role": "hero", "orientation": "wide", "dimensions": "1600x900", "text_policy": "exact copy", "prompt_recipe": "Title / Subtitle", "exact_title": "Title", "exact_subtitle": "Subtitle", "alt_text": "A clear story", "usage": "README hero", "crop_behavior": "center", "rejection_conditions": ["garbled copy"], "review_decision": "accepted", "provider": "built-in image_gen", "prompt_record": "IMAGE_NOTES.md", "hash": hashlib.sha256(b"placeholder").hexdigest()}]},
                "review-rubric.json": {"schema_version": "content-generation.review-rubric.v1", "dimensions": [{"id": "clarity", "question": "clear?"}], "decision_rule": "human review"},
            }
            for name, value in files.items():
                (adapter / name).write_text(json.dumps(value), encoding="utf-8")
            project_root = Path(directory) / "project"
            project_root.mkdir()
            (project_root / "hero.svg").write_bytes(b"placeholder")
            (project_root / "IMAGE_NOTES.md").write_text("prompt record", encoding="utf-8")
            errors = check_adapter(adapter, project_root)
            self.assertTrue(any("must be a raster image" in error for error in errors))

    def test_prompt_record_accepts_a_markdown_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "assets").mkdir()
            image = project / "assets" / "hero.png"
            image.write_bytes(b"image bytes")
            image_hash = hashlib.sha256(image.read_bytes()).hexdigest()
            (project / "assets" / "IMAGE_NOTES.md").write_text(
                f"# Hero\n\n- Output: `assets/hero.png`\n- SHA-256: `{image_hash}`\n",
                encoding="utf-8",
            )
            asset = {
                "path": "assets/hero.png",
                "role": "hero",
                "orientation": "wide",
                "dimensions": "1600x900",
                "text_policy": "exact copy",
                "prompt_recipe": "Title / Subtitle",
                "exact_title": "Title",
                "exact_subtitle": "Subtitle",
                "alt_text": "A clear story",
                "usage": "README hero",
                "crop_behavior": "center-safe",
                "rejection_conditions": ["garbled copy"],
                "review_decision": "accepted",
                "provider": "built-in image_gen",
                "prompt_record": "assets/IMAGE_NOTES.md#hero",
                "hash": hashlib.sha256(image.read_bytes()).hexdigest(),
            }
            visual = {"generation_workflow": "built-in image_gen", "narrative_roles": ["hero"]}
            self.assertEqual(check_narrative_assets(visual, {"assets": [asset]}, project), [])

    def test_non_narrative_role_cannot_claim_readme_hero_usage(self):
        asset = {
            "path": "assets/flow.svg",
            "role": "diagram",
            "usage": "README hero and How it works supporting visual",
        }
        visual = {"generation_workflow": "built-in image_gen", "narrative_roles": ["hero", "supporting"]}
        errors = check_narrative_assets(visual, {"assets": [asset]})
        self.assertTrue(any("usage declares a narrative role" in error for error in errors), errors)

    def test_readme_minimum_counts_only_raster_images(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "templates").mkdir()
            (target / "templates" / "readme-contract.json").write_bytes(
                (ROOT / "templates" / "readme-contract.json").read_bytes()
            )
            (target / "assets").mkdir()
            (target / "assets" / "one.svg").write_text("<svg/>", encoding="utf-8")
            (target / "assets" / "two.svg").write_text("<svg/>", encoding="utf-8")
            (target / "README.md").write_text(
                "# Project\n\n**A useful story.**\n\n"
                "![One](assets/one.svg)\n\n![Two](assets/two.svg)\n",
                encoding="utf-8",
            )
            errors = check_readme(target)
            self.assertTrue(any("raster narrative image" in error for error in errors), errors)

    def test_adapter_validation_checks_target_readme_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            adapter = base / ".content-system"
            adapter.mkdir()
            write_adapter(adapter, "v2")
            target = base / "project"
            target.mkdir()
            (target / "README.md").write_text("# Internal API\n\n## Setup\n", encoding="utf-8")
            errors = check_adapter(adapter, target, helper_root=ROOT)
            self.assertTrue(any("raster narrative image" in error for error in errors), errors)

    def test_v2_claim_record_requires_bounded_revision_pinned_evidence(self):
        evidence = sample_evidence()
        readme = f"The report is generated. [Implementation]({SOURCE_URI})"
        brief = {"schema_version": "content-generation.project-brief.v2", "evidence": [evidence]}
        self.assertEqual(check_project_brief_v2(brief, readme), [])
        bounded = sample_evidence(valid_time={"start": "2026-09-20T00:00:00Z", "end": "2026-09-23T12:00:00Z"})
        self.assertEqual(check_project_brief_v2({**brief, "evidence": [bounded]}, readme), [])

        cases = [
            ({**evidence, "supports": ""}, "missing non-empty supports"),
            ({**evidence, "limits": ""}, "missing non-empty limits"),
            ({**evidence, "recorded_at": "2026-09-23T12:00:00"}, "recorded_at must be an RFC 3339 timestamp"),
            ({**evidence, "valid_time": {"start": "2026-09-23T12:00:00Z", "end": "2026-09-22T12:00:00Z"}}, "must not follow"),
            ({**evidence, "status": []}, "has invalid status"),
            ({**evidence, "source_revision": {**evidence["source_revision"], "uri": "https://github.com/Pukujan/demo/blob/main/src/app.py"}}, "immutable web permalink"),
            ({**evidence, "source_revision": {**evidence["source_revision"], "uri": "https://[invalid"}}, "immutable web permalink"),
            ({**evidence, "cite_in_readme": True}, "not linked in the target README"),
            ({**evidence, "status": "shipped", "source_revision": {"kind": "unknown_search", "reference": "Searched the available repository", "observed_at": "2026-09-23"}}, "cannot label a claim shipped"),
        ]
        for invalid, expected in cases:
            with self.subTest(expected=expected):
                target_readme = "" if expected == "not linked in the target README" else readme
                errors = check_project_brief_v2({**brief, "evidence": [invalid]}, target_readme)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_v2_claim_order_is_metamorphically_invariant(self):
        first = sample_evidence()
        second = sample_evidence(claim="The same implementation has a defined entry point.")
        brief = {"schema_version": "content-generation.project-brief.v2", "evidence": [first, second]}
        readme = ""
        self.assertEqual(check_project_brief_v2(brief, readme), [])
        brief["evidence"].reverse()
        self.assertEqual(check_project_brief_v2(brief, readme), [])

    def test_04_adapter_requires_v2_brief_and_accepts_valid_v2(self):
        with tempfile.TemporaryDirectory() as directory:
            adapter = Path(directory) / ".content-system"
            adapter.mkdir()
            write_adapter(adapter, "v2")
            self.assertEqual(check_adapter(adapter), [])

            write_adapter(adapter, "v1")
            errors = check_adapter(adapter)
            self.assertTrue(any("require project-brief.v2" in error for error in errors), errors)

    def test_adapter_requires_a_full_pinned_helper_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            adapter = Path(directory) / ".content-system"
            adapter.mkdir()
            write_adapter(adapter, "v2")
            system_path = adapter / "system-version.json"
            system = json.loads(system_path.read_text(encoding="utf-8"))
            system["helper_commit"] = "abc123"
            system_path.write_text(json.dumps(system), encoding="utf-8")
            errors = check_adapter(adapter)
            self.assertTrue(any("helper_commit must be a full commit ID" in error for error in errors), errors)

    def test_041_requires_target_readme_to_repeat_protected_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            adapter = base / ".content-system"
            adapter.mkdir()
            write_adapter(adapter, helper_version="0.4.1")
            brief_path = adapter / "project-brief.json"
            brief = json.loads(brief_path.read_text(encoding="utf-8"))
            brief["boundaries"] = ["The V0 does not include portable-pack export or import."]
            brief["must_preserve"] = brief["boundaries"]
            brief_path.write_text(json.dumps(brief), encoding="utf-8")
            target = base / "project"
            target.mkdir()
            (target / "diagram.png").write_bytes(b"placeholder")
            readme_path = target / "README.md"
            readme_path.write_text(
                "# Demo\n\nThe V0 does not include portable-pack export or import.\n",
                encoding="utf-8",
            )
            self.assertEqual(check_adapter(adapter, target), [])

            readme_path.write_text("# Demo\n\nExport is planned.\n", encoding="utf-8")
            errors = check_adapter(adapter, target)
            self.assertTrue(any("must_preserve boundary is not stated" in error for error in errors), errors)

    def test_041_requires_target_readme_to_repeat_every_declared_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            adapter = base / ".content-system"
            adapter.mkdir()
            write_adapter(adapter, helper_version="0.4.1")
            brief_path = adapter / "project-brief.json"
            brief = json.loads(brief_path.read_text(encoding="utf-8"))
            brief["boundaries"] = [
                "The V0 does not include portable-pack export or import.",
                "The V0 does not include hosted collaboration.",
            ]
            brief["must_preserve"] = [brief["boundaries"][0]]
            brief_path.write_text(json.dumps(brief), encoding="utf-8")
            target = base / "project"
            target.mkdir()
            (target / "diagram.png").write_bytes(b"placeholder")
            (target / "README.md").write_text(
                "# Demo\n\nThe V0 does not include portable-pack export or import.\n",
                encoding="utf-8",
            )

            errors = check_adapter(adapter, target)

            self.assertTrue(any("declared boundary is not stated" in error for error in errors), errors)

    def test_041_requires_boundary_text_to_be_verbatim(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            adapter = base / ".content-system"
            adapter.mkdir()
            write_adapter(adapter, helper_version="0.4.1")
            brief_path = adapter / "project-brief.json"
            brief = json.loads(brief_path.read_text(encoding="utf-8"))
            brief["boundaries"] = ["The V0 does not include portable-pack export or import."]
            brief["must_preserve"] = brief["boundaries"]
            brief_path.write_text(json.dumps(brief), encoding="utf-8")
            target = base / "project"
            target.mkdir()
            (target / "diagram.png").write_bytes(b"placeholder")
            (target / "README.md").write_text(
                "# Demo\n\nthe V0 does not include portable-pack export or import.\n",
                encoding="utf-8",
            )

            errors = check_adapter(adapter, target)

            self.assertTrue(any("boundary is not stated" in error for error in errors), errors)

    def test_041_requires_must_preserve_entries_to_be_declared_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            adapter = base / ".content-system"
            adapter.mkdir()
            write_adapter(adapter, helper_version="0.4.1")
            brief_path = adapter / "project-brief.json"
            brief = json.loads(brief_path.read_text(encoding="utf-8"))
            brief["boundaries"] = ["The V0 does not include portable-pack export or import."]
            brief["must_preserve"] = ["The V0 does not include hosted collaboration."]
            brief_path.write_text(json.dumps(brief), encoding="utf-8")
            target = base / "project"
            target.mkdir()
            (target / "diagram.png").write_bytes(b"placeholder")
            (target / "README.md").write_text(
                "# Demo\n\nThe V0 does not include hosted collaboration.\n",
                encoding="utf-8",
            )

            errors = check_adapter(adapter, target)

            self.assertTrue(any("must_preserve entry is not a declared boundary" in error for error in errors), errors)

    def test_041_requires_at_least_one_protected_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            adapter = base / ".content-system"
            adapter.mkdir()
            write_adapter(adapter, helper_version="0.4.1")
            target = base / "project"
            target.mkdir()
            (target / "diagram.png").write_bytes(b"placeholder")
            (target / "README.md").write_text("# Demo\n", encoding="utf-8")
            errors = check_adapter(adapter, target)
            self.assertTrue(any("must_preserve must contain at least one" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
