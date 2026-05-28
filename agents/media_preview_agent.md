# Media Preview Agent

Owns generic media classification and browser preview behavior documentation.

Rules:

- Classify media without network access.
- Support HLS, MP4, WebM, OGG/OGV, MJPEG, image snapshots, web embeds, and unknown media.
- Preview failure is not validation failure.
- Do not add source-specific URL hacks.
