"""
AI Model Connector for Government Scheme Finder (MITRA AI)
==========================================================
Supports:
  1. Google Gemini API (via GEMINI_API_KEY environment variable)
  2. OpenAI API (via OPENAI_API_KEY environment variable)
  3. Safe offline fallback when no API key is configured.

Features:
  - Zero external SDK dependencies (uses Python urllib.request).
  - Environment variable credential management (never hardcoded or exposed to frontend).
  - Handles authentication errors, network timeouts (5s), and rate limits (429).
  - Grounded system instructions using verified Indian government welfare data.
  - Transparent status reporting: discloses whether a genuine LLM model is active
    or if the offline context engine is running.
"""
import os
import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Timeout in seconds for LLM API calls
LLM_TIMEOUT_SECONDS = 6


def get_ai_config() -> Dict[str, Any]:
    """
    Check environment variables for genuine LLM API credentials.
    Returns provider info without exposing secrets.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()

    if gemini_key:
        return {
            "is_connected": True,
            "provider": "gemini",
            "model": os.environ.get("GEMINI_MODEL", "gemini-1.5-flash"),
            "has_key": True
        }
    elif openai_key:
        return {
            "is_connected": True,
            "provider": "openai",
            "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            "has_key": True
        }
    else:
        return {
            "is_connected": False,
            "provider": "none",
            "model": None,
            "has_key": False,
            "note": "No GEMINI_API_KEY or OPENAI_API_KEY configured. Running in offline rule-grounded context mode."
        }


def call_gemini_api(prompt: str, system_instruction: str, api_key: str, model: str = "gemini-1.5-flash") -> Optional[str]:
    """
    Call Google Gemini generateContent REST endpoint using urllib.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "generationConfig": {
            "temperature": 0.25,
            "topP": 0.85,
            "maxOutputTokens": 600
        }
    }

    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=LLM_TIMEOUT_SECONDS) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            candidates = res_data.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
    except urllib.error.HTTPError as e:
        status_code = e.code
        logger.warning(f"Gemini API HTTP Error {status_code}: {e.reason}")
        if status_code in (401, 403):
            logger.error("Invalid or unauthorized GEMINI_API_KEY.")
        elif status_code == 429:
            logger.warning("Gemini API rate limit exceeded.")
    except urllib.error.URLError as e:
        logger.warning(f"Gemini API Connection Error: {e.reason}")
    except Exception as e:
        logger.warning(f"Unexpected error calling Gemini API: {e}")

    return None


def call_openai_api(prompt: str, system_instruction: str, api_key: str, model: str = "gpt-4o-mini") -> Optional[str]:
    """
    Call OpenAI Chat Completions REST endpoint using urllib.
    """
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }

    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=LLM_TIMEOUT_SECONDS) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            choices = res_data.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "").strip()
    except Exception as e:
        logger.warning(f"Error calling OpenAI API: {e}")

    return None


def generate_ai_response(
    message: str,
    conversation_history: List[Dict[str, str]],
    user_profile: Dict[str, Any],
    candidate_schemes: List[Dict[str, Any]],
    language: str = "en"
) -> Optional[Dict[str, Any]]:
    """
    Attempt to generate a response using a genuine configured LLM.
    Returns:
      { "text": "...", "provider": "gemini"|"openai", "model": "..." }
      or None if no key configured or call failed.
    """
    config = get_ai_config()
    if not config["is_connected"]:
        return None

    # Construct concise scheme context from SQLite candidate records
    scheme_summaries = []
    for s in candidate_schemes[:5]:
        scheme_summaries.append(
            f"- {s.get('title')} ({s.get('acronym')}): {s.get('benefit')}. "
            f"State: {', '.join(s.get('states', ['Central']))}. Scope: {s.get('scope')}. Official: {s.get('official_url')}"
        )
    schemes_text = "\n".join(scheme_summaries) if scheme_summaries else "No specific schemes retrieved yet."

    lang_instructions = {
        "te": "Respond in natural, polite Telugu. If the user message is in Telugu script or Tanglish (Telugu in English letters), understand the Telugu intent directly and reply in clear, natural Telugu. Do not translate their message to English and do not respond in English.",
        "hi": "Respond in natural, polite Hindi in Devanagari script (देवनागरी लिपि में उत्तर दें). Do not respond in English.",
        "en": "Respond in clear, professional English."
    }

    system_instruction = (
        "You are Mitra AI, an expert citizen benefits and government scheme co-pilot for India. "
        "Your mission is to guide Indian citizens to genuine Central and State welfare programs, scholarships, and employment initiatives. "
        "STRICT GUIDELINES:\n"
        "1. Never invent or hallucinate scheme names, amounts, or URLs. Only refer to verified official Indian government portals (.gov.in).\n"
        "2. Never claim confirmed approval; only evaluate potential eligibility.\n"
        "3. If a student (e.g. studying B.Tech) asks about employment schemes, explain genuine programs like NATS apprenticeships, Skill India / PMKVY, and PMEGP/Mudra for self-employment. Ask which State they reside in for state-specific engineering incentives.\n"
        "4. If essential details (state, course, land size, income) are missing, ask a concise, friendly follow-up question before recommending specific schemes.\n"
        f"5. {lang_instructions.get(language, 'Respond in clear, professional English.')}\n"
        f"Verified Database Schemes available:\n{schemes_text}"
    )

    # Format history
    history_lines = []
    for turn in conversation_history[-4:]:
        role = "User" if turn.get("role") == "user" else "Mitra"
        history_lines.append(f"{role}: {turn.get('message', '')}")
    history_str = "\n".join(history_lines)

    profile_facts = ", ".join([f"{k}: {v}" for k, v in user_profile.items() if v is not None])
    prompt = f"Known Profile: [{profile_facts}]\nConversation History:\n{history_str}\n\nLatest User Message: {message}\nMitra AI Response:"

    provider = config["provider"]
    response_text = None

    if provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY", "")
        response_text = call_gemini_api(prompt, system_instruction, api_key, config["model"])
    elif provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY", "")
        response_text = call_openai_api(prompt, system_instruction, api_key, config["model"])

    if response_text:
        return {
            "text": response_text,
            "provider": provider,
            "model": config["model"]
        }

    return None
