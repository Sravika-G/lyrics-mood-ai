from transformers import pipeline
from typing import Tuple, Dict

MODEL_NAME = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
_classifier = None

LABEL_TO_MOOD = {
    "positive": "happy/energetic",
    "neutral": "chill/reflective",
    "negative": "sad/melancholic"
}

MAX_LEN = 512

def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = pipeline("sentiment-analysis", model=MODEL_NAME, device=-1)
    return _classifier

def classify_mood(text: str) -> Tuple[str, Dict[str, float]]:
    try:
        safe_text = text[:3000] if len(text) > 3000 else text
        classifier = get_classifier()
        result = classifier(safe_text)[0]
        label = result["label"].lower()
        mood = LABEL_TO_MOOD.get(label, "unknown")
        scores = {lbl: float(result["score"]) if lbl == label else 0.0 for lbl in LABEL_TO_MOOD.keys()}
        return mood, scores
    except Exception:
        return "unknown", {lbl: 0.0 for lbl in LABEL_TO_MOOD.keys()}
