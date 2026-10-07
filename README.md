# SCI Companion

SCI Companion is a Windows desktop IDE for creating and maintaining Sierra SCI games from SCI0 through SCI1.1.
It provides editors and tooling for scripts, pictures, views, fonts, audio, messages, vocabularies, and other SCI
resources.

Official website: [scicompanion.com](http://scicompanion.com)

## Repository structure

- `SCICompanion/` is the executable project and a thin shell over the shared library.
- `SCICompanionLib/` contains most application code; start in `SCICompanionLib/Src/`.
- `UnitTests/` contains Microsoft Visual Studio C++ tests and their fixtures.
- `Prof-UIS.2.92/` is the bundled user-interface framework.

See [the architecture guide](docs/ARCHITECTURE.md) for the component map and boundaries.

## Build

The solution targets Windows and uses MFC. Open `SCICompanion.sln` in a compatible Visual Studio installation with
the Desktop development with C++ and MFC components, or use a Visual Studio Developer Command Prompt:

```bat
msbuild SCICompanion.sln /m /p:Configuration=Release /p:Platform=Win32
```

The checked-in projects currently name the `v140_xp` platform toolset. The exact supported modern Visual Studio
version and retargeting requirements have not yet been verified; see [TESTING.md](docs/TESTING.md) before relying on
the command above.

## Test

Build the `UnitTests` project and run `Release\UnitTests.dll` with Visual Studio Test Explorer or
`vstest.console.exe`. The current suite contains tests for compilation, class browsing, resource loading and
deletion, picture drawing, polygon loading, and loading fixture games.

Documentation-only changes can be checked on any system with Python 3:

```bash
python3 tools/check_docs.py
```

Exact prerequisites, limitations, and manual release checks are in [TESTING.md](docs/TESTING.md).

## Contributing

Read [CONTRIBUTING.md](docs/CONTRIBUTING.md) before making a change. Current work and open verification gaps are in
[ROADMAP.md](ROADMAP.md), and the next session should begin with [HANDOFF.md](docs/HANDOFF.md).
