# camera-discovery-map-ui

`camera-discovery-map-ui` is a standalone static-review scaffold for artifacts produced by the `camera-discovery` project. It consumes a review artifact directory or ZIP and writes a deterministic map bundle that can be rendered by a Leaflet-based `map.html`.

This repository intentionally does **not** make `camera-discovery` a Python dependency. The interface between the projects is the artifact bundle contract documented in `docs/artifact_contract.md`.

## Current capabilities

- Load a camera-discovery artifact directory or ZIP.
- Read known GeoJSON and CSV artifact files.
- Normalize trusted, untrusted, and future harvested records into `camera-discovery-map-bundle/v1`.
- Preserve unmapped rows for table review while writing only coordinate-bearing records to `camera_map.geojson`.
- Copy a contract-focused dark Leaflet map template to `map.html`.
- Classify media types without network access.
- Document future on-demand video summarization without faking summaries.


## Colab notebook

A Colab-ready notebook is included at:

```text
notebooks/camera_discovery_map_ui_colab.ipynb
```

The notebook installs the package, builds the sample fixture map, displays `map.html` through a local Colab HTTP server, accepts an uploaded camera-discovery artifact ZIP, and downloads the generated review-map output.

## CLI

```bash
camera-discovery-map-ui inspect --input review_artifacts.zip
camera-discovery-map-ui build --input review_artifacts.zip --output-dir review-map
```

The build command writes:

```text
camera_map_bundle.json
camera_map.geojson
map.html
```

## Development checks

```bash
python -m compileall -q src tests
PYTHONPATH=src python -m pytest -q
python -m ruff check src tests
python -m mypy src/camera_discovery_map_ui
```

`ruff` and `mypy` are development extras and may need to be installed with `pip install -e .[dev]`.

## Deferred work

This initial scaffold does not implement the full UI redesign, live-media validation, live geocoding, a local review server, or actual video summarization. Those are intentionally documented as future phases.
