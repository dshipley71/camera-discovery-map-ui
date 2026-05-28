from __future__ import annotations

from collections import Counter
from typing import Any

from camera_discovery_map_ui.artifacts import parse_csv_rows, parse_geojson, parse_jsonl_rows
from camera_discovery_map_ui.normalize import normalize_csv_row, normalize_geojson_feature
from camera_discovery_map_ui.schema import BUNDLE_SCHEMA_VERSION, CSV_ARTIFACTS, GEOJSON_ARTIFACTS, JSONL_ARTIFACTS, ArtifactSet, NormalizedRecord


def _feature_from_record(record: NormalizedRecord) -> dict[str, Any] | None:
    if not record.get("has_coordinates"):
        return None
    lat = record.get("latitude")
    lon = record.get("longitude")
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        return None
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": dict(record),
    }


def _count_by(records: list[NormalizedRecord], key: str) -> dict[str, int]:
    return dict(Counter(str(record.get(key) or "unknown") for record in records))


def _summary(records: list[NormalizedRecord]) -> dict[str, Any]:
    mapped = sum(1 for record in records if record.get("has_coordinates"))
    by_status = Counter(str(record.get("status") or "unknown") for record in records)
    return {
        "records_total": len(records),
        "mapped_records": mapped,
        "unmapped_records": len(records) - mapped,
        "live": by_status.get("live", 0),
        "dead": by_status.get("dead", 0),
        "unknown": by_status.get("unknown", 0),
        "by_record_stage": _count_by(records, "record_stage"),
        "by_media_type": _count_by(records, "media_type"),
        "by_camera_type": _count_by(records, "camera_type"),
        "by_trust_level": _count_by(records, "trust_level"),
        "by_scope_status": _count_by(records, "scope_status"),
    }


def build_bundle(artifact_set: ArtifactSet) -> dict[str, Any]:
    """Build a deterministic camera-discovery map bundle from loaded artifacts."""
    records: list[NormalizedRecord] = []

    for artifact in GEOJSON_ARTIFACTS:
        text = artifact_set.files.get(artifact)
        if text is None:
            continue
        data = parse_geojson(text, artifact)
        for index, feature in enumerate(data.get("features") or []):
            if isinstance(feature, dict):
                records.append(normalize_geojson_feature(feature, artifact, index))

    for artifact in CSV_ARTIFACTS:
        text = artifact_set.files.get(artifact)
        if text is None:
            continue
        for index, row in enumerate(parse_csv_rows(text)):
            records.append(normalize_csv_row(row, artifact, index))

    for artifact in JSONL_ARTIFACTS:
        text = artifact_set.files.get(artifact)
        if text is None:
            continue
        for index, row in enumerate(parse_jsonl_rows(text, artifact)):
            records.append(normalize_csv_row(row, artifact, index))

    features = [feature for record in records if (feature := _feature_from_record(record)) is not None]
    return {
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "source": {
            "input_path": str(artifact_set.input_path),
            "input_type": artifact_set.input_type,
            "artifacts_found": artifact_set.artifacts_found,
        },
        "summary": _summary(records),
        "geojson": {"type": "FeatureCollection", "features": features},
        "rows": records,
    }
