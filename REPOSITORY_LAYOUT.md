# Repository Layout

```text
camera-discovery-map-ui/
  AGENTS.md                    # repository-wide behavioral rules
  README.md                    # user/developer overview
  MAPS.md                      # map UI notes and current limitations
  REPOSITORY_LAYOUT.md         # this file
  Makefile                     # local check commands
  pyproject.toml               # package metadata and CLI entry point

  agents/                      # focused agent ownership documents
  docs/                        # artifact, media, summarization, and development docs
  src/camera_discovery_map_ui/  # importable Python package
  tests/                       # local deterministic tests and fixtures
```

## Skills markdown decision

No custom `skills/` markdown system is required for the initial scaffold. The repository follows the simpler camera-discovery-style `AGENTS.md` plus focused `agents/*.md` pattern.
