from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
from datetime import datetime
import re

def safe_filename(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "client"

def get_priority(item):
    critical = [
        "No RN clinical supervisor",
        "Clinical leadership not qualified",
        "Licensing documentation incomplete",
        "No defined payer strategy"
    ]

    high = [
        "Policies and procedures not prepared",
        "HIPAA system not in place",
        "No documentation system selected",
        "Not prepared for state inspection"
    ]

    for phrase in critical:
        if phrase in item:
            return "CRITICAL"

    for phrase in high:
        if phrase in item:
            return "HIGH"

    return "MEDIUM"

def generate_audit_pdf(result, fixes, agency_name, owner_name, location, start_date):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    agency_slug = safe_filename(agency_name)
    filename = reports_dir / f"{agency_slug}_audit_report_{timestamp}.pdf"

    doc = SimpleDocTemplate(str(filename))
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Home Health Startup Risk & Readiness Intelligence Report", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Agency: {agency_name}", styles["Normal"]))
    content.append(Paragraph(f"Owner: {owner_name}", styles["Normal"]))
    content.append(Paragraph(f"Location: {location}", styles["Normal"]))
    content.append(Paragraph(f"Target Start Date: {start_date}", styles["Normal"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Startup Risk Score: {result['risk_score']}/100", styles["Heading2"]))
    content.append(Paragraph(f"Risk Classification: {result['risk_tier']}", styles["Heading3"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("Immediate Next Best Action", styles["Heading2"]))
    if result["missing_items"]:
        first_item = result["missing_items"][0]
        content.append(Paragraph(f"{get_priority(first_item)} - {first_item}", styles["Normal"]))
    else:
        content.append(Paragraph("No immediate critical action identified.", styles["Normal"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("Risk Diagnosis", styles["Heading2"]))
    content.append(Paragraph(
        "The agency is currently exposed to operational and regulatory risk due to missing critical startup components. "
        "These gaps may delay licensing, prevent operational readiness, or result in compliance failure during inspection.",
        styles["Normal"]
    ))

    content.append(Spacer(1, 10))

    content.append(Paragraph("Prioritized Risk Areas Identified", styles["Heading2"]))
    for item in result["missing_items"]:
        content.append(Paragraph(f"- {get_priority(item)}: {item}", styles["Normal"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("Required Corrective Actions", styles["Heading2"]))
    for fix in fixes:
        content.append(Paragraph("- " + fix, styles["Normal"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("Failure Risk Warning", styles["Heading2"]))
    content.append(Paragraph(
        "If the above issues are not resolved, the agency may face licensing delays, failed inspections, inability to operate legally, or financial instability.",
        styles["Normal"]
    ))

    content.append(Spacer(1, 10))

    content.append(Paragraph("90-Day De-Risking Plan", styles["Heading2"]))
    content.append(Paragraph(
        "1. Complete licensing application<br/>"
        "2. Secure qualified clinical leadership<br/>"
        "3. Develop full compliance and policy framework<br/>"
        "4. Implement operational and documentation systems<br/>"
        "5. Prepare for inspection and launch readiness",
        styles["Normal"]
    ))

    doc.build(content)
    return str(filename)
