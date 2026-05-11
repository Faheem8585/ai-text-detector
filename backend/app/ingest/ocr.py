import io
from PIL import Image, ImageOps

try:
    import pytesseract
    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False


def image_to_text(data):
    if not _AVAILABLE:
        raise RuntimeError("pytesseract is not installed")
    img = Image.open(io.BytesIO(data))
    img = ImageOps.exif_transpose(img)
    if img.mode != "L":
        img = img.convert("L")
    img = ImageOps.autocontrast(img)
    return pytesseract.image_to_string(img).strip()
