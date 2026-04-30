def calculate_risk_score(answers: dict):
    base_score = 100

    penalties = {
        # CRITICAL
        "rn_secured": 20,
        "clinical_qualified": 20,
        "license_docs_ready": 15,
        "revenue_model": 15,

        # HIGH
        "policies_ready": 10,
        "hipaa_system": 10,
        "documentation_system": 10,
        "inspection_ready": 10,

        # MEDIUM
        "qa_process": 5,
        "background_check_process": 5,
        "intake_process": 5,
        "revenue_timeline": 5,
    }

    messages = {
        "rn_secured": "No RN clinical supervisor (cannot operate legally)",
        "clinical_qualified": "Clinical leadership not qualified",
        "license_docs_ready": "Licensing documentation incomplete",
        "revenue_model": "No defined payer strategy",
        "policies_ready": "Policies and procedures not prepared",
        "hipaa_system": "HIPAA system not in place",
        "documentation_system": "No documentation system selected",
        "inspection_ready": "Not prepared for state inspection",
        "qa_process": "No quality assurance process",
        "background_check_process": "No background check workflow",
        "intake_process": "No patient intake process",
        "revenue_timeline": "No understanding of reimbursement timeline",
    }

    missing_items = []

    for key, penalty in penalties.items():
        if answers.get(key) != "yes":
            base_score -= penalty
            missing_items.append(messages[key])

    # Prevent unrealistic floor
    score = max(base_score, 20)

    if score >= 80:
        tier = "Low Risk"
    elif score >= 60:
        tier = "Moderate Risk"
    else:
        tier = "High Risk"

    return {
        "risk_score": score,
        "risk_tier": tier,
        "missing_items": missing_items
    }


