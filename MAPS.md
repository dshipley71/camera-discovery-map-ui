# MAPS.md

The map UI is a downstream review surface for camera-discovery artifacts. The current template is a contract-focused dark Leaflet page that loads `camera_map_bundle.json` when served over HTTP and also supports manual JSON/GeoJSON file loading.

## Current map contract

- `camera_map_bundle.json` is the preferred input.
- `camera_map.geojson` contains only mapped records with valid coordinates.
- `rows` inside the bundle may include unmapped CSV-only records for table review.
- Marker status uses the simple normalized values `live`, `dead`, and `unknown`.
- Detailed validation status remains available in popup/table metadata.
- Camera type and media type are separate fields.

## Media preview direction

The UI contract supports HLS, native video files, MJPEG, image snapshots, thumbnails, web embeds, and unknown media. The initial static page does not validate media and does not treat preview failure as validation failure.

## Summarization direction

Video summarization is future optional server-mode behavior. The static page shows the summarization controls as disabled unless a backend endpoint is configured.
