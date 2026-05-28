from pathlib import Path

from camera_discovery_map_ui.artifacts import load_artifacts
from camera_discovery_map_ui.bundle import build_bundle

FIXTURES = Path(__file__).parent / "fixtures"


def test_bundle_preserves_mapped_and_unmapped_records():
    bundle = build_bundle(load_artifacts(FIXTURES))
    assert bundle["schema_version"] == "camera-discovery-map-bundle/v1"
    assert bundle["summary"]["records_total"] == 3
    assert bundle["summary"]["mapped_records"] == 2
    assert bundle["summary"]["unmapped_records"] == 1
    assert len(bundle["geojson"]["features"]) == 2
    assert len(bundle["rows"]) == 3


def test_bundle_does_not_invent_coordinates_for_csv_only_rows():
    bundle = build_bundle(load_artifacts(FIXTURES))
    csv_rows = [row for row in bundle["rows"] if row["source_artifact"] == "camera_candidates_table.csv"]
    assert len(csv_rows) == 1
    assert csv_rows[0]["has_coordinates"] is False
    assert csv_rows[0]["latitude"] is None
    assert csv_rows[0]["longitude"] is None


def test_bundle_preserves_source_artifact_provenance():
    bundle = build_bundle(load_artifacts(FIXTURES))
    artifacts = {row["source_artifact"] for row in bundle["rows"]}
    assert {"camera.geojson", "untrusted_camera_candidates.geojson", "camera_candidates_table.csv"} <= artifacts
