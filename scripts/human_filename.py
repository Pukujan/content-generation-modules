#!/usr/bin/env python3
"""Human-readable generated artifact / asset filenames (CGM 0.5.5+).

Adopters MUST call this before writing generated media so pitch, speed, and
other dimensions stay labeled segments — never opaque ``p0`` / short-hash stems.
"""

from __future__ import annotations

import re
from collections import OrderedDict
from collections.abc import Iterable, Mapping, Sequence
from typing import Union

Dimensions = Union[
    Mapping[str, object],
    Sequence[tuple[str, object]],
    Iterable[tuple[str, object]],
]

# First-segment identity keys: value alone forms the stem (see issue #26 examples).
_STEM_KEYS = frozenset({"line", "stem", "name", "title", "base"})

# Classic hashy junk: song_food-p0-00e86d.mp3 / song_food-p20-8eb807.wav
_HASHY_BASENAME = re.compile(
    r"(?i)^(?P<head>.+)-p(?P<tag>\d+)-(?P<hex>[0-9a-f]{6})\.(?P<ext>[a-z0-9]+)$"
)

_UNSAFE = re.compile(r"[^a-z0-9._+-]+")
_MULTI_DASH = re.compile(r"-{2,}")


def sanitize_label(value: object) -> str:
    """Filesystem-safe token: lowercase, spaces to -, +N to plus-N, % to pct."""
    text = str(value if value is not None else "").strip().lower()
    # "+8st" -> "plus-8st"; leftover "+" -> "plus"
    text = re.sub(r"\+(?=\d)", "plus-", text)
    text = text.replace("+", "plus")
    text = text.replace("%", "pct")
    text = text.replace(" ", "-").replace("/", "-").replace("\\", "-")
    text = _UNSAFE.sub("-", text)
    text = _MULTI_DASH.sub("-", text).strip("-._")
    return text or "unnamed"


def _as_ordered_pairs(dimensions: Dimensions) -> list[tuple[str, object]]:
    if isinstance(dimensions, OrderedDict):
        return list(dimensions.items())
    if isinstance(dimensions, Mapping):
        return list(dimensions.items())
    pairs = list(dimensions)
    out: list[tuple[str, object]] = []
    for item in pairs:
        if not isinstance(item, (tuple, list)) or len(item) != 2:
            raise TypeError(
                "dimensions must be a mapping or an ordered sequence of (key, value) pairs"
            )
        out.append((str(item[0]), item[1]))
    return out


def _normalize_extension(extension: str) -> str:
    ext = str(extension or "").strip().lower().lstrip(".")
    if not ext or not re.fullmatch(r"[a-z0-9]+", ext):
        raise ValueError(f"extension must be alphanumeric, got {extension!r}")
    return ext


def build_basename(
    dimensions: Dimensions,
    extension: str,
    *,
    disambiguator: str | None = None,
    content_hash: str | None = None,
) -> str:
    """Build a pronounceable, deterministic basename from ordered dimension labels.

    Example::

        build_basename(
            [("line", "song-food"), ("pitch", "+8st"), ("speed", "0%")],
            "mp3",
        )
        # -> "song-food_pitch-plus-8st_speed-0pct.mp3"

    ``content_hash`` (and optional ``disambiguator``) append only **after** the
    human label segments, never instead of them.
    """
    pairs = _as_ordered_pairs(dimensions)
    if not pairs:
        raise ValueError("dimensions must contain at least one label")

    segments: list[str] = []
    stem_used = False
    for key, value in pairs:
        key_tok = sanitize_label(key)
        val_tok = sanitize_label(value)
        if not key_tok:
            raise ValueError("dimension keys must sanitize to a non-empty token")
        if key_tok in _STEM_KEYS and not stem_used:
            segments.append(val_tok)
            stem_used = True
        else:
            segments.append(f"{key_tok}-{val_tok}")

    if disambiguator:
        segments.append(sanitize_label(disambiguator))
    if content_hash:
        # Short suffix only — never the sole discriminator in place of labels.
        digest = sanitize_label(content_hash)
        if len(digest) > 12:
            digest = digest[:12]
        segments.append(digest)

    ext = _normalize_extension(extension)
    return f"{'_'.join(segments)}.{ext}"


def build_relative_path(
    dimensions: Dimensions,
    extension: str,
    *,
    parent: str | None = None,
    disambiguator: str | None = None,
    content_hash: str | None = None,
) -> str:
    """Basename plus optional human parent folder (forward-slash relative path)."""
    name = build_basename(
        dimensions,
        extension,
        disambiguator=disambiguator,
        content_hash=content_hash,
    )
    if not parent:
        return name
    folder = "/".join(
        sanitize_label(part) for part in str(parent).replace("\\", "/").split("/") if part
    )
    return f"{folder}/{name}" if folder else name


def is_hashy_junk_basename(name: str) -> bool:
    """True when the basename matches classic ``stem-pN-<6hex>.ext`` folklore.

    Detects names like ``song_food-p0-00e86d.mp3`` or ``song_food-p20-8eb807.wav``
    where a short hex tag is the sole discriminator after an opaque ``pN`` token.
    """
    base = str(name or "").replace("\\", "/").rsplit("/", 1)[-1].strip()
    match = _HASHY_BASENAME.fullmatch(base)
    if not match:
        return False
    return len(match.group("hex")) == 6


__all__ = [
    "build_basename",
    "build_relative_path",
    "is_hashy_junk_basename",
    "sanitize_label",
]
