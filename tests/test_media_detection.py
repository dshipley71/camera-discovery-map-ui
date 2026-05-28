from camera_discovery_ui.media import detect_media_type, preview_capability


def test_media_detection_supported_types():
    assert detect_media_type("https://fixture.invalid/live.m3u8") == "hls"
    assert detect_media_type("https://fixture.invalid/video.mp4") == "mp4"
    assert detect_media_type("https://fixture.invalid/video.webm") == "webm"
    assert detect_media_type("https://fixture.invalid/video.ogv") == "ogg"
    assert detect_media_type("https://fixture.invalid/live.mjpeg") == "mjpeg"
    assert detect_media_type("https://fixture.invalid/snapshot.jpg") == "image_snapshot"
    assert detect_media_type("https://fixture.invalid/player", "iframe") == "web_embed"
    assert detect_media_type("https://fixture.invalid/no-extension") == "unknown"


def test_preview_capabilities():
    assert preview_capability("hls") == "hls_video"
    assert preview_capability("mp4") == "native_video"
    assert preview_capability("mjpeg") == "mjpeg_image"
    assert preview_capability("image_snapshot") == "refreshing_image"
    assert preview_capability("web_embed") == "iframe_or_link"
    assert preview_capability("unknown") == "metadata_only"
