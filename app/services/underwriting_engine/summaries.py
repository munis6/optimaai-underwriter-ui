def build_summary_block(customer, drivers, vehicles, risk_score, base_premium, eligibility):
    """
    Builds the underwriting summary block for the PDF and UI.
    """

    return {
        "customer": {
            "firstName": customer.get("firstName"),
            "lastName": customer.get("lastName"),
            "age": customer.get("age"),
            "zip": (customer.get("raw") or {}).get("address", {}).get("zip"),
        },

        "drivers": [
            {
                "firstName": d["raw"].get("firstName"),
                "lastName": d["raw"].get("lastName"),
                "age": d["raw"].get("age"),
                "accidents": d["raw"].get("accidents"),
                "violations": d["raw"].get("violations"),
            }
            for d in drivers
        ],

        "vehicles": [
            {
                "model": v["raw"].get("model"),
                "year": v["raw"].get("year"),
                "annualMileage": v["raw"].get("annualMileage"),
            }
            for v in vehicles
        ],

        "riskScore": risk_score,
        "basePremium": base_premium,
        "eligibility": eligibility,
    }
