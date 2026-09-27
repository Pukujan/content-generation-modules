"""Unit tests for human-readable generated artifact filenames (issue #26)."""

from __future__ import annotations

import tempfile
import unittest
from collections import OrderedDict
from pathlib import Path

from scripts.human_filename import (
    build_basename,
    build_relative_path,
    is_hashy_junk_basename,
    sanitize_label,
)
from scripts.validate_content_system import (
    check_asset_manifest_human_paths,
    check_human_output_naming_contract,
    is_hashy_junk_basename as validate_is_hashy,
)


ROOT = Path(__file__).resolve().parents[1]


class HumanFilenameUnitTests(unittest.TestCase):
    def test_example_before_after(self):
        name = build_basename(
            [("line", "song-food"), ("pitch", "+8st"), ("speed", "0%")],
            "mp3",
        )
        self.assertEqual(name, "song-food_pitch-plus-8st_speed-0pct.mp3")
        self.assertFalse(is_hashy_junk_basename(name))
        self.assertTrue(is_hashy_junk_basename("song_food-p0-00e86d.mp3"))

    def test_pitch_speed_matrix_unique_and_labeled(self):
        pitches = ["+0st", "+8st", "-4st"]
        speeds = ["0%", "20%", "+10%"]
        names = set()
        for pitch in pitches:
            for speed in speeds:
                name = build_basename(
                    [("line", "song-food"), ("pitch", pitch), ("speed", speed)],
                    "mp3",
                )
                self.assertIn("pitch-", name)
                self.assertIn("speed-", name)
                self.assertNotRegex(name, r"-p\d+-[0-9a-f]{6}\.")
                self.assertFalse(is_hashy_junk_basename(name))
                names.add(name)
        self.assertEqual(len(names), len(pitches) * len(speeds))

    def test_deterministic_same_labels(self):
        dims = OrderedDict([("line", "song-food"), ("pitch", "+8st"), ("speed", "0%")])
        a = build_basename(dims, "mp3")
        b = build_basename(list(dims.items()), "mp3")
        self.assertEqual(a, b)

    def test_collision_fixture_formerly_shared_p0_stem(self):
        # Two configs that folklore flattened to …-p0-….mp3 now diverge.
        pitch_zero = build_basename(
            [("line", "song-food"), ("pitch", "+0st"), ("speed", "0%")],
            "mp3",
        )
        speed_zero_different_pitch = build_basename(
            [("line", "song-food"), ("pitch", "+8st"), ("speed", "0%")],
            "mp3",
        )
        self.assertNotEqual(pitch_zero, speed_zero_different_pitch)
        self.assertIn("pitch-plus-0st", pitch_zero)
        self.assertIn("pitch-plus-8st", speed_zero_different_pitch)
        self.assertTrue(pitch_zero.endswith("_speed-0pct.mp3"))
        self.assertTrue(speed_zero_different_pitch.endswith("_speed-0pct.mp3"))

    def test_hash_suffix_only_after_human_labels(self):
        name = build_basename(
            [("line", "song-food"), ("pitch", "+8st"), ("speed", "0%")],
            "mp3",
            content_hash="00e86dabcdef",
        )
        self.assertTrue(name.startswith("song-food_pitch-plus-8st_speed-0pct_"))
        self.assertTrue(name.endswith(".mp3"))
        self.assertIn("00e86d", name)
        self.assertFalse(is_hashy_junk_basename(name))

    def test_sanitize_rules(self):
        self.assertEqual(sanitize_label("+8st"), "plus-8st")
        self.assertEqual(sanitize_label("0%"), "0pct")
        self.assertEqual(sanitize_label("Song Food"), "song-food")

    def test_relative_path(self):
        path = build_relative_path(
            [("line", "song-food"), ("pitch", "+8st"), ("speed", "0%")],
            "mp3",
            parent="generated/audio",
        )
        self.assertEqual(path, "generated/audio/song-food_pitch-plus-8st_speed-0pct.mp3")

    def test_hashy_detector_variants(self):
        self.assertTrue(is_hashy_junk_basename("song_food-p0-00e86d.mp3"))
        self.assertTrue(is_hashy_junk_basename("song_food-p20-8eb807.wav"))
        self.assertTrue(validate_is_hashy("nested/song_food-p0-00e86d.mp3"))
        self.assertFalse(is_hashy_junk_basename("song-food_pitch-plus-8st_speed-0pct.mp3"))
        self.assertFalse(is_hashy_junk_basename("song_food-p0.mp3"))  # no 6-hex discriminator


class FilenameContractTests(unittest.TestCase):
    def test_helper_checkout_has_filename_contract(self):
        self.assertEqual(check_human_output_naming_contract(ROOT), [])

    def test_validator_fails_closed_when_helper_api_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            staging = Path(directory)
            (staging / "modules" / "human-output-naming").mkdir(parents=True)
            (staging / "modules" / "human-output-naming" / "SKILL.md").write_text(
                "# hon\n", encoding="utf-8"
            )
            (staging / "docs").mkdir()
            (staging / "docs" / "HUMAN_OUTPUT_NAMING.md").write_text("# doc\n", encoding="utf-8")
            # Claim the API in the contract, but omit scripts/human_filename.py
            (staging / "docs" / "human-output-naming.json").write_text(
                (
                    '{"schema_version":"content-generation.human-output-naming.v1",'
                    '"application":"must_load","module":"human-output-naming",'
                    '"surfaces":["generated artifact filenames","asset-manifest paths",'
                    '"committed media basenames"],'
                    '"python_api":{"path":"scripts/human_filename.py",'
                    '"required_symbols":["build_basename","is_hashy_junk_basename",'
                    '"sanitize_label","build_relative_path"]},'
                    '"apply_checklist":["a","b","c"]}'
                ),
                encoding="utf-8",
            )
            errors = check_human_output_naming_contract(staging)
            self.assertTrue(
                any("helper module/API is missing" in e for e in errors),
                errors,
            )

    def test_adapter_smoke_rejects_hashy_basenames_at_0_5_5(self):
        manifest = {
            "assets": [
                {"path": "song_food-p0-00e86d.mp3", "role": "audio", "hash": "ab" * 32},
            ]
        }
        errors = check_asset_manifest_human_paths(manifest, (0, 5, 5))
        self.assertTrue(any("hashy junk basename" in e for e in errors), errors)
        # Pre-0.5.5 pins are not forced to rename historical paths.
        self.assertEqual(check_asset_manifest_human_paths(manifest, (0, 5, 4)), [])

    def test_adapter_smoke_accepts_human_basenames_at_0_5_5(self):
        human = build_basename(
            [("line", "song-food"), ("pitch", "+8st"), ("speed", "0%")],
            "mp3",
        )
        manifest = {
            "assets": [
                {"path": human, "role": "audio", "hash": "cd" * 32},
            ]
        }
        self.assertEqual(check_asset_manifest_human_paths(manifest, (0, 5, 5)), [])


if __name__ == "__main__":
    unittest.main()
