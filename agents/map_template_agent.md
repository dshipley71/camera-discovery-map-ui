# Map Template Agent

Owns `templates/map_template.html`, map/table layout, popup metadata, and static-mode browser behavior.

Rules:

- Keep the polished dark Leaflet review-console direction.
- Do not include active hard-coded global geography overlays in the camera-discovery contract.
- Load `camera_map_bundle.json` when available.
- Explain disabled summarization behavior in static mode.
- Do not claim final preview or summarization behavior is complete until implemented and tested.
