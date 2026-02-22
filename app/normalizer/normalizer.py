from .utils.safe_get import safe_get
from .utils.find_value import find_value
from .utils.find_list import find_list

def normalize_incoming_json(raw_json):
    """
    Convert ANY insurer JSON into the Canonical OptimaAI JSON format.
    """

    # -------------------------
    # CUSTOMER SECTION
    # -------------------------
    customer = {
        "firstName": find_value(raw_json, [
            "customer.firstName",
            "insured.givenName",
            "applicant.firstName",
            "policyHolder.firstName"
        ]) or "",
        "lastName": find_value(raw_json, [
            "customer.lastName",
            "insured.familyName",
            "applicant.lastName",
            "policyHolder.lastName"
        ]) or "",
        "age": find_value(raw_json, [
            "customer.age",
            "insured.age",
            "applicant.age"
        ]),
        "licenseNumber": find_value(raw_json, [
            "customer.licenseNumber",
            "insured.license",
            "applicant.licenseNumber"
        ]) or "",
        "address": {
            "street": find_value(raw_json, [
                "customer.address.street",
                "insured.location.street",
                "riskLocation.street"
            ]) or "",
            "city": find_value(raw_json, [
                "customer.address.city",
                "insured.location.city",
                "riskLocation.city"
            ]) or "",
            "state": find_value(raw_json, [
                "customer.address.state",
                "insured.location.stateCd",
                "riskLocation.state"
            ]) or "",
            "zip": find_value(raw_json, [
                "customer.address.zip",
                "insured.location.postalCode",
                "riskLocation.zipCode"
            ]) or ""
        },
        "raw": raw_json.get("customer", {})
    }

    # -------------------------
    # DRIVERS SECTION
    # -------------------------
    raw_drivers = find_list(raw_json, [
        "drivers",
        "operatorList",
        "driverInfo",
        "riskDrivers"
    ])

    drivers = []
    for d in raw_drivers:
        normalized_driver = {
            "firstName": find_value(d, ["firstName", "fname", "givenName"]) or "",
            "lastName": find_value(d, ["lastName", "lname", "familyName"]) or "",
            "age": find_value(d, ["age"]),
            "licenseNumber": find_value(d, ["licenseNumber", "license"]) or "",
            "accidents": find_value(d, ["accHist", "accidents", "accidentCount"]) or 0,
            "violations": find_value(d, ["violations", "violationCount"]) or 0,
            "majorViolation": find_value(d, ["majorViolation", "majorViol"]) or False
        }

        drivers.append({
            "raw": d,
            "normalized": normalized_driver
        })

    # -------------------------
    # VEHICLES SECTION (FIXED)
    # -------------------------
    raw_vehicles = find_list(raw_json, [
        "vehicles",
        "autos",
        "riskVehicles",
        "vehicleList"
    ])

    vehicles = []
    for v in raw_vehicles:
        normalized_vehicle = {
            "vin": find_value(v, ["vin", "VIN", "vehicleId"]),
            "year": find_value(v, ["year", "modelYear"]),
            "make": find_value(v, ["make", "manufacturer"]),
            "model": find_value(v, ["model", "vehicleModel"]),
            "annualMileage": find_value(v, ["annualMileage", "mileage"])
        }

        vehicles.append({
            "raw": v,
            "normalized": normalized_vehicle
        })

    # -------------------------
    # POLICY SECTION
    # -------------------------
    policy = {
        "state": find_value(raw_json, [
            "policy.state",
            "insured.location.stateCd",
            "riskLocation.state"
        ]),
        "effectiveDate": find_value(raw_json, [
            "policy.effectiveDate",
            "transaction.effectiveDate"
        ]),
        "expirationDate": find_value(raw_json, [
            "policy.expirationDate",
            "transaction.expirationDate"
        ]),
        "transactionId": find_value(raw_json, [
            "policy.transactionId",
            "transaction.id"
        ]),
        "sourceSystem": find_value(raw_json, [
            "sourceSystem",
            "system",
            "origin"
        ]),
        "raw": raw_json.get("policy", {})
    }

    # -------------------------
    # APPLICANT (for PDF)
    # -------------------------
    raw_applicant = raw_json.get("applicant", {})

    applicant = {
        "name": raw_applicant.get("name", ""),
        "state": raw_applicant.get("state", ""),
        "zip": raw_applicant.get("zip", ""),
        "address": raw_applicant.get("address", ""),
        "raw": raw_applicant
    }

    # -------------------------
    # RISK SECTION (for PDF)
    # -------------------------
    risk = {
        "score": find_value(raw_json, [
            "risk.score",
            "underwriting.riskScore",
            "uw.risk.score",
            "score"
        ]),
        "eligibility": find_value(raw_json, [
            "risk.eligibility",
            "underwriting.eligibility",
            "uw.eligibility",
            "eligibility"
        ]),
        "topDrivers": find_list(raw_json, [
            "risk.topDrivers",
            "underwriting.topRiskDrivers",
            "uw.riskDrivers"
        ])
    }

    # -------------------------
    # PRICING SECTION (for PDF)
    # -------------------------
    pricing = {
        "finalPremium": find_value(raw_json, [
            "pricing.finalPremium",
            "premium.final",
            "premium.total",
            "finalPremium"
        ]),
        "base": find_value(raw_json, [
            "pricing.base",
            "premium.base",
            "basePremium"
        ]),
        "driverImpact": find_value(raw_json, [
            "pricing.driverImpact",
            "premium.driverImpact"
        ]),
        "vehicleImpact": find_value(raw_json, [
            "pricing.vehicleImpact",
            "premium.vehicleImpact"
        ]),
        "zipImpact": find_value(raw_json, [
            "pricing.zipImpact",
            "premium.zipImpact"
        ]),
        "coverageImpact": find_value(raw_json, [
            "pricing.coverageImpact",
            "premium.coverageImpact"
        ]),
        "discounts": find_value(raw_json, [
            "pricing.discounts",
            "premium.discounts"
        ]),
        "narrative": find_value(raw_json, [
            "pricing.narrative",
            "premium.narrative",
            "pricingNotes"
        ]),
        "topPricingFactors": find_list(raw_json, [
            "pricing.topPricingFactors",
            "pricing.factors",
            "underwriting.pricingFactors"
        ])
    }

    # -------------------------
    # SUMMARY SECTION (for PDF)
    # -------------------------
    summary = {
        "narrative": find_value(raw_json, [
            "summary.narrative",
            "underwriting.summary",
            "uw.summary",
            "executiveSummary",
            "narrative"
        ])
    }

    # -------------------------
    # COMPLIANCE SECTION (for PDF)
    # -------------------------
    compliance = {
        "state": find_value(raw_json, [
            "compliance.state",
            "policy.state",
            "riskLocation.state",
            "insured.location.stateCd"
        ]),
        "overallStatus": find_value(raw_json, [
            "compliance.overallStatus",
            "compliance.status",
            "uw.complianceStatus",
            "underwriting.complianceStatus"
        ]),
        "notes": find_value(raw_json, [
            "compliance.notes",
            "compliance.message",
            "uw.complianceNotes",
            "underwriting.complianceNotes"
        ]),
        "rulesChecked": find_list(raw_json, [
            "compliance.rulesChecked",
            "compliance.rules",
            "uw.rulesChecked",
            "underwriting.rules"
        ])
    }

    # -------------------------
    # AI INSIGHTS SECTION (for PDF)
    # -------------------------
    ai_insights = {
        "driverRisk": find_value(raw_json, [
            "aiInsights.driverRisk",
            "insights.driverRisk",
            "underwriting.driverRisk",
            "uw.driverRisk"
        ]),
        "pricingRationale": find_value(raw_json, [
            "aiInsights.pricingRationale",
            "insights.pricingRationale",
            "underwriting.pricingRationale",
            "uw.pricingRationale"
        ]),
        "underwritingExplanation": find_value(raw_json, [
            "aiInsights.underwritingExplanation",
            "insights.underwritingExplanation",
            "underwriting.explanation",
            "uw.explanation"
        ]),
        "improvementSuggestions": find_value(raw_json, [
            "aiInsights.improvementSuggestions",
            "insights.improvementSuggestions",
            "underwriting.suggestions",
            "uw.suggestions"
        ]),
        "narrative": find_value(raw_json, [
            "aiInsights.narrative",
            "insights.narrative",
            "underwriting.narrative",
            "uw.narrative"
        ])
    }

    # -------------------------
    # DATA LINEAGE SECTION (for PDF)
    # -------------------------
    lineage = {
        "fields": find_list(raw_json, [
            "lineage.fields",
            "dataLineage.fields",
            "traceability.fields"
        ]) or [],
        "missing": find_list(raw_json, [
            "lineage.missing",
            "dataLineage.missing",
            "traceability.missing"
        ]) or []
    }

    # -------------------------
    # GUIDEWIRE SECTION
    # -------------------------
    raw_guidewire = raw_json.get("guidewire", {})

    guidewire = {
        "state": raw_guidewire.get("state") or policy.get("state"),
        "raw": raw_guidewire
    }

    # -------------------------
    # COVERAGE SECTION (FIXED)
    # -------------------------
    raw_coverage = raw_json.get("coverage", {})

    coverage = {
        "liabilityLimit": raw_coverage.get("liabilityLimit")
            or find_value(raw_json, [
                "coverage.liabilityLimit",
                "limits.liability",
                "policy.coverage.liability",
                "liabilityLimit"
            ]),

        "collisionDeductible": raw_coverage.get("collisionDeductible")
            or find_value(raw_json, [
                "coverage.collisionDeductible",
                "deductibles.collision",
                "collisionDeductible"
            ]),

        "comprehensiveDeductible": raw_coverage.get("comprehensiveDeductible")
            or find_value(raw_json, [
                "coverage.comprehensiveDeductible",
                "deductibles.comprehensive",
                "comprehensiveDeductible"
            ]),

        "deductible": raw_coverage.get("deductible")
            or raw_coverage.get("collisionDeductible")
            or find_value(raw_json, [
                "coverage.deductible",
                "deductible",
                "deductibles.collision",
                "coverage.collisionDeductible"
            ]),

        "coverageType": (
            raw_coverage.get("coverageType")
            or find_value(raw_json, [
                "coverage.coverageType",
                "coverage.type",
                "policy.coverage.type",
                "coverageType"
            ])
            or "Standard Auto"
        ),

        "raw": raw_coverage
    }

    # -------------------------
    # FINAL CANONICAL STRUCTURE
    # -------------------------
    normalized = {
        "customer": customer,
        "applicant": applicant,
        "drivers": drivers,
        "vehicles": vehicles,
        "coverage": coverage,
        "policy": policy,
        "guidewire": guidewire,

        "pricing": pricing,
        "risk": risk,
        "summary": summary,
        "compliance": compliance,
        "aiInsights": ai_insights,
        "lineage": lineage
    }

    return normalized
