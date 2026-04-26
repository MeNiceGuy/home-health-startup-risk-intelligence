import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ai_enabled():
    return bool(os.getenv("OPENAI_API_KEY"))

def read_text_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()[:12000]
    except Exception:
        return ""

def analyze_uploaded_business_file(client_name, filename, filepath):
    if not ai_enabled():
        return """
Executive Summary:
AI analysis is not active because OPENAI_API_KEY is missing.

Recommended Fix:
Add OPENAI_API_KEY to your local environment and Render environment variables.

Next Step:
Once the key is added, uploaded files will generate detailed operational, compliance, staffing, revenue cycle, and policy intelligence reports.
"""
    content = read_text_file(filepath)

    if not content.strip():
        content = "The uploaded file could not be text-extracted. Provide a high-level consultant review based on filename and expected home health business document type."

    prompt = f"""
You are a senior home health business operations, compliance, staffing, and revenue cycle consultant.

Client business: {client_name}
Uploaded file: {filename}

Document content:
{content}

Create a detailed consultant intelligence report with these sections:

1. Executive Summary
2. What This Document Appears To Be
3. Operational Gaps Identified
4. Compliance Risks
5. Staffing / Administrative Risks
6. Revenue Cycle or Billing Risks
7. Missing Policies, SOPs, or Controls
8. Recommended Fixes
9. Recommended Template Kits to Sell
10. 30-Day Action Plan
11. Consultant Talking Points

Make the report practical, direct, and business-focused.
Do not give legal advice. Include a disclaimer that this is business and compliance-readiness guidance, not legal counsel.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text

