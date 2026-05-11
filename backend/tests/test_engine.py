from app.engine.scorer import analyze
from app.engine.burstiness import burstiness_score, split_sentences
from app.engine.signatures import signature_frequency
from app.engine.drift import semantic_drift_score
from app.engine.cohesion import centroid_tightness_score
from app.engine.structural import structural_score
from app.engine.hedges import hedge_score


HUMAN = (
    "Eight minutes awake, maybe less. The kettle started hissing on the "
    "stove and I noticed I'd forgotten to put coffee in the filter again. "
    "Outside, the seagulls were screaming about something - a chip bag, "
    "probably. My phone, dead since four, sat face-down on the counter "
    "like it owed me money. I thought about the email from Dave and then "
    "decided, no, absolutely not, not yet. The bread on the cutting board "
    "was stale but I ate two slices anyway. Later, the cat threw up on "
    "the new rug. Typical."
)

AI = (
    "In today's fast-paced digital world, it is important to note that "
    "navigating the multifaceted landscape of modern technology plays a "
    "crucial role in fostering a productive environment. It seems that "
    "the integration of advanced systems may be considered essential. "
    "Research suggests that organizations tend to benefit significantly. "
    "In conclusion, harnessing the power of innovation underscores the "
    "importance of embracing an ever-evolving paradigm."
)


def test_burstiness_uniform_higher_than_bursty():
    bursty = ("Cold. The wind cut through my jacket as if the fabric "
              "weren't there at all, and I wished I had brought the "
              "heavier coat. Stupid. Whatever.")
    uniform = ("The system processes data efficiently. The algorithm "
               "handles requests in parallel. The response times are "
               "consistently low. The architecture scales horizontally.")
    assert burstiness_score(split_sentences(bursty)) < burstiness_score(split_sentences(uniform))


def test_signature_catches_ai_phrases():
    score, matches = signature_frequency(AI)
    assert score > 0.3
    assert len(matches) >= 3


def test_signature_clean_on_human():
    score, _ = signature_frequency(HUMAN)
    assert score < 0.1


def test_drift_higher_for_ai():
    h, _ = semantic_drift_score(split_sentences(HUMAN))
    a, _ = semantic_drift_score(split_sentences(AI))
    assert a > h


def test_centroid_tightness_separates():
    h, _ = centroid_tightness_score(split_sentences(HUMAN))
    a, _ = centroid_tightness_score(split_sentences(AI))
    assert a > h


def test_hedge_detects_neutrality():
    h, _ = hedge_score(HUMAN)
    a, hits = hedge_score(AI)
    assert a > h
    assert len(hits) >= 2


def test_structural_runs():
    s, t = structural_score(AI)
    assert 0.0 <= s <= 1.0
    assert "paragraph_count" in t


def test_analyze_ranks_ai_higher():
    h = analyze(HUMAN)["ai_probability"]
    a = analyze(AI)["ai_probability"]
    assert a > h


def test_output_format():
    out = analyze(AI)
    assert "predictive_confidence_score" in out
    assert "analyzed_modality" in out
    assert isinstance(out["layers_triggered"], list)
    assert "quote" in out["smoking_gun"]
    assert "reason" in out["smoking_gun"]
    assert out["final_verdict"] in {
        "DEEPLY SYNTHESIZED", "LIKELY AI",
        "MIXED / INCONCLUSIVE", "LIKELY HUMAN",
    }


def test_smoking_gun_fires_on_ai():
    out = analyze(AI)
    assert out["smoking_gun"]["quote"]
    assert out["smoking_gun"]["reason"]


def test_all_components_present():
    out = analyze(AI)
    c = out["components"]
    for key in ("linguistic_predictability", "sentence_variance",
                "ai_phrase_frequency", "semantic_drift",
                "structural_symmetry", "hedge_density",
                "centroid_tightness"):
        assert key in c
        assert 0.0 <= c[key] <= 1.0
