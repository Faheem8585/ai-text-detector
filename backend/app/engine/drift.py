from .embeddings import encode


def semantic_drift_score(sentences):
    sents = [s.strip() for s in sentences if s.strip() and len(s.split()) >= 3]
    if len(sents) < 3:
        return 0.5, {"reason": "too short", "n_sentences": len(sents)}

    vecs = encode(sents)
    sims = (vecs[:-1] * vecs[1:]).sum(axis=1)

    mean_sim = float(sims.mean())
    std_sim = float(sims.std()) if len(sims) > 1 else 0.0

    mean_signal = max(0.0, min(1.0, (mean_sim - 0.30) / 0.45))
    std_signal = max(0.0, min(1.0, (0.25 - std_sim) / 0.20))
    score = 0.70 * mean_signal + 0.30 * std_signal

    return round(score, 4), {
        "mean_adjacent_similarity": round(mean_sim, 4),
        "stdev_adjacent_similarity": round(std_sim, 4),
        "n_sentences": len(sents),
        "min_similarity": round(float(sims.min()), 4),
        "max_similarity": round(float(sims.max()), 4),
    }
