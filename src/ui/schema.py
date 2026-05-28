from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, TypedDict

BUNDLE_SCHEMA_VERSION = "camera-discovery-map-bundle/v1"
RECORD_SCHEMA_VERSION = "camera-map-record/v1"

GEOJSON_ARTIFACTS = (
    "camera.geojson",
    "untrusted_camera_candidates.geojson",
    "untrusted_camera.geojson",
    "harvest_unvalidated.geojson",
    "harvest_untrusted.geojson",
    "harvest_geocoded.geojson",
)

CSV_ARTIFACTS = (
    "camera_candidates_table.csv",
    "harvest_records.csv",
)

JSONL_ARTIFACTS = (
    "harvest_records.jsonl",
)

SUMMARY_ARTIFACTS = (
    "harvest_summary.json",
    "logs/output_summary.json",
    "logs/run_explanation.json",
    "logs/target_resolution_all.json",
)

KNOWN_ARTIFACTS = GEOJSON_ARTIFACTS + CSV_ARTIFACTS + JSONL_ARTIFACTS + SUMMARY_ARTIFACTS

STATUS_VALUES = ("live", "dead", "unknown")
MEDIA_TYPES = ("hls", "mp4", "webm", "ogg", "mjpeg", "image_snapshot", "web_embed", "unknown")
PREVIEW_CAPABILITIES = ("hls_video", "native_video", "mjpeg_image", "refreshing_image", "iframe_or_link", "metadata_only")

InputType = Literal["directory", "zip"]


class NormalizedRecord(TypedDict, total=False):
    schema_version: str
    record_id: str
    record_stage: str
    label: str | None
    location_label: str | None
    target_label: str | None
    latitude: float | None
    longitude: float | None
    has_coordinates: bool
    coordinate_source: str
    coordinate_confidence: float | None
    status: str
    validation_status: str | None
    trust_level: str
    scope_status: str
    review_required: bool
    camera_type: str
    raw_camera_type: str | None
    media_type: str
    asset_role: str
    stream_url: str | None
    snapshot_url: str | None
    thumbnail_url: str | None
    source_url: str | None
    json_endpoint_url: str | None
    summarization: dict[str, Any]
    metadata: dict[str, Any]
    source_artifact: str


@dataclass(frozen=True)
class ArtifactSet:
    input_path: Path
    input_type: InputType
    files: dict[str, str]

    @property
    def artifacts_found(self) -> list[str]:
        return sorted(self.files)


@dataclass(frozen=True)
class MapBuildResult:
    output_dir: Path
    bundle_path: Path
    geojson_path: Path
    map_html_path: Path
    summary: dict[str, Any]
