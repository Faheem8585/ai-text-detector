from pydantic import BaseModel, Field
from typing import Any, Optional


class HeatmapSpan(BaseModel):
    sentence: str
    perplexity_proxy: float
    predictable: bool


class ComponentScores(BaseModel):
    linguistic_predictability: float
    sentence_variance: float
    ai_phrase_frequency: float
    semantic_drift: float
    structural_symmetry: float
    hedge_density: float
    centroid_tightness: float


class ArtifactReport(BaseModel):
    flags: list[str]
    nonsense_count: int
    melting_glyphs: int
    kerning_anomalies: int
    glyph_noise: int
    impossible_signage: list[str] = Field(default_factory=list)
    score: float


class SmokingGun(BaseModel):
    quote: str
    reason: str


class AnalysisResult(BaseModel):
    predictive_confidence_score: float
    ai_probability: float
    analyzed_modality: str
    verdict: str
    final_verdict: str
    layers_triggered: list[str]
    smoking_gun: SmokingGun
    source: str
    extracted_text: str
    components: ComponentScores
    weights: dict[str, float]
    matched_phrases: list[str]
    hedge_phrases: list[str]
    heatmap: list[HeatmapSpan]
    artifacts: Optional[ArtifactReport] = None
    telemetry: dict[str, Any] = Field(default_factory=dict)
    engine_version: str = "0.4"


class ReportRequest(BaseModel):
    result: AnalysisResult
    case_name: Optional[str] = "untitled"
