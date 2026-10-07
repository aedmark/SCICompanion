# Architecture

How SCI Companion fits together for a session that has never seen it. This is the map, not the territory: it names
the parts and the rules between them and leaves detail to the code. Why things are this way lives in
[DECISIONS.md](DECISIONS.md); this file says what exists now.

## The shape, in one paragraph

`SCICompanion/SCICompanion.cpp` starts the MFC multiple-document application, restores settings, and registers the
document/frame/view templates used by each editor. The executable delegates shared state and nearly all product
behaviour to `SCICompanionLib`: a game folder is identified, its SCI version and resource storage are detected,
resources are exposed through document models, and MFC views/dialogs edit them. Scripts pass through the parser,
compiler, or decompiler; pictures, raster assets, audio, text, messages, and vocabularies have resource-specific
code. Saves write back into the user's game project or its selected patch/resource storage.

## Code map

| Area | Where | Entry point | Talks to |
| --- | --- | --- | --- |
| Application shell | `SCICompanion/` | `SCICompanionApp::InitInstance()` | App state, document templates, main frame |
| Shared application state | `SCICompanionLib/Src/Util/` | `AppState` | Resource map, settings, editors, run logic |
| Resource model and storage | `SCICompanionLib/Src/Resources/` | `ResourceMap` and resource sources | Game files, resource entities, caches |
| Script language tools | `SCICompanionLib/Src/Compile/` | compiler/parser/decompiler entry points | Script files, class browser, compiled resources |
| Document models | `SCICompanionLib/Src/MFCDocuments/` | MFC `CDocument` subclasses | Resources, views, undo/save operations |
| Editor views and frames | `SCICompanionLib/Src/MFCViews/`, `MFCFrames/` | MFC view/frame subclasses | Documents, dialogs, frame components |
| Commands and panels | `SCICompanionLib/Src/Dialogs/`, `FrameComponents/` | Dialog and pane classes | App state, documents, resources |
| Tests | `UnitTests/` | Visual Studio `TEST_METHOD` cases | Library code and committed fixtures |
| Bundled UI framework | `Prof-UIS.2.92/` | Prof-UIS MFC controls | Application shell and editor UI |

## Interfaces and data flow

```text
game folder / imported asset / user edit
    -> version and format detection
    -> ResourceMap and resource-specific model
    -> MFC document/view or compiler operation
    -> game resource storage, patch file, export, or executable launch
```

| Interface | Producer | Consumer | Contract / compatibility |
| --- | --- | --- | --- |
| SCI game directory and resource files | Sierra games, templates, users | Resource sources and `ResourceMap` | Multiple SCI generations and storage layouts; preserve existing data |
| Script source and headers | User/editor | parser, compiler, class browser | Sierra and Studio syntax variants are handled by compiler code |
| `ResourceEntity`/resource blobs | Resource loaders and editors | documents, views, encoders | Type and SCI version determine encoding and valid operations |
| MFC document/view notifications | document models | frames, views, panes | UI-thread-oriented MFC lifetime and update semantics |
| Windows profile settings | application and dialogs | later application sessions | Stored under the `mtnPhilms` registry key; defaults must remain safe |
| Game executable/profile settings | user preferences | `RunLogic` | Paths and parameters cross a process-launch boundary |

## Invariants

- `SCICompanion` remains a thin executable wrapper; reusable product logic belongs in `SCICompanionLib`. Enforced by:
  project references and existing layout; no structural test yet.
- Resource parsing and writing must use the active game's SCI version and resource-map traits. Enforced by: types and
  resource tests in `UnitTests/`; coverage is incomplete.
- Editing an existing game must not silently discard unknown or unrelated resources. Enforced by: resource load,
  create, delete, and save/reload tests; release-level coverage still requires manual checks.
- UI documents own editor lifetime and save/undo integration through MFC document/view patterns. Enforced by: class
  structure; no dedicated lifecycle test.
- Bundled third-party notices and provenance stay with their code. Enforced by: review only.

## Boundaries

