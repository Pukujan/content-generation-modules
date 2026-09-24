#!/usr/bin/env python3
"""Dependency-free structural checks for the content-generation helper contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.parse import unquote, urlparse


EXPECTED_MODULES = {
    "brand-foundation",
    "content-context",
    "writing-direction",
    "visual-direction",
    "image-generation",
    "html-demo",
}

NARRATIVE_ROLE_MARKERS = ("hero", "problem", "supporting", "evidence", "story", "social")
NARRATIVE_RASTER_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
FULL_COMMIT_RE = r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}"
GITHUB_COMMIT_PINNED_LINK_RE = re.compile(
    rf"https?://(?:www\.)?github\.com/[^\s<>()\[\]\"']+",
    flags=re.IGNORECASE,
)
PROMPT_RECORD_HASH_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:sha-?256|hash)\s*:\s*`?([0-9a-fA-F]+)`?\s*[.,]?\s*$",
    flags=re.IGNORECASE | re.MULTILINE,
)
WINDOWS_ABSOLUTE_PATH_RE = re.compile(
    r"(?<![\w])(?:[A-Za-z]:[\\/])(?:[^<>\s\[\]()`\"']+)",
    flags=re.IGNORECASE,
)
USER_HOME_PATH_RE = re.compile(
    r"(?<![\w])(?:[\\/]+Users[\\/][A-Za-z0-9._-]+(?:[\\/][^<>\s\[\]()`\"']*)?)",
    flags=re.IGNORECASE,
)
REQUIRED_NARRATIVE_ASSET_FIELDS = (
    "path",
    "role",
    "orientation",
    "dimensions",
    "text_policy",
    "prompt_recipe",
    "exact_title",
    "exact_subtitle",
    "alt_text",
    "usage",
    "crop_behavior",
    "rejection_conditions",
    "review_decision",
    "provider",
    "prompt_record",
    "hash",
)

REQUIRED_HELPER_DOCS = (
    "docs/CONTENT_RESEARCH.md",
    "docs/BRAND_DIRECTION.md",
    "docs/README_PLAYBOOK.md",
    "docs/IMAGE_GUIDE.md",
    "docs/PRIOR_WORK.md",
    "docs/HOLDOUT_EVALUATION.md",
    "docs/MIGRATING_TO_0.3.md",
    "docs/MIGRATING_TO_0.2.md",
    "docs/MIGRATING_TO_0.4.md",
    "docs/README_QUALITY_PDD.md",
    "docs/README_QUALITY_SDD.md",
    "docs/README_QUALITY_TDD.md",
    "docs/PROVENANCE_AND_CITATION.md",
    "docs/REVERSE_ANALYSIS_PCM_AND_ADOPTERS.md",
)


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"expected object in {path}")
    return value


def _version_tuple(value: object) -> tuple[int, int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", str(value or ""))
    if not match:
        return (0, 0, 0)
    return tuple(int(part) for part in match.groups())


def _valid_date(value: object) -> bool:
    try:
        date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return False
    return True


def _parse_aware_datetime(value: object) -> datetime | None:
    if not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})",
        str(value or ""),
    ):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return parsed if parsed.utcoffset() is not None else None


def _valid_web_uri(value: object) -> bool:
    try:
        parsed = urlparse(str(value or ""))
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _valid_repository_permalink(uri: object, repository: str, commit: str, source_path: str) -> bool:
    try:
        parsed = urlparse(str(uri or ""))
    except ValueError:
        return False
    if parsed.scheme != "https" or not parsed.netloc:
        return False
    parts = [unquote(part) for part in parsed.path.split("/") if part]
    repository_parts = repository.split("/")
    repo_index = next(
        (index for index in range(len(parts) - len(repository_parts) + 1)
         if parts[index:index + len(repository_parts)] == repository_parts),
        None,
    )
    if repo_index is None:
        return False
    commit_index = next(
        (index for index in range(repo_index + len(repository_parts), len(parts))
         if parts[index].lower() == commit.lower()),
        None,
    )
    if commit_index is None:
        return False
    linked_path = "/".join(parts[commit_index + 1:])
    return linked_path == source_path or linked_path.startswith(f"{source_path}/")


def _check_github_commit_pinned_links(readme_text: str) -> list[str]:
    """Check only GitHub blob/tree URLs that visibly pin a full commit ID.

    This is intentionally structural and offline. Branch links, issue links, and
    ordinary external references are outside this check.
    """
    errors: list[str] = []
    for match in GITHUB_COMMIT_PINNED_LINK_RE.finditer(readme_text):
        raw_url = match.group(0).rstrip(".,;:!?")
        try:
            parsed = urlparse(raw_url)
        except ValueError:
            continue
        if parsed.netloc.lower().removeprefix("www.") != "github.com":
            continue
        parts = [unquote(part) for part in parsed.path.split("/") if part]
        if len(parts) < 4 or parts[2].lower() not in {"blob", "tree"}:
            continue
        if not re.fullmatch(FULL_COMMIT_RE, parts[3]):
            continue
        if len(parts) == 4:
            errors.append(
                "README contains a malformed commit-pinned GitHub blob/tree link "
                f"(missing repository path): {raw_url}"
            )
    return errors


def _user_facing_readme_lines(readme_text: str):
    """Yield README lines with fenced and inline code removed."""
    fence: str | None = None
    for line_number, line in enumerate(readme_text.splitlines(), start=1):
        fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_match:
            marker = fence_match.group(1)[0]
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            continue
        if fence is not None:
            continue
        without_inline_code = re.sub(r"`[^`\n]*`", "", line)
        without_urls = re.sub(r"(?i)\b(?:https?|file)://[^\s<>()\[\]]+", "", without_inline_code)
        yield line_number, without_urls


def _check_readme_absolute_local_paths(readme_text: str) -> list[str]:
    errors: list[str] = []
    seen: set[tuple[int, str]] = set()
    for line_number, line in _user_facing_readme_lines(readme_text):
        windows_matches = list(WINDOWS_ABSOLUTE_PATH_RE.finditer(line))
        home_matches = [
            match
            for match in USER_HOME_PATH_RE.finditer(line)
            if not any(
                windows.start() <= match.start() and windows.end() >= match.end()
                for windows in windows_matches
            )
        ]
        matches = windows_matches + home_matches
        for match in matches:
            path_text = match.group(0).rstrip(".,;:!?)]}")
            key = (line_number, path_text)
            if key in seen:
                continue
            seen.add(key)
            errors.append(
                "README contains an absolute local path in user-facing content "
                f"at line {line_number}: {path_text}"
            )
    return errors


def _prompt_record_section(prompt_record_text: str, asset_path: str) -> str:
    """Return the Markdown section that records one asset, when identifiable."""
    normalized_path = asset_path.replace("\\", "/")
    filename = Path(normalized_path).name
    headings = list(re.finditer(r"^#{1,6}\s+.+$", prompt_record_text, flags=re.MULTILINE))
    if not headings:
        return prompt_record_text
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(prompt_record_text)
        section = prompt_record_text[heading.start():end]
        if normalized_path in section.replace("\\", "/") or filename in section:
            return section
    return ""


def _check_prompt_record_hash(
    asset: dict,
    image_path: Path,
    manifest_digest: str,
    prompt_record: Path,
) -> list[str]:
    errors: list[str] = []
    try:
        prompt_record_text = prompt_record.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        errors.append(f"narrative asset prompt record cannot be read: {asset.get('prompt_record')}")
        return errors

    asset_path = str(asset.get("path", ""))
    section = _prompt_record_section(prompt_record_text, asset_path)
    declared_hashes = [match.group(1) for match in PROMPT_RECORD_HASH_RE.finditer(section)]
    if not declared_hashes:
        errors.append(f"narrative asset prompt record missing SHA-256 declaration: {asset_path}")
        return errors

    actual_digest = hashlib.sha256(image_path.read_bytes()).hexdigest() if image_path.is_file() else None
    for declared_hash in declared_hashes:
        if not re.fullmatch(r"[0-9a-fA-F]{64}", declared_hash):
            errors.append(f"narrative asset prompt record hash must be a SHA-256 digest: {asset_path}")
            continue
        if declared_hash.lower() != manifest_digest.lower():
            errors.append(f"narrative asset prompt record hash does not match manifest: {asset_path}")
        if actual_digest is not None and declared_hash.lower() != actual_digest.lower():
            errors.append(f"narrative asset prompt record hash does not match file: {asset_path}")
    return errors


def check_project_brief_v2(project: dict, readme_text: str | None = None) -> list[str]:
    """Check claim explanations and the source identity needed to reproduce them."""
    errors: list[str] = []
    if project.get("schema_version") != "content-generation.project-brief.v2":
        errors.append("project brief must declare content-generation.project-brief.v2")
    evidence = project.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("project-brief v2 must contain at least one evidence item")
        return errors

    allowed_statuses = {"shipped", "experimentally_supported", "planned", "unknown"}
    allowed_kinds = {
        "repository_artifact",
        "external_source",
        "user_observation",
        "owner_decision",
        "experiment_result",
        "unknown_search",
    }
    repo_kinds = {"repository_artifact"}

    for index, item in enumerate(evidence, start=1):
        label = f"project-brief evidence item {index}"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue

        for field in ("claim", "source", "supports", "limits"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{label} missing non-empty {field}")
        if item.get("supports") == item.get("limits") and item.get("supports"):
            errors.append(f"{label} supports and limits must explain different things")
        if _parse_aware_datetime(item.get("recorded_at")) is None:
            errors.append(f"{label} recorded_at must be an RFC 3339 timestamp with a timezone")

        valid_time = item.get("valid_time")
        if valid_time is not None:
            if not isinstance(valid_time, dict) or set(valid_time) != {"start", "end"}:
                errors.append(f"{label} valid_time must contain start and end")
            else:
                start_value, end_value = valid_time["start"], valid_time["end"]
                start = _parse_aware_datetime(start_value) if start_value is not None else None
                end = _parse_aware_datetime(end_value) if end_value is not None else None
                if start_value is not None and start is None:
                    errors.append(f"{label} valid_time.start must be a timezone-aware RFC 3339 timestamp")
                if end_value is not None and end is None:
                    errors.append(f"{label} valid_time.end must be a timezone-aware RFC 3339 timestamp")
                if start_value is None and end_value is None:
                    errors.append(f"{label} valid_time must have at least one bounded endpoint")
                if start is not None and end is not None and start > end:
                    errors.append(f"{label} valid_time.start must not follow valid_time.end")

        status = item.get("status")
        if not isinstance(status, str) or status not in allowed_statuses:
            errors.append(f"{label} has invalid status: {status}")
        cite_in_readme = item.get("cite_in_readme")
        if not isinstance(cite_in_readme, bool):
            errors.append(f"{label} cite_in_readme must be a boolean")

        revision = item.get("source_revision")
        if not isinstance(revision, dict):
            errors.append(f"{label} missing source_revision object")
            continue

        kind = revision.get("kind")
        if not isinstance(kind, str) or kind not in allowed_kinds:
            errors.append(f"{label} has unsupported source_revision kind: {kind}")
            continue

        if not isinstance(revision.get("reference"), str) or not revision["reference"].strip():
            errors.append(f"{label} source_revision missing reference")

        if kind in repo_kinds:
            repository = str(revision.get("repository", ""))
            if not re.fullmatch(r"[^/\s]+/[^/\s]+", repository):
                errors.append(f"{label} repository source needs owner/repository")
            commit = str(revision.get("commit", ""))
            if not re.fullmatch(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})", commit):
                errors.append(f"{label} repository source needs a full commit ID")
            source_path = str(revision.get("path", ""))
            if (
                not source_path
                or "\\" in source_path
                or Path(source_path).is_absolute()
                or ".." in Path(source_path).parts
            ):
                errors.append(f"{label} repository source needs a repository-relative path")
            if not isinstance(revision.get("locator"), str) or not revision["locator"].strip():
                errors.append(f"{label} repository source needs a line, heading, or record locator")
            if not _valid_repository_permalink(revision.get("uri"), repository, commit, source_path):
                errors.append(
                    f"{label} repository source needs an immutable web permalink containing its repository, full commit ID, and path"
                )
        elif kind in {"external_source", "experiment_result"}:
            if not _valid_web_uri(revision.get("uri")):
                errors.append(f"{label} {kind} source needs a direct HTTP(S) URI")
            if not _valid_date(revision.get("accessed_at")):
                errors.append(f"{label} {kind} source needs accessed_at in YYYY-MM-DD form")
            if kind == "experiment_result" and not revision.get("locator"):
                errors.append(f"{label} experiment source needs a run or artifact locator")
        elif kind in {"user_observation", "owner_decision", "unknown_search"}:
            if not _valid_date(revision.get("observed_at")):
                errors.append(f"{label} {kind} source needs observed_at in YYYY-MM-DD form")
        if revision.get("uri") and not _valid_web_uri(revision["uri"]):
            errors.append(f"{label} source_revision URI must use HTTP(S)")
        if revision.get("observed_at") and not _valid_date(revision["observed_at"]):
            errors.append(f"{label} observed_at must use YYYY-MM-DD form")
        if revision.get("published_at") and not _valid_date(revision["published_at"]):
            errors.append(f"{label} published_at must use YYYY-MM-DD form")
        if revision.get("accessed_at") and not _valid_date(revision["accessed_at"]):
            errors.append(f"{label} accessed_at must use YYYY-MM-DD form")
        if revision.get("sha256") and not re.fullmatch(r"[0-9a-fA-F]{64}", str(revision["sha256"])):
            errors.append(f"{label} sha256 must be a SHA-256 digest")

        if status != "unknown" and kind == "unknown_search":
            errors.append(f"{label} cannot label a claim {status} when its only source is an unknown search")
        if cite_in_readme:
            uri = revision.get("uri")
            if not _valid_web_uri(uri):
                errors.append(f"{label} requires a public citation URI")
            elif readme_text is None:
                errors.append(f"{label} citation check requires the target README")
            elif str(uri) not in readme_text:
                errors.append(f"{label} citation URI is not linked in the target README")

    return errors


def check_narrative_assets(
    visual: dict, manifest: dict, project_root: Path | None = None
) -> list[str]:
    """Enforce the 0.3.x narrative-image provenance contract for target adapters."""
    errors: list[str] = []
    if visual.get("generation_workflow") != "built-in image_gen":
        errors.append("adapter visual-style.json must declare generation_workflow: built-in image_gen")

    roles = visual.get("narrative_roles")
    if not isinstance(roles, list) or not roles:
        errors.append("adapter visual-style.json must declare narrative_roles")
        role_markers = NARRATIVE_ROLE_MARKERS
    else:
        role_markers = tuple(str(role).lower() for role in roles)

    for asset in manifest.get("assets", []):
        role = str(asset.get("role", "")).lower()
        is_narrative_role = any(
            role == marker or role.startswith(f"{marker} ") for marker in role_markers
        )
        usage = str(asset.get("usage", "")).lower()
        narrative_usage = any(
            marker in usage
            for marker in (
                "readme hero",
                "readme problem",
                "readme supporting",
                "readme narrative",
                "hero image",
                "supporting image",
                "problem image",
                "story image",
            )
        )
        if narrative_usage and not is_narrative_role:
            errors.append(
                f"narrative asset usage declares a narrative role but its manifest role is not narrative: {asset.get('path', '<unknown>')}"
            )
        if not is_narrative_role:
            continue

        for field in REQUIRED_NARRATIVE_ASSET_FIELDS:
            if not asset.get(field):
                errors.append(f"narrative asset {asset.get('path', '<unknown>')} missing {field}")

        asset_path = str(asset.get("path", ""))
        if Path(asset_path).suffix.lower() not in NARRATIVE_RASTER_SUFFIXES:
            errors.append(f"narrative asset must be a raster image, not SVG: {asset_path}")

        if str(asset.get("provider", "")).lower() != "built-in image_gen":
            errors.append(f"narrative asset must record provider built-in image_gen: {asset_path}")

        prompt_recipe = str(asset.get("prompt_recipe", ""))
        if str(asset.get("exact_title", "")) not in prompt_recipe:
            errors.append(f"narrative asset prompt must include exact_title: {asset_path}")
        if str(asset.get("exact_subtitle", "")) not in prompt_recipe:
            errors.append(f"narrative asset prompt must include exact_subtitle: {asset_path}")

        digest = str(asset.get("hash", ""))
        if not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            errors.append(f"narrative asset hash must be a SHA-256 digest: {asset_path}")

        if project_root:
            image_path = project_root / asset_path
            prompt_record_reference = str(asset.get("prompt_record", ""))
            prompt_record_path = prompt_record_reference.split("#", 1)[0].split("?", 1)[0]
            prompt_record = project_root / prompt_record_path
            if not prompt_record.is_file():
                errors.append(f"narrative asset prompt record does not exist: {asset.get('prompt_record')}")
            if image_path.is_file() and re.fullmatch(r"[0-9a-fA-F]{64}", digest):
                actual_digest = hashlib.sha256(image_path.read_bytes()).hexdigest()
                if actual_digest.lower() != digest.lower():
                    errors.append(f"narrative asset hash does not match file: {asset_path}")
                if prompt_record.is_file():
                    errors.extend(
                        _check_prompt_record_hash(
                            asset,
                            image_path,
                            digest,
                            prompt_record,
                        )
                    )

    return errors


def check_readme(
    root: Path,
    content_root: Path | None = None,
    *,
    visual: dict | None = None,
    manifest: dict | None = None,
    include_required_references: bool = True,
    check_guides: bool = True,
    enforce_sections: bool = True,
) -> list[str]:
    errors: list[str] = []
    readme_root = content_root or root
    readme_path = readme_root / "README.md"
    if not readme_path.is_file():
        return ["missing README.md"]

    try:
        contract = load_json(root / "templates" / "readme-contract.json")
    except ValueError as exc:
        return [str(exc)]

    text = readme_path.read_text(encoding="utf-8")
    errors.extend(_check_github_commit_pinned_links(text))
    errors.extend(_check_readme_absolute_local_paths(text))
    if enforce_sections:
        for section in contract.get("required_sections", []):
            heading = section.get("heading")
            if heading and f"## {heading}" not in text:
                errors.append(f"README missing required section: {heading}")

    story_heading = "## Why this exists"
    mechanism_heading = "## How it works"
    story_position = text.find(story_heading)
    mechanism_position = text.find(mechanism_heading)
    if story_position == -1 or mechanism_position == -1:
        pass
    elif story_position > mechanism_position:
        errors.append("README must explain why the project exists before how it works")
    first_code_block = text.find("```")
    if first_code_block != -1 and story_position != -1 and first_code_block < story_position:
        errors.append("README must place technical code after the human situation")

    if include_required_references:
        for reference in contract.get("required_references", []):
            if reference not in text:
                errors.append(f"README missing required reference: {reference}")

    expected_claim_fields = ["claim", "source", "status", "supports", "limits", "source_revision", "recorded_at"]
    if contract.get("schema_version") != "content-generation.readme-contract.v2":
        errors.append("README contract must declare content-generation.readme-contract.v2")
    story_policy = contract.get("story_policy", {})
    if not story_policy.get("sequence") or not story_policy.get("worked_example") or not story_policy.get("reader_paths"):
        errors.append("README contract must define its story sequence, worked example, and reader paths")
    evidence_policy = contract.get("evidence_policy", {})
    if evidence_policy.get("claim_fields") != expected_claim_fields:
        errors.append("README contract must require the v2 claim fields in order")

    if contract.get("scanability_policy"):
        if not re.search(r"\*\*[^*\n]+\*\*", text):
            errors.append("README must include at least one meaningful bold scan anchor")
        if not re.search(r"^## .+", text, flags=re.MULTILINE):
            errors.append("README must use semantic level-two headings for scan structure")

    visual_policy = contract.get("visual_policy", {})
    image_refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    image_refs.extend(re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", text, flags=re.IGNORECASE))
    local_image_refs = [ref for ref in image_refs if not ref.startswith(("http://", "https://", "#"))]
    referenced_image_paths = {
        ref.split("#", 1)[0].split("?", 1)[0].strip("<>").replace("\\", "/")
        for ref in local_image_refs
    }
    minimum_images = int(visual_policy.get("minimum_narrative_images_for_this_helper", 0))
    raster_image_paths = {
        path for path in referenced_image_paths
        if Path(path).suffix.lower() in NARRATIVE_RASTER_SUFFIXES
    }
    if len(raster_image_paths) < minimum_images:
        errors.append(
            "README must reference at least "
            f"{minimum_images} local raster narrative image(s); found {len(raster_image_paths)}"
        )
    for reference in local_image_refs:
        image_path = reference.split("#", 1)[0].split("?", 1)[0].strip("<>")
        if not (readme_root / image_path).is_file():
            errors.append(f"README image does not exist: {image_path}")

    if visual is not None and manifest is not None:
        narrative_roles = visual.get("narrative_roles", [])
        narrative_paths = {
            str(asset.get("path", "")).replace("\\", "/")
            for asset in manifest.get("assets", [])
            if any(
                str(asset.get("role", "")).lower() == str(marker).lower()
                or str(asset.get("role", "")).lower().startswith(f"{str(marker).lower()} ")
                for marker in narrative_roles
            )
        }
        linked_narrative_rasters = {
            path for path in referenced_image_paths
            if path in narrative_paths and Path(path).suffix.lower() in NARRATIVE_RASTER_SUFFIXES
        }
        if len(linked_narrative_rasters) < minimum_images:
            errors.append(
                "README must link at least "
                f"{minimum_images} raster assets declared with narrative roles; found {len(linked_narrative_rasters)}"
            )

    if check_guides:
        for guide in visual_policy.get("required_guides", []):
            if not (readme_root / guide).is_file():
                errors.append(f"missing required image guide or record: {guide}")

    return errors


def check(root: Path) -> list[str]:
    errors: list[str] = []
    version_path = root / "system-version.json"
    try:
        version = load_json(version_path)
    except ValueError as exc:
        return [str(exc)]

    if not re.fullmatch(r"\d+\.\d+\.\d+", str(version.get("version", ""))):
        errors.append("system-version.json version must use semantic-version form")
    modules = set(version.get("modules", []))
    if modules != EXPECTED_MODULES:
        errors.append(f"system modules must be exactly {sorted(EXPECTED_MODULES)}")
    human_output = version.get("human_output_contract", {})
    if human_output.get("version") != "content-generation.readme-contract.v2":
        errors.append("system-version.json must declare content-generation.readme-contract.v2")
    for field in ("template", "playbook", "image_guide", "prior_work"):
        if not human_output.get(field):
            errors.append(f"system-version.json human_output_contract missing {field}")
    if not human_output.get("research"):
        errors.append("system-version.json human_output_contract missing research")
    if not human_output.get("brand_direction"):
        errors.append("system-version.json human_output_contract missing brand_direction")
    for field in ("product_definition", "system_design", "test_design", "provenance", "reverse_analysis"):
        if not human_output.get(field):
            errors.append(f"system-version.json human_output_contract missing {field}")
    claim_contract = version.get("claim_explanation_contract", {})
    if claim_contract.get("version") != "content-generation.claim-evidence.v2":
        errors.append("system-version.json must declare content-generation.claim-evidence.v2")
    expected_claim_fields = ["claim", "source", "status", "supports", "limits", "source_revision", "recorded_at"]
    if claim_contract.get("fields") != expected_claim_fields:
        errors.append("system-version.json claim_explanation_contract fields do not match the v2 contract")
    if claim_contract.get("truth_boundary") != "citation establishes traceability, not truth":
        errors.append("system-version.json claim_explanation_contract must preserve the citation truth boundary")
    if claim_contract.get("required_for_helper_version") != "0.4.0":
        errors.append("system-version.json claim_explanation_contract must be required from 0.4.0")
    if claim_contract.get("optional_fields") != ["valid_time"] or not claim_contract.get("temporal_model"):
        errors.append("system-version.json claim_explanation_contract must define the valid-time model")
    boundary_contract = version.get("boundary_disclosure_contract", {})
    if _version_tuple(version.get("version")) >= (0, 4, 1):
        if boundary_contract.get("version") != "content-generation.must-preserve.v1":
            errors.append("system-version.json must declare content-generation.must-preserve.v1 from 0.4.1")
        if boundary_contract.get("field") != "project-brief.v2.must_preserve":
            errors.append("system-version.json boundary_disclosure_contract must name project-brief.v2.must_preserve")
        if boundary_contract.get("inventory_field") != "project-brief.v2.boundaries":
            errors.append("system-version.json boundary_disclosure_contract must name project-brief.v2.boundaries as its inventory")
        if boundary_contract.get("minimum") != 1 or boundary_contract.get("maximum") != 8:
            errors.append("system-version.json boundary_disclosure_contract must require one to eight disclosures")
        if boundary_contract.get("required_for_helper_version") != "0.4.1":
            errors.append("system-version.json boundary disclosure must be required from 0.4.1")
        if not boundary_contract.get("readme_rule"):
            errors.append("system-version.json boundary_disclosure_contract must define its README rule")
    scanability = version.get("scanability_contract", {})
    if scanability.get("version") != "content-generation.scanability.v1":
        errors.append("system-version.json must declare content-generation.scanability.v1")
    for field in ("heading_rule", "bolding_rule", "scan_test", "accessibility_rule"):
        if not scanability.get(field):
            errors.append(f"system-version.json scanability_contract missing {field}")
    for module in EXPECTED_MODULES:
        path = root / "modules" / module / "SKILL.md"
        if not path.is_file():
            errors.append(f"missing module entry point: {path.relative_to(root)}")
        elif len(path.read_text(encoding="utf-8").splitlines()) > 500:
            errors.append(f"module entry point is over 500 lines: {path.relative_to(root)}")

    required_schemas = {
        "adapter-system-version.schema.json",
        "project-brief.schema.json",
        "project-brief.v2.schema.json",
        "asset-manifest.schema.json",
        "review-rubric.schema.json",
        "readme-contract.schema.json",
    }
    for name in required_schemas:
        path = root / "schemas" / name
        try:
            schema = load_json(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if "$schema" not in schema or "$id" not in schema:
            errors.append(f"schema missing $schema or $id: {path.relative_to(root)}")

    for relative_path in version.get("helper_contract_files", []):
        if not (root / relative_path).is_file():
            errors.append(f"missing versioned helper contract file: {relative_path}")

    for name in (
        "system-version.json",
        "project-brief.json",
        "brand-language.json",
        "visual-style.json",
        "asset-manifest.json",
        "review-rubric.json",
        "readme-contract.json",
    ):
        if not (root / "templates" / name).is_file():
            errors.append(f"missing template: templates/{name}")

    if not (root / "CHATGPT_SETUP.md").is_file():
        errors.append("missing CHATGPT_SETUP.md")
    for path in REQUIRED_HELPER_DOCS:
        if not (root / path).is_file():
            errors.append(f"missing helper guide: {path}")
    errors.extend(check_readme(root))
    return errors


def check_adapter(
    adapter: Path,
    project_root: Path | None = None,
    *,
    helper_root: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    required = {
        "system-version.json": "content-generation.adapter.v1",
        "brand-language.json": "content-generation.brand-language.v1",
        "visual-style.json": "content-generation.visual-style.v1",
        "asset-manifest.json": "content-generation.asset-manifest.v1",
        "review-rubric.json": "content-generation.review-rubric.v1",
    }
    values: dict[str, dict] = {}
    for name, schema_version in required.items():
        path = adapter / name
        try:
            values[name] = load_json(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if values[name].get("schema_version") != schema_version:
            errors.append(f"{name} must declare {schema_version}")

    system = values.get("system-version.json", {})
    for field in ("helper_repository", "helper_version", "helper_commit"):
        if not system.get(field):
            errors.append(f"adapter system-version.json missing {field}")
    if system.get("helper_repository") and not _valid_web_uri(system["helper_repository"]):
        errors.append("adapter system-version.json helper_repository must be a direct HTTP(S) URL")
    if system.get("helper_version") and not re.fullmatch(r"\d+\.\d+\.\d+", str(system["helper_version"])):
        errors.append("adapter system-version.json helper_version must use semantic-version form")
    if system.get("helper_commit") and not re.fullmatch(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})", str(system["helper_commit"])):
        errors.append("adapter system-version.json helper_commit must be a full commit ID")
    if not system.get("modules") or set(system["modules"]) != EXPECTED_MODULES:
        errors.append("adapter system-version.json modules do not match the helper contract")

    project = values.get("project-brief.json", {})
    project_path = adapter / "project-brief.json"
    try:
        project = load_json(project_path)
    except ValueError as exc:
        errors.append(str(exc))
    helper_version = _version_tuple(system.get("helper_version"))
    brief_version = project.get("schema_version")
    if brief_version not in {"content-generation.project-brief.v1", "content-generation.project-brief.v2"}:
        errors.append("project-brief.json must declare content-generation.project-brief.v1 or v2")
    if helper_version >= (0, 4, 0) and brief_version != "content-generation.project-brief.v2":
        errors.append("helper versions 0.4.0 and later require project-brief.v2")
    for field in ("project", "audience", "problem", "solution", "evidence", "boundaries"):
        if not project.get(field):
            errors.append(f"adapter project-brief.json missing {field}")
    if brief_version == "content-generation.project-brief.v2":
        readme_text = None
        if project_root and (project_root / "README.md").is_file():
            readme_text = (project_root / "README.md").read_text(encoding="utf-8")
        errors.extend(check_project_brief_v2(project, readme_text))

    if helper_version >= (0, 4, 1):
        boundaries = project.get("boundaries")
        if not isinstance(boundaries, list) or not boundaries:
            errors.append(
                "project-brief.json boundaries must contain at least one declared boundary for helper versions 0.4.1 and later"
            )
            declared_boundaries: list[str] = []
        else:
            declared_boundaries = [
                boundary for boundary in boundaries if isinstance(boundary, str) and boundary.strip()
            ]
            if len(declared_boundaries) != len(boundaries):
                errors.append("project-brief.json boundaries entries must be non-empty strings")

        must_preserve = project.get("must_preserve")
        if not isinstance(must_preserve, list) or not must_preserve:
            errors.append(
                "project-brief.json must_preserve must contain at least one evidence-backed boundary for helper versions 0.4.1 and later"
            )
            disclosures: list[str] = []
        else:
            disclosures = [value for value in must_preserve if isinstance(value, str) and value.strip()]
            if len(disclosures) != len(must_preserve):
                errors.append("project-brief.json must_preserve entries must be non-empty strings")
            if len(disclosures) > 8:
                errors.append("project-brief.json must_preserve must contain no more than eight boundaries")
        target_readme = project_root / "README.md" if project_root else None
        if target_readme is None or not target_readme.is_file():
            errors.append("must_preserve validation requires the target README")
        else:
            target_text = target_readme.read_text(encoding="utf-8")
            for boundary in declared_boundaries:
                if boundary not in target_text:
                    errors.append(
                        f"declared boundary is not stated in the target README: {boundary}"
                    )
            for disclosure in disclosures:
                if disclosure not in target_text:
                    errors.append(
                        f"must_preserve boundary is not stated in the target README: {disclosure}"
                    )
        for disclosure in disclosures:
            if disclosure not in declared_boundaries:
                errors.append(
                    f"must_preserve entry is not a declared boundary: {disclosure}"
                )

    brand = values.get("brand-language.json", {})
    for field in ("name", "personality", "promise", "avoid"):
        if not brand.get(field):
            errors.append(f"adapter brand-language.json missing {field}")

    visual = values.get("visual-style.json", {})
    for field in ("reference_asset", "palette", "roles", "reject_when"):
        if not visual.get(field):
            errors.append(f"adapter visual-style.json missing {field}")

    manifest = values.get("asset-manifest.json", {})
    assets = manifest.get("assets", [])
    if not assets:
        errors.append("adapter asset-manifest.json must contain at least one asset")
    if project_root:
        for asset in assets:
            asset_path = asset.get("path")
            if asset_path and not (project_root / asset_path).is_file():
                errors.append(f"asset does not exist under project root: {asset_path}")
    if helper_version >= (0, 3, 0):
        errors.extend(check_narrative_assets(visual, manifest, project_root))
    if project_root and helper_root and (project_root / "README.md").is_file():
        errors.extend(
            check_readme(
                helper_root,
                project_root,
                visual=visual,
                manifest=manifest,
                include_required_references=False,
                check_guides=False,
                enforce_sections=False,
            )
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--adapter", type=Path)
    parser.add_argument("--project-root", type=Path)
    args = parser.parse_args()
    errors = check(args.root.resolve())
    if args.adapter:
        errors.extend(
            check_adapter(
                args.adapter.resolve(),
                args.project_root.resolve() if args.project_root else None,
                helper_root=args.root.resolve(),
            )
        )
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID: content-generation-modules contract" + (" and target adapter" if args.adapter else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
