from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path

from camera_discovery_map_ui.artifacts import load_artifacts
from camera_discovery_map_ui.bundle import build_bundle
from camera_discovery_map_ui.schema import MapBuildResult


class CameraDiscoveryMapAgent:
    """Facade for building static map-review artifacts from camera-discovery outputs."""

    def __init__(self, input_path: str | Path, output_dir: str | Path) -> None:
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)

    def run(self) -> MapBuildResult:
        artifact_set = load_artifacts(self.input_path)
        bundle = build_bundle(artifact_set)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        bundle_path = self.output_dir / "camera_map_bundle.json"
        geojson_path = self.output_dir / "camera_map.geojson"
        map_html_path = self.output_dir / "map.html"

        bundle_path.write_text(json.dumps(bundle, indent=2, sort_keys=True), encoding="utf-8")
        geojson_path.write_text(json.dumps(bundle["geojson"], indent=2, sort_keys=True), encoding="utf-8")
        map_html_path.write_text(_template_text(), encoding="utf-8")

        return MapBuildResult(
            output_dir=self.output_dir,
            bundle_path=bundle_path,
            geojson_path=geojson_path,
            map_html_path=map_html_path,
            summary=bundle["summary"],
        )


def _template_text() -> str:
    template = files("camera_discovery_map_ui").joinpath("templates/map_template.html")
    return template.read_text(encoding="utf-8")
