import re
import unicodedata


_CONFUSABLE_BLOCKS = {"CYRILLIC", "GREEK", "ARMENIAN"}

_SIGN_LEXICON = {
    "STOP", "YIELD", "EXIT", "ENTER", "OPEN", "CLOSED", "DANGER",
    "WARNING", "CAUTION", "POLICE", "FIRE", "HOSPITAL", "SCHOOL",
    "ONE", "WAY", "NO", "PARKING", "SPEED", "LIMIT", "AHEAD",
    "MERGE", "DETOUR", "SLOW", "ROAD", "WORK", "BUS", "TAXI",
    "RESTROOM", "MEN", "WOMEN", "PUSH", "PULL", "EMERGENCY",
    "STAFF", "ONLY", "PRIVATE", "PUBLIC", "RESERVED",
}


def _has_confusable(token):
    for ch in token:
        try:
            name = unicodedata.name(ch, "")
        except ValueError:
            continue
        if any(b in name for b in _CONFUSABLE_BLOCKS):
            return True
    return False


def _melting(token):
    letters = re.sub(r"[^A-Za-z]", "", token)
    return len(letters) >= 5 and not re.search(r"[aeiouAEIOU]", letters)


def _impossible_signage(tokens):
    candidates = [t for t in tokens
                  if 3 <= len(t) <= 6 and t.isupper() and t.isalpha()]
    if not candidates:
        return []
    knowns = sum(1 for t in candidates if t in _SIGN_LEXICON)
    unknowns = [t for t in candidates if t not in _SIGN_LEXICON]
    if knowns >= 1 and unknowns:
        return unknowns
    if len(unknowns) >= 3:
        return unknowns
    return []


def detect_ocr_artifacts(text):
    tokens = text.split()
    if not tokens:
        return {"flags": [], "nonsense_count": 0, "melting_glyphs": 0,
                "kerning_anomalies": 0, "glyph_noise": 0,
                "impossible_signage": [], "score": 0.0}

    melting = [t for t in tokens if _melting(t)]
    weird_case = [t for t in tokens if re.search(r"[a-z][A-Z]|[A-Z]{2,}[a-z]+[A-Z]", t)]
    repeated = [t for t in tokens if re.search(r"(.)\1{3,}", t)]
    confusables = [t for t in tokens if _has_confusable(t)]
    impossible = _impossible_signage(tokens)

    flagged = list({*melting, *weird_case, *repeated, *confusables, *impossible})
    score = min(1.0, len(flagged) / max(len(tokens), 1) * 5.0)

    return {
        "flags": flagged[:30],
        "nonsense_count": len(melting),
        "melting_glyphs": len(melting),
        "kerning_anomalies": len(weird_case),
        "glyph_noise": len(repeated) + len(confusables),
        "impossible_signage": impossible[:10],
        "score": round(score, 4),
    }
