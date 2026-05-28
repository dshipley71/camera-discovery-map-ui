import json
from pathlib import Path

from typer.testing import CliRunner

from camera_discovery_ui.cli import app

FIXTURES = Path(__file__).parent / "fixtures"
runner = CliRunner()


def test_cli_build_writes_expected_outputs(tmp_path):
    result = runner.invoke(app, ["build", "--input", str(FIXTURES), "--output-dir", str(tmp_path)])
    assert result.exit_code == 0, result.output
    bundle_path = tmp_path / "camera_map_bundle.json"
    geojson_path = tmp_path / "camera_map.geojson"
    map_path = tmp_path / "map.html"
    assert bundle_path.exists()
    assert geojson_path.exists()
    assert map_path.exists()
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    geojson = json.loads(geojson_path.read_text(encoding="utf-8"))
    assert bundle["summary"]["records_total"] == 3
    assert len(geojson["features"]) == 2


def test_cli_inspect_reports_artifacts():
    result = runner.invoke(app, ["inspect", "--input", str(FIXTURES)])
    assert result.exit_code == 0, result.output
    assert "camera.geojson" in result.output
    assert "records_total" in result.output
