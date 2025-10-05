# 🎵 Real-time AI Lyrics Summarizer & Mood Classifier

A web app to summarize lyrics, classify mood/emotion, and recommend similar songs using AI and Spotify.

## Features
- Accepts pasted lyrics, uploaded audio (transcribed via Whisper), or YouTube URL (transcript).
- Summarizes lyrics (~120 words) using Hugging Face transformers.
- Classifies mood/emotion (happy/chill/sad) using multilingual sentiment.
- Optional Spotify recommendations based on mood.
- Sleek, single-page Streamlit UI.
- Container-ready (Dockerfile included).

## Multilingual support
We auto-detect language, translate to English with MarianMT, then summarize; mood uses a small multilingual sentiment model for speed and disk usage.

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # leave keys empty for base flow
streamlit run app.py
```

## Optional Features
- **Audio transcription**: Set `OPENAI_API_KEY` in `.env` to enable Whisper API for audio uploads.
- **Spotify recommendations**: Set `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` in `.env` for song recommendations.

## Docker
```bash
docker build -t lyrics-mood-ai .
docker run -p 8501:8501 --env-file .env lyrics-mood-ai
```

## Notes
- YouTube transcripts may be unavailable for some videos.
- All failures are handled gracefully with warnings/info.
- Copyright: Transcripts and lyrics are for personal/educational use only.

## CI
Minimal GitHub Actions workflow checks install and imports.