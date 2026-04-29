
def build_executive_summary(audit):
    findings = audit.get("findings", [])
    total_impact = audit.get("total_estimated_impact", 0)
    score = audit.get("total_score", 0)

    top = sorted(findings, key=lambda x: x.get("estimated_impact", 0), reverse=True)[:3]
    top_issues = [f.get("label") for f in top]

    return {
        "top_issues": top_issues,
        "monthly_impact": total_impact,
        "score": score,
        "narrative": (
            "The agency is currently operating below benchmark in key performance areas. "
            f"Primary pressure is driven by {', '.join(top_issues)} which are contributing "
            "to measurable revenue and operational inefficiencies."
        )
    }


def build_priority_roadmap(audit):
    findings = audit.get("findings", [])
    ordered = sorted(findings, key=lambda x: x.get("estimated_impact", 0), reverse=True)

    roadmap = []
    for i, f in enumerate(ordered[:3], start=1):
        roadmap.append({
            "priority": i,
            "focus": f.get("label"),
            "action": f"Address {f.get('label')} to reduce performance gap and improve efficiency"
        })

    return roadmap

from app.services.cms_data import get_cms_benchmarks, get_agency_cms_profile, extract_performance_metrics, get_percentile_rankings

BENCHMARKS = {
    "denial_rate": {
        "label": "Denial Rate",
        "benchmark": 10,
        "unit": "%",
        "category": "Financial",
        "why": "Higher denial rates reduce collected revenue and increase billing rework."
    },
    "ar_days": {
        "label": "A/R Days",
        "benchmark": 35,
        "unit": "days",
        "category": "Financial",
        "why": "Higher A/R days slow cash flow and increase collection risk."
    },
    "intake_time": {
        "label": "Intake Completion Time",
        "benchmark": 2,
        "unit": "days",
        "category": "Operations",
        "why": "Slow intake delays care starts and can reduce referral conversion."
    },
    "missed_visits": {
        "label": "Missed Visits",
        "benchmark": 5,
        "unit": "%",
        "category": "Operations",
        "why": "Missed visits create care gaps, operational waste, and compliance exposure."
    },
    "staff_turnover": {
        "label": "Staff Turnover",
        "benchmark": 25,
        "unit": "%",
        "category": "Staffing",
        "why": "High turnover weakens continuity, scheduling stability, and care reliability."
    },
    "compliance_findings": {
        "label": "Compliance Findings",
        "benchmark": 2,
        "unit": "findings",
        "category": "Compliance",
        "why": "More findings increase audit exposure and indicate weak internal controls."
    }
}

def validate_inputs(inputs):
    cleaned = {}

    defaults = {
        "denial_rate": 10,
        "ar_days": 35,
        "intake_time": 2,
        "missed_visits": 5,
        "staff_turnover": 25,
        "compliance_findings": 2
    }

    bounds = {
        "denial_rate": (0, 100),
        "ar_days": (0, 180),
        "intake_time": (0, 30),
        "missed_visits": (0, 100),
        "staff_turnover": (0, 200),
        "compliance_findings": (0, 50)
    }

    for key in BENCHMARKS.keys():
        raw = inputs.get(key, defaults[key])

        try:
            value = float(raw)
        except:
            value = defaults[key]

        low, high = bounds[key]
        if value < low or value > high:
            value = defaults[key]

        cleaned[key] = value

    cleaned["agency_name"] = inputs.get("agency_name") or ""
    cleaned["state"] = inputs.get("state") or ""

    return cleaned

def score_metric(value, benchmark):
    value = float(value)
    benchmark = float(benchmark)

    if value <= benchmark:
        return 100
    elif value <= benchmark * 1.25:
        return 85
    elif value <= benchmark * 1.5:
        return 70
    elif value <= benchmark * 2:
        return 50
    else:
        return 25

def risk_label(score):
    if score >= 85:
        return "Low Risk"
    elif score >= 70:
        return "Moderate Risk"
    elif score >= 50:
        return "High Risk"
    return "Critical Risk"

def confidence_level(inputs):
    missing = [k for k, v in inputs.items() if v is None or v == ""]
    if not missing:
        return "High"
    if len(missing) <= 2:
        return "Moderate"
    return "Low"

