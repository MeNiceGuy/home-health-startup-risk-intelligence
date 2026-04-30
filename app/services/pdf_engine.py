from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

BRAND = "Home Health Performance Intelligence"

def add_header_footer(canvas, doc):
    canvas.saveState()
    width, height = letter

    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(colors.HexColor("#991b1b"))
    canvas.drawString(40, height - 28, BRAND)

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawRightString(width - 40, height - 28, "Revenue Risk & Performance Audit")
    canvas.drawString(40, 24, "Decision-support report | Not legal, clinical, billing, or regulatory advice")
    canvas.drawRightString(width - 40, 24, f"Page {doc.page}")

    canvas.restoreState()

def generate_audit_pdf(audit, output_path="audit_report.pdf"):
    styles = getSampleStyleSheet()
    story = []

    def H(txt):
        story.append(Paragraph(f"<b>{txt}</b>", styles["Heading2"]))
        story.append(Spacer(1, 10))

    def P(txt):
        story.append(Paragraph(txt, styles["Normal"]))
        story.append(Spacer(1, 8))

    def KPI(label, value):
        t = Table([[label, value]], colWidths=[250, 230])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (1,0), colors.whitesmoke),
            ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#d1d5db")),
            ("PADDING", (0,0), (-1,-1), 8),
            ("FONTNAME", (0,0), (0,0), "Helvetica-Bold"),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))

    impact = audit.get("total_estimated_impact", 0)
    ro = audit.get("revenue_opportunity", {})
    market = audit.get("market_analysis", {})
    demand = market.get("demand", {})
    cms = audit.get("cms_percentiles", {})

    # COVER / ONE-PAGE EXECUTIVE SUMMARY
    story.append(Paragraph("<b>Revenue Risk & Performance Audit</b>", styles["Title"]))
    story.append(Spacer(1, 14))
    P("Prepared using CMS benchmark data, market demand indicators, and agency-specific operational inputs.")

    H("One-Page Executive Summary")
    KPI("Estimated Monthly Revenue at Risk", f"${impact:,}")
    KPI("Revenue Opportunity Score", f"{ro.get('score','N/A')}/100")
    KPI("Opportunity Tier", ro.get("tier","N/A"))
    KPI("Senior Market Demand", f"{demand.get('pct_65_plus','N/A')}% age 65+")
    KPI("Recommended System", "Full Agency Optimization System")

    P("<b>Executive Interpretation:</b> The agency shows performance indicators that may signal preventable revenue leakage, operational drag, and unrealized market opportunity.")
    P("<b>Recommended Next Step:</b> Prioritize correction of the highest-impact revenue drivers and implement the Full Agency Optimization System.")
    P("<b>Important Guardrail:</b> This report supports business decision-making only. Findings should be validated against agency records, payer requirements, and applicable regulations.")

    story.append(PageBreak())

    # FULL REPORT
    H("Executive Summary")
    P(f"Estimated monthly revenue at risk: <b>${impact:,}</b>. This indicates potential leakage driven by operational inefficiencies and workflow gaps.")

    H("Revenue Opportunity Score")
    KPI("Score", f"{ro.get('score','N/A')}/100")
    KPI("Tier", ro.get("tier","N/A"))
    P(ro.get("explanation",""))

    H("Market Demand & Performance Positioning")
    P(market.get("insight","Market demand data unavailable."))
    KPI("Senior Population", f"{demand.get('pct_65_plus','N/A')}%")

    if cms:
        H("CMS Benchmark Positioning")
        for k, v in cms.items():
            KPI(k, f"{v.get('value')} | {v.get('percentile')} percentile | n={v.get('sample_size')}")

    H("Primary Revenue Leakage Drivers")
    for f in audit.get("findings", []):
        if isinstance(f, dict):
            P(f"- <b>{f.get('label','Finding')}:</b> {f.get('risk','N/A')} | Impact: ${f.get('estimated_impact',0):,}")
        else:
            P(f"- {f}")

    H("Priority Action Roadmap")
    P("1. Address the highest-impact revenue drivers first.")
    P("2. Stabilize intake and billing workflows.")
    P("3. Strengthen staffing and execution consistency.")
    P("4. Implement operational controls to prevent recurrence.")

    H("Recommended Action")
    P("Implement the <b>Full Agency Optimization System</b> to correct the gaps identified in this report.")
    P("If even a portion of the estimated revenue loss is recovered, the system can pay for itself quickly.")
    P("Activate implementation: http://127.0.0.1:8000/cart/add/full-optimization")

    H("Important Note")
    P("This report is based on publicly available CMS data and user-provided inputs. It is intended for operational insight only and does not constitute legal, clinical, billing, or regulatory advice.")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=42,
        leftMargin=42,
        topMargin=55,
        bottomMargin=45
    )
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    return output_path

def generate_paid_audit_pdf(output_path="audit_report.pdf", data=None):
    from app.services.benchmark_audit import audit_from_inputs
    audit = audit_from_inputs(data or {})
    return generate_audit_pdf(audit, output_path)

def generate_consulting_audit_pdf(inputs, output_path="audit_report.pdf"):
    from app.services.benchmark_audit import audit_from_inputs
    audit = audit_from_inputs(inputs)
    return generate_audit_pdf(audit, output_path)


