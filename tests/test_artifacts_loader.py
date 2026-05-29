from pathlib import Path
from zipfile import ZipFile

from camera_discovery_map_ui.artifacts import load_artifacts

FIXTURES = Path(__file__).parent / "fixtures"


def test_artifact_loader_reads_directory_fixture():
    artifacts = load_artifacts(FIXTURES)
    assert artifacts.input_type == "directory"
    assert "camera.geojson" in artifacts.files
    assert "untrusted_camera_candidates.geojson" in artifacts.files
    assert "camera_candidates_table.csv" in artifacts.files


def test_artifact_loader_reads_zip_fixture(tmp_path):
    zip_path = tmp_path / "review_artifacts.zip"
    with ZipFile(zip_path, "w") as zf:
        for path in FIXTURES.iterdir():
            if path.is_file() and path.name != "README.md":
                zf.write(path, arcname=f"review/{path.name}")
    artifacts = load_artifacts(zip_path)
    assert artifacts.input_type == "zip"
    assert set(artifacts.files) >= {"camera.geojson", "untrusted_camera_candidates.geojson", "camera_candidates_table.csv"}


def test_load_single_geojson_file(tmp_path):
    source = tmp_path / "my_cameras.geojson"
    source.write_text(
        '{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[-75.0,40.0]},"properties":{"name":"Single File Camera"}}]}',
        encoding="utf-8",
    )

    artifacts = load_artifacts(source)

    assert artifacts.input_type == "geojson"
    assert artifacts.artifacts_found == ["camera.geojson"]
    assert "Single File Camera" in artifacts.files["camera.geojson"]


def test_load_single_untrusted_geojson_file(tmp_path):
    source = tmp_path / "untrusted_camera_candidates.geojson"
    source.write_text('{"type":"FeatureCollection","features":[]}', encoding="utf-8")

    artifacts = load_artifacts(source)

    assert artifacts.input_type == "geojson"
    assert artifacts.artifacts_found == ["untrusted_camera_candidates.geojson"]
