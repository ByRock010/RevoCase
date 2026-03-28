import json
from openai import OpenAI
from app.config import OPENAI_API_KEY


def generate_company_analysis(name: str, hq: str, website: str) -> dict:
    """Use OpenAI GPT-4o-mini to generate company summary and 5 competitors."""
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""You are a senior business intelligence analyst. Analyze the following company and produce a structured competitive landscape report.

Company: {name}
Headquarters: {hq}
Website: {website}

Your task:
1. Write a concise summary of the company covering: what they do, their core product/service, target market, notable strengths, and a key recent development or strategic focus.
2. Identify exactly 5 real, well-known competitors in the same industry or market segment.
3. For each competitor, write a concise summary covering: what they do, how they compete with {name}, their key differentiator, market position, and a notable strength or weakness relative to {name}.

Rules:
- Each summary must have exactly 5 bullet points.
- Each bullet point must be one concise sentence (max 15 words).
- Competitors must be real companies, not fictional.
- Prefer direct competitors over tangential ones.

Return ONLY valid JSON in this exact format:
{{
  "company_summary": "• Point 1\\n• Point 2\\n• Point 3\\n• Point 4\\n• Point 5",
  "competitors": [
    {{
      "name": "Competitor Name",
      "summary": "• Point 1\\n• Point 2\\n• Point 3\\n• Point 4\\n• Point 5"
    }}
  ]
}}

The competitors array must contain exactly 5 entries."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a business intelligence analyst. You return only valid JSON with no markdown formatting, no code blocks, and no extra text.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )

    text = response.choices[0].message.content.strip()
    return json.loads(text)
