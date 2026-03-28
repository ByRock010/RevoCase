import json
import logging
import httpx
from openai import OpenAI
from app.config import OPENAI_API_KEY

logger = logging.getLogger(__name__)


def fetch_website_content(url: str) -> str:
    """Fetch and extract text content from a company website."""
    if not url.startswith("http"):
        url = f"https://{url}"
    try:
        response = httpx.get(url, timeout=10, follow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (compatible; RevoCase/1.0)"
        })
        response.raise_for_status()
        html = response.text

        # Strip HTML tags to get raw text
        import re
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        # Limit to first 3000 chars to stay within token limits
        return text[:3000]
    except Exception as e:
        logger.warning(f"Could not fetch website {url}: {e}")
        return ""


def generate_company_analysis(name: str, hq: str, website: str) -> dict:
    """Use OpenAI GPT-4o-mini to generate company summary and 5 competitors."""
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Fetch actual website content for context
    site_content = fetch_website_content(website)

    website_context = ""
    if site_content:
        website_context = f"""
Here is the actual content scraped from the company's website for accurate context:
---
{site_content}
---
Use the above website content as your PRIMARY source of information about what this company does. Do NOT guess or hallucinate if the website content clearly describes the company.
"""

    prompt = f"""You are a senior business intelligence analyst. Analyze the following company and produce a structured competitive landscape report.

Company: {name}
Headquarters: {hq}
Website: {website}
{website_context}
Your task:
1. Write a concise summary of the company covering: what they do, their core product/service, target market, notable strengths, and a key recent development or strategic focus.
2. Identify exactly 5 real, well-known competitors in the same industry or market segment.
3. For each competitor, write a concise summary covering: what they do, how they compete with {name}, their key differentiator, market position, and a notable strength or weakness relative to {name}.

Rules:
- Each summary must have exactly 5 bullet points.
- Each bullet point must be one concise sentence (max 15 words).
- Competitors must be real companies, not fictional.
- Prefer direct competitors over tangential ones.
- Base your analysis on the website content provided, not assumptions from the company name.

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
        model="gpt-4o",
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
