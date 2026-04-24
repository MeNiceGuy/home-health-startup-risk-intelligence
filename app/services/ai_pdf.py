from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
from datetime import datetime
import re

def safe_filename(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "client"

def generate_ai_kit_pdf(client_data, kit_name, kit_content):
    reports_dir = Path("generated_kits")
    reports_dir.mkdir(exist_ok=True)

    agency = safe_filename(client_data.get("agency_name", "client"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = reports_dir / f"{agency}_{safe_filename(kit_name)}_{timestamp}.pdf"

    doc = SimpleDocTemplate(str(filename))
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(f"Boswell Consulting Group | {kit_name}", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Prepared for: {client_data.get('agency_name', 'N/A')}", styles["Normal"]))
    content.append(Paragraph(f"Owner: {client_data.get('owner_name', 'N/A')}", styles["Normal"]))
    content.append(Paragraph(f"Location: {client_data.get('location', 'N/A')}", styles["Normal"]))
    content.append(Paragraph(f"Target Start Date: {client_data.get('start_date', 'N/A')}", styles["Normal"]))
    content.append(Spacer(1, 12))

    for line in kit_content.split("\n"):
        line = line.strip()
        if not line:
            content.append(Spacer(1, 8))
        elif line.endswith(":") or line.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.")):
            content.append(Paragraph(line, styles["Heading3"]))
        else:
            content.append(Paragraph(line, styles["Normal"]))

    doc.build(content)
    return str(filename)
