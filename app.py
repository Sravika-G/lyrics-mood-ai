import osimport os

import streamlit as stimport streamlit as st

from services.summarizer import summarize_lyricsfrom services.summarizer import summarize_lyrics

from services.mood_classifier import classify_moodfrom services.mood_classifier import classify_mood

from services.transcribe import transcribe_audio, fetch_youtube_transcriptfrom services.transcribe import transcribe_audio, fetch_youtube_transcript

from services.recommender import recommend_tracksfrom services.recommender import recommend_tracks



st.set_page_config(page_title="🎵 Real-time AI Lyrics Summarizer & Mood Classifier", layout="centered")st.set_page_config(page_title="🎵 Real-time AI Lyrics Summarizer & Mood Classifier", layout="centered")

st.title("🎵 Real-time AI Lyrics Summarizer & Mood Classifier")st.title("🎵 Real-time AI Lyrics Summarizer & Mood Classifier")



with st.expander("Input Options", expanded=True):with st.expander("Input Options", expanded=True):

    input_mode = st.radio("Select input type:", ["Paste lyrics", "Upload audio (transcribe)", "YouTube URL transcript"])    input_mode = st.radio("Select input type:", ["Paste lyrics", "Upload audio (transcribe)", "YouTube URL transcript"])

    lyrics = ""    lyrics = ""

    if input_mode == "Paste lyrics":    transcript_warning = ""

        lyrics = st.text_area("Paste lyrics here:", height=250)    if input_mode == "Paste lyrics":

    elif input_mode == "Upload audio (transcribe)":        lyrics = st.text_area("Paste lyrics here:", height=250)

        audio_file = st.file_uploader("Upload audio file (mp3/wav/m4a):", type=["mp3", "wav", "m4a"])    elif input_mode == "Upload audio (transcribe)":

        if not os.getenv("OPENAI_API_KEY"):        audio_file = st.file_uploader("Upload audio file (mp3/wav/m4a):", type=["mp3", "wav", "m4a"])

            st.info("Audio transcription requires OPENAI_API_KEY. Skipping transcription.")        if not os.getenv("OPENAI_API_KEY"):

        elif audio_file:            st.info("Audio transcription requires OPENAI_API_KEY. Skipping transcription.")

            try:        elif audio_file:

                with st.spinner("Transcribing audio..."):            try:

                    lyrics = transcribe_audio(audio_file)                with st.spinner("Transcribing audio..."):

                if not lyrics:                    lyrics = transcribe_audio(audio_file)

                    st.warning("Transcription failed or returned empty.")                if not lyrics:

            except Exception:                    st.warning("Transcription failed or returned empty.")

                st.error("Audio transcription failed.")            except Exception:

    elif input_mode == "YouTube URL transcript":                st.error("Audio transcription failed.")

        yt_url = st.text_input("Enter YouTube URL:")    elif input_mode == "YouTube URL transcript":

        if yt_url:        yt_url = st.text_input("Enter YouTube URL:")

            try:        if yt_url:

                with st.spinner("Fetching YouTube transcript..."):            try:

                    lyrics = fetch_youtube_transcript(yt_url)                with st.spinner("Fetching YouTube transcript..."):

                if not lyrics:                    lyrics = fetch_youtube_transcript(yt_url)

                    st.info("Transcript unavailable for this video.")                if not lyrics:

            except Exception:                    st.info("Transcript unavailable for this video.")

                st.error("Transcript fetch failed.")            except Exception:

                st.error("Transcript fetch failed.")

run_summary = st.checkbox("Generate summary", value=True)

run_mood = st.checkbox("Classify mood", value=True)run_summary = st.checkbox("Generate summary", value=True)

show_recs = st.checkbox("Recommend similar songs (Spotify)", value=False)run_mood = st.checkbox("Classify mood", value=True)

show_recs = st.checkbox("Recommend similar songs (Spotify)", value=False)

if st.button("Run"):

    if not lyrics or not lyrics.strip():if st.button("Run"):

        st.warning("No lyrics or transcript provided.")    if not lyrics or not lyrics.strip():

    else:        st.warning("No lyrics or transcript provided.")

        st.subheader("Lyrics / Transcript Preview")    else:

        preview = lyrics[:400] + ("..." if len(lyrics) > 400 else "")        st.subheader("Lyrics / Transcript Preview")

        st.text_area("Preview", preview, height=120)        preview = lyrics[:400] + ("..." if len(lyrics) > 400 else "")

        if run_summary:        st.text_area("Preview", preview, height=120)

            try:        if run_summary:

                with st.spinner("Summarizing lyrics..."):            try:

                    summary = summarize_lyrics(lyrics)                with st.spinner("Summarizing lyrics..."):

                st.subheader("AI Summary")                    summary = summarize_lyrics(lyrics)

                st.write(summary)                st.subheader("AI Summary")

            except Exception:                st.write(summary)

                st.error("Summarization failed.")            except Exception:

        if run_mood:                st.error("Summarization failed.")

            try:        if run_mood:

                with st.spinner("Classifying mood..."):            try:

                    mood, scores = classify_mood(lyrics)                with st.spinner("Classifying mood..."):

                st.subheader("Mood / Emotion")                    mood, scores = classify_mood(lyrics)

                st.metric("Mood", mood)                st.subheader("Mood / Emotion")

                st.write("Scores:", scores)                st.metric("Mood", mood)

                if show_recs and mood in ["happy/energetic", "chill/reflective", "sad/melancholic"]:                st.write("Scores:", scores)

                    if os.getenv("SPOTIFY_CLIENT_ID") and os.getenv("SPOTIFY_CLIENT_SECRET"):                if show_recs and mood in ["happy/energetic", "chill/reflective", "sad/melancholic"]:

                        try:                    if os.getenv("SPOTIFY_CLIENT_ID") and os.getenv("SPOTIFY_CLIENT_SECRET"):

                            with st.spinner("Fetching Spotify recommendations..."):                        try:

                                tracks = recommend_tracks(mood)                            with st.spinner("Fetching Spotify recommendations..."):

                            if tracks:                                tracks = recommend_tracks(mood)

                                st.subheader("Spotify Recommendations")                            if tracks:

                                for t in tracks:                                st.subheader("Spotify Recommendations")

                                    st.markdown(f"[{t['name']} — {t['artist']}]({t['url']})")                                for t in tracks:

                            else:                                    st.markdown(f"[{t['name']} — {t['artist']}]({t['url']})")

                                st.info("No recommendations found.")                            else:

                        except Exception:                                st.info("No recommendations found.")

                            st.error("Spotify recommendations failed.")                        except Exception:

                    else:                            st.error("Spotify recommendations failed.")

                        st.info("Spotify credentials missing. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env.")                    else:

            except Exception:                        st.info("Spotify credentials missing. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env.")

                st.error("Mood classification failed.")            except Exception:

                st.error("Mood classification failed.")
