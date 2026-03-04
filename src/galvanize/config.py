"""LLM and app configuration. Uses Gemini via LangChain; loads API key from env or GCP Secret Manager."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (parent of src/galvanize)
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path)


def get_google_api_key() -> str:
    """Get Google (Gemini) API key from env or GCP Secret Manager."""
    key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if key:
        return key
    # Optional: pull from GCP Secret Manager if running in GCP / when secret is configured
    gcp_secret = os.environ.get("GALVANIZE_GEMINI_SECRET_VALUE")
    if gcp_secret:
        return gcp_secret.strip()
    return ""


def get_embedder_config():
    """Return CrewAI embedder config so knowledge/RAG uses Google embeddings (no OPENAI_API_KEY)."""
    api_key = get_google_api_key()
    if not api_key:
        return None
    return {
        "provider": "google-generativeai",
        "config": {
            "model_name": "gemini-embedding-001",
            "api_key": api_key,
        },
    }


def get_knowledge_dir() -> Path:
    """Return the project's knowledge directory (contains segments/, strategy_matrix.md, etc.)."""
    return Path(__file__).resolve().parent.parent.parent / "knowledge"


def get_llm():
    """Build the LLM instance for CrewAI agents. Uses CrewAI native Gemini (provider=gemini)."""
    from crewai import LLM

    api_key = get_google_api_key()
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is not set. Set it in .env or export it. "
            "For GCP: gcloud secrets versions access latest --secret=galvanize-gemini-api-key --project=genuine-park-487014-a7"
        )
    return LLM(
        model=os.environ.get("GALVANIZE_LLM_MODEL", "gemini-2.5-flash"),
        provider="gemini",
        api_key=api_key,
        temperature=float(os.environ.get("GALVANIZE_LLM_TEMPERATURE", "0.4")),
    )
