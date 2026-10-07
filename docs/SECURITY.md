# Security

This document describes the project's current security assumptions and reporting gap. It is not a claim that SCI
Companion is vulnerability-free.

## Supported versions

No supported security branch or version is documented yet. The latest observed tag is `3.2.0`, and `master` is the
default branch as of 2026-10-07; neither observation is a support promise. P2-01 and Q-002 track a maintainer-owned
policy.

## Report a vulnerability

No private reporting channel is recorded in the repository. Do not publish exploit details or sensitive game data
in a public issue. Contact the repository maintainer privately through an established channel and ask for a secure
route; Q-002 tracks replacing this interim guidance with an explicit address or private reporting URL.

Include affected versions, impact, minimal reproduction steps, and any workaround. Remove credentials, personal
paths, copyrighted/private game assets, and unrelated data. Acknowledgement time and coordinated-disclosure timing
are not yet defined.

## Assets and boundaries

| Asset or boundary | Sensitivity / threat | Protection and validation | Owner |
| --- | --- | --- | --- |
| User game project | Corruption, unintended overwrite, disclosure of private assets | Work on backups; version-aware parsing/writing; validate before conversion | Resource and compiler code |
| Imported files and SCI resources | Malformed sizes/offsets, memory corruption, path abuse | Bounds/format checks and negative fixture tests | Format-specific loaders |
| Executable path and arguments | Command/argument injection or launching the wrong program | Preserve argument boundaries; do not invoke a shell with concatenated input | `RunLogic` |
| Registry preferences and recent paths | Personal path disclosure, unsafe stale settings | Local profile APIs, safe defaults, explicit reset | Application shell and dialogs |
| Bundled dependencies | Known vulnerabilities, provenance/license drift | Isolated review, preserved notices, maintainer approval for upgrades | Maintainers |
| Diagnostic output and reports | Leakage of paths, scripts, game metadata, or assets | Sanitize before sharing; keep only minimal reproducer data | Reporter/contributor |

Architecture details are in [ARCHITECTURE.md](ARCHITECTURE.md); this table records the security consequence.

## Secure development rules

- Keep credentials, personal information, private game assets, and personal paths out of code, documentation,
  prompts, logs, screenshots, fixtures, and commits.
- Treat files, resource metadata, scripts, registry values, paths, and command-line input as untrusted. Validate
  lengths, offsets, counts, formats, and integer conversions before allocation or access.
- Preserve argument boundaries when launching an interpreter, emulator, documentation command, or helper process.
  Avoid shell interpretation; test paths and arguments containing spaces and metacharacters.
- Save through recoverable or atomic patterns where practical. Never use the user's only copy for destructive tests.
- New or upgraded dependencies require maintainer approval under `AGENTS.md`; preserve and review license notices.
- Authentication, cryptography, installer trust, or destructive migration changes require targeted review and a
  rollback/recovery plan.

## Security verification

There is no configured CI, dependency scanner, fuzzer, or documented security test suite as of 2026-10-07. Existing
native tests exercise some parsing and resource operations but are not a security boundary audit. For changes at a
boundary, add malformed/truncated/oversized cases where feasible, run the full native suite, manually verify safe
failure on a disposable copy, and record evidence in `HANDOFF.md`. P2-02 tracks baseline automation.

## Incident response

If active exploitation, malicious binaries, or private-data exposure is suspected: stop using affected builds on
valuable game projects, preserve minimal evidence without copying sensitive data into the repository, notify the
maintainer privately, restore projects from known-good backups, and rotate any exposed external credentials. No
project-specific incident runbook or response owner exists yet; establish both under P2-01.
