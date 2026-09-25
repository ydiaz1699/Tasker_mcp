"""LOADER: fetch and parse the authoritative Tasker code list.

Source: Taskomater/Tasker-XML-Info / Tasker_XML_Codes.md (MIT, Tasker v5.15.5-beta).
The file is a Markdown list under sections like `### Task Actions (373):`, with
one entry per line in the form:  `CODE`: `Name`

This module reads code -> name -> section, and NOTHING else (the source carries no
descriptions, args or variables). Enrichment happens in build_db.py using this
repo's knowledge/*.py. Stdlib only (urllib), no third-party deps.
"""

from __future__ import annotations

import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

SOURCE_URL = (
    "https://raw.githubusercontent.com/"
    "Taskomater/Tasker-XML-Info/master/Tasker_XML_Codes.md"
)

# A local vendored copy used as offline fallback (kept in the package data dir).
VENDORED = Path(__file__).parent / "data" / "Tasker_XML_Codes.md"

# `123`: `Some Name`   (trailing spaces / CRLF tolerated)
_ENTRY_RE = re.compile(r"^`(\d+)`\s*:\s*`([^`]+)`\s*$")
# `### Task Actions (373):`
_SECTION_RE = re.compile(r"^#{2,3}\s*(.+?)\s*(?:\(\d+\))?\s*:?\s*$")

# Map the source section headings to our kinds.
_SECTION_KIND = {
    "task actions": "action",
    "profile events": "event",
    "profile states": "state",
    "deprecated task actions": "action_deprecated",
}


@dataclass
class SourceEntry:
    """A single code->name entry as read from the authoritative source."""

    code: int
    name: str
    kind: str  # action | event | state | action_deprecated
    section: str  # original section heading


def fetch_source(refresh: bool = False, timeout: float = 20.0) -> str:
    """Return the raw Markdown source.

    If refresh=True, download from SOURCE_URL and update the vendored copy.
    Otherwise prefer the vendored copy (offline), falling back to download.
    """
    if not refresh and VENDORED.exists():
        return VENDORED.read_text(encoding="utf-8")

    try:
        with urllib.request.urlopen(SOURCE_URL, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001 - offline fallback below
        if VENDORED.exists():
            return VENDORED.read_text(encoding="utf-8")
        raise RuntimeError(
            f"Could not fetch Tasker source and no vendored copy at {VENDORED}: {e}"
        ) from e

    # Persist the vendored copy so future builds work offline.
    VENDORED.parent.mkdir(parents=True, exist_ok=True)
    VENDORED.write_text(text, encoding="utf-8")
    return text


def parse_source(markdown: str) -> list[SourceEntry]:
    """Parse the Markdown into a flat list of SourceEntry.

    Tracks the current section heading to assign a kind to each `code`: `name` line.
    """
    entries: list[SourceEntry] = []
    current_kind: Optional[str] = None
    current_section = ""

    for line in markdown.splitlines():
        sect = _SECTION_RE.match(line)
        if sect:
            heading = sect.group(1).strip()
            key = heading.lower()
            # Match the known section keys by prefix (headings carry counts we stripped).
            current_kind = None
            for k, kind in _SECTION_KIND.items():
                if key.startswith(k):
                    current_kind = kind
                    current_section = heading
                    break
            continue

        if current_kind is None:
            continue

        m = _ENTRY_RE.match(line)
        if m:
            entries.append(
                SourceEntry(
                    code=int(m.group(1)),
                    name=m.group(2).strip(),
                    kind=current_kind,
                    section=current_section,
                )
            )
    return entries


def load_entries(refresh: bool = False) -> list[SourceEntry]:
    """Convenience: fetch + parse in one call."""
    return parse_source(fetch_source(refresh=refresh))
