from __future__ import annotations

import hashlib
from typing import Any

from camera_discovery_map_ui.media import asset_role_for_media, detect_media_type
from camera_discovery_map_ui.schema import RECORD_SCHEMA_VERSION, NormalizedRecord
from camera_discovery_map_ui.status import normalize_status

THUMBNAIL_KEYS = (
    "thumbnail_url",
    "snapshot_url",
    "image_url",
    "camera_image_url",
    "preview_image_url",
    "poster_url",
)


def _first_text(mapping: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = mapping.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    metadata = mapping.get("source_metadata")
    if isinstance(metadata, dict):
        for key in keys:
            value = metadata.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def _first_value(mapping: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = mapping.get(key)
        if value not in (None, ""):
            return value
    metadata = mapping.get("source_metadata")
    if isinstance(metadata, dict):
        for key in keys:
            value = metadata.get(key)
            if value not in (None, ""):
                return value
    return None


def _as_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _valid_lat_lon(latitude: float | None, longitude: float | None) -> bool:
    return latitude is not None and longitude is not None and -90 <= latitude <= 90 and -180 <= longitude <= 180


def _coordinates_from_feature(feature: dict[str, Any]) -> tuple[float | None, float | None]:
    props = feature.get("properties") if isinstance(feature.get("properties"), dict) else {}
    lat = _as_float(_first_value(props, "lat", "latitude"))
    lon = _as_float(_first_value(props, "lon", "lng", "longitude"))
    if _valid_lat_lon(lat, lon):
        return lat, lon
    geometry = feature.get("geometry") if isinstance(feature.get("geometry"), dict) else {}
    coordinates = geometry.get("coordinates") if isinstance(geometry, dict) else None
    if isinstance(coordinates, (list, tuple)) and len(coordinates) >= 2:
        lon = _as_float(coordinates[0])
        lat = _as_float(coordinates[1])
    return lat, lon


def _source_stage(source_artifact: str) -> str:
    if source_artifact == "camera.geojson":
        return "trusted"
    if source_artifact.startswith("harvest_") or source_artifact.startswith("harvest_records"):
        return "harvested"
    if source_artifact.startswith("untrusted") or source_artifact == "camera_candidates_table.csv":
        return "candidate"
    return "unknown"


def _trust_level(source_artifact: str, props: dict[str, Any]) -> str:
    explicit = _first_text(props, "trust_level", "output_policy")
    if explicit:
        return explicit.lower()
    if source_artifact == "camera.geojson":
        return "trusted"
    if source_artifact.startswith("untrusted") or source_artifact == "camera_candidates_table.csv":
        return "untrusted"
    return "unknown"


def find_thumbnail_url(properties: dict[str, Any]) -> str | None:
    for key in THUMBNAIL_KEYS:
        value = _first_text(properties, key)
        if value and value.startswith(("http://", "https://", "data:")):
            return value
    return None


def normalize_camera_type(properties: dict[str, Any]) -> tuple[str, str | None]:
    raw = _first_text(properties, "camera_type", "raw_camera_type", "type", "category")
    if not raw:
        return "unknown", None
    lowered = raw.strip().lower()
    if "traffic" in lowered:
        return "traffic", raw
    if "weather" in lowered:
        return "weather", raw
    if "transit" in lowered or "rail" in lowered or "bus" in lowered:
        return "transit", raw
    if "public" in lowered or "webcam" in lowered:
        return "public", raw
    return lowered.replace(" ", "_"), raw


def _record_id(source_artifact: str, index: int, props: dict[str, Any]) -> str:
    explicit = _first_text(props, "record_id", "camera_id", "id")
    basis = "|".join(
        str(part or "")
        for part in (
            source_artifact,
            explicit,
            _first_text(props, "stream_url", "url", "media_url"),
            _first_text(props, "source_url"),
            index,
        )
    )
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:24]


def _base_record(source_artifact: str, index: int, props: dict[str, Any], lat: float | None, lon: float | None) -> NormalizedRecord:
    declared_media = _first_text(props, "media_type", "asset_type", "content_type")
    stream_url = _first_text(props, "stream_url", "media_url", "url", "hls_url", "video_url")
    snapshot_url = _first_text(props, "snapshot_url", "image_url", "camera_image_url")
    media_url_for_detection = stream_url or snapshot_url or _first_text(props, "thumbnail_url", "source_url")
    media_type = detect_media_type(media_url_for_detection, declared_media)
    validation_status = _first_text(props, "validation_status", "camera_status", "status")
    camera_type, raw_camera_type = normalize_camera_type(props)
    has_coordinates = _valid_lat_lon(lat, lon)
    coordinate_source = _first_text(props, "coordinate_source", "bbox_source", "geocode_source") or ("source" if has_coordinates else "unknown")
    return {
        "schema_version": RECORD_SCHEMA_VERSION,
        "record_id": _record_id(source_artifact, index, props),
        "record_stage": _source_stage(source_artifact),
        "label": _first_text(props, "name", "title", "camera_name", "source_name") or f"Record {index + 1}",
        "location_label": _first_text(props, "location_display", "location_text", "geocoded_display_name", "source_scope_hint"),
        "target_label": _first_text(props, "target_label", "target_id"),
        "latitude": lat if has_coordinates else None,
        "longitude": lon if has_coordinates else None,
        "has_coordinates": has_coordinates,
        "coordinate_source": coordinate_source,
        "coordinate_confidence": _as_float(_first_value(props, "coordinate_confidence", "geocode_confidence")),
        "status": normalize_status(validation_status),
        "validation_status": validation_status,
        "trust_level": _trust_level(source_artifact, props),
        "scope_status": (_first_text(props, "scope_status") or "unknown").lower(),
        "review_required": bool(_first_value(props, "review_required")) if _first_value(props, "review_required") is not None else False,
        "camera_type": camera_type,
        "raw_camera_type": raw_camera_type,
        "media_type": media_type,
        "asset_role": asset_role_for_media(media_type),
        "stream_url": stream_url,
        "snapshot_url": snapshot_url,
        "thumbnail_url": find_thumbnail_url(props),
        "source_url": _first_text(props, "source_url", "page_url"),
        "json_endpoint_url": _first_text(props, "json_endpoint_url", "endpoint_url"),
        "summarization": {
            "available": media_type in {"hls", "mp4", "webm", "ogg", "mjpeg"},
            "status": "not_requested",
            "last_summary_id": None,
        },
        "metadata": dict(props),
        "source_artifact": source_artifact,
    }


def normalize_geojson_feature(feature: dict[str, Any], source_artifact: str, index: int) -> NormalizedRecord:
    props = feature.get("properties") if isinstance(feature.get("properties"), dict) else {}
    lat, lon = _coordinates_from_feature(feature)
    return _base_record(source_artifact, index, dict(props), lat, lon)


def normalize_csv_row(row: dict[str, Any], source_artifact: str, index: int) -> NormalizedRecord:
    props = dict(row)
    lat = _as_float(_first_value(props, "lat", "latitude"))
    lon = _as_float(_first_value(props, "lon", "lng", "longitude"))
    return _base_record(source_artifact, index, props, lat, lon)
