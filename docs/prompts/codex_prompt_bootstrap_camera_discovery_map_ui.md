# Codex Prompt — Bootstrap `camera-discovery-map-ui` Repository

You are creating a new standalone repository named `camera-discovery-map-ui`.

The purpose of this repository is to provide a polished map/review UI for artifacts produced by the `camera-discovery` repository. The UI must remain independently developed and testable. For now, **do not make `camera-discovery` depend on this repository as a Python library**. Treat `camera-discovery` as an upstream artifact producer and this project as a downstream artifact consumer.

This prompt is intentionally limited to bootstrapping the new repository structure, package scaffold, documentation, agent markdown files, artifact contract, minimal working bundle builder, initial map template placement, and tests. Do not attempt to complete the entire map UI redesign, video summarization backend, or deep camera-discovery integration in this first pass.

---

## Non-Negotiable Rules

1. **Follow camera-discovery behavioral conventions.** Mirror the style and guardrails used by the root `AGENTS.md` and `/docs/codex_prompt_*.md` files in the `camera-discovery` repository.
2. **No fake runtime evidence.** Do not create fake camera records, fake streams, fake validation results, fake coordinates, fake browser success, fake video summaries, fake LLM responses, fake geocoding, or synthetic runtime inventories.
3. **No source-specific hacks.** Do not hard-code real-world locations, agencies, source domains, source-specific behavior, or one-off camera types. Generic media normalization, URL/media classification, artifact loading, status normalization, and diagnostics are allowed.
4. **Do not weaken contracts to make tests pass.** Add tests that protect the artifact contract and scaffold behavior. Do not relax assertions to hide incomplete behavior.
5. **No notebook-specific source code.** This project may eventually support notebooks, but notebook helper/display code must not be placed under `src/`.
6. **Keep dependencies lean.** Do not introduce a web framework, browser automation framework, database, LLM SDK, or heavy media dependency in the initial scaffold unless explicitly required below. Use Python standard library where practical.
7. **Static review mode first.** The initial deliverable should support static/local artifact review and deterministic bundle generation. Server-mode summarization is a future phase and must not be faked.
8. **Preserve camera-discovery artifact meanings.** This repository consumes `camera-discovery` artifacts but must not redefine what `camera.geojson`, `untrusted_camera_candidates.geojson`, `camera_candidates_table.csv`, or `review_artifacts.zip` mean.
9. **Do not modify the camera-discovery repository.** Create or update only files in the new `camera-discovery-map-ui` repository unless explicitly instructed otherwise.
10. **If a prompt detail conflicts with verified source/artifact contents, prefer verified files.** Inspect attached/available artifacts before deciding paths, schemas, or field names.

---

## Inputs to Inspect Before Editing

Before creating files, inspect the current working directory and any provided reference artifacts. If these files are present, use them as inputs:

```text
map.zip
  map_template.html
  MAPS.md
  map_agent.py
  untrusted_camera_candidates.geojson
  camera_candidates_table.csv

camera-discovery repository or zip
  AGENTS.md
  docs/codex_prompt_*.md
  agents/*.md
  docs/output_artifacts.md
  docs/project_structure.md
  src/camera_discovery/utils/geojson_viewer.py
```

Record in your final response which of these inputs were found and used.

If `map_template.html` is present, copy it into this new project as the initial visual baseline, then remove or clearly isolate old webcam-discovery assumptions in documentation. Do not claim the template is fully camera-discovery-compatible until the required contract tests pass.

---

## High-Level Goal

Create a clean initial repository scaffold for `camera-discovery-map-ui` that can:

1. Accept a `camera-discovery` review artifact bundle such as `review_artifacts.zip` or `artifacts.zip`.
2. Read known camera-discovery artifact files from a directory or zip.
3. Normalize trusted, untrusted, and future harvested/unvalidated camera records into a stable map UI bundle.
4. Write a deterministic `camera_map_bundle.json` and `camera_map.geojson`.
5. Write or copy an initial `map.html` from a versioned template.
6. Document the map data contract, media-preview plan, artifact boundaries, and future on-demand summarization contract.
7. Provide root and focused agent markdown files similar to the `camera-discovery` repository.
8. Provide tests that verify the scaffold and data-contract behavior.

This first pass should make the project ready for iterative development. It should not implement expensive video summarization, real media validation, real geocoding, or camera-discovery pipeline integration.

---

## Required Repository Layout

Create the following structure, adjusted only if the current repository already has an equivalent layout:

