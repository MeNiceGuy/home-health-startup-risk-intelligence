import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TEMPLATE_PRODUCTS = {
    "billing": "Billing & Denial Workflow Template",
    "revenue": "Revenue Cycle Policy Pack",
    "intake": "Intake & Scheduling SOP",
    "operations": "Operations Workflow System",
    "hiring": "Hiring & Onboarding Kit",
    "staff": "Staff Retention System",
    "compliance": "Compliance Policy Pack",
    "incidents": "Incident Reporting System"
}

def generate_tailored_template(slug, client_data):
    name = TEMPLATE_PRODUCTS.get(slug, "Custom Home Health Template")

    prompt = f"""
Create a professional, ready-to-use home health agency document.

Document: {name}
Agency: {client_data.get("agency_name", "Client Agency")}
State: {client_data.get("state", "Virginia or North Carolina")}
Agency Type: {client_data.get("agency_type", "Home Health / Home Care")}
Client Email: {client_data.get("email", "N/A")}

Include:
1. Purpose
2. Scope
3. Policy Statement
4. Step-by-step procedure
5. Staff responsibilities
6. Required documentation
7. Quality control process
8. Compliance notes
9. Implementation checklist
10. Disclaimer: educational business guidance, not legal advice

Make it practical, professional, and tailored for a startup or operating agency.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return name, response.output_text


