#!/usr/bin/env python3
"""Check project documentation for stale placeholders and broken references.

Run from the repository root with:

    python3 tools/check_docs.py

Errors (exit 1):
  - a template placeholder left in a managed document
  - a roadmap ID used twice, filed under the wrong phase, or given an unknown checkbox
  - a decision number used twice or out of order, or superseded incorrectly
  - an open question defined twice
  - a referenced roadmap ID, decision number, or question that does not exist
  - two session-log entries with the same number
  - a relative Markdown/HTML link or AGENTS.md Layout path that points at nothing

Warnings (exit 0):
  - HANDOFF's Last updated date is missing or older than its newest session
  - HANDOFF's session log or Current state has outgrown the limits below

HTML comments are ignored so examples can live in comments.
"""

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DOCS = [
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "ROADMAP.md",
    "docs/README.md",
    "docs/ROADMAP.md",
    "docs/HANDOFF.md",
    "docs/ARCHITECTURE.md",
    "docs/DECISIONS.md",
    "docs/TESTING.md",
    "docs/SECURITY.md",
    "docs/CHANGELOG.md",
    "docs/CONTRIBUTING.md",
]
LOG_LIMIT = 10
CURRENT_STATE_LINES = 80

ITEM_RE = re.compile(r"\bP(\d+)-(\d+)\b")
DECISION_RE = re.compile(r"\bD-(\d{3})\b")
QUESTION_RE = re.compile(r"\bQ-(\d{3})\b")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
LINK_RE = re.compile(r'\]\(([^)\s]+)\)|\b(?:href|src)="([^"]+)"')

errors = []
warnings = []


def read(path):
    text = path.read_text(encoding="utf-8")
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def where(path, text, pos):
    return f"{path.relative_to(ROOT)}:{text.count(chr(10), 0, pos) + 1}"


def section(text, heading):
    match = re.search(rf"^## {heading}\b.*?(?=^## |\Z)", text, flags=re.M | re.S)
    return (match.group(0), match.start()) if match else ("", 0)