```text
camera-discovery-map-ui/
  AGENTS.md
  README.md
  MAPS.md
  REPOSITORY_LAYOUT.md
  Makefile
  pyproject.toml

  agents/
    project_scaffold_agent.md
    artifact_contract_agent.md
    map_template_agent.md
    media_preview_agent.md
    summarization_agent.md
    tests_agent.md

  docs/
    README.md
    artifact_contract.md
    project_structure.md
    media_preview_contract.md
    summarization_contract.md
    development_plan.md

  src/
    camera_discovery_map_ui/
      __init__.py
      agent.py
      artifacts.py
      bundle.py
      cli.py
      media.py
      normalize.py
      schema.py
      status.py
      templates/
        map_template.html

  tests/
    fixtures/
      README.md
      camera.geojson
      untrusted_camera_candidates.geojson
      camera_candidates_table.csv
    test_artifacts_loader.py
    test_bundle_builder.py
    test_cli_contracts.py
    test_media_detection.py
    test_status_mapping.py
    test_template_contract.py
```

Optional `skills/` guidance:

- Inspect whether the repository or attached reference files contain any existing skills markdown convention.
- If no such convention exists, do **not** invent a skills system.
- If you need to document this decision, add a short section to `REPOSITORY_LAYOUT.md` or `docs/development_plan.md` stating that no custom skills markdown files are required for the initial scaffold.

---

## Required `pyproject.toml`

Use setuptools with a `src/` layout.

Required metadata:

```toml
[project]
name = "camera-discovery-map-ui"
version = "0.1.0"
description = "Standalone map and review UI for camera-discovery artifacts"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [{name = "Camera Discovery Contributors"}]
```

Core dependencies should be lean. Suggested runtime dependencies:

```text
typer>=0.12
rich>=13.7
```

Do **not** add `camera-discovery` as a dependency in this initial scaffold.

Suggested optional dependencies:

```toml
[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.8", "mypy>=1.8"]
```

Expose a CLI:

```toml
[project.scripts]
camera-discovery-map-ui = "camera_discovery_map_ui.cli:app"
```

Set up pytest, ruff, mypy, and package discovery similarly to camera-discovery, but scoped to this package.

---

## Required CLI

Implement a thin Typer CLI in `src/camera_discovery_map_ui/cli.py`.

Required commands:

```bash
camera-discovery-map-ui build --input <artifact-zip-or-dir> --output-dir <out-dir>
camera-discovery-map-ui inspect --input <artifact-zip-or-dir>
```

Behavior:

### `build`

- Accept either a directory or a `.zip` file.
- Load available camera-discovery artifacts.
- Build `camera_map_bundle.json`.
- Build `camera_map.geojson` containing only mapped records with valid coordinates.
- Write `map.html` from `src/camera_discovery_map_ui/templates/map_template.html`.
- Print a concise summary including total records, mapped records, unmapped records, live/dead/unknown counts, and output paths.

### `inspect`

- Accept either a directory or a `.zip` file.
- Report which known artifacts are present or missing.
- Report record counts where they can be computed deterministically.
- Do not attempt validation, geocoding, or summarization.

CLI command bodies must remain thin. Put loading, normalization, and writing behavior in focused modules.

---

## Required Python Modules

### `schema.py`

Define constants and small dataclasses/TypedDicts if helpful for the stable bundle contract.

The internal normalized record should include at minimum:

```text
schema_version
record_id
record_stage
label
location_label
target_label
latitude
longitude
has_coordinates
coordinate_source
coordinate_confidence
status
validation_status
trust_level
scope_status
review_required
camera_type
raw_camera_type
media_type
asset_role
stream_url
snapshot_url
thumbnail_url
source_url
json_endpoint_url
summarization
metadata
source_artifact
```

Do not require all upstream records to contain every field. Missing fields should normalize to explicit `None`, empty strings, or `unknown` values as appropriate.

### `status.py`

Implement deterministic status normalization:

```text
live
  active_live_unknown
  active_live_verified
  active_image_snapshot_refreshing
  active_image_snapshot_static_unverified
  active_live_static_view
  active_live_dynamic
  active_prerecorded_loop_short
  active_prerecorded_loop_long

dead
  dead_link
  offline_http
  restricted_http
  active_playlist_dead_segments
  static_image_asset
  image_snapshot_not_image
  decode_failed

unknown
  null/empty
  not_validated
  unknown
  review
  anything unmapped
```

Expose a function similar to:

```python
def normalize_status(validation_status: str | None) -> str: ...
```

### `media.py`

Implement generic media detection and preview classification. Support at least:

```text
hls / .m3u8
mp4
webm
ogg/ogv
mjpeg / mjpg
image_snapshot / jpg/jpeg/png/webp/gif
web_embed
unknown
```

