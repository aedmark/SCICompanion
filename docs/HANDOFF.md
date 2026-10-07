# Session handoff

Read this first when resuming work. Rewrite the top half whenever current state changes materially or work pauses
with context another session needs. The session log is append-only history; archive older entries as described below.

Protocol: [AGENTS.md](../AGENTS.md). Plan: [ROADMAP.md](../ROADMAP.md). Architecture:
[ARCHITECTURE.md](ARCHITECTURE.md). Decisions: [DECISIONS.md](DECISIONS.md). Tests: [TESTING.md](TESTING.md).
Security: [SECURITY.md](SECURITY.md). Changes: [CHANGELOG.md](CHANGELOG.md). Older sessions:
[archive/](archive/README.md).

---

## Current state

_Last updated: 2026-10-07, session 2, on `master` at `538fe71a`: the 3x companion manual and its vendored generator
are uncommitted in this working tree._

**Where things stand, in one paragraph:** The canonical repository-memory documents are committed, and a generated
3x What/How/Why manual now provides a searchable orientation across product behavior, architecture, workflows, and
maintenance. Both documentation systems validate locally without changing product code. The main gap remains the
absence of a verified clean Windows build and native unit-test baseline, tracked by P1-02 and P1-03.

**Verified** (2026-10-07, on `538fe71a` plus the uncommitted 3x documentation application, Linux Codex workspace)

| Suite | Result |
| --- | --- |
| `python3 tools/check_docs.py` | **Pass: 0 errors** |
| `python3 tools/3x_manual.py check docs/SCICompanion.manual.json` | **Pass: 4 sections, 17 entries, 0 warnings** |
| `python3 tools/3x_manual.py build docs/SCICompanion.manual.json --output docs/manual.html` | **Pass: standalone manual generated** |
| Source inventory with `rg`, project files, `git log`, and `git status` | **Pass: claims in the new docs grounded in the checked-out repository** |

**What works**

- **Repository continuity** (P1-01, D-002). Agent rules, current state, architecture, decisions, test guidance,
  security boundaries, contribution workflow, roadmap, changelog, and archive policy each have an explicit home.
- **Documentation validation** (P1-01). `tools/check_docs.py` checks placeholders, references, links, and history IDs.
- **Explorable project manual** (P1-04, D-003). The evidence-linked 3x source generates a searchable standalone
  HTML manual while canonical project facts retain their existing owners.
- **Existing product shape** (D-001). The solution contains the thin `SCICompanion` executable,
  `SCICompanionLib`, bundled Prof-UIS, and a native `UnitTests` DLL with 14 discovered test methods.

**Not verified**

- No C++ project was built and no native unit test or UI workflow was run in this Linux workspace.
- The supported Visual Studio/SDK/MFC combination, exact output paths, Wine support level, release procedure, and
  private vulnerability reporting channel require maintainer or Windows-environment confirmation.

**Gotchas for the next session**

- Most projects request `v140_xp`, while one library configuration requests `v145`; do not silently retarget.
- Solution configuration names include x64 variants that can map to Win32 or analysis project configurations.
- Unit tests can copy fixtures and product operations can modify game files and registry settings. Use disposable
  data and resolve output paths before cleanup.
- The checked-in `Release/SCICompanion.exe` is an artifact, not evidence that the current checkout builds.

## Next steps (in order)

1. Review and commit P1-04 and the generated manual.
2. Resolve Q-001 and complete P1-02 on a clean Windows development environment.
3. Run and record all native tests for P1-03, then use that evidence to design P2-02 CI.
4. Resolve Q-002 and document the release/security workflow in P2-01.

## Open questions for maintainers

- Q-001: Which Windows/Visual Studio toolchain and retargeting path are supported? This blocks P1-02.
- Q-002: Who owns releases and private security reports, and what versions are supported? This blocks P2-01.

## Session log

Newest first. Past 10 entries, move the oldest complete entries to `docs/archive/` and leave a pointer here.

### Session 2: 2026-10-07: Apply the 3x Documentation Scheme

**Contributor:** Codex

**Goal:** Apply the supplied 3x template to SCI Companion after the repository-memory baseline was committed.

**Done:** P1-04.

**Changed:** Added `docs/SCICompanion.manual.json`, its schema, generated `docs/manual.html`, and the vendored
MIT-licensed generator; integrated validation and regeneration into the README, agent rules, documentation map,
testing guide, contribution guide, roadmap, decision log, and handoff; removed the nested staging repository.

**Decisions:** D-003 recorded.

**Verified:** Both documentation checkers pass without warnings; the generator builds 17 entries across 4 sections;
the standalone page's navigation, search, responsive triads, and evidence sections were smoke-tested.

**Not verified:** Native Windows build, unit tests, application smoke test, and Wine behavior remain outside this
Linux documentation-only change.

**Problems / surprises:** The supplied template arrived as a nested Git repository with IDE and bytecode state;
only the generator, schema, and required MIT license were retained.

**Corrections:** Session 1's template application was already committed as `538fe71a`, rather than remaining
uncommitted as its original handoff snapshot stated.

**Left undone:** P1-02, P1-03, P2-01, P2-02, and maintainer-directed product planning.

**Next session should start with:** Review the 3x source and generated manual, then resolve Q-001 in a Windows
environment.

### Session 1: 2026-10-07: Apply the Manifold template

**Contributor:** Codex

**Goal:** Apply the vendored `the-manifold` project-memory template to SCI Companion.

**Done:** P1-01.

**Changed:** Added and tailored `AGENTS.md`, `CLAUDE.md`, `ROADMAP.md`, the `docs/` set, and
`tools/check_docs.py`; expanded the root README with build, test, and documentation entry points; removed the
applied `the-manifold/` staging directory.

**Decisions:** D-001 and D-002 recorded.

**Verified:** `python3 tools/check_docs.py` passes; inspected Git state/history, solution and project metadata, unit
test sources, main application initialization, profile storage, and source layout.

**Not verified:** Native Windows build, unit tests, application smoke test, and Wine behaviour.

**Problems / surprises:** The project metadata names historical and mixed platform toolsets; no CI or release
procedure is present. The source template includes a large presentation file unrelated to runtime code.

**Corrections:** None.

**Left undone:** P1-02, P1-03, P2-01, P2-02, and maintainer-directed product planning.

**Next session should start with:** Review the applied documentation, then resolve Q-001 in a Windows environment.
