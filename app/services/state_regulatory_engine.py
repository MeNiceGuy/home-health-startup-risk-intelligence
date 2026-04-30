REGULATORY_RULES = {
    "virginia": {
        "display": "Virginia",
        "authority": "Virginia Department of Health / 12VAC5-381",
        "source_note": "Virginia home care organizations are regulated under 12VAC5-381.",
        "startup_requirements": [
            "Obtain required Virginia home care organization license before operation.",
            "Establish management and administration structure.",
            "Prepare policies and procedures.",
            "Prepare documentation, patient rights, infection control, and emergency preparedness processes.",
            "For skilled or medical services, maintain appropriate clinical oversight."
        ],
        "operating_requirements": [
            "Maintain compliance with 12VAC5-381.",
            "Maintain documentation and patient records.",
            "Follow internal policies and procedures.",
            "Prepare for inspections, surveys, and complaint investigations.",
            "Maintain clinical oversight when providing skilled services."
        ]
    },
    "north_carolina": {
        "display": "North Carolina",
        "authority": "NC DHHS / DHSR / 10A NCAC 13J",
        "source_note": "North Carolina home care agency licensure is governed through DHSR resources and 10A NCAC 13J.",
        "startup_requirements": [
            "Complete North Carolina home care agency licensure process.",
            "Prepare application materials, policies, training, and operational readiness documentation.",
            "Prepare for initial licensure survey or review.",
            "Maintain personnel, client rights, documentation, and service delivery systems.",
            "For Medicare-certified home health, also prepare for federal CMS requirements."
        ],
        "operating_requirements": [
            "Maintain compliance with 10A NCAC 13J.",
            "Keep personnel files, training records, and documentation audit-ready.",
            "Maintain client rights, care records, incident processes, and complaint readiness.",
            "Prepare for survey or complaint investigation.",
            "Monitor payer, referral, staffing, and operational performance."
        ]
    },
    "federal": {
        "display": "Federal",
        "authority": "CMS / 42 CFR Part 484 / HIPAA",
        "source_note": "Federal Medicare home health agencies must meet CMS Conditions of Participation under 42 CFR Part 484.",
        "requirements": [
            "Patient rights process.",
            "Comprehensive assessment process.",
            "Care planning and coordination of services.",
            "Quality assessment and performance improvement.",
            "OASIS reporting when applicable.",
            "Administrative and supervisory controls.",
            "HIPAA privacy and security safeguards."
        ]
    }
}

def normalize_state(state):
    value = (state or "").strip().lower().replace("-", "_")
    if value in ["va", "virginia"]:
        return "virginia"
    if value in ["nc", "north_carolina", "north carolina"]:
        return "north_carolina"
    return None

def is_medical_model(agency_type):
    value = (agency_type or "").lower()
    return value in ["medical", "skilled", "home_health", "home health", "medical / skilled home health"]

def uses_federal_medicare(payer_model):
    value = (payer_model or "").lower()
    return value in ["medicare", "hybrid"]

def generate_regulatory_intelligence(state, agency_type, payer_model, answers):
    state_key = normalize_state(state)
    medical = is_medical_model(agency_type)
    medicare = uses_federal_medicare(payer_model)

    if not state_key:
        return {
            "state": state or "Unknown",
            "authority": "Unsupported state",
            "risk_level": "Unsupported",
            "findings": ["This state is not currently supported. Current supported states: Virginia and North Carolina."],
            "blockers": [],
            "recommended_kits": [],
            "startup_requirements": [],
            "operating_requirements": []
        }

    state_rules = REGULATORY_RULES[state_key]
    federal = REGULATORY_RULES["federal"]

    findings = []
    blockers = []
    recommended_kits = []

    findings.append(f"State regulatory framework detected: {state_rules['authority']}.")

    if answers.get("license_docs_ready") != "yes":
        blockers.append("Licensing documentation is incomplete.")
        recommended_kits.append("State License Application Kit")

    if answers.get("policies_ready") != "yes":
        blockers.append("Policies and procedures are not fully prepared.")
        recommended_kits.append("Policies & Procedures Template Pack")

    if answers.get("inspection_ready") != "yes":
        blockers.append("Inspection or survey readiness is incomplete.")
        recommended_kits.append("Inspection / Survey Readiness Kit")

    if answers.get("documentation_system") not in ["yes"]:
        blockers.append("Documentation or EMR system is not fully selected or active.")
        recommended_kits.append("HIPAA Records Process Kit")

    if answers.get("hipaa_system") != "yes":
        blockers.append("HIPAA records process is incomplete.")
        recommended_kits.append("HIPAA Records Process Kit")

    if medical and answers.get("rn_secured") not in ["yes", "contracted"]:
        blockers.append("Clinical oversight appears incomplete for medical or skilled services.")
        recommended_kits.append("Administrator & Clinical Leadership Kit")

    if medical and answers.get("clinical_qualified") != "yes":
        blockers.append("Clinical leadership qualifications are not confirmed.")
        recommended_kits.append("Administrator & Clinical Leadership Kit")

    if medicare:
        findings.append(f"Federal Medicare readiness triggered: {federal['authority']}.")
        if answers.get("qa_process") != "yes":
            blockers.append("QAPI / QA process is not ready for Medicare-level compliance.")
            recommended_kits.append("Compliance QA System")
        if answers.get("revenue_timeline") != "yes":
            blockers.append("Medicare or hybrid reimbursement timeline is not fully understood.")
            recommended_kits.append("Revenue Intelligence System")

    if state_key == "north_carolina":
        findings.append("North Carolina pathway requires close attention to DHSR licensure steps, survey readiness, personnel records, and client rights processes.")
        if answers.get("background_check_process") != "yes":
            blockers.append("Staff screening / background check workflow is incomplete.")
            recommended_kits.append("Staff Training & Personnel Compliance Kit")

    if state_key == "virginia":
        findings.append("Virginia pathway requires strong alignment with home care organization administration, policy, documentation, and inspection readiness requirements.")
        if answers.get("business_registered") != "yes":
            blockers.append("Business entity formation is incomplete before licensing preparation.")
            recommended_kits.append("Launch Foundation Bundle")

    blocker_count = len(blockers)
    if blocker_count >= 6:
        risk_level = "Critical Regulatory Risk"
    elif blocker_count >= 3:
        risk_level = "High Regulatory Risk"
    elif blocker_count >= 1:
        risk_level = "Moderate Regulatory Risk"
    else:
        risk_level = "Low Regulatory Risk"

    return {
        "state": state_rules["display"],
        "authority": state_rules["authority"],
        "risk_level": risk_level,
        "findings": findings,
        "blockers": blockers,
        "recommended_kits": list(dict.fromkeys(recommended_kits)),
        "startup_requirements": state_rules["startup_requirements"],
        "operating_requirements": state_rules["operating_requirements"],
        "federal_requirements": federal["requirements"] if medicare else []
    }


