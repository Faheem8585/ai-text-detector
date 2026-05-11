from .burstiness import burstiness_score, split_sentences
from .perplexity import predictability_score
from .signatures import signature_frequency
from .drift import semantic_drift_score
from .cohesion import centroid_tightness_score
from .structural import structural_score
from .hedges import hedge_score
from .artifacts import detect_ocr_artifacts


WEIGHTS = {
    "linguistic_predictability": 0.08,
    "sentence_variance":         0.08,
    "ai_phrase_frequency":       0.12,
    "semantic_drift":            0.22,
    "structural_symmetry":       0.12,
    "hedge_density":             0.15,
    "centroid_tightness":        0.23,
}

LAYER_TRIGGER_THRESHOLD = 0.55


def _verdict(p, artifacts):
    deep = p >= 0.82 or (p >= 0.68 and artifacts and artifacts.get("score", 0) >= 0.5)
    if deep:
        return "DEEPLY SYNTHESIZED"
    if p >= 0.52:
        return "LIKELY AI"
    if p >= 0.28:
        return "MIXED / INCONCLUSIVE"
    return "LIKELY HUMAN"


def _modality(source, has_text):
    if source == "image" and has_text:
        return "Combined (OCR Image + Text)"
    if source == "image":
        return "OCR Image"
    if source == "pdf":
        return "PDF Text"
    return "Text"


def _smoking_gun(sentences, heatmap, matched_phrases, hedge_hits,
                 drift_tele, cohesion_tele):
    for phrase in matched_phrases:
        for s in sentences:
            if phrase.lower() in s.lower():
                return {"quote": s.strip(),
                        "reason": f'Matched signature phrase: "{phrase}".'}

    for phrase in hedge_hits:
        for s in sentences:
            if phrase.lower() in s.lower():
                return {"quote": s.strip(),
                        "reason": f'Hedge phrase detected: "{phrase}".'}

    centroid = cohesion_tele.get("mean_centroid_distance")
    if centroid is not None and centroid < 0.18 and sentences:
        return {"quote": sentences[len(sentences) // 2].strip(),
                "reason": f"Topic centroid distance {centroid} — every "
                          "sentence orbits the same concept."}

    sim = drift_tele.get("mean_adjacent_similarity")
    if sim is not None and sim > 0.72 and sentences:
        return {"quote": sentences[0].strip(),
                "reason": f"Adjacent-sentence similarity {sim} — no "
                          "semantic deviation."}

    if heatmap:
        most = min(heatmap, key=lambda h: h["perplexity_proxy"])
        return {"quote": most["sentence"],
                "reason": f"Lowest surprisal (proxy {most['perplexity_proxy']})."}

    return {"quote": "", "reason": ""}


def _layers_triggered(components, artifacts):
    labels = {
        "linguistic_predictability": "Linguistic Predictability",
        "sentence_variance":         "Sentence Variance",
        "ai_phrase_frequency":       "AI-Phrase Patterns",
        "semantic_drift":            "Semantic Drift",
        "structural_symmetry":       "Structural Symmetry",
        "hedge_density":             "Hedge Frequency",
        "centroid_tightness":        "Topic Centroid Tightness",
    }
    triggered = [labels[k] for k, v in components.items()
                 if v >= LAYER_TRIGGER_THRESHOLD]
    if artifacts and artifacts.get("score", 0) >= 0.30:
        triggered.append("OCR Artifacts")
    return triggered


def analyze(text, source="text", human_baseline=None):
    text = (text or "").strip()
    sentences = split_sentences(text)

    w1, proxies = predictability_score(sentences)
    w2 = burstiness_score(sentences)
    w3, matched = signature_frequency(text)
    w4, drift_telemetry = semantic_drift_score(sentences)
    w5, struct_telemetry = structural_score(text)
    w6, hedge_hits = hedge_score(text)
    w7, cohesion_telemetry = centroid_tightness_score(sentences)

    if human_baseline:
        base_sents = split_sentences(human_baseline)
        base_w1, _ = predictability_score(base_sents)
        base_w4, _ = semantic_drift_score(base_sents)
        base_w7, _ = centroid_tightness_score(base_sents)
        w1 = max(0.0, w1 - 0.6 * base_w1)
        w4 = max(0.0, w4 - 0.6 * base_w4)
        w7 = max(0.0, w7 - 0.6 * base_w7)

    components = {
        "linguistic_predictability": w1,
        "sentence_variance": w2,
        "ai_phrase_frequency": w3,
        "semantic_drift": w4,
        "structural_symmetry": w5,
        "hedge_density": w6,
        "centroid_tightness": w7,
    }

    ai_probability = round(sum(WEIGHTS[k] * components[k] for k in WEIGHTS), 4)

    heatmap = []
    if proxies:
        cutoff = sorted(proxies)[max(0, len(proxies) // 3)]
        for s, p in zip([s for s in sentences if s.strip()], proxies):
            heatmap.append({"sentence": s, "perplexity_proxy": p,
                            "predictable": p <= cutoff})

    artifacts = detect_ocr_artifacts(text) if source == "image" else None
    if artifacts and artifacts["score"] >= 0.3:
        ai_probability = round(min(1.0, ai_probability + 0.18 * artifacts["score"]), 4)

    return {
        "predictive_confidence_score": round(ai_probability * 100, 1),
        "ai_probability": ai_probability,
        "analyzed_modality": _modality(source, bool(text)),
        "verdict": _verdict(ai_probability, artifacts),
        "final_verdict": _verdict(ai_probability, artifacts),
        "layers_triggered": _layers_triggered(components, artifacts),
        "smoking_gun": _smoking_gun(sentences, heatmap, matched,
                                    hedge_hits, drift_telemetry,
                                    cohesion_telemetry),
        "source": source,
        "extracted_text": text,
        "components": components,
        "weights": WEIGHTS,
        "matched_phrases": matched,
        "hedge_phrases": hedge_hits,
        "heatmap": heatmap,
        "artifacts": artifacts,
        "telemetry": {"drift": drift_telemetry, "cohesion": cohesion_telemetry,
                      "structural": struct_telemetry},
        "engine_version": "0.4",
    }
