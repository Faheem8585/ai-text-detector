from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..engine.scorer import analyze
from ..ingest.ocr import image_to_text
from ..ingest.pdf import pdf_to_text


router = APIRouter()

_IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff")
_MAX_BYTES = 10 * 1024 * 1024


@router.post("/analyze")
async def analyze_endpoint(
    file: UploadFile | None = File(None),
    text: str | None = Form(None),
    human_baseline: str | None = Form(None),
):
    source = "text"
    content = (text or "").strip()

    if file is not None:
        data = await file.read()
        if len(data) > _MAX_BYTES:
            raise HTTPException(413, "file exceeds 10 MB limit")

        name = (file.filename or "").lower()
        if name.endswith(_IMAGE_EXT):
            try:
                content = image_to_text(data)
            except Exception as exc:
                raise HTTPException(422, f"OCR failed: {exc}") from exc
            source = "image"
        elif name.endswith(".pdf"):
            try:
                content = pdf_to_text(data)
            except Exception as exc:
                raise HTTPException(422, f"PDF parse failed: {exc}") from exc
            source = "pdf"
        elif name.endswith(".txt"):
            content = data.decode("utf-8", errors="ignore")
        else:
            raise HTTPException(415, f"unsupported file type: {name}")

    if not content:
        raise HTTPException(400, "no text provided or extracted")

    return analyze(content, source=source, human_baseline=human_baseline)
