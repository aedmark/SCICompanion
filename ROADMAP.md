# Roadmap

Item IDs are permanent: `P<phase>-<nn>`. Never renumber; append new items at the end of their phase.
`[ ]` open · `[~]` in progress (who holds it, since when, and what is left) · `[x]` done · `[-]` dropped (say why,
and the decision). An item held `[~]` by someone else is theirs until they or a maintainer release it.

A finished item says what was done, the decision if any, the evidence, and the date. A new item says where it came
from and the date. Keep an item's useful investigation history in the item.

## Phase 1: Reproducible maintenance baseline

Goal: make a fresh maintenance session able to understand, build, and verify the existing application.

- [x] P1-01 Adopt the Manifold repository-memory documentation set and tailor it to the observed codebase (D-002).
  Evidence: `python3 tools/check_docs.py` passes (2026-10-07).
- [ ] P1-02 Establish and verify the supported Visual Studio, Windows SDK, MFC workload, and project-retargeting
  recipe. Acceptance: a clean Windows checkout builds Release/Win32 using the documented command; record tool
  versions and any required retargeting. Origin: template adoption found mixed `v140_xp`/`v145` metadata
  (2026-10-07); blocked by Q-001.
- [ ] P1-03 Establish the unit-test baseline on the supported Windows environment. Acceptance: all 14 discovered
  `TEST_METHOD` cases are enumerated, their result is recorded in `docs/HANDOFF.md`, and fixture/output side effects
  are documented. Origin: no runnable Windows test environment was available during template adoption (2026-10-07).
- [x] P1-04 Apply the 3x Documentation Scheme as a generated companion manual without displacing canonical project
  documents (D-003). Evidence: the source validates with 4 sections, 17 entries, and 0 warnings; the standalone HTML
  builds reproducibly and was visually smoke-tested (2026-10-07).

## Phase 2: Automated maintenance

Goal: turn the verified manual baseline into repeatable project checks and release guidance.

- [ ] P2-01 Document the release owner, version source of truth, supported security branch, private reporting route,
  and release checklist. Origin: repository inspection found tag `3.2.0` but no release procedure (2026-10-07);
  blocked by Q-002.
- [ ] P2-02 Add CI for the documentation checker and, after P1-02 and P1-03, the supported Windows build and unit
  tests. Acceptance: pull requests report doc, build, and test status without publishing artifacts. Origin: no CI
  configuration was present during template adoption (2026-10-07).

## Phase 3: Product work

Goal: keep feature and compatibility work maintainer-directed rather than inferred from repository archaeology.

- [ ] P3-01 Seed concrete product work from a maintainer request or linked issue, including acceptance evidence.
  Origin: the documentation migration intentionally did not invent a feature roadmap (2026-10-07).
