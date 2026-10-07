# Decisions

Short, append-only record of choices that a future session might otherwise re-litigate. Newest entries go at the
bottom. To reverse a decision, add a new entry that supersedes it; retain the old text and change only its status.

## D-001 Preserve the native Windows/MFC architecture  (2026-10-07, status: accepted, recorded)

**Context:** SCI Companion is an established native desktop IDE whose solution, document/view editors, Windows
resources, profile storage, and bundled UI framework are all organized around MFC.

**Decision:** Treat the current Windows/MFC solution and thin-executable/shared-library split as the architecture to
maintain. Cross-platform rewrites, framework replacement, and repository-wide modernization require separate,
explicit maintainer direction.

**Alternatives:** Inferring a rewrite from old project metadata would create broad product and compatibility risk
without a maintainer request or evidence that the current architecture cannot be maintained.

**Consequences:** Changes should fit existing MFC lifetimes and build projects. Toolchain verification and targeted
modernization remain valid, but P1-02 must prove the supported path before project-wide retargeting.

## D-002 Use repository documentation as durable session memory  (2026-10-07, status: accepted)

**Context:** The Manifold template was added to the repository, and the user requested that it be applied. The code
base previously had only a minimal root README and no canonical agent, handoff, decision, security, or test guide.

**Decision:** Keep standing instructions in `AGENTS.md`, current state in `docs/HANDOFF.md`, plans in `ROADMAP.md`,
and enduring technical facts in the mapped documents under `docs/`. `CLAUDE.md` only imports the canonical agent
instructions. Validate the set with `python3 tools/check_docs.py`.

**Alternatives:** Leaving the template as an unfilled subdirectory would not describe this project. Duplicating
instructions per tool would let them drift.

**Consequences:** Contributors must update the owning document when its trigger applies. The documentation should
be removed or simplified if it stops being maintained rather than allowed to become ceremonial.

## Open questions

Questions requiring maintainer input live here. Numbers are permanent; answered questions remain with their answer
and date.

- **Q-001** Which Visual Studio release, Windows SDK, MFC workload, architecture/configuration, and retargeting steps
  are officially supported? (asked 2026-10-07 during template adoption; blocks P1-02; recommendation: verify the
  newest toolchain that builds Release/Win32 without source changes, then document any legacy-toolset exception)
- **Q-002** Who owns releases and private vulnerability reports, which branch/version receives fixes, and what is
  the version source of truth? (asked 2026-10-07 during template adoption; blocks P2-01; recommendation: use GitHub
  private vulnerability reporting and SemVer-style tags if they match existing maintainer practice)