def data_quality_score(inputs):
    required = list(BENCHMARKS.keys())
    valid = sum(1 for k in required if inputs.get(k) is not None)
    return int((valid / len(required)) * 100)

def performance_tier(score):
    if score >= 85:
        return "Top Tier"
    elif score >= 70:
        return "Above Average"
    elif score >= 50:
        return "Below Average"
    return "High Risk Tier"

def metric_revenue_impact(key, value, benchmark):
    gap = max(0, float(value) - float(benchmark))

    if key == "denial_rate":
        return int(gap * 2500)
    if key == "ar_days":
        return int(gap * 500)
    if key == "intake_time":
        return int(gap * 3500)
    if key == "missed_visits":
        return int(gap * 1200)
    if key == "staff_turnover":
        return int(gap * 600)
    if key == "compliance_findings":
        return int(gap * 1500)

    return 0





def audit_from_inputs(inputs):
    inputs = validate_inputs(inputs)

    cms = get_cms_benchmarks()
    agency_profile = get_agency_cms_profile(inputs.get("agency_name", ""), inputs.get("state", ""))

    agency_metrics = {}
    percentile_rankings = {}

    if agency_profile.get("matched"):
        profile = agency_profile.get("profile", {})
        agency_metrics = extract_performance_metrics(profile)
        percentile_rankings = get_percentile_rankings(profile)

    findings = []
    category_scores = {}

    for key, meta in BENCHMARKS.items():
        value = inputs.get(key)
        benchmark = meta["benchmark"]
        score = score_metric(value, benchmark)
        gap = round(float(value) - float(benchmark), 2)
        impact = metric_revenue_impact(key, value, benchmark)

        finding = {
            "key": key,
            "label": meta["label"],
            "category": meta["category"],
            "value": value,
            "benchmark": benchmark,
            "unit": meta["unit"],
            "gap": gap,
            "score": score,
            "risk": risk_label(score),
            "why": meta["why"],
            "estimated_impact": impact
        }

        findings.append(finding)
        category_scores.setdefault(meta["category"], []).append(score)

    categories = {
        category: int(sum(scores) / len(scores))
        for category, scores in category_scores.items()
    }

    total = int(sum(categories.values()) / len(categories)) if categories else 0
    total_estimated_impact = sum(f.get("estimated_impact", 0) for f in findings)

    recommended_kits = recommend_kits({
        "findings": findings,
        "total_estimated_impact": total_estimated_impact,
        "total_score": total
    })

    recommended_kits = recommend_kits({
        "findings": findings,
        "total_estimated_impact": total_estimated_impact,
        "total_score": total
    })

    executive_summary = build_executive_summary({
        "findings": findings,
        "total_estimated_impact": total_estimated_impact,
        "total_score": total
    })

    roadmap = build_priority_roadmap({
        "findings": findings
    })

    return {
        "executive_summary": executive_summary,
        "roadmap": roadmap,
        "recommended_kits": recommended_kits,
        "recommended_kits": recommended_kits,
        "cms_data": cms,
        "agency_cms_profile": agency_profile,
        "agency_metrics": agency_metrics,
        "percentile_rankings": percentile_rankings,
        "total_score": total,
        "tier": performance_tier(total),
        "categories": categories,
        "findings": findings,
        "estimated_loss": total_estimated_impact,
        "total_estimated_impact": total_estimated_impact,
        "confidence": confidence_level(inputs),
        "data_quality": data_quality_score(inputs)
    }




def recommend_kits(audit):
    findings = audit.get("findings", [])
    total_impact = audit.get("total_estimated_impact", 0)
    score = audit.get("total_score", 100)

    # Severity override → Full system only
    if total_impact >= 30000 or score < 65:
        return ["full-optimization"]

    kits = set()

    for f in findings:
        key = f.get("key")

        if key in ["denial_rate", "ar_days"]:
            kits.add("revenue")

        if key in ["intake_time", "missed_visits"]:
            kits.add("operations")

        if key == "staff_turnover":
            kits.add("hiring")

        if key == "compliance_findings":
            kits.add("compliance")

    return list(kits)





