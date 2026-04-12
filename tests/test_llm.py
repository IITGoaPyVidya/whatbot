import pytest
from unittest.mock import MagicMock, patch


def test_llm_service_imports():
    """LLMService should be importable without errors."""
    from app.services.llm import LLMService

    service = LLMService()
    assert service is not None


def test_llm_fallback_no_providers():
    """When no providers are available, return a friendly error message."""
    from app.services.llm import LLMService

    service = LLMService()
    service._gemini_client = None
    service._groq_client = None

    result = service.get_response("Hello")
    assert result["provider"] == "none"
    assert "trouble" in result["text"].lower() or result["text"]


def test_llm_uses_groq_fallback():
    """When Gemini fails, Groq should be used as fallback."""
    from app.services.llm import LLMService

    service = LLMService()
    service._gemini_client = MagicMock()
    service._groq_client = MagicMock()

    with patch.object(service, "_call_gemini", return_value={"text": "", "provider": "gemini", "error": "fail"}):
        with patch.object(service, "_call_groq", return_value={"text": "Groq reply", "provider": "groq", "error": None}):
            result = service.get_response("Hello")

    assert result["provider"] == "groq"
    assert result["text"] == "Groq reply"


def test_llm_uses_gemini_first():
    """Gemini should be tried first when available."""
    from app.services.llm import LLMService

    service = LLMService()
    service._gemini_client = MagicMock()

    with patch.object(service, "_call_gemini", return_value={"text": "Gemini reply", "provider": "gemini", "error": None}):
        result = service.get_response("Hello")

    assert result["provider"] == "gemini"
    assert result["text"] == "Gemini reply"
