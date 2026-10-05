# Faceless YouTube Pipeline

Four channels, one daily automated pipeline, entirely free tools.

- `channels/` — one file per channel: where its topic comes from and its writing style
- `common/` — the shared steps every channel uses: script, voice, visuals, video, upload
- `data/used_topics.json` — tracks what's already been covered, so nothing repeats
- `.github/workflows/daily_pipeline.yml` — runs the whole thing at 6 AM daily
