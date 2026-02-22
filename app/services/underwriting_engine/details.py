def build_underwriting_details(drivers, vehicles, risk_score, base_premium):
    """
    Centralized underwriting detail builder.
    Produces underwriting.vehicles and underwriting.drivers blocks.
    """

    eligibility = "Eligible"

    # -----------------------------
    # VEHICLES (FIXED)
    # -----------------------------
    uw_vehicles = []
    for v in vehicles:
        uw_vehicles.append({
            "raw": v.get("raw", {}),
            "normalized": v.get("normalized", {}),
            "rulesResult": {
                "rulesFired": [],
                "status": "rules evaluated (placeholder)"
            },
            "riskScore": risk_score,
            "premium": base_premium,
            "eligibility": eligibility,
        })

    # -----------------------------
    # DRIVERS (SAFE + NORMALIZED)
    # -----------------------------
    uw_drivers = []
    for d in drivers:
        raw = d.get("raw", {})
        norm = d.get("normalized", {})

        uw_drivers.append({
            "raw": raw,
            "normalized": norm,
            "firstName": raw.get("firstName"),
            "lastName": raw.get("lastName"),
            "age": raw.get("age"),
            "licenseNumber": raw.get("licenseNumber"),
            "yearsLicensed": raw.get("yearsLicensed"),
            "accidents": raw.get("accidents"),
            "violations": raw.get("violations"),
            "claims": raw.get("claims"),
            "isPrimaryDriver": raw.get("isPrimaryDriver"),
        })

    # -----------------------------
    # FINAL UNDERWRITING BLOCK
    # -----------------------------
    return {
        "vehicles": uw_vehicles,
        "drivers": uw_drivers,
        "riskScore": risk_score,
        "eligibility": eligibility
    }