| Boundary | Comes in as | Checked by | Rule |
| --- | --- | --- | --- |
| Game project | Paths, scripts, resource maps, volumes, patches | Version detection, parsers, resource readers | Treat malformed or unsupported data as errors; do not corrupt source files |
| Imported/exported media | Image, audio, font, view, and other files | Format-specific loaders and dialogs | Validate size/format before allocation or conversion |
| File and folder selection | Windows/Wine dialog results | Dialog wrappers and path utilities | Preserve paths faithfully; cancellation must not mutate project state |
| Process launch | Emulator/game executable path and arguments | `RunLogic` and stored profiles | Never build an unsafe shell command from untrusted text |
| Windows profile | Registry-backed strings and integers | MFC profile APIs and local defaults | Invalid or stale settings must fall back safely |

## Dependencies

| Dependency | Version | For | Why this one |
| --- | --- | --- | --- |
| Microsoft Visual C++/MFC and Windows SDK | Project files use `v140_xp`; exact supported install unresolved | Build, UI, OLE, media, tests | The application is a native Windows/MFC program |
| Prof-UIS | 2.92, bundled | Advanced MFC controls and frame UI | Existing UI framework; license is in `Prof-UIS.2.92/license.txt` |
| Microsoft C++ Unit Test Framework | Visual Studio-provided | `UnitTests` | Existing native test integration |
| GDI+ and Video for Windows | Windows SDK libraries | Graphics and media operations | Platform APIs already used by the library |
| Crystal Edit, GIFLIB, cpptoml, r8brain, CppFormat | Bundled source | Text editing, GIF handling, TOML, resampling, formatting | Existing source dependencies kept local for the native build |

New dependencies require maintainer approval under [AGENTS.md](../AGENTS.md).

## State and caches

| What | Where | Written by | Reset by | Committed? |
| --- | --- | --- | --- | --- |
| Game project data | User-selected game directory | Resource writers, compiler, editors | User backup/version control; no global reset | No, except shipped templates/test fixtures |
| Preferences and recent files | Windows registry under the app's `mtnPhilms` profile | MFC profile APIs | Holding Shift during startup resets settings in current code | No |
| Build output | `Debug/`, `Release/`, project/intermediate directories | Visual Studio/MSBuild | Visual Studio Clean or remove a resolved output directory | Generally ignored; a release executable exists in `Release/` |
| IDE caches | `.vs/`, `.idea/` | Visual Studio/JetBrains tools | IDE or user after closing the IDE | No, ignored |
| Unit-test copied fixtures | Build output under `TestFiles/` | `UnitTests` post-build event | Clean the test output directory | No |

## Failure modes and observability

| Failure | User-visible behaviour | Detection | Recovery |
| --- | --- | --- | --- |
| Unsupported/corrupt SCI data | Load, compile, or editor error; legacy paths may assert or fail | Dialog/output pane, debugger, focused fixture test | Work on a copy, capture a sanitized reproducer, fix parser/writer |
| Missing build toolset/MFC | Solution fails before compilation | MSBuild/Visual Studio diagnostic | Install required workload or follow the verified retargeting recipe from P1-02 |
| Invalid emulator/game launch profile | Game does not start | UI error and debugger/log output | Correct executable and argument profile in preferences |
| Partial write or incompatible conversion | Game resource fails to reload or changes unexpectedly | Save/reload tests and manual open/compile/run | Restore backup/source control; isolate writer defect before retrying |
| Wine-specific Windows behaviour | Dialog or UI behaviour differs from native Windows | Manual Wine reproduction | Keep workaround localized and verify both Wine and Windows |

Diagnostic output may include file paths and game metadata. Sanitize it before sharing; never commit private game
projects or personal paths. Security consequences and reporting belong in [SECURITY.md](SECURITY.md).

## Claims vs. code

- The README says SCI0 through SCI1.1; fixtures include some SCI2 picture resources. Fixture presence alone does not
  establish full SCI2 product support.
- Recent commits address Wine compatibility, but no supported Wine version or complete compatibility promise is
  documented.
- The solution identifies Visual Studio 14 and most projects request `v140_xp`; one library configuration mentions
  `v145`. P1-02 must determine the reproducible supported toolchain.
