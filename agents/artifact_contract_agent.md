# Artifact Contract Agent

Owns artifact discovery, loading, source provenance, and the normalized bundle contract.

Rules:

- Preserve upstream artifact meanings.
- Do not invent coordinates or trust decisions.
- Preserve source artifact provenance on every normalized record.
- Keep mapped GeoJSON records separate from unmapped table rows.
- Support both directory and ZIP inputs without extracting arbitrary paths.
