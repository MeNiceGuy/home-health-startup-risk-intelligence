import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_custom_kit(client_data, kit_name, kit_slug):
    prompt = f"""
Create a professional implementation kit for a home health agency.

Kit: {kit_name}
Agency: {client_data.get("agency_name", "Client Agency")}
Owner/Email: {client_data.get("owner_name", "Client")}
Location: {client_data.get("location", "N/A")}
State: {client_data.get("state", "N/A")}

Include:
1. Executive Summary
2. Why This Matters
3. Step-by-Step Implementation Plan
4. Required Documents
5. Compliance Considerations
6. Common Mistakes
7. 30-Day Action Plan
8. Disclaimer: educational guidance, not legal advice

Make it specific, practical, and professional.
"""
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return response.output_text
