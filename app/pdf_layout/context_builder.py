"""
Phase‑2 Context Builder
-----------------------
Takes the enriched underwriting JSON (Phase 2 output)
and passes it directly into the PDF pages.

The enriched JSON is already canonical and does NOT need normalization.
"""

def build_context(enriched_json):
    """
    Phase‑2 unified context builder.
    The enriched JSON from dispatch_output() is already in the correct
    canonical structure for all PDF pages.
    """

    # Pass enriched JSON directly to PDF pages
    return {
        "customer": enriched_json.get("customer"),
        "applicant": enriched_json.get("applicant"),
        "drivers": enriched_json.get("drivers"),
        "vehicles": enriched_json.get("vehicles"),
        "coverage": enriched_json.get("coverage"),
        "policy": enriched_json.get("policy"),
        "pricing": enriched_json.get("pricing"),
        "risk": enriched_json.get("risk"),
        "summary": enriched_json.get("summary"),
        "compliance": enriched_json.get("compliance"),
        "aiInsights": enriched_json.get("aiInsights"),
        "lineage": enriched_json.get("lineage"),
    }
