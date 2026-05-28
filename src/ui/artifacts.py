from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path
from typing import Any

from camera_discovery_map_ui.schema import ArtifactSet, KNOWN_ARTIFACTS


def load_artifacts(input_path: str | Path) -> ArtifactSet:
    """Load known camera-discovery artifacts from a directory or ZIP file."""
    path = Path(input_path)
    if path.is_dir():
        return _load_from_directory(path)
    if path.is_file() and path.suffix.lower() == ".zip":
        return _load_from_zip(path)
    raise FileNotFoundError(f"Input must be an artifact directory or .zip file: {path}")


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
