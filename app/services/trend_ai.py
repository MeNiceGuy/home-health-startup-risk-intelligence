import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_trend_insights(scores):
    if not scores:
        return "No intelligence history is available yet. Run at least one operating audit to generate trend insights."

    score_text = ""
    for row in scores[:10]:
        agency, audit, total, compliance, clinical, revenue, operations, date = row
        score_text += f"""
Date: {date}
Agency: {agency}
Audit: {audit}
Total: {total}
Compliance: {compliance}
Clinical: {clinical}
Revenue: {revenue}
Operations: {operations}
"""

    prompt = f"""
You are a healthcare business intelligence analyst for Boswell Consulting Group.

Analyze this agency intelligence score history:

{score_text}

Write a concise executive insight report with:
1. Overall trend
2. Biggest operating risk
3. Strongest area
4. Weakest area
5. Recommended next action
6. Whether the agency should consider subscription monitoring

Keep it professional and strategic.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text


