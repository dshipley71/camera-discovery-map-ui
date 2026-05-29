from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path
from typing import Any

from camera_discovery_map_ui.schema import ArtifactSet, KNOWN_ARTIFACTS


def load_artifacts(input_path: str | Path) -> ArtifactSet:
    """Load camera-discovery map inputs from a directory, ZIP, or single data file.

    Direct single-file input is useful during UI development and analyst review when a
    user only has one GeoJSON/CSV/JSONL artifact instead of a full camera-discovery
    artifact bundle. Single GeoJSON/JSON files are treated as camera GeoJSON unless
    their filename clearly indicates an untrusted or harvest artifact.
    """
    path = Path(input_path)
    if path.is_dir():
        return _load_from_directory(path)
    if path.is_file() and path.suffix.lower() == ".zip":
        return _load_from_zip(path)
    if path.is_file():
        return _load_from_file(path)
    raise FileNotFoundError(f"Input must be an artifact directory, .zip file, or supported data file: {path}")


def _artifact_key_for_file(path: Path) -> str | None:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if suffix in {".geojson", ".json"}:
        if "harvest" in name and "geocoded" in name:
            return "harvest_geocoded.geojson"
        if "harvest" in name and "untrusted" in name:
            return "harvest_untrusted.geojson"
        if "harvest" in name:
            return "harvest_unvalidated.geojson"
        if "untrusted" in name or "candidate" in name:
            return "untrusted_camera_candidates.geojson"
        return "camera.geojson"
    if suffix == ".csv":
        if "harvest" in name:
            return "harvest_records.csv"
        return "camera_candidates_table.csv"
    if suffix == ".jsonl":
        return "harvest_records.jsonl"
    return None


def _load_from_file(path: Path) -> ArtifactSet:
    key = _artifact_key_for_file(path)
    if key is None:
        raise FileNotFoundError(f"Unsupported input file type: {path}")
    input_type = path.suffix.lower().lstrip(".") or "file"
    return ArtifactSet(input_path=path, input_type=input_type, files={key: path.read_text(encoding="utf-8")})


def _load_from_directory(path: Path) -> ArtifactSet:
    files: dict[str, str] = {}
    for artifact in KNOWN_ARTIFACTS:
        candidate = path / artifact
        if candidate.exists() and candidate.is_file():
            files[artifact] = candidate.read_text(encoding="utf-8")
    return ArtifactSet(input_path=path, input_type="directory", files=files)


def _safe_zip_name(name: str) -> str:
    return name.replace("\\", "/").lstrip("/")


def _artifact_key_for_zip_member(name: str) -> str | None:
    safe = _safe_zip_name(name)
    parts = safe.split("/")
    for artifact in KNOWN_ARTIFACTS:
        artifact_parts = artifact.split("/")
        if parts[-len(artifact_parts) :] == artifact_parts:
            return artifact
    return None


def _load_from_zip(path: Path) -> ArtifactSet:
    files: dict[str, str] = {}
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            key = _artifact_key_for_zip_member(info.filename)
            if key is None or key in files:
                continue
            with zf.open(info) as fh:
                files[key] = fh.read().decode("utf-8")
    return ArtifactSet(input_path=path, input_type="zip", files=files)


def parse_json_object(text: str, source: str) -> dict[str, Any]:
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {source}")
    return data


def parse_geojson(text: str, source: str) -> dict[str, Any]:
    data = parse_json_object(text, source)
    features = data.get("features")
    if features is None:
        data["features"] = []
    elif not isinstance(features, list):
        raise ValueError(f"GeoJSON features must be a list in {source}")
    return data


def parse_csv_rows(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


def parse_jsonl_rows(text: str, source: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        data = json.loads(stripped)
        if not isinstance(data, dict):
            raise ValueError(f"Expected JSON object at {source}:{line_number}")
        rows.append(data)
    return rows
