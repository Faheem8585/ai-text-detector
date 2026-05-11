import os
import numpy as np

_MODEL = None
_MODEL_NAME = os.environ.get("AEGIS_EMBED_MODEL",
                             "sentence-transformers/all-MiniLM-L6-v2")


def get_model():
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer
        _MODEL = SentenceTransformer(_MODEL_NAME)
    return _MODEL


def encode(sentences):
    if not sentences:
        return np.zeros((0, 384), dtype=np.float32)
    vecs = get_model().encode(
        sentences, convert_to_numpy=True,
        normalize_embeddings=True, show_progress_bar=False,
    )
    return vecs.astype(np.float32)


def warm_up():
    try:
        encode(["warm up"])
        return True
    except Exception:
        return False
