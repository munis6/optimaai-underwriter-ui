# app/processor/decision_builder.py

from app.processor.ai_engine import AIEngine
from app.processor.compliance_preprocessor import build_compliance_block
from app.processor.ai_insights import parse_ai_output
from app.processor.summary_builder import build_summary
from app.processor.executive_summary import build_executive_summary
from app.processor.state_compliance_builder import build_state_compliance

from app.services.underwriting_engine import (
    generate_underwriting_summary,
    generate_ai_insights
)

def build_decision_json(extracted, underwriting):
    print(">>> USING UPDATED DECISION BUILDER <<<")

    # -----------------------------
    # 1. Build underwriting context for AI  
    # -----------------------------
    underwriting_context = {
        "customer": underwriting.get("customer"),
        "coverage": underwriting.get("coverage"),
        "vehicles": underwriting.get("vehicles"),
        "drivers": underwriting.get("drivers")
    }

    # -----------------------------
    # 2. Call AI engine (Groq)
    # -----------------------------
    engine = AIEngine()
    ai_output = engine.generate_insights(underwriting_context)

    # -----------------------------
    # 3. Parse AI output into 4 fields
    # -----------------------------
    ai_insights_dict = parse_ai_output(ai_output)

    # -----------------------------
    # 4. Build base final JSON
    # -----------------------------
    final_output = {
        "customer": extracted.get("customer"),
        "coverage": extracted.get("coverage"),
        "vehicles": extracted.get("vehicles"),
        "drivers": extracted.get("drivers"),
        "guidewire": extracted.get("guidewire"),

        # ⭐ FIX: include riskScore at the top level
        "riskScore": underwriting.get("riskScore"),

        "underwriting": {
            "vehicles": underwriting.get("vehicles"),
            "drivers": underwriting.get("drivers"),

            # ⭐ FIX: include riskScore inside underwriting block
            "riskScore": underwriting.get("riskScore"),
            "eligibility": underwriting.get("eligibility"),
            "details": underwriting.get("details"),
            "summary": underwriting.get("summary"),
        },

        "aiInsights": ai_insights_dict,
    }

    # -----------------------------
    # 5. Summaries
    # -----------------------------
    final_output["summary"] = build_summary(underwriting)
    final_output["executiveSummary"] = build_executive_summary(final_output["summary"])

    # -----------------------------
    # 6. Compliance / Audit Block
    # -----------------------------
    final_output["compliance"] = build_compliance_block(extracted, underwriting, ai_insights_dict)
    final_output["stateCompliance"] = build_state_compliance(extracted)

    # -----------------------------
    # 7. NEW — Underwriting Summary + AI Insights Summary for PDF
    # -----------------------------
    rules_checked = final_output["compliance"].get("rulesChecked", [])

    final_output["underwritingSummary"] = generate_underwriting_summary(rules_checked)
    final_output["aiInsightsSummary"] = generate_ai_insights(rules_checked)

    return final_output
