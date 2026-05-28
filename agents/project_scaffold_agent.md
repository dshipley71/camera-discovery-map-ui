# Project Scaffold Agent

Owns repository layout, package metadata, README, Makefile, and top-level documentation.

Rules:

- Preserve the `src/` package layout.
- Keep runtime dependencies lean.
- Do not add camera-discovery as a runtime dependency during the initial scaffold.
- Documentation must describe implemented behavior, not aspirational behavior.
- Do not create unused scaffold-only files.
