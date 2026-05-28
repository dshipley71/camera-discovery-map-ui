# Project Structure

The package is organized around thin CLI commands and focused modules:

```text
src/camera_discovery_map_ui/
  cli.py          # Typer command declarations only
  artifacts.py    # artifact discovery/loading for directories and ZIPs
  normalize.py    # record normalization from GeoJSON/CSV to bundle rows
  status.py       # validation status normalization
  media.py        # media-type detection and preview capability classification
  bundle.py       # deterministic bundle/GeoJSON generation
  agent.py        # public service/facade class
  schema.py       # schema constants and result dataclasses
  templates/      # map template
```

No notebook-specific code belongs under `src/`.
