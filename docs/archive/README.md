# Archive

History moved out of the live docs so they stay short enough to read. Nothing here is current; everything here was
true when it was written. Search it before retrying an investigation that sounds familiar.

- **Session logs:** when `HANDOFF.md` passes 10 entries, move the oldest complete entries to
  `SESSION_LOG_YYYY_MM.md` (the month the sessions happened), newest first as in the handoff. Move entries whole;
  do not summarize them. `tools/check_docs.py` reads archive files so session numbers stay unique.
- **Roadmap phases:** a finished phase can move to `ROADMAP_YYYY_MM.md`, items unchanged. IDs stay reserved.
- **Anything else:** use one file per retired document or section, with a line at the top saying when and why it was
  moved.

Archive content is historical, not normative. Never store secrets, private game assets, personal paths, or sensitive
incident evidence here merely because it is old; follow [SECURITY.md](../SECURITY.md).

Leave a one-line pointer where archived text used to be.
