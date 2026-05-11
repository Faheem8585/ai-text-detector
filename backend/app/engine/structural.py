import re
import statistics


_BULLET_RX = re.compile(r"^\s*(?:[-*•·]|\d+[.)])\s+", re.MULTILINE)

_SAFE_OPENERS = (
    "in today", "in the modern", "in recent years", "in the world of",
    "as we", "when it comes to", "in the realm of", "with the rise of",
    "in an era", "in the context of",
)
_SAFE_CLOSERS = (
    "in conclusion", "ultimately", "in summary", "to sum up",
    "in essence", "all in all", "in the end", "overall", "to conclude",
)


def _paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def _politeness_gradient(text):
    t = text.strip().lower()
    if len(t) < 60:
        return 0.0
    head = t[:200]
    tail = t[-200:]
    head_hit = any(s in head for s in _SAFE_OPENERS)
    tail_hit = any(s in tail for s in _SAFE_CLOSERS)
    return (0.5 if head_hit else 0.0) + (0.5 if tail_hit else 0.0)


def structural_score(text):
    paras = _paragraphs(text)
    telemetry = {
        "paragraph_count": len(paras),
        "paragraph_length_cv": None,
        "bullet_balance": None,
        "politeness_gradient": 0.0,
    }
    signals = []

    if len(paras) >= 3:
        lens = [len(p.split()) for p in paras]
        cv = statistics.pstdev(lens) / max(statistics.mean(lens), 1)
        telemetry["paragraph_length_cv"] = round(cv, 4)
        signals.append(max(0.0, min(1.0, (0.70 - cv) / 0.60)))

    bullets = _BULLET_RX.findall(text)
    if len(bullets) >= 3:
        bullet_lines = [l for l in text.splitlines() if _BULLET_RX.match(l)]
        bl = [len(b.split()) for b in bullet_lines]
        bcv = statistics.pstdev(bl) / max(statistics.mean(bl), 1)
        telemetry["bullet_balance"] = round(bcv, 4)
        signals.append(max(0.0, min(1.0, (0.45 - bcv) / 0.40)))

    pg = _politeness_gradient(text)
    telemetry["politeness_gradient"] = pg
    signals.append(pg)

    score = sum(signals) / len(signals) if signals else 0.0
    return round(score, 4), telemetry
