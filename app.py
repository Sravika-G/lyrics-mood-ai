import os
import streamlit as st
from services.summarizer import summarize_lyrics
from services.mood_classifier import classify_mood
from services.transcribe import transcribe_audio, fetch_youtube_transcript
from services.recommender import recommend_tracks

st.set_page_config(page_title="🎵 Real-time AI Lyrics Summarizer & Mood Classifier", layout="centered")
st.title("🎵 Real-time AI Lyrics Summarizer & Mood Classifier")

with st.expander("Input Options", expanded=True):
    input_mode = st.radio("Select input type:", ["Paste lyrics", "Upload audio (transcribe)", "YouTube URL transcript"])
    lyrics = ""
    if input_mode == "Paste lyrics":
        lyrics = st.text_area("Paste lyrics here:", height=250)
    elif input_mode == "Upload audio (transcribe)":
        audio_file = st.file_uploader("Upload audio file (mp3/wav/m4a):", type=["mp3", "wav", "m4a"])
        if not os.getenv("OPENAI_API_KEY"):
            st.info("Audio transcription requires OPENAI_API_KEY. Skipping transcription.")
        elif audio_file:
            try:
                with st.spinner("Transcribing audio..."):
                    lyrics = transcribe_audio(audio_file)
                if not lyrics:
                    st.warning("Transcription failed or returned empty.")
            except Exception:
                st.error("Audio transcription failed.")
    elif input_mode == "YouTube URL transcript":
        yt_url = st.text_input("Enter YouTube URL:")
        if yt_url:
            try:
                with st.spinner("Fetching YouTube transcript..."):
                    lyrics = fetch_youtube_transcript(yt_url)
                if not lyrics:
                    st.info("Transcript unavailable for this video.")
            except Exception:
                st.error("Transcript fetch failed.")

run_summary = st.checkbox("Generate summary", value=True)
run_mood = st.checkbox("Classify mood", value=True)
show_recs = st.checkbox("Recommend similar songs (Spotify)", value=False)

if st.button("Run"):
    if not lyrics or not lyrics.strip():
        st.warning("No lyrics or transcript provided.")
    else:
        st.subheader("Lyrics / Transcript Preview")
        preview = lyrics[:400] + ("..." if len(lyrics) > 400 else "")
        st.text_area("Preview", preview, height=120)
        if run_summary:
            try:
                with st.spinner("Summarizing lyrics..."):
                    summary = summarize_lyrics(lyrics)
                st.subheader("AI Summary")
                st.write(summary)
            except Exception:
                st.error("Summarization failed.")
        if run_mood:
            try:
                with st.spinner("Classifying mood..."):
                    mood, scores = classify_mood(lyrics)
                st.subheader("Mood / Emotion")
                st.metric("Mood", mood)
                st.write("Scores:", scores)
                if show_recs and mood in ["happy/energetic", "chill/reflective", "sad/melancholic"]:
                    if os.getenv("SPOTIFY_CLIENT_ID") and os.getenv("SPOTIFY_CLIENT_SECRET"):
                        try:
                            with st.spinner("Fetching Spotify recommendations..."):
                                tracks = recommend_tracks(mood)
                            if tracks:
                                st.subheader("Spotify Recommendations")
                                for t in tracks:
                                    st.markdown(f"[{t['name']} — {t['artist']}]({t['url']})")
                            else:
                                st.info("No recommendations found.")
                        except Exception:
                            st.error("Spotify recommendations failed.")
                    else:
                        st.info("Spotify credentials missing. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env.")
            except Exception:
                st.error("Mood classification failed.")
