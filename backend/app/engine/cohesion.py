import numpy as np
from .embeddings import encode


def centroid_tightness_score(sentences):
    sents = [s.strip() for s in sentences if s.strip() and len(s.split()) >= 3]
    if len(sents) < 4:
        return 0.5, {"reason": "too short", "n_sentences": len(sents)}

    vecs = encode(sents)
    centroid = vecs.mean(axis=0)
    centroid /= np.linalg.norm(centroid) + 1e-9
    distances = 1.0 - (vecs @ centroid)

    mean_dist = float(distances.mean())
    max_dist = float(distances.max())

    tightness = max(0.0, min(1.0, (0.45 - mean_dist) / 0.35))
    no_outlier = max(0.0, min(1.0, (0.55 - max_dist) / 0.30))
    score = 0.65 * tightness + 0.35 * no_outlier

    return round(score, 4), {
        "mean_centroid_distance": round(mean_dist, 4),
        "max_centroid_distance": round(max_dist, 4),
        "n_sentences": len(sents),
    }
