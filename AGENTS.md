# SCI Companion

SCI Companion is a Windows desktop IDE for creating and maintaining Sierra Creative Interpreter games from SCI0
through SCI1.1. It is a C++/MFC solution: `SCICompanion` is the executable shell, most behaviour lives in the
`SCICompanionLib` static library, and `UnitTests` uses the Microsoft Visual Studio C++ test framework.

This is the canonical instruction file for coding agents. `CLAUDE.md` imports it; do not duplicate these rules in
tool-specific files. Project facts belong in the documents linked below, not in an agent's private memory.

## Start here

1. Read `docs/HANDOFF.md` for the current state, active work, and gotchas.
2. Read the relevant roadmap item and the parts of `docs/ARCHITECTURE.md` and `docs/TESTING.md` that apply.
3. Inspect `git status` and recent history. Do not overwrite work you did not create.
4. Verify important inherited claims before relying on them. Use the fastest relevant check first.
5. State the intended scope briefly, then work on one independently reviewable change at a time.

If the repository is new or unfamiliar, read `README.md` and `docs/README.md` first. If the request conflicts with
these instructions or the working tree contains overlapping edits, stop and ask the maintainer.

## While working

- Reference roadmap or issue IDs where one exists. Do not invent an ID for an incidental, self-contained fix.
- Keep changes scoped. Do not mix opportunistic refactors with requested work.
- Preserve user changes. Never reset, clean, or rewrite history without explicit permission.
- Record a decision in `docs/DECISIONS.md` when reasonable maintainers could revisit the choice later.
- Update documentation in the same change when behaviour, interfaces, commands, risks, or project structure change.
- Distinguish observed facts from inference. Include the command, date, environment, or source behind volatile claims.
- Prefer enforcement to prose: important invariants should have a test, type, schema, linter, or runtime check.
- Treat game assets, scripts, imported media, and project paths as untrusted input at their boundary.
- Never expose credentials, private game data, or personal paths in logs, fixtures, prompts, or commits.
- Add newly discovered work to `ROADMAP.md` only when it is genuinely out of scope for the current change.

## Finishing a change

1. Run the checks appropriate to the change, following `docs/TESTING.md`. Record failures and anything not run.
2. Review the diff for unrelated edits, generated files, credentials, stale names, and documentation drift.
3. Update `docs/HANDOFF.md` if work will continue in another session or if the repository's current state changed.
4. Update the roadmap item, decision record, architecture, security notes, and changelog only when their documented
   update trigger applies (see `docs/README.md`).
5. Run `python3 tools/check_docs.py` and report the result.

Do not manufacture ceremony: typo-only or mechanical changes do not need a decision, changelog entry, or handoff
rewrite unless they alter a claim those documents make.

## Working agreement

Use a branch and pull request for shared changes. Agents may inspect, edit, build, and run local checks within the
requested scope. Creating commits, pushing, merging, publishing releases, adding dependencies, changing bundled
third-party code, or deleting user/game data requires explicit maintainer permission.

- Default branch: `master`.
- Working branch pattern: `codex/<topic>` for agent-created branches; maintainers may use their own convention.
- Commit format: concise imperative summary; prefix planned work with its roadmap ID when useful.
- Release/version scheme: Git tags such as `3.2.0`; the release procedure and version source of truth remain Q-002.

Never force-push, rewrite shared history, publish, or rotate/delete production or user data without explicit
permission.

## Maintainer preferences

- **Writing:** Use concise plain language, repository-relative paths, and the product name “SCI Companion”.
- **Code comments:** Explain non-obvious constraints, compatibility workarounds, and why; do not narrate syntax.
- **Asking vs. doing:** Make scoped reversible edits and run local checks; ask before the authority-sensitive actions
  listed in the working agreement.
- **Reporting:** Lead with the result, list exact checks and outcomes, and call out anything the current environment
  could not verify.

## Protected areas

