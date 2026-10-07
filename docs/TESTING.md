# Testing

How to run the available checks, what each proves, and what it cannot. Current results live in
[HANDOFF.md](HANDOFF.md); this file explains how to produce them.

## The suites

| Suite | File | Proves | Does not prove | Time, needs |
| --- | --- | --- | --- | --- |
| Documentation consistency | `tools/check_docs.py` | No placeholders; internal links and roadmap/decision/session references are consistent | C++ correctness or external links | Seconds, Python 3 |
| Native unit tests | `UnitTests/*.cpp` | Covered compiler, class-browser, resource, picture, polygon, and fixture-game behaviour | Complete UI workflows, every SCI variant, installation, or Wine compatibility | Windows, compatible Visual Studio/MFC toolchain |
| Manual desktop smoke test | Built `SCICompanion.exe` | The selected build starts and core user workflows operate in the tested environment | Untested Windows/Wine versions and resource formats | Windows or Wine, disposable game copy |

**Fast set:** `python3 tools/check_docs.py`, then build the affected C++ project for code changes.

**Full set:** build Release/Win32 for `SCICompanion.sln`, run the native unit-test DLL, and complete the manual smoke
checks below. P1-02 and P1-03 track the first fully recorded Windows baseline.

## Before any run

- **Protect game data:** Run editor, compiler, conversion, and deletion checks only against committed fixtures or a
  disposable copy. Tests and manual runs can write resource maps, volumes, patches, scripts, and preferences.
- **Clean state:** Start a baseline build with Visual Studio's Clean Solution, then Rebuild Solution. Resolve the
  exact output directory before deleting anything; never recursively delete an unresolved variable or workspace.
- **Preferences:** Existing registry settings can affect recent paths, tool profiles, and UI behaviour. Holding Shift
  while starting SCI Companion resets settings in the current code; do this only when losing those settings is okay.
- **Services:** No network service is required for the known automated suites. Running a game may require the user
  to configure an interpreter or emulator.

## Running each suite

### Documentation consistency

From the repository root:

```bash
python3 tools/check_docs.py
```

A pass exits 0 and ends with `0 error(s)`. Warnings are maintenance signals and should be addressed or explained.
The checker reads source documentation only and does not write files.

### Build and native unit tests

From a Visual Studio Developer Command Prompt after installing the compatible Desktop development with C++ and MFC
workload:

```bat
msbuild SCICompanion.sln /m /t:Rebuild /p:Configuration=Release /p:Platform=Win32
vstest.console.exe Release\UnitTests.dll
```

- The solution builds Prof-UIS, `SCICompanionLib`, the executable, and `UnitTests` in dependency order.
- The test post-build event copies `UnitTests/Files/` into `TestFiles/` beside the test DLL.
- A pass requires MSBuild success and a VSTest summary with no failed tests; individual pass lines without a final
  successful summary are incomplete evidence.
- The exact supported toolchain and output path still require Windows verification under P1-02. If Visual Studio
  emits elsewhere, run the built `UnitTests.dll` and update this guide with the verified path.

### Adding a native check

- Put focused cases in the relevant `UnitTests/Test*.cpp` file using the Microsoft C++ Unit Test Framework; add new
  source or fixture files to `UnitTests/UnitTests.vcxproj`.
- Use the committed fixtures under `UnitTests/Files/` or create isolated temporary copies. Do not depend on a
  developer's installed games or personal directories.
- Assert on parsed/written state, not only a message string. For persistence changes, reload the result.
- Before trusting a regression check, make only the intended fix fail and confirm the new test catches it.

## Change-to-check matrix

| Changed area | Minimum checks | Additional evidence |
| --- | --- | --- |
| Documentation only | `python3 tools/check_docs.py` | Inspect Markdown diff and links |
| Compiler, parser, decompiler, class browser | Affected build plus `TestCompile`/`TestClassBrowser` | Compile representative SCI0 and SCI1.1 fixture projects |
| Resource readers/writers | Affected build plus resource tests | Save/reload a disposable game; inspect unchanged unrelated resources |
| Picture/raster conversion | Affected build plus picture tests | Open, render, save, reload representative EGA and VGA assets |
| MFC UI, dialogs, frames | Build plus relevant unit tests | Manual native-Windows workflow; repeat under Wine for Wine-related changes |
| Project/toolchain/dependency | Full rebuild and all unit tests | Clean-machine or CI reproduction; license/provenance review |
| Security boundary or process launch | Relevant negative and abuse cases | Targeted review of path, size, quoting, and failure handling |

## Manual checks before a release

Record Windows/Wine version, architecture, build configuration, and the disposable game used in `HANDOFF.md`.

- Start the application with default settings and open a disposable SCI0 and SCI1.1 game.
- Open representative script, picture, view, font, sound/audio, text/message, and vocabulary editors supported by
  each game; make a reversible edit, save, close, reopen, and confirm it persisted.
- Compile scripts, inspect error navigation with an intentional syntax error, then restore and compile successfully.
- Add/export/delete a resource in the disposable copy and confirm unrelated resources remain readable.
- Configure and launch the game/interpreter; verify paths containing spaces are handled correctly.
- Exercise File > Open Game and at least one import/export dialog, including cancel and last-folder persistence.
- For a Wine-targeted change, repeat the affected workflow under the supported Wine version once Q-001 documents it.

## Environment recipes

- **Windows:** Use a Visual Studio Developer Command Prompt so `msbuild` and `vstest.console.exe` resolve. The
  project files identify Visual Studio 14 and mostly request `v140_xp`; do not silently retarget and call the result
  canonical. Record the installed Visual Studio edition/version, Windows SDK, MFC components, and any retargeting.
- **Linux/Codex:** Run the Python documentation check and source-level inspections only. This does not verify the
  native build or tests.

## Known pitfalls

- Solution configurations include many historical names and x64 entries that map back to Win32 or analysis
  configurations. State the exact solution configuration and actual project platform in test evidence.
- The tests are a DLL, not a standalone executable; use Visual Studio Test Explorer or `vstest.console.exe`.
- Test and application operations can modify game files and registry preferences. Never point exploratory tests at
  the only copy of a game project.
- A mutation check must break the fix, not the test. Reverting a whole file can fail for an unrelated reason.
- A test that calls internals breaks when they are cleaned up. Prefer the path the application uses and rerun the
  full set after deleting or moving code.
