import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_custom_kit(client_data, kit_name, kit_slug):
    prompt = f"""
You are writing a professional implementation kit for a home health startup client.

Company: {client_data.get("agency_name")}
Owner: {client_data.get("owner_name")}
Location: {client_data.get("location")}
Target Start Date: {client_data.get("start_date")}

Purchased Kit: {kit_name}

Create a tailored business implementation document with:
1. Executive summary
2. Why this matters
3. Step-by-step action plan
4. Required documents
5. Common mistakes to avoid
6. 30-day execution plan
7. Disclaimer: educational guidance, not legal advice

Keep it professional, practical, and specific to the client.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
