from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
from datetime import datetime
import re

def safe_name(text):
    return re.sub(r"[^a-zA-Z0-9_-]", "_", text or "client")

def generate_ai_kit_pdf(client_data, kit_name, kit_content):
    Path("generated_kits").mkdir(exist_ok=True)

    agency = safe_name(client_data.get("agency_name", "client"))
    kit = safe_name(kit_name)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_kits/{agency}_{kit}_{stamp}.pdf"

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"Boswell Consulting Group | {kit_name}", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Prepared For: {client_data.get('agency_name', 'Client Agency')}", styles["Normal"]))
    story.append(Paragraph(f"Location: {client_data.get('location', 'N/A')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    for line in kit_content.splitlines():
        line = line.strip()
        if not line:
            story.append(Spacer(1, 8))
        elif line[:2] in ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8."]:
            story.append(Paragraph(line, styles["Heading2"]))
        else:
            story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)
    return filename
