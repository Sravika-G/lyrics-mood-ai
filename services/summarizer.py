from transformers import pipeline# services/summarizer.py

from typing import Listfrom transformers import pipeline

from langdetect import detect, DetectorFactoryfrom typing import List

from langdetect import detect, DetectorFactory

DetectorFactory.seed = 42

# Deterministic langdetect

_summarizer = pipeline(DetectorFactory.seed = 42

    "summarization",

    model="sshleifer/distilbart-cnn-12-6",# Summarizer pipeline (English)

    device=-1,_summarizer = pipeline(

    framework="pt"    "summarization",

)    model="sshleifer/distilbart-cnn-12-6",

    device=-1,

LANG_CODE_TO_MODEL = {    framework="pt"

    "hi": "Helsinki-NLP/opus-mt-hi-en",)

    "te": "Helsinki-NLP/opus-mt-te-en",

    "ta": "Helsinki-NLP/opus-mt-ta-en",# Supported MarianMT translation models

    "bn": "Helsinki-NLP/opus-mt-bn-en",LANG_CODE_TO_MODEL = {

    "ml": "Helsinki-NLP/opus-mt-ml-en",    "hi": "Helsinki-NLP/opus-mt-hi-en",

    "mr": "Helsinki-NLP/opus-mt-mr-en",    "te": "Helsinki-NLP/opus-mt-te-en",

    "ur": "Helsinki-NLP/opus-mt-ur-en",    "ta": "Helsinki-NLP/opus-mt-ta-en",

    "es": "Helsinki-NLP/opus-mt-es-en",    "bn": "Helsinki-NLP/opus-mt-bn-en",

    "fr": "Helsinki-NLP/opus-mt-fr-en",    "ml": "Helsinki-NLP/opus-mt-ml-en",

    "de": "Helsinki-NLP/opus-mt-de-en"    "mr": "Helsinki-NLP/opus-mt-mr-en",

}    "ur": "Helsinki-NLP/opus-mt-ur-en",

    "es": "Helsinki-NLP/opus-mt-es-en",

_translators = {}    "fr": "Helsinki-NLP/opus-mt-fr-en",

    "de": "Helsinki-NLP/opus-mt-de-en"

def get_translator(lang_code):}

    if lang_code not in LANG_CODE_TO_MODEL:

        return None_translators = {}

    if lang_code not in _translators:

        try:def get_translator(lang_code):

            _translators[lang_code] = pipeline(    if lang_code not in LANG_CODE_TO_MODEL:

                "translation",        return None

                model=LANG_CODE_TO_MODEL[lang_code],    if lang_code not in _translators:

                device=-1        try:

            )            _translators[lang_code] = pipeline(

        except Exception:                "translation",

            return None                model=LANG_CODE_TO_MODEL[lang_code],

    return _translators[lang_code]                device=-1

            )

def chunk_text(text: str, chunk_size: int) -> List[str]:        except Exception:

    text = text.strip()            return None

    if len(text) <= chunk_size:    return _translators[lang_code]

        return [text]

    chunks = []def chunk_text(text: str, chunk_size: int) -> List[str]:

    start = 0    text = text.strip()

    while start < len(text):    if len(text) <= chunk_size:

        end = min(start + chunk_size, len(text))        return [text]

        chunk = text[start:end]    chunks = []

        chunks.append(chunk)    start = 0

        start = end    while start < len(text):

    return chunks        end = min(start + chunk_size, len(text))

        chunk = text[start:end]

def translate_to_english(text: str, lang_code: str) -> str:        chunks.append(chunk)

    translator = get_translator(lang_code)        start = end

    if not translator:    return chunks

        return f"[Translation unavailable for language: {lang_code}]"

    try:def translate_to_english(text: str, lang_code: str) -> str:

        chunks = chunk_text(text, 1500)    translator = get_translator(lang_code)

        translated = []    if not translator:

        for chunk in chunks:        return "[Translation unavailable for language: {}]".format(lang_code)

            out = translator(chunk)    try:

            translated.append(out[0]["translation_text"])        chunks = chunk_text(text, 1500)

        return " ".join(translated)        translated = []

    except Exception:        for chunk in chunks:

        return "[Translation failed]"            out = translator(chunk)

            translated.append(out[0]["translation_text"])

SUMMARY_WORDS = 120        return " ".join(translated)

    except Exception:

def summarize_lyrics(text: str) -> str:        return "[Translation failed]"

    try:

        if not text or not text.strip():SUMMARY_WORDS = 120

            return "[No lyrics provided]"

        try:# Main summarization function

            lang = detect(text)

        except Exception:def summarize_lyrics(text: str) -> str:

            lang = "en"    try:

        resolved_text = text        if not text or not text.strip():

        if lang != "en":            return "[No lyrics provided]"

            resolved_text = translate_to_english(text, lang)        # Detect language

        chunks = chunk_text(resolved_text, 2500)        try:

        summaries = []            lang = detect(text)

        for chunk in chunks:        except Exception:

            try:            lang = "en"

                out = _summarizer(chunk, max_length=130, min_length=30, do_sample=False)        resolved_text = text

                summaries.append(out[0]["summary_text"])        if lang != "en":

            except Exception:            resolved_text = translate_to_english(text, lang)

                summaries.append("[Summarization failed for chunk]")        # Summarize in chunks

        meta = " ".join(summaries)        chunks = chunk_text(resolved_text, 2500)

        if len(meta.split()) > SUMMARY_WORDS:        summaries = []

            try:        for chunk in chunks:

                meta_summary = _summarizer(meta, max_length=SUMMARY_WORDS+20, min_length=SUMMARY_WORDS-20, do_sample=False)            try:

                return meta_summary[0]["summary_text"]                out = _summarizer(chunk, max_length=130, min_length=30, do_sample=False)

            except Exception:                summaries.append(out[0]["summary_text"])

                return meta            except Exception:

        return meta                summaries.append("[Summarization failed for chunk]")

    except Exception:        meta = " ".join(summaries)

        return "[Summarization failed]"        if len(meta.split()) > SUMMARY_WORDS:

            try:
                meta_summary = _summarizer(meta, max_length=SUMMARY_WORDS+20, min_length=SUMMARY_WORDS-20, do_sample=False)
                return meta_summary[0]["summary_text"]
            except Exception:
                return meta
        return meta
    except Exception:
        return "[Summarization failed]"
