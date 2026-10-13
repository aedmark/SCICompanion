# Changelog

User-visible changes, newest first, in plain words. This is not a copy of the Git or session log. Add to
“Unreleased” as changes land; on release, rename it to the version and date and start a new section.

## Unreleased

### Fixed

- File dialogs remember the last browsed folder, including when SCI Companion runs under Wine.
- Message resources in the SCI1.1-era format (version 0xD53 and older, such as Laura Bow 2) can now be saved. Previously
  a save wrote only a 4-byte header and lost every message. Each entry's three reference bytes are preserved.

Documentation migration and maintenance-only changes are intentionally omitted because they do not alter product
behaviour.
