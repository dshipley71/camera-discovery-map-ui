from __future__ import annotations

LIVE_STATUSES = {
    "active_live_unknown",
    "active_live_verified",
    "active_image_snapshot_refreshing",
    "active_image_snapshot_static_unverified",
    "active_live_static_view",
    "active_live_dynamic",
    "active_prerecorded_loop_short",
    "active_prerecorded_loop_long",
}

DEAD_STATUSES = {
    "dead_link",
    "offline_http",
    "restricted_http",
    "active_playlist_dead_segments",
    "static_image_asset",
    "image_snapshot_not_image",
    "decode_failed",
}

UNKNOWN_STATUSES = {"", "not_validated", "unknown", "review", "none", "null"}


def normalize_status(validation_status: str | None) -> str:
    """Collapse a detailed camera-discovery validation status into live/dead/unknown."""
    if validation_status is None:
        return "unknown"
    normalized = str(validation_status).strip().lower()
    if normalized in LIVE_STATUSES:
        return "live"
    if normalized in DEAD_STATUSES:
        return "dead"
    if normalized in UNKNOWN_STATUSES:
        return "unknown"
    return "unknown"
