from fastapi import APIRouter, Response
from pydantic import BaseModel

from app.processor.processor import process_data
from app.dispatcher.dispatcher import dispatch_output
from app.pdf_layout.pdf_render import generate_pdf
from app.models.compliance_summary import ComplianceSummary

router = APIRouter()

class UnderwriterInput(BaseModel):
    data: dict

@router.get("/")
def home():
    return {"message": "OptimaAI Underwriter is running"}

@router.post("/receive")
def receive_input(payload: UnderwriterInput):
    processed = process_data(payload.data)
    final_output = dispatch_output(processed)

    risk_score = final_output.get("finalDecision", {}).get("riskScore")

    return {
        "status": "received",
        "riskScore": risk_score
    }

@router.post("/generate-compliance-report")
def generate_compliance_report(payload: dict):
    print(">>> PDF ENDPOINT HIT <<<")

    # Render-safe temp path
    output_path = "/tmp/compliance_report.pdf"

    try:
        print(">>> Generating PDF at:", output_path)
        generate_pdf(output_path)
    except Exception as e:
        print(">>> PDF GENERATION ERROR:", e)
        return {
            "error": "PDF generation failed",
            "details": str(e)
        }

    try:
        print(">>> Reading PDF bytes...")
        with open(output_path, "rb") as f:
            pdf_bytes = f.read()
    except Exception as e:
        print(">>> FILE READ ERROR:", e)
        return {
            "error": "PDF read failed",
            "details": str(e)
        }

    print(">>> PDF SUCCESSFULLY RETURNED <<<")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=compliance_report.pdf"},
    )
