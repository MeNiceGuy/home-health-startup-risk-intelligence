def generate_intelligence(result):
    score = result["risk_score"]
    tier = result["risk_tier"]
    missing = result["missing_items"]

    if score < 40:
        readiness = "The agency is not currently launch-ready."
        urgency = "Immediate corrective action is recommended before moving forward."
    elif score < 70:
        readiness = "The agency has partial readiness but still has meaningful launch risk."
        urgency = "The agency should address priority gaps before submitting or expanding operations."
    else:
        readiness = "The agency appears mostly ready, but remaining gaps should be resolved."
        urgency = "Final readiness review is recommended."

    next_action = missing[0] if missing else "Maintain compliance monitoring."

    kit_recommendations = []

    for item in missing:
        if "RN" in item or "Clinical" in item:
            kit_recommendations.append("Administrator & Clinical Leadership Kit")
        elif "Licensing" in item or "payer" in item:
            kit_recommendations.append("Virginia Home Care License Application Kit")
        elif "Policies" in item:
            kit_recommendations.append("Policies & Procedures Template Pack")
        elif "HIPAA" in item or "documentation" in item:
            kit_recommendations.append("HIPAA Records Process Kit")
        elif "inspection" in item or "quality" in item:
            kit_recommendations.append("Inspection Readiness Kit")
        elif "background" in item or "intake" in item:
            kit_recommendations.append("Staff Onboarding Kit")

    return {
        "readiness_diagnosis": readiness,
        "urgency": urgency,
        "next_best_action": next_action,
        "recommended_kits": list(dict.fromkeys(kit_recommendations)),
        "business_impact": "Unresolved gaps may delay licensing, weaken inspection readiness, increase compliance exposure, and slow revenue generation."
    }


