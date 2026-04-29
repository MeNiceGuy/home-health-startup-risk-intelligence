from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_audit_pdf(result, fixes, agency_name="Your Agency", owner_name="", location="", start_date=""):
    doc = SimpleDocTemplate("audit_report.pdf", pagesize=letter, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
    styles = getSampleStyleSheet()

    title = ParagraphStyle("TitleRed", parent=styles["Title"], textColor=colors.HexColor("#991b1b"), fontSize=22, leading=26)
    h2 = ParagraphStyle("Header", parent=styles["Heading2"], textColor=colors.HexColor("#111827"), fontSize=14, leading=18)
    body = styles["BodyText"]

    score = result.get("score", result.get("total_score", 56))
    financial = result.get("financial", 35)
    operations = result.get("operations", 62)
    staffing = result.get("staffing", 62)
    compliance = result.get("compliance", 68)
    loss = result.get("loss", result.get("estimated_loss", 30500))

    story = []

    story.append(Paragraph("Home Health Performance Intelligence Report", title))
    story.append(Paragraph(f"<b>Agency:</b> {agency_name}", body))
    story.append(Paragraph(f"<b>Location:</b> {location}", body))
    story.append(Paragraph(f"<b>Date:</b> {start_date}", body))
    story.append(Spacer(1, .25 * inch))

    story.append(Paragraph("Executive Summary", h2))
    story.append(Paragraph(
        f"This benchmark-based audit identified an estimated monthly performance impact of <b>${loss:,.0f}</b>. "
        f"The agency's overall score is <b>{score}%</b>, indicating operational, staffing, compliance, or revenue cycle gaps requiring structured corrective action.",
        body
    ))
    story.append(Spacer(1, .2 * inch))

    data = [
        ["Area", "Score", "Risk Signal"],
        ["Financial", f"{financial}%", "Revenue-cycle exposure"],
        ["Operations", f"{operations}%", "Workflow and execution gaps"],
        ["Staffing", f"{staffing}%", "Coverage and retention risk"],
        ["Compliance", f"{compliance}%", "Control-readiness concern"],
        ["Overall", f"{score}%", "Total performance signal"],
    ]

    table = Table(data, colWidths=[2.1*inch, 1.2*inch, 3.1*inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#991b1b")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), .5, colors.HexColor("#d1d5db")),
        ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#f9fafb")),
        ("PADDING", (0,0), (-1,-1), 9),
    ]))
    story.append(table)
    story.append(Spacer(1, .25 * inch))

    story.append(Paragraph("Recommended Corrective Actions", h2))
    for fix in fixes:
        story.append(Paragraph(f"• {fix}", body))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, .18 * inch))
    story.append(Paragraph("Source Notes", h2))
    story.append(Paragraph(
        "This report uses benchmark-based decision logic informed by common home health operational and revenue-cycle indicators, including denial rate, A/R days, intake completion time, missed visits, turnover, and compliance findings.",
        body
    ))

    story.append(Spacer(1, .18 * inch))
    story.append(Paragraph("Disclaimer", h2))
    story.append(Paragraph(
        "This report is a decision-support tool and is not legal advice, a regulatory determination, a financial guarantee, or an official CMS assessment. Estimated impact is directional and should be validated against agency records.",
        body
    ))

    story.append(Spacer(1, .25 * inch))
    story.append(Paragraph("Next Step", h2))
    story.append(Paragraph(
        "Use the recommended kits or full implementation system to convert these findings into corrective action.",
        body
    ))

    doc.build(story)
    return "audit_report.pdf"

def generate_paid_audit_pdf(output_path, data):
    return generate_audit_pdf(
        data,
        [
            "Reduce denial risk through structured revenue-cycle QA.",
            "Improve intake speed with standardized workflow controls.",
            "Reduce missed visits through scheduling and accountability systems.",
            "Strengthen compliance readiness through recurring internal audits.",
            "Stabilize staffing with onboarding, retention, and backup coverage controls."
        ],
        "Home Health Agency",
        "Agency Owner",
        "Local Market",
        "Today"
    )
