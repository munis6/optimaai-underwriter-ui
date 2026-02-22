print(">>> USING REPORTLAB RENDERER <<<")

"""
Phase‑2 PDF Renderer
--------------------
This file wires the Phase‑2 context builder into the
8‑page PDF layout engine.

Responsibilities:
1. Build unified context (Phase 2) from API JSON
2. Pass context into each PDF page renderer
3. Generate final multi‑page PDF

NO layout logic belongs here.
NO Phase‑3 polish belongs here.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from app.pdf_layout.context_builder import build_context

# Import all page renderers
from app.pdf_layout.pages.executive_summary_page import render_executive_summary_page
from app.pdf_layout.pages.customer_driver_page import render_customer_driver_details_page
from app.pdf_layout.pages.vehicle_page import render_vehicle_details_page
from app.pdf_layout.pages.coverage_page import render_coverage_summary_page
from app.pdf_layout.pages.pricing_breakdown_page import render_pricing_breakdown_page
from app.pdf_layout.pages.compliance_page import render_compliance_summary_page
from app.pdf_layout.pages.ai_insights_page import render_ai_insights_summary_page
from app.pdf_layout.pages.data_lineage_page import render_data_lineage_page
from app.pdf_layout.fonts.register_fonts import register_fonts

register_fonts()


def safe_context(ctx):
    """
    Global null‑safety wrapper.
    Ensures every PDF page receives safe defaults.
    Prevents: 'NoneType' object has no attribute 'get'
    """

    ctx = ctx or {}

    # Coverage fallback
    coverage = ctx.get("coverage") or {}
    coverage["coverageType"] = coverage.get("coverageType") or "Standard Auto"
    coverage["liabilityLimit"] = coverage.get("liabilityLimit") or 0
    coverage["deductible"] = coverage.get("deductible") or 0
    ctx["coverage"] = coverage

    # Vehicles fallback
    vehicles = ctx.get("vehicles") or []
    ctx["vehicles"] = vehicles

    # Drivers fallback
    drivers = ctx.get("drivers") or []
    ctx["drivers"] = drivers

    # Risk score fallback
    ctx["riskScore"] = ctx.get("riskScore") or 0

    # Compliance fallback
    ctx["compliance"] = ctx.get("compliance") or {}

    # State compliance fallback
    ctx["stateCompliance"] = ctx.get("stateCompliance") or {}

    # AI insights fallback
    ctx["aiInsights"] = ctx.get("aiInsights") or {}

    return ctx


def generate_pdf(output_path, enriched_json):
    """
    Phase‑2 PDF generation pipeline.
    1. Build context from API-provided JSON
    2. Render all 8 pages
    """

    print(">>> Building Phase‑2 context from API payload <<<")
    context = build_context(enriched_json)

    # ⭐ Apply global null‑safety
    context = safe_context(context)

    print(">>> Rendering PDF <<<")
    c = canvas.Canvas(output_path, pagesize=letter)

    # Page 1
    print("Rendering page 1…")
    render_executive_summary_page(c, context, page_number=1)

    # Page 2
    print("Rendering page 2…")
    render_customer_driver_details_page(c, context, page_number=2)

    # Page 3
    print("Rendering page 3…")
    render_vehicle_details_page(c, context, page_number=3)

    # Page 4
    print("Rendering page 4…")
    render_coverage_summary_page(c, context, page_number=4)

    # Page 5
    print("Rendering page 5…")
    render_pricing_breakdown_page(c, context, page_number=5)

    # Page 6
    print("Rendering page 6…")
    render_compliance_summary_page(c, context, page_number=6)

    # Page 7
    print("Rendering page 7…")
    render_ai_insights_summary_page(c, context, page_number=7)

    # Page 8
    print("Rendering page 8…")
    render_data_lineage_page(c, context, page_number=8)

    c.save()
    print(f"PDF generated: {output_path}")
