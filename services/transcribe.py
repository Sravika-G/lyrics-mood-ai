import osimport os

import tempfileimport tempfile

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFoundfrom youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound



def transcribe_audio(uploaded_file) -> str:def transcribe_audio(uploaded_file) -> str:

    api_key = os.getenv("OPENAI_API_KEY")    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:    if not api_key:

        return ""        return ""

    try:    try:

        import openai        import openai

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:

            tmp.write(uploaded_file.read())            tmp.write(uploaded_file.read())

            tmp_path = tmp.name            tmp_path = tmp.name

        openai.api_key = api_key        openai.api_key = api_key

        with open(tmp_path, "rb") as audio_file:        with open(tmp_path, "rb") as audio_file:

            transcript = openai.audio.transcriptions.create(            transcript = openai.audio.transcriptions.create(

                model="whisper-1",                model="whisper-1",

                file=audio_file                file=audio_file

            )            )

        os.remove(tmp_path)        os.remove(tmp_path)

        return transcript.text if hasattr(transcript, "text") else ""        return transcript.text if hasattr(transcript, "text") else ""

    except Exception:    except Exception:

        return ""        return ""



def extract_youtube_id(url: str) -> str:def extract_youtube_id(url: str) -> str:

    import re    import re

    patterns = [    patterns = [

        r"youtu\.be/([\w-]+)",        r"youtu\.be/([\w-]+)",

        r"v=([\w-]+)",        r"v=([\w-]+)",

        r"youtube\.com/watch\?v=([\w-]+)"        r"youtube\.com/watch\?v=([\w-]+)"

    ]    ]

    for pat in patterns:    for pat in patterns:

        match = re.search(pat, url)        match = re.search(pat, url)

        if match:        if match:

            return match.group(1)            return match.group(1)

    return ""    return ""



def fetch_youtube_transcript(url: str) -> str:def fetch_youtube_transcript(url: str) -> str:

    try:    try:

        video_id = extract_youtube_id(url)        video_id = extract_youtube_id(url)

        if not video_id:        if not video_id:

            return ""            return ""

        transcript = YouTubeTranscriptApi.get_transcript(video_id)        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        return " ".join([seg["text"] for seg in transcript])        return " ".join([seg["text"] for seg in transcript])

    except (TranscriptsDisabled, NoTranscriptFound, Exception):    except (TranscriptsDisabled, NoTranscriptFound, Exception):

        return ""        return ""

