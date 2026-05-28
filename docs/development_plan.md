# Development Plan

## Phase 1 — Scaffold and artifact contract

- Create package structure, docs, agents, CLI, deterministic artifact loader, normalizer, bundle builder, and tests.
- Consume directories and ZIP files.
- Write `camera_map_bundle.json`, `camera_map.geojson`, and `map.html`.

## Phase 2 — Full map template alignment

- Evolve the template into the final review console.
- Add richer filters, popup metadata, media preview behavior, and table ergonomics.
- Keep source-provided and LLM-inferred coordinates visually distinct.

## Phase 3 — Optional review server

- Add a local server only when needed for on-demand summarization and browser-friendly artifact serving.
- Do not make static review mode depend on the server.

## Phase 4 — On-demand video summarization

- Add popup-driven summarization with interval selection.
- Cache summaries by stream/model/interval/prompt/code version.
- Record LLM provider and model in every summary.

## Skills markdown decision

No custom skills markdown files are required for the initial scaffold. The repository uses `AGENTS.md` and focused `agents/*.md` files.
