# Contributing

This is the shared workflow for human and automated contributors. Agent-specific standing instructions are in
[AGENTS.md](../AGENTS.md).

## Before changing code

1. Read the root README, relevant roadmap item, architecture section, and test guidance.
2. Install a compatible Visual Studio C++ desktop/MFC workload; see [TESTING.md](TESTING.md) and Q-001 before
   treating a particular toolchain or retargeting step as canonical.
3. Check `git status` and recent history; confirm the change will not overlap unrelated work.
4. Use committed fixtures or a disposable game copy for any operation that writes SCI data.
5. For a large, compatibility-breaking, or irreversible change, agree on scope and rollback first.

## Make the change

- Keep each change reviewable and focused on one outcome.
- Preserve existing SCI file/script compatibility unless the roadmap and an accepted decision allow a break.
- Match the C++/MFC style in the touched files; keep reusable behaviour in `SCICompanionLib`.
- Add or update tests for changed behaviour. Make a new regression test fail for the intended reason before trusting
  it, then restore the fix and rerun the relevant suite.
- Update documentation according to [the documentation triggers](README.md#update-triggers).
- Do not include credentials, personal data/paths, private game assets, generated caches, or local configuration.
- Get maintainer approval before adding a dependency or changing bundled third-party code.

## Verify

```text
python3 tools/check_docs.py
msbuild SCICompanion.sln /m /p:Configuration=Release /p:Platform=Win32
vstest.console.exe Release\UnitTests.dll
```

The MSBuild and VSTest commands require a compatible Windows/Visual Studio environment and are not yet verified on
a clean machine. Follow [TESTING.md](TESTING.md) for prerequisites, exact scope, and manual checks. Report every
command run, its outcome, and what was skipped; a partial pass is not a full pass.

## Submit and review

Create a focused branch (agents use `codex/<topic>`), use concise imperative commit summaries, and open a pull
request against `master`. Reference a roadmap or issue ID when the work has one. Describe user and compatibility
impact, tests run, manual environments, fixture/data effects, and rollback considerations. A maintainer reviews and
merges; do not push, merge, publish, or rewrite shared history without explicit authority.

A change is ready when its scope is clear, relevant checks pass, user and migration impact is described, sensitive
data is absent, and the documentation it invalidated has been updated.

## Compatibility and migrations

Existing game projects are user data. Changes to resource encodings, scripts, templates, settings, or conversion
paths must define the affected SCI versions, preserve a recovery route, and verify both old-data reads and new-data
save/reload behaviour on disposable copies. Do not silently migrate the only copy or remove backward compatibility
without an accepted decision and maintainer approval.

## Reporting security issues

Do not open a public issue for a suspected vulnerability. Follow [SECURITY.md](SECURITY.md).
