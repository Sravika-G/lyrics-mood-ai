from transformers import pipeline
from typing import List
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 42

_summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    device=-1,
    framework="pt"
)

LANG_CODE_TO_MODEL = {
    "hi": "Helsinki-NLP/opus-mt-hi-en",
    "te": "Helsinki-NLP/opus-mt-te-en",
    "ta": "Helsinki-NLP/opus-mt-ta-en",
    "bn": "Helsinki-NLP/opus-mt-bn-en",
    "ml": "Helsinki-NLP/opus-mt-ml-en",
    "mr": "Helsinki-NLP/opus-mt-mr-en",
    "ur": "Helsinki-NLP/opus-mt-ur-en",
    "es": "Helsinki-NLP/opus-mt-es-en",
    "fr": "Helsinki-NLP/opus-mt-fr-en",
    "de": "Helsinki-NLP/opus-mt-de-en"
}

_translators = {}

def get_translator(lang_code):
    if lang_code not in LANG_CODE_TO_MODEL:
        return None
    if lang_code not in _translators:
        try:
            _translators[lang_code] = pipeline(
                "translation",
                model=LANG_CODE_TO_MODEL[lang_code],
                device=-1
            )
        except Exception:
            return None
    return _translators[lang_code]

def chunk_text(text: str, chunk_size: int) -> List[str]:
    text = text.strip()
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start = end
    return chunks

def translate_to_english(text: str, lang_code: str) -> str:
    translator = get_translator(lang_code)
    if not translator:
        return f"[Translation unavailable for language: {lang_code}]"
    try:
        chunks = chunk_text(text, 1500)
        translated = []
        for chunk in chunks:
            out = translator(chunk)
            translated.append(out[0]["translation_text"])
        return " ".join(translated)
    except Exception:
        return "[Translation failed]"

SUMMARY_WORDS = 120

def summarize_lyrics(text: str) -> str:
    try:
        if not text or not text.strip():
            return "[No lyrics provided]"
        try:
            lang = detect(text)
        except Exception:
            lang = "en"
        resolved_text = text
        if lang != "en":
            resolved_text = translate_to_english(text, lang)
        chunks = chunk_text(resolved_text, 2500)
        summaries = []
        for chunk in chunks:
            try:
                out = _summarizer(chunk, max_length=130, min_length=30, do_sample=False)
                summaries.append(out[0]["summary_text"])
            except Exception:
                summaries.append("[Summarization failed for chunk]")
        meta = " ".join(summaries)
        if len(meta.split()) > SUMMARY_WORDS:
            try:
                meta_summary = _summarizer(meta, max_length=SUMMARY_WORDS+20, min_length=SUMMARY_WORDS-20, do_sample=False)
                return meta_summary[0]["summary_text"]
            except Exception:
                return meta
        return meta
    except Exception:
        return "[Summarization failed]"
