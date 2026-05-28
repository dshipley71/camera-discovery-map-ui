from pathlib import Path
from zipfile import ZipFile

from camera_discovery_ui.artifacts import load_artifacts

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