Do not perform network access. This is classification only.

Expose functions similar to:

```python
def detect_media_type(url: str | None, declared_type: str | None = None) -> str: ...
def preview_capability(media_type: str) -> str: ...
```

### `artifacts.py`

Implement deterministic artifact discovery for either a directory or zip file.

Known input artifact names include:

```text
camera.geojson
untrusted_camera_candidates.geojson
untrusted_camera.geojson
camera_candidates_table.csv
review_artifacts.zip
artifacts.zip
harvest_unvalidated.geojson
harvest_untrusted.geojson
harvest_geocoded.geojson
harvest_records.jsonl
harvest_records.csv
harvest_summary.json
logs/output_summary.json
logs/run_explanation.json
logs/target_resolution_all.json
```

The loader should:

- Read available known artifacts.
- Avoid extracting arbitrary files outside the output/temp location.
- Return file contents/records to callers without mutating source artifacts.
- Preserve source artifact provenance for every normalized record.

### `normalize.py`

Implement normalization from:

- trusted GeoJSON features;
- untrusted/review GeoJSON features;
- future harvested/unvalidated GeoJSON features;
- candidate CSV rows.

Rules:

- Do not invent coordinates.
- Do not mark anything trusted unless the source artifact and fields indicate trusted output.
- Preserve source metadata as much as possible.
- Preserve `target_id`, `target_label`, `target_index`, `validation_status`, `scope_status`, `trust_level`, `candidate_priority_bucket`, `review_required`, and `untrusted_reason` when present.
- Normalize camera type separately from media type.
- Treat CSV-only rows without coordinates as table records, not map features.

### `bundle.py`

Implement the bundle builder.

Required output bundle shape:

```json
{
  "schema_version": "camera-discovery-map-bundle/v1",
  "source": {
    "input_path": "...",
    "input_type": "directory|zip",
    "artifacts_found": []
  },
  "summary": {
    "records_total": 0,
    "mapped_records": 0,
    "unmapped_records": 0,
    "live": 0,
    "dead": 0,
    "unknown": 0,
    "by_record_stage": {},
    "by_media_type": {},
    "by_camera_type": {},
    "by_trust_level": {},
    "by_scope_status": {}
  },
  "geojson": {
    "type": "FeatureCollection",
    "features": []
  },
  "rows": []
}
```

### `agent.py`

Implement a small public service class, similar in spirit to the service/facade pattern in camera-discovery:

```python
from camera_discovery_map_ui.agent import CameraDiscoveryMapAgent
```

Responsibilities:

- call artifact loader;
- call bundle builder;
- write `camera_map_bundle.json`;
- write `camera_map.geojson`;
- write `map.html`;
- return a result object with artifact paths and summary.

### `templates/map_template.html`

Use the supplied `map_template.html` as the visual baseline if available.

Initial template requirements:

- Keep the polished dark Leaflet layout.
- Do not retain hard-coded Tier 1/Tier 2/Tier 3 geography as an active camera-discovery feature.
- Do not claim all final media-preview behavior is complete unless implemented.
- Load `camera_map_bundle.json` when served over HTTP.
- Allow manual loading of `.json`, `.geojson`, and eventually `.zip` files.
- Include clear static-mode behavior for summarization: button disabled or explanatory text unless a summarization endpoint is configured.

It is acceptable in this initial scaffold to make the template contract-focused rather than fully feature-complete, but it must not contain stale documentation claims that conflict with the implemented behavior.

---

## Documentation Requirements

### Root `AGENTS.md`

Create root behavioral rules for this repository. Include:

- no fake camera/media/geocode/summary evidence;
- no source-specific hacks;
- static artifact review boundary;
- camera-discovery artifact meanings are upstream-owned;
- LLM/video summarization is future optional server-mode behavior and must be user-triggered;
- no camera-discovery runtime dependency yet;
- verification expectations.

### `agents/*.md`

Create focused agent docs similar to the camera-discovery repository:

1. `project_scaffold_agent.md` — owns package layout, pyproject, Makefile, README, docs.
2. `artifact_contract_agent.md` — owns artifact ingestion and normalized bundle contract.
3. `map_template_agent.md` — owns static HTML template, table/map layout, filters, and popup UI contract.
4. `media_preview_agent.md` — owns media-type detection and browser preview behavior contract.
5. `summarization_agent.md` — owns future on-demand summarization contract only; no fake backend.
6. `tests_agent.md` — owns tests and verification commands.

### `docs/artifact_contract.md`

Document:

