from fastapi import APIRouter
from fastapi.responses import Response

from ..reports.evidence_pdf import build_pdf
from ..schemas import ReportRequest


router = APIRouter()


@router.post("/report")
def report_endpoint(req: ReportRequest):
    pdf = build_pdf(req.result.model_dump(), case_name=req.case_name or "untitled")
    filename = f"report-{req.case_name or 'untitled'}.pdf"
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
