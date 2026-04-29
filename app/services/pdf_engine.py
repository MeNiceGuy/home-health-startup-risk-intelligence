from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from app.services.benchmark_audit import audit_from_inputs


def build_recommended_slugs(audit):
    impact = audit.get("total_estimated_impact", 0)
    score = audit.get("total_score", 100)

    if impact >= 30000 or score < 65:
        return ["full-optimization"]

    keys = [f.get("key") for f in audit.get("findings", []) if isinstance(f, dict)]
    slugs = []

    if "denial_rate" in keys or "ar_days" in keys:
        slugs.append("revenue")
    if "intake_time" in keys or "missed_visits" in keys:
        slugs.append("operations")
    if "staff_turnover" in keys:
        slugs.append("hiring")
    if "compliance_findings" in keys:
        slugs.append("compliance")

    return list(dict.fromkeys(slugs))


def build_recommended_solutions(audit):
    slugs = build_recommended_slugs(audit)

    names = {
        "revenue": "Revenue Cycle Policy Pack",
        "operations": "Operations Workflow System",
        "hiring": "Hiring & Onboarding Kit",
        "compliance": "Compliance Readiness Pack",
        "full-optimization": "Full Agency Optimization System (Recommended)"
    }

    return [names.get(s, s) for s in slugs]


def generate_consulting_audit_pdf(inputs, output_path="audit_report.pdf"):
    audit = audit_from_inputs(inputs)
    solutions = build_recommended_solutions(audit)
    slugs = build_recommended_slugs(audit)

    checkout_url = "http://127.0.0.1:8000/cart/add-bundle?kits=" + ",".join(slugs)

    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Home Health Performance Audit", styles["Title"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    story.append(Paragraph(
        audit.get("executive_summary", {}).get("narrative", "Audit summary unavailable."),
        styles["BodyText"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Key Metrics", styles["Heading2"]))
    story.append(Paragraph(f"Total Score: {audit.get('total_score', 0)}%", styles["BodyText"]))
    story.append(Paragraph(f"Performance Tier: {audit.get('tier', 'N/A')}", styles["BodyText"]))
    story.append(Paragraph(f"Estimated Monthly Impact: ${audit.get('total_estimated_impact', 0):,}", styles["BodyText"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Priority Roadmap", styles["Heading2"]))
    for r in audit.get("roadmap", []):
        story.append(Paragraph(
            f"Priority {r['priority']}: {r['focus']} - {r['action']}",
            styles["BodyText"]
        ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Implementation Timeline", styles["Heading2"]))
    timeline = [
        "Week 1: Stabilize the highest revenue leakage area.",
        "Week 2: Implement workflow controls and accountability checks.",
        "Week 3: Strengthen staffing, compliance, and documentation processes.",
        "Week 4: Review results, monitor KPIs, and adjust operating cadence."
    ]
    for item in timeline:
        story.append(Paragraph(item, styles["BodyText"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Expected Outcomes", styles["Heading2"]))
    story.append(Paragraph(
        "If implemented effectively, the agency can target improved revenue-cycle discipline, reduced leakage, stronger intake execution, and better compliance readiness.",
        styles["BodyText"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Recommended Solutions", styles["Heading2"]))
    for s in solutions:
        story.append(Paragraph(f"- {s}", styles["BodyText"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Recommended Next Step", styles["Heading2"]))
    story.append(Paragraph(
        f"<a href='{checkout_url}'>Click here to add the recommended implementation bundle to cart</a>",
        styles["BodyText"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Disclaimer", styles["Heading2"]))
    story.append(Paragraph(
        "This audit is a decision-support tool and not a regulatory determination, legal opinion, financial guarantee, or official CMS assessment.",
        styles["BodyText"]
    ))

    doc.build(story)
    return output_path


def generate_audit_pdf(*args, **kwargs):
    return generate_consulting_audit_pdf({}, "audit_report.pdf")


def generate_paid_audit_pdf(output_path="audit_report.pdf", data=None):
    return generate_consulting_audit_pdf(data or {}, output_path)