def main():
    docs = [ROOT / name for name in DOCS if (ROOT / name).is_file()]
    archive = ROOT / "docs" / "archive"
    if archive.is_dir():
        docs += sorted(
            path
            for path in archive.iterdir()
            if path.suffix in (".md", ".html") and not path.name.startswith("_")
        )
    texts = {path: read(path) for path in docs}

    for path, content in texts.items():
        for match in re.finditer(r"\{\{[^}]*\}\}", content):
            errors.append(
                f"{where(path, content, match.start())}: placeholder left: {match.group(0)[:60]}"
            )

    roadmap = next(
        (path for path in (ROOT / "ROADMAP.md", ROOT / "docs" / "ROADMAP.md") if path in texts),
        None,
    )
    items = set()
    if roadmap is None:
        errors.append("no ROADMAP.md (looked in the root and in docs/)")
    else:
        content = texts[roadmap]
        phase = None
        pattern = r"^## Phase (\d+)|^- \[(.)\] (P(\d+)-(\d+))\b"
        for match in re.finditer(pattern, content, flags=re.M):
            if match.group(1):
                phase = match.group(1)
                continue
            box, item, item_phase = match.group(2), match.group(3), match.group(4)
            if item in items:
                errors.append(f"{where(roadmap, content, match.start())}: {item} is used twice")
            items.add(item)
            if box not in " x~-":
                errors.append(
                    f"{where(roadmap, content, match.start())}: {item} has checkbox [{box}]; "
                    "use [ ], [~], [x] or [-]"
                )
            if phase is not None and item_phase != phase:
                errors.append(
                    f"{where(roadmap, content, match.start())}: {item} is filed under Phase {phase}"
                )
        for path, content in texts.items():
            if path.parent.name == "archive":
                items.update(
                    match.group(1)
                    for match in re.finditer(r"^- \[.\] (P\d+-\d+)\b", content, flags=re.M)
                )

    decisions_path = ROOT / "docs" / "DECISIONS.md"
    decisions = set()
    supersessions = []
    questions = set()
    if decisions_path in texts:
        content = texts[decisions_path]
        last = 0
        for match in re.finditer(r"^## D-(\d{3})\b([^\n]*)", content, flags=re.M):
            number = int(match.group(1))
            identifier = f"D-{match.group(1)}"
            if identifier in decisions:
                errors.append(
                    f"{where(decisions_path, content, match.start())}: {identifier} is used twice"
                )
            elif number < last:
                errors.append(
                    f"{where(decisions_path, content, match.start())}: {identifier} comes after D-{last:03d}"
                )
            decisions.add(identifier)
            last = max(last, number)
            superseded_by = re.search(r"superseded by D-(\d{3})", match.group(2))
            if superseded_by:
                supersessions.append((number, int(superseded_by.group(1)), match.start()))
        for number, superseded_by, pos in supersessions:
            if f"D-{superseded_by:03d}" in decisions and superseded_by <= number:
                errors.append(
                    f"{where(decisions_path, content, pos)}: D-{number:03d} is superseded by "
                    f"an earlier decision, D-{superseded_by:03d}"
                )
        for match in re.finditer(r"^- \*\*Q-(\d{3})\*\*", content, flags=re.M):
            identifier = f"Q-{match.group(1)}"
            if identifier in questions:
                errors.append(
                    f"{where(decisions_path, content, match.start())}: {identifier} is used twice"
                )
            questions.add(identifier)

    for path, content in texts.items():
        if roadmap is not None:
            for match in ITEM_RE.finditer(content):
                if match.group(0) not in items:
                    errors.append(
                        f"{where(path, content, match.start())}: {match.group(0)} is not in the roadmap"
                    )
        if decisions_path in texts:
            for match in DECISION_RE.finditer(content):
                if match.group(0) not in decisions:
                    errors.append(
                        f"{where(path, content, match.start())}: {match.group(0)} is not in DECISIONS.md"
                    )
            for match in QUESTION_RE.finditer(content):
                if match.group(0) not in questions:
                    errors.append(
                        f"{where(path, content, match.start())}: {match.group(0)} is not in "
                        "DECISIONS.md's open questions"
                    )
        for match in LINK_RE.finditer(content):
            target = (match.group(1) or match.group(2)).split("#")[0]
            if not target or re.match(r"[a-z][a-z0-9+.-]*:", target):
                continue
            if not (path.parent / target).exists():
                errors.append(
                    f"{where(path, content, match.start())}: link to {target}, which does not exist"
                )

    agents = ROOT / "AGENTS.md"
    if agents in texts:
        layout, offset = section(texts[agents], "Layout")
        for match in re.finditer(r"^\| `([^`]+)` \|", layout, flags=re.M):
            if not (ROOT / match.group(1)).exists():
                errors.append(
                    f"{where(agents, texts[agents], offset + match.start())}: Layout lists "
                    f"{match.group(1)}, which does not exist"
                )

    handoff = ROOT / "docs" / "HANDOFF.md"
    if handoff in texts:
        content = texts[handoff]
        session_re = re.compile(r"^### Session (\d+)\b([^\n]*)", flags=re.M)
        sessions = [
            (match.group(1), (DATE_RE.search(match.group(2)) or [None])[0])
            for match in session_re.finditer(content)
        ]
        seen = set()
        for path in [handoff] + [path for path in texts if path.parent.name == "archive"]:
            for match in session_re.finditer(texts[path]):
                if match.group(1) in seen:
                    errors.append(
                        f"{where(path, texts[path], match.start())}: a second entry for Session {match.group(1)}"
                    )
                seen.add(match.group(1))
        updated = re.search(r"Last updated:\s*(\d{4}-\d{2}-\d{2})", content)
        newest = max((date for _, date in sessions if date), default=None)
        if not updated:
            warnings.append("docs/HANDOFF.md: no 'Last updated: YYYY-MM-DD' line in Current state")
        elif newest and updated.group(1) < newest:
            warnings.append(
                f"docs/HANDOFF.md: Current state was last updated {updated.group(1)}, "
                f"but the session log has an entry from {newest}"
            )
        if len(sessions) > LOG_LIMIT:
            warnings.append(
                f"docs/HANDOFF.md: {len(sessions)} session-log entries; move all but the newest "
                f"{LOG_LIMIT} to docs/archive/"
            )
        current, _ = section(content, "Current state")
        if current.count("\n") > CURRENT_STATE_LINES:
            warnings.append(
                f"docs/HANDOFF.md: Current state is {current.count(chr(10))} lines "
                f"(limit {CURRENT_STATE_LINES}); move history to the session log"
            )

    for line in errors:
        print(f"ERROR {line}")
    for line in warnings:
        print(f"WARN  {line}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s) in {len(texts)} file(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