| Path or thing | Rule | Why |
| --- | --- | --- |
| `Prof-UIS.2.92/` | Change only when the task explicitly requires it; preserve upstream notices | Bundled third-party UI library with its own license |
| `SCICompanionLib/Src/CrystalEdit/`, `GIFLIB/`, `r8brain/`, `cpptoml/` | Isolate changes and preserve provenance/license text | Vendored or imported components |
| `Release/` | Do not replace binaries without an explicit release request | Generated/distribution output |
| `SCICompanion/Files/TemplateGame/` | Treat compatibility changes as user-visible and test them | Shipped starter-game content |

## Names and terms

| Canonical term | Meaning | Not to be confused with |
| --- | --- | --- |
| SCI Companion | The desktop IDE/product | `SCICompanion`, the executable project |
| SCICompanionLib | Shared static library containing most product behaviour | The thin executable shell |
| game project | A user's SCI source tree and resources | This source repository |
| resource | An SCI asset such as a picture, view, sound, vocabulary, or message | A Windows `.rc` resource |

## Layout

| Path | Purpose |
| --- | --- |
| `SCICompanion/` | Executable shell, application startup, Windows resources, help sources, and shipped files |
| `SCICompanionLib/` | Core editors, compiler/decompiler, resource model, documents, views, dialogs, and utilities |
| `UnitTests/` | Visual Studio C++ unit tests and fixture data |
| `Prof-UIS.2.92/` | Bundled Prof-UIS UI framework |
| `SCICompanion.sln` | Visual Studio solution |
| `AGENTS.md` | Canonical agent instructions |
| `ROADMAP.md` | Planned work with stable IDs |
| `docs/README.md` | Documentation map and update triggers |
| `docs/HANDOFF.md` | Current state, next steps, gotchas, and bounded session history |
| `docs/ARCHITECTURE.md` | Components, boundaries, invariants, state, and failure modes |
| `docs/DECISIONS.md` | Append-only architectural and product decisions; open questions |
| `docs/TESTING.md` | Test strategy, commands, limitations, and environment recipes |
| `docs/SECURITY.md` | Assets, trust boundaries, secret handling, and reporting |
| `docs/CONTRIBUTING.md` | Human and agent contribution workflow |
| `docs/CHANGELOG.md` | User-visible release notes |
| `docs/archive/` | Historical material no longer current |
| `tools/check_docs.py` | Documentation consistency checks |

## Engineering conventions

- Match the existing C++/MFC style in the files being changed. The core library requests C++17 in its project file.
- Windows is the build and runtime target. Wine compatibility matters where behaviour is already supported, but its
  exact support level is not yet documented.
- Keep the executable shell thin; put reusable application behaviour in `SCICompanionLib`.
- Preserve compatibility with existing SCI game resources and scripts unless an accepted decision permits a break.
- New external dependencies require maintainer approval. Prefer the standard library and already-bundled code.
- Visual Studio output, IDE state, and generated help are not source; do not commit them unless the release workflow
  explicitly requires an artifact update.

## Environments

| Environment | Can access | Cannot access / caveats |
| --- | --- | --- |
| Windows development | Visual Studio, MFC, Windows SDK, Test Explorer, native app | Exact supported VS/toolset is unresolved in Q-001 |
| Linux/Codex workspace | Source inspection, Python documentation checker, Git tooling | Cannot build or run the MFC solution without a configured Windows toolchain |
| CI | No repository CI configuration observed as of 2026-10-07 | No automated build or test evidence yet (P2-02) |

## Run and verify

- Setup: install a compatible Visual Studio C++ desktop/MFC workload and Windows SDK; resolve Q-001 before treating
  a particular toolset as canonical.
- Build: `msbuild SCICompanion.sln /m /p:Configuration=Release /p:Platform=Win32` from a Visual Studio Developer
  Command Prompt.
- Run: `Release\SCICompanion.exe` after a successful Release/Win32 build.
- Fast checks: `python3 tools/check_docs.py`; for C++ changes, build the affected project in Visual Studio.
- Full checks: build `SCICompanion.sln`, then run `vstest.console.exe Release\UnitTests.dll` and perform the manual
  checks in `docs/TESTING.md`.
- Detailed test guidance: `docs/TESTING.md`.
