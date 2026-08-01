"""Gemini API client — replaces llm-council subprocess calls.

Works in both Google Colab (via userdata) and local environments (via env var).
"""

import os
import json
import re
from typing import Optional

from google import genai
from google.genai import types


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DEFAULT_MODEL = "gemini-2.0-flash"
MAX_RETRIES = 3

# System instruction that emulates the multi-perspective deliberation the
# llm-council was performing (multiple models + chairman synthesis).
_COUNCIL_SYSTEM_INSTRUCTION = (
    "You are a panel of expert advisors deliberating on the task below. "
    "Consider the problem from multiple angles — data-driven, creative, and "
    "strategic — then synthesize the best answer. Be concise and actionable."
)


def _get_api_key() -> str:
    """Retrieve the Gemini API key from Colab userdata or environment."""
    # 1. Try Google Colab userdata (preferred in notebooks)
    try:
        from google.colab import userdata  # type: ignore[import-not-found]
        key = userdata.get("GEMINI_API_KEY")
        if key:
            return key
    except (ImportError, ModuleNotFoundError, Exception):
        pass

    # 2. Fall back to environment variable
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        return key

    # 3. Fall back to interactive prompt (useful in notebooks if secrets/env not set)
    try:
        import getpass
        key = getpass.getpass("🔑 Enter your Gemini API Key: ").strip()
        if key:
            os.environ["GEMINI_API_KEY"] = key
            return key
    except Exception:
        pass

    raise RuntimeError(
        "Gemini API key not found. Set it via:\n"
        "  • Google Colab: Add 'GEMINI_API_KEY' in Colab Secrets (🔑 sidebar)\n"
        "  • Local: export GEMINI_API_KEY='your-key'"
    )


def _get_client() -> genai.Client:
    """Create a configured Gemini client."""
    return genai.Client(api_key=_get_api_key())


def generate(
    prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    system_instruction: str = _COUNCIL_SYSTEM_INSTRUCTION,
    max_tokens: int = 4096,
    temperature: float = 0.7,
) -> str:
    """Send a prompt to Gemini and return the text response.

    Parameters
    ----------
    prompt : str
        The user prompt to send.
    model : str
        Gemini model ID (default: gemini-2.0-flash).
    system_instruction : str
        System-level instruction for the model.
    max_tokens : int
        Maximum output tokens.
    temperature : float
        Sampling temperature (0.0–2.0).

    Returns
    -------
    str
        The model's text response.
    """
    client = _get_client()

    last_error: Optional[Exception] = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                ),
            )
            return response.text or ""
        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                import time
                time.sleep(2 ** attempt)  # Exponential back-off
            continue

    raise RuntimeError(
        f"Gemini API call failed after {MAX_RETRIES} retries: {last_error}"
    )


def generate_json(prompt: str, **kwargs) -> dict | list:
    """Generate content and parse the JSON from the response.

    Handles both ```json ... ``` fenced blocks and raw JSON.
    """
    raw = generate(prompt, **kwargs)

    # Try to extract fenced JSON block first
    json_match = re.search(r"```json\s*(.+?)\s*```", raw, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))

    # Try to extract raw JSON array or object
    json_match = re.search(r"(\[.+?\]|\{.+?\})", raw, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))

    return {"raw_response": raw, "error": "Could not parse JSON from response"}
