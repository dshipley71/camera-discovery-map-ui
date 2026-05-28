# Media Preview Contract

Media classification is deterministic and local. It does not perform network access.

## Preview rules

```text
HLS .m3u8 -> hls.js + video element
MP4/WebM/OGG -> native video element
MJPEG -> img stream where browser permits
image snapshot -> refreshing img with cache-busting
thumbnail -> still preview
web embed -> optional iframe/fallback link
unknown -> metadata + open-link buttons
```

Browser preview can fail because of CORS, authentication, mixed content, redirects, unavailable codecs, or endpoint behavior. Preview failure is not validation failure and must not mark a camera dead.

## Supported media classes

```text
hls
mp4
webm
ogg
mjpeg
image_snapshot
web_embed
unknown
```
