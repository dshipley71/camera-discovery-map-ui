# Summarization Agent

Owns the future on-demand video summarization contract.

Rules:

- Summarization must be user-triggered from a popup control.
- Static mode must not fake summaries.
- Summary records must include provider, model, prompt version, code version, interval, frames sampled, cache status, warnings, and errors.
- Cache keys must include camera identity, media URL hash, interval, frame sampling profile, provider, model, prompt version, and code version.
