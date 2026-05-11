import re


HEDGE_PATTERNS = [
    r"\bit (?:seems|appears) (?:that|like)\b",
    r"\bit (?:may|might|could) be (?:argued|noted|said|considered)\b",
    r"\bit is (?:worth|important|essential|crucial) (?:to (?:note|consider|remember|recognize))?\b",
    r"\bis (?:likely|unlikely|possibly|potentially)\b",
    r"\bcan be (?:seen|viewed|interpreted|considered) as\b",
    r"\b(?:some|many|certain|various) (?:experts|researchers|studies|scholars)\b",
    r"\bresearch (?:suggests|indicates|shows)\b",
    r"\bstudies have shown\b",
    r"\b(?:tends|tend) to\b",
    r"\bmay (?:include|involve|require|depend on|vary)\b",
    r"\bgenerally speaking\b",
    r"\bin most cases\b",
    r"\bon the other hand\b",
    r"\bthat (?:being|having) said\b",
    r"\bone could (?:argue|say|note|posit)\b",
    r"\b(?:relatively|fairly|somewhat|rather|quite) (?:common|important|significant|complex)\b",
    r"\bperhaps (?:the most|one of)\b",
    r"\bit (?:is|'?s) (?:often|generally|widely) (?:said|believed|known|accepted)\b",
    r"\bmore (?:research|study|investigation) is needed\b",
    r"\bwhile (?:it is|it'?s) (?:true|important|essential) (?:that|to)\b",
    r"\b(?:depending|depend) on (?:the|various|several|specific)\b",
    r"\bthere (?:are|is) (?:a number of|several|multiple|various)\b",
    r"\b(?:largely|mainly|primarily|chiefly) (?:due to|because of|depends)\b",
    r"\bin (?:general|some respects|certain ways)\b",
    r"\bcan vary (?:depending|based on|significantly)\b",
    r"\b(?:often|frequently|typically) (?:considered|regarded|seen)\b",
    r"\bnot necessarily\b",
    r"\bto some (?:extent|degree)\b",
    r"\bmay or may not\b",
    r"\bit (?:would|might) be (?:beneficial|prudent|wise|helpful) to\b",
    r"\b(?:critics|proponents|supporters) (?:argue|claim|contend)\b",
    r"\b(?:should|must) be (?:noted|considered|taken into account)\b",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in HEDGE_PATTERNS]


def hedge_score(text):
    matches = []
    for rx in _COMPILED:
        for m in rx.finditer(text):
            matches.append(m.group(0))
    words = max(len(text.split()), 1)
    density = len(matches) / (words / 100.0)
    score = max(0.0, min(1.0, density / 2.0))
    return round(score, 4), matches[:20]
