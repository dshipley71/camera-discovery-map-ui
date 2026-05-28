# Summarization Contract

Video summarization is a future optional server-mode capability. The static map may display controls, but it must not fake summaries.

## Popup controls

The popup should provide:

```text
Video Summary
Interval: [15s | 30s | 60s | 120s | 240s | 300s]
[Summarize Video]
```

In static mode, the button is disabled with an explanatory message unless a summarization endpoint is configured.

## Required summary record fields

```text
summary_id
camera_id
stream_url_hash
summarized_at
sample_window_seconds
frames_sampled
media_type
summarizer.provider
summarizer.model
summarizer.model_role
summarizer.prompt_version
summarizer.code_version
summary
observations
warnings
status
cached
error
```

## Cache key inputs

A safe cache key should include:

```text
camera_id
stream_url_hash
sample_window_seconds
frame sampling profile
summarizer provider
summarizer model
prompt version
summarizer code version
```

Do not return canned summaries or fake LLM output.
