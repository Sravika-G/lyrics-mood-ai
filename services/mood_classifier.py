from transformers import pipeline# services/mood_classifier.py

from typing import Tuple, Dictfrom transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

from typing import Tuple, Dict

MODEL_NAME = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"

_classifier = pipeline("sentiment-analysis", model=MODEL_NAME, device=-1)MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

LABEL_TO_MOOD = {_model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

    "positive": "happy/energetic",_classifier = pipeline("sentiment-analysis", model=_model, tokenizer=_tokenizer, device=-1)

    "neutral": "chill/reflective",

    "negative": "sad/melancholic"LABEL_TO_MOOD = {

}    "positive": "happy/energetic",

    "neutral": "chill/reflective",

MAX_LEN = 512    "negative": "sad/melancholic"

}

def classify_mood(text: str) -> Tuple[str, Dict[str, float]]:

    try:MAX_LEN = 512  # XLM-R model max tokens

        safe_text = text[:3000] if len(text) > 3000 else text

        result = _classifier(safe_text)[0]def classify_mood(text: str) -> Tuple[str, Dict[str, float]]:

        label = result["label"].lower()    try:

        mood = LABEL_TO_MOOD.get(label, "unknown")        safe_text = text[:3000] if len(text) > 3000 else text

        scores = {lbl: float(result["score"]) if lbl == label else 0.0 for lbl in LABEL_TO_MOOD.keys()}        result = _classifier(safe_text)[0]

        return mood, scores        label = result["label"].lower()

    except Exception:        mood = LABEL_TO_MOOD.get(label, "unknown")

        return "unknown", {lbl: 0.0 for lbl in LABEL_TO_MOOD.keys()}        # Scores dict: always return all keys

        scores = {lbl: float(result["score"]) if lbl == label else 0.0 for lbl in LABEL_TO_MOOD.keys()}
        return mood, scores
    except Exception:
        return "unknown", {lbl: 0.0 for lbl in LABEL_TO_MOOD.keys()}