- supported input artifact names;
- `camera-discovery-map-bundle/v1` schema;
- trusted vs untrusted vs harvested record stages;
- mapped vs unmapped rows;
- status normalization;
- camera type vs media type;
- coordinate source/confidence fields;
- source artifact provenance.

### `docs/media_preview_contract.md`

Document preview rules:

```text
HLS .m3u8 -> hls.js + video element
MP4/WebM/OGG -> native video element
MJPEG -> img stream where browser permits
image snapshot -> refreshing img with cache-busting
thumbnail -> still preview
web embed -> optional iframe/fallback link
unknown -> metadata + open-link buttons
```

Document that preview failure is not validation failure.

### `docs/summarization_contract.md`

Document future user-triggered summarization:

- popup button;
- interval dropdown values such as `15s`, `30s`, `60s`, `120s`, `240s`, `300s`;
- optional local/server mode endpoint;
- disabled static-mode behavior;
- summary cache key;
- summary record including LLM provider and model.

Required summary record fields:

```text
summary_id
camera_id
stream_url_hash
summarized_at
sample_window_seconds
frames_sampled
media_type
summarizer.provider
summarizer.model
summarizer.model_role
summarizer.prompt_version
summarizer.code_version
summary
observations
warnings
status
cached
error
```

Do not implement fake summarization. Do not return canned summaries.

---

## Test Requirements

Add tests that pass using only local fixtures and no network access.

Required coverage:

1. Status mapping.
2. Media detection for HLS, MP4, WebM, OGG/OGV, MJPEG, image snapshots, web embeds, and unknown URLs.
3. Artifact loader can read a directory fixture.
4. Artifact loader can read a zip fixture created during the test.
5. Bundle builder preserves mapped and unmapped records.
6. Bundle builder does not invent coordinates.
7. Trusted GeoJSON and untrusted GeoJSON preserve source artifact provenance.
8. CSV-only rows without coordinates remain in `rows` and not `geojson.features`.
9. CLI `build` writes `camera_map_bundle.json`, `camera_map.geojson`, and `map.html`.
10. Template contract does not contain active Tier 1/Tier 2/Tier 3 camera-discovery overlays.
11. Template contract references `camera_map_bundle.json`.
12. Summarization docs/contract include provider, model, and interval fields.

Fixtures may be small, hand-written, and deterministic. They must not pretend to be real runtime evidence. Use obviously minimal local fixture labels such as `Fixture Camera 1`; do not claim they are real cameras.

---

## Makefile Requirements

Create a small Makefile with at least:

```makefile
test:
	PYTHONPATH=src python -m pytest -q

lint:
	python -m ruff check src tests

typecheck:
	python -m mypy src/camera_discovery_map_ui

compile:
	python -m compileall -q src tests

check: compile test lint typecheck
```

Adjust only if the repository already has equivalent commands.

---

## Verification Commands

Before returning final results, run the most relevant available checks:

```bash
python -m compileall -q src tests
PYTHONPATH=src python -m pytest -q
python -m ruff check src tests
python -m mypy src/camera_discovery_map_ui
```

If a tool is unavailable, report that honestly and run what is available. Do not claim a check passed if it was not run.

---

## Acceptance Criteria

The initial bootstrap is complete when:

1. The repository has a coherent `src/` package named `camera_discovery_map_ui`.
2. `pyproject.toml` exposes `camera-discovery-map-ui` CLI.
3. Root `AGENTS.md` exists and matches the behavioral expectations above.
4. Focused `agents/*.md` files exist and describe ownership boundaries.
5. Documentation explains artifact ingestion, bundle schema, media preview, and future summarization.
6. The project can build a `camera_map_bundle.json` from local directory fixtures.
7. The project can build a `camera_map_bundle.json` from a zip fixture.
8. `camera_map.geojson` contains only records with valid coordinates.
9. CSV-only/unmapped records are preserved in bundle `rows`.
10. `map.html` is copied from the versioned template.
11. Active Tier 1/Tier 2/Tier 3 overlays are not part of the initial camera-discovery map contract.
12. Video summarization is documented as an on-demand future/server-mode action, including interval dropdown and LLM provider/model fields, but is not faked.
13. Tests pass without network access.
14. Final response lists files created/changed and checks run.

---

## Final Response Requirements

When finished, provide:

1. A concise summary of what was created.
2. The input/reference files you found and used.
3. The generated repository tree.
4. Tests/checks run and their results.
5. Any checks that could not be run and why.
6. Any intentionally deferred work, especially:
   - full map-template redesign;
   - on-demand summarization backend;
   - camera-discovery direct integration;
   - browser/video preview edge cases that require live media testing.

Do not overstate completion. If the initial scaffold is functional but the full UI is not complete, say that clearly.
