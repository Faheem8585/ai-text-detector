import io
from datetime import datetime, timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)


_CYAN = colors.HexColor("#22d3ee")
_RED = colors.HexColor("#f87171")
_AMBER = colors.HexColor("#fbbf24")
_GREEN = colors.HexColor("#34d399")
_SLATE = colors.HexColor("#94a3b8")


def _verdict_color(p):
    if p >= 0.70:
        return _RED
    if p >= 0.40:
        return _AMBER
    return _GREEN


def _escape(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace("\n", "<br/>"))


def build_pdf(result, case_name="untitled"):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=LETTER,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.7 * inch, bottomMargin=0.7 * inch,
    )

    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Heading1"],
                        textColor=_CYAN, fontSize=18, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=styles["Heading2"],
                        textColor=_CYAN, fontSize=12, spaceBefore=14, spaceAfter=6)
    body = ParagraphStyle("body", parent=styles["BodyText"],
                          fontSize=9.5, leading=13)
    mono = ParagraphStyle("mono", parent=body, fontName="Courier",
                          fontSize=8.5, leading=11)

    story = []
    pct = round(result["ai_probability"] * 100, 1)
    color = _verdict_color(result["ai_probability"])

    story.append(Paragraph("AI Text Detection Report", h1))
    story.append(Paragraph(
        f"<font color='#94a3b8'>Case: <b>{case_name}</b> &nbsp;|&nbsp; "
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')} "
        f"&nbsp;|&nbsp; Source: {result['source'].upper()}</font>",
        body,
    ))
    story.append(Spacer(1, 12))

    verdict_tbl = Table(
        [[
            Paragraph(f"<font size='28' color='{color.hexval()}'>"
                      f"<b>{pct}%</b></font>", body),
            Paragraph(
                f"<b>Verdict:</b> <font color='{color.hexval()}'>"
                f"{result['verdict']}</font><br/>"
                f"<font color='#64748b' size='8'>"
                f"Weighted score across seven detection layers."
                f"</font>", body),
        ]],
        colWidths=[1.4 * inch, 5.4 * inch],
    )
    verdict_tbl.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, _SLATE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#f1f5f9")),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(verdict_tbl)

    story.append(Paragraph("Analyzed Modality", h2))
    story.append(Paragraph(f"<b>{result.get('analyzed_modality', 'Text')}</b>", body))

    layers = result.get("layers_triggered") or []
    story.append(Paragraph("Layers Triggered", h2))
    if layers:
        story.append(Paragraph(
            "<br/>".join(f"&#9632; <b>{_escape(l)}</b>" for l in layers), body))
    else:
        story.append(Paragraph("<i>No layers crossed the trigger threshold.</i>", body))

    sg = result.get("smoking_gun") or {}
    if sg.get("quote"):
        story.append(Paragraph("Key Evidence", h2))
        story.append(Paragraph(f'<i>"{_escape(sg["quote"])}"</i>', body))
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            f"<font color='#64748b' size='8'>{_escape(sg['reason'])}</font>", body))

    story.append(Paragraph("Component Scores", h2))
    c = result["components"]
    w = result.get("weights") or {}
    label = {
        "centroid_tightness":        "Centroid Tightness (W7)",
        "semantic_drift":            "Semantic Drift (W4)",
        "hedge_density":             "Hedge Frequency (W6)",
        "ai_phrase_frequency":       "AI-Phrase Frequency (W3)",
        "structural_symmetry":       "Structural Symmetry (W5)",
        "linguistic_predictability": "Linguistic Predictability (W1)",
        "sentence_variance":         "Sentence Variance (W2)",
    }
    rows = [["Signal", "Weight", "Score", "Contribution"]]
    for k, lbl in label.items():
        wt = w.get(k, 0)
        rows.append([lbl, f"{wt*100:.0f}%",
                     f"{c[k]*100:.1f}%",
                     f"{c[k]*wt*100:.1f}%"])
    comp_tbl = Table(rows, colWidths=[2.8*inch, 0.8*inch, 1.2*inch, 1.4*inch])
    comp_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("GRID", (0, 0), (-1, -1), 0.25, _SLATE),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(comp_tbl)

    matched = result.get("matched_phrases") or []
    story.append(Paragraph("Matched AI-Signature Phrases", h2))
    if matched:
        story.append(Paragraph(", ".join(f"<i>{m}</i>" for m in matched), body))
    else:
        story.append(Paragraph("<i>None detected.</i>", body))

    story.append(Paragraph("Highly Predictable Sentences", h2))
    flagged = [h for h in result.get("heatmap", []) if h.get("predictable")]
    if flagged:
        for h in flagged[:25]:
            story.append(Paragraph(
                f"<font color='#dc2626'>&#9632;</font> "
                f"<i>(p&approx;{h['perplexity_proxy']})</i> "
                f"{_escape(h['sentence'])}", body))
            story.append(Spacer(1, 2))
    else:
        story.append(Paragraph(
            "<i>No sentences crossed the predictability threshold.</i>", body))

    if result.get("artifacts"):
        a = result["artifacts"]
        story.append(PageBreak())
        story.append(Paragraph("OCR Artifacts", h2))
        story.append(Paragraph(
            f"Melting glyphs: <b>{a.get('melting_glyphs', 0)}</b> &nbsp; "
            f"Kerning anomalies: <b>{a['kerning_anomalies']}</b> &nbsp; "
            f"Glyph noise: <b>{a['glyph_noise']}</b> &nbsp; "
            f"Score: <b>{a['score']*100:.1f}%</b>", body))
        if a.get("impossible_signage"):
            story.append(Spacer(1, 4))
            story.append(Paragraph(
                f"<b>Impossible signage:</b> "
                f"{', '.join(a['impossible_signage'])}", body))

    story.append(Paragraph("Extracted Text", h2))
    story.append(Paragraph(_escape(result["extracted_text"][:5000]), mono))

    doc.build(story)
    return buf.getvalue()
