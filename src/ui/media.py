from __future__ import annotations

from urllib.parse import urlparse

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")
VIDEO_EXTENSIONS = {
    ".mp4": "mp4",
    ".webm": "webm",
    ".ogv": "ogg",
    ".ogg": "ogg",
}
MJPEG_EXTENSIONS = (".mjpg", ".mjpeg")
HLS_EXTENSIONS = (".m3u8",)
WEB_EMBED_TYPES = {"web", "embed", "iframe", "web_embed", "html"}

MEDIA_ALIASES = {
    "hls": "hls",
    "m3u8": "hls",
    "application/vnd.apple.mpegurl": "hls",
    "application/x-mpegurl": "hls",
    "mp4": "mp4",
    "video/mp4": "mp4",
    "webm": "webm",
    "video/webm": "webm",
    "ogg": "ogg",
    "ogv": "ogg",
    "video/ogg": "ogg",
    "mjpeg": "mjpeg",
    "mjpg": "mjpeg",
    "multipart/x-mixed-replace": "mjpeg",
    "image_snapshot": "image_snapshot",
    "image": "image_snapshot",
    "snapshot": "image_snapshot",
    "jpg": "image_snapshot",
    "jpeg": "image_snapshot",
    "png": "image_snapshot",
    "webp": "image_snapshot",
    "gif": "image_snapshot",
    "web_embed": "web_embed",
    "iframe": "web_embed",
    "embed": "web_embed",
}


def _clean_declared(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip().lower()
    return cleaned or None


def _url_path(url: str | None) -> str:
    if not url:
        return ""
    parsed = urlparse(url.strip())
    return (parsed.path or "").lower()


def detect_media_type(url: str | None, declared_type: str | None = None) -> str:
    """Detect a generic media type from an optional declared type and URL.

    The function is local/deterministic and performs no network access.
    """
    declared = _clean_declared(declared_type)
    if declared in MEDIA_ALIASES:
        return MEDIA_ALIASES[declared]

    path = _url_path(url)
    if path.endswith(HLS_EXTENSIONS):
        return "hls"
    for extension, media_type in VIDEO_EXTENSIONS.items():
        if path.endswith(extension):
            return media_type
    if path.endswith(MJPEG_EXTENSIONS):
        return "mjpeg"
    if path.endswith(IMAGE_EXTENSIONS):
        return "image_snapshot"
    if declared in WEB_EMBED_TYPES:
        return "web_embed"
    if url and not path:
        return "web_embed"
    if path.endswith((".html", "/")) and declared in {None, "page"}:
        return "web_embed"
    return "unknown"


def preview_capability(media_type: str) -> str:
    normalized = (media_type or "unknown").strip().lower()
    if normalized == "hls":
        return "hls_video"
    if normalized in {"mp4", "webm", "ogg"}:
        return "native_video"
    if normalized == "mjpeg":
        return "mjpeg_image"
    if normalized == "image_snapshot":
        return "refreshing_image"
    if normalized == "web_embed":
        return "iframe_or_link"
    return "metadata_only"


def asset_role_for_media(media_type: str) -> str:
    return {
        "hls": "hls_stream",
        "mp4": "video_file",
        "webm": "video_file",
        "ogg": "video_file",
        "mjpeg": "mjpeg_stream",
        "image_snapshot": "image_snapshot",
        "web_embed": "web_embed",
    }.get(media_type, "unknown_media")
