# Artifact Contract

`camera-discovery-map-ui` consumes artifacts written by `camera-discovery`. It does not redefine upstream artifact meaning.

## Supported input artifact names

```text
camera.geojson
untrusted_camera_candidates.geojson
untrusted_camera.geojson
camera_candidates_table.csv
harvest_unvalidated.geojson
harvest_untrusted.geojson
harvest_geocoded.geojson
harvest_records.jsonl
harvest_records.csv
harvest_summary.json
logs/output_summary.json
logs/run_explanation.json
logs/target_resolution_all.json
```

Inputs may be provided as a directory or as a ZIP file such as `review_artifacts.zip` or `artifacts.zip`.

## Bundle schema

The generated bundle uses:

```text
schema_version: camera-discovery-map-bundle/v1
```

Top-level shape:

```json
{
  "schema_version": "camera-discovery-map-bundle/v1",
  "source": {
    "input_path": "...",
    "input_type": "directory|zip",
    "artifacts_found": []
  },
  "summary": {
    "records_total": 0,
    "mapped_records": 0,
    "unmapped_records": 0,
    "live": 0,
    "dead": 0,
    "unknown": 0,
    "by_record_stage": {},
    "by_media_type": {},
    "by_camera_type": {},
    "by_trust_level": {},
    "by_scope_status": {}
  },
  "geojson": {"type": "FeatureCollection", "features": []},
  "rows": []
}
```

## Record stages

Recommended normalized stages:

```text
trusted      # records from trusted camera output
candidate    # review/untrusted validation candidates
harvested    # future harvested/unvalidated records
unknown      # source did not provide enough lifecycle context
```

## Mapped vs unmapped

- Mapped records have valid numeric latitude/longitude and appear in `geojson.features`.
- Unmapped records stay in `rows` and should still be available for table review.
- The normalizer must not invent coordinates.

## Trust and provenance

Every normalized row includes `source_artifact`. Trust should only be set to `trusted` when the source artifact or explicit fields support that state.

## Status normalization

Detailed upstream statuses are preserved in `validation_status`. The simplified UI status is one of:

```text
live
dead
unknown
```

## Camera type vs media type

`camera_type` describes what the camera is about, such as traffic or weather. `media_type` describes the asset format, such as HLS, MP4, MJPEG, image snapshot, or web embed.
