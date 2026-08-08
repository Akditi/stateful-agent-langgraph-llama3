import requests 
import streamlit as st 

GROQ_MODELS_URL = "https://api.groq.com/openai/v1/models" 

_EXCLUDE_KEYWORDS = ("whisper", "tts", "guard", "moderation", "embed")

_FALLBACK_MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

@st.cache_data(ttl=3600, show_spinner=False) 
def get_groq_chat_models(api_key: str) -> list:
    """
    Fetches the live list of chat-capable models from Groq instead of relying
    on a hardcoded list, which goes stale quickly since Groq deprecates and
    replaces models every few months. Cached for 1 hour per API key so we
    don't hit the endpoint on every Streamlit rerun.
    """

    if not api_key:
        return _FALLBACK_MODELS 
    
    try:
        response = requests.get(
            GROQ_MODELS_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=5,
        )
        response.raise_for_status()
        models = response.json().get("data", [])

        chat_models = sorted(
            m["id"] for m in models
            if not any(kw in m["id"].lower() for kw in _EXCLUDE_KEYWORDS)
        )
        return chat_models or _FALLBACK_MODELS

    except requests.RequestException:
        st.warning("Couldn't fetch live model list from Groq — showing a fallback list.")
        return _FALLBACK_MODELS