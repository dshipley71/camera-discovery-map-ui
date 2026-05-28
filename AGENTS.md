# AGENTS.md — camera-discovery-map-ui Build Rules

This repository implements a standalone map and review UI for artifacts produced by `camera-discovery`. It is a downstream artifact consumer, not part of the discovery runtime.

## Architecture boundary

```text
camera-discovery
  -> writes review artifacts / artifacts.zip
camera-discovery-map-ui
  -> reads artifact directory or ZIP
  -> writes camera_map_bundle.json, camera_map.geojson, map.html
```

Do not add a runtime dependency from this project to `camera-discovery` in the initial scaffold. Do not modify camera-discovery from this repository.

## Behavioral rules

- Do not create fake camera records, fake streams, fake validation results, fake coordinates, fake geocoding, fake video summaries, fake LLM responses, or synthetic runtime inventories.
- Do not hard-code real-world locations, agencies, source domains, source-specific behavior, or one-off camera types.
- Keep artifact semantics upstream-owned. This project consumes `camera.geojson`, `untrusted_camera_candidates.geojson`, `camera_candidates_table.csv`, and review ZIPs without redefining their meaning.
- Do not weaken tests to make a change pass.
- Do not perform network access during tests.
- Notebook-specific helper/display code does not belong under `src/`.
- Static review mode comes first. Server-mode video summarization is optional future behavior and must be user-triggered.
- Preview failure is not validation failure. Browser preview limitations must not mark a stream dead.
- Keep runtime dependencies lean. Do not add a web framework, browser automation framework, database, LLM SDK, or heavy media dependency without an explicit implementation phase.

## Verification expectations

For broad changes, run:

```bash
python -m compileall -q src tests
PYTHONPATH=src python -m pytest -q
python -m ruff check src tests
python -m mypy src/camera_discovery_map_ui
```

If a tool is unavailable, report that honestly rather than claiming the check passed.
