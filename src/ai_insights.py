"""
ai_insights.py

AI-generated business insights for the
AI Business Intelligence Dashboard.

The LLM receives verified metrics calculated
by Python and converts them into plain-English
business insights.
"""

import os
import json

from dotenv import load_dotenv
from google import genai


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# CLIENT
# ============================================================

def get_gemini_client():
    """
    Create and return the Gemini API client.
    """

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file."
        )

    return genai.Client(
        api_key=api_key
    )


# ============================================================
# BUSINESS CONTEXT
# ============================================================

def build_business_context(
    metrics,
    model_metadata
):
    """
    Combine verified dashboard metrics into
    a structured context for the LLM.
    """

    context = {
        "business_metrics": metrics,
        "forecast": model_metadata
    }

    return context


# ============================================================
# PROMPT
# ============================================================

def build_insight_prompt(
    business_context
):
    """
    Build a controlled prompt for the LLM.
    """

    context_json = json.dumps(
        business_context,
        indent=2,
        default=str
    )

    prompt = f"""
You are an experienced business intelligence analyst.

Your task is to analyze the VERIFIED business metrics
provided below and write a concise weekly business report.

IMPORTANT RULES:

1. Use ONLY the numbers provided in the JSON.
2. Do not invent or estimate missing numbers.
3. Do not perform new calculations unless they are
   simple interpretations of the provided values.
4. Do not claim that correlation proves causation.
5. Clearly distinguish observations from recommendations.
6. Do not describe forecasts as guaranteed outcomes.
7. Keep the language understandable to a small-business owner.
8. Focus on actionable business insights.
9. If a metric is missing, do not invent it.
10. Do not mention that you are an AI unless necessary.

Return the response using exactly these sections:

## Executive Summary

Write 2-3 sentences summarizing overall performance.

## Key Changes

Provide 3-5 bullet points describing the most important
changes in the supplied metrics.

## Business Insights

Provide 3 concise insights explaining what the numbers
could mean for the business.

## Recommended Actions

Provide 3 practical actions the business owner could consider.

## Forecast Outlook

Briefly explain the forecast and selected model.
Do not present the forecast as guaranteed.

VERIFIED BUSINESS DATA:

{context_json}
"""

    return prompt


# ============================================================
# GENERATE INSIGHTS
# ============================================================

def generate_business_insights(
    metrics,
    model_metadata,
    model_name=None
):
    """
    Generate business insights using Gemini.
    """

    context = build_business_context(
        metrics,
        model_metadata
    )

    prompt = build_insight_prompt(
        context
    )

    if model_name is None:
        model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash"
        )

    client = get_gemini_client()

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    if response is None:
        raise RuntimeError(
            "The AI service returned no response."
        )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:
        raise RuntimeError(
            "The AI service returned an empty response."
        )

    return text.strip()