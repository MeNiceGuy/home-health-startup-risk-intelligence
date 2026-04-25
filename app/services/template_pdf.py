from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
from datetime import datetime
import re

def safe_name(text):
    return re.sub(r"[^a-zA-Z0-9_-]", "_", text or "client")

def generate_template_pdf(template_name, content, client_data):
    Path("generated_templates").mkdir(exist_ok=True)

    agency = safe_name(client_data.get("agency_name", "client"))
    doc = safe_name(template_name)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"generated_templates/{agency}_{doc}_{stamp}.pdf"

    pdf = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"Boswell Consulting Group | {template_name}", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Prepared For: {client_data.get('agency_name', 'Client Agency')}", styles["Normal"]))
    story.append(Paragraph(f"State: {client_data.get('state', 'N/A')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    for line in content.splitlines():
        line = line.strip()
        if not line:
            story.append(Spacer(1, 8))
        elif line[:2] in ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9."]:
            story.append(Paragraph(line, styles["Heading2"]))
        else:
            story.append(Paragraph(line, styles["Normal"]))

    pdf.build(story)
    return path
