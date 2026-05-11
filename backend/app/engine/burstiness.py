import re
import statistics

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")


def split_sentences(text):
    parts = _SENT_SPLIT.split(text.strip())
    return [s.strip() for s in parts if s.strip()]


def burstiness_score(sentences):
    if len(sentences) < 2:
        return 0.5
    lengths = [len(s.split()) for s in sentences]
    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.5
    cv = statistics.pstdev(lengths) / mean
    return round(max(0.0, min(1.0, 1.0 - (cv / 0.85))), 4)
