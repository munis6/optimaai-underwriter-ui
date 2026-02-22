# app/processor/processor.py

# -----------------------------
# Imports
# -----------------------------
from app.normalizer.normalizer import normalize_incoming_json

from app.services.underwriting_engine import (
    calculate_risk_score,
    determine_eligibility,
    build_summary_block,
    build_ai_insights,
    build_underwriting_details,
)

from .extractors import (
    handle_customer,
    handle_vehicle,
    handle_driver,
    handle_coverage,
    handle_guidewire,
)

from .decision_builder import build_decision_json


# -----------------------------
# Main Processor
# -----------------------------
def process_data(payload):
    """
    Step 4.0:
    - Normalize raw data
    - Run underwriting logic
    - Build final OptimaAI decision JSON with AI insights
    """

    # -----------------------------
    # Raw payload extraction
    # -----------------------------
    customer = payload.get("customer", {})
    vehicles = payload.get("vehicles", [])
    drivers = payload.get("drivers", [])
    coverage = payload.get("coverage", {})
    guidewire = payload.get("guidewire", {})

    previous_premium = payload.get("previousPremium")
    current_premium = payload.get("currentPremium")
    accidents = payload.get("accidents", [])

    # -----------------------------
    # Step 1 — Extraction Layer (raw → extracted)
    # -----------------------------
    _customer_info = handle_customer(customer)
    _vehicle_info_list = [handle_vehicle(v) for v in vehicles]
    _driver_info_list = [handle_driver(d) for d in drivers]
    _coverage_info = handle_coverage(coverage)
    _guidewire_info = handle_guidewire(guidewire)

    base_premium = _coverage_info.get("basePremium")

    extracted = {
        "customer": _customer_info,
        "vehicles": _vehicle_info_list,
        "drivers": _driver_info_list,
        "coverage": _coverage_info,
        "guidewire": _guidewire_info,
        "state": _guidewire_info.get("state"),

        "documents": payload.get("documents", []),
        "hadPriorInsurance": payload.get("hadPriorInsurance"),

        "previousPremium": previous_premium,
        "currentPremium": current_premium,
        "accidents": accidents,
    }

    # -----------------------------
    # Step 2 — NORMALIZATION (raw → normalized)
    # -----------------------------
    normalized = normalize_incoming_json(payload)

    customer_n = normalized["customer"]
    drivers_n = normalized["drivers"]
    vehicles_n = normalized["vehicles"]
    coverage_n = normalized["coverage"]
    guidewire_n = normalized["guidewire"]
    policy_n = normalized["policy"]     # <-- FIXED (now defined)

    # -----------------------------
    # Step 3 — Underwriting Logic (normalized → scoring)
    # -----------------------------
    risk_score = calculate_risk_score(
        customer_n,
        drivers_n,
        vehicles_n,
        coverage_n,
        guidewire_n
    )

    eligibility = determine_eligibility(drivers_n, vehicles_n)

    summary = build_summary_block(
        customer_n,
        drivers_n,
        vehicles_n,
        risk_score,
        base_premium,
        eligibility
    )

    ai = build_ai_insights(customer_n, coverage_n, risk_score)

    details = build_underwriting_details(
        drivers_n,
        vehicles_n,
        risk_score,
        base_premium
    )

    # -----------------------------
    # FULL Underwriting Context (for AI + PDF)
    # -----------------------------
    underwriting = {
        "customer": customer_n,
        "drivers": drivers_n,
        "vehicles": vehicles_n,
        "coverage": coverage_n,
        "policy": policy_n,        # <-- FIXED
        "guidewire": guidewire_n,

        "riskScore": risk_score,
        "eligibility": eligibility,
        "summary": summary,
        "aiInsights": ai,
        "details": details,
    }

    # -----------------------------
    # Step 4 — Final Decision JSON
    # -----------------------------
    final_decision = build_decision_json(extracted, underwriting)
    return final_decision
