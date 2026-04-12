from typing import Optional
from app.config import get_settings
from app.utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)


class LLMService:
    """Handles LLM calls with Gemini as primary and Groq as fallback."""

    def __init__(self):
        self._gemini_client = None
        self._groq_client = None
        self._init_clients()

    def _init_clients(self):
        # Initialize Google Gemini client
        if settings.google_api_key:
            try:
                import google.generativeai as genai

                genai.configure(api_key=settings.google_api_key)
                self._gemini_client = genai.GenerativeModel(settings.gemini_model)
                logger.info("Google Gemini client initialized")
            except Exception as exc:
                logger.warning(f"Failed to initialize Gemini client: {exc}")

        # Initialize Groq client
        if settings.groq_api_key:
            try:
                from groq import Groq

                self._groq_client = Groq(api_key=settings.groq_api_key)
                logger.info("Groq client initialized")
            except Exception as exc:
                logger.warning(f"Failed to initialize Groq client: {exc}")

    def get_response(
        self, user_message: str, history: Optional[list] = None
    ) -> dict:
        """
        Get a response from LLMs with fallback.
        Tries Gemini first, then Groq.

        Returns:
            {"text": str, "provider": str, "error": str | None}
        """
        history = history or []

        # Try Gemini first
        if self._gemini_client:
            result = self._call_gemini(user_message, history)
            if result["text"]:
                return result

        # Fallback to Groq
        if self._groq_client:
            result = self._call_groq(user_message, history)
            if result["text"]:
                return result

        return {
            "text": "I'm sorry, I'm having trouble connecting to my AI services right now. Please try again later.",
            "provider": "none",
            "error": "All LLM providers failed",
        }

    def _call_gemini(self, user_message: str, history: list) -> dict:
        """Call Google Gemini API."""
        try:
            import google.generativeai as genai

            # Build conversation history for Gemini
            chat_history = []
            for msg in history:
                role = "user" if msg["role"] == "user" else "model"
                chat_history.append({"role": role, "parts": [msg["content"]]})

            chat = self._gemini_client.start_chat(history=chat_history)
            response = chat.send_message(user_message)
            text = response.text.strip()
            logger.info(f"Gemini response generated ({len(text)} chars)")
            return {"text": text, "provider": "gemini", "error": None}
        except Exception as exc:
            logger.error(f"Gemini API error: {exc}")
            return {"text": "", "provider": "gemini", "error": str(exc)}

    def _call_groq(self, user_message: str, history: list) -> dict:
        """Call Groq API."""
        try:
            messages = []
            messages.append(
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Be concise and friendly.",
                }
            )
            for msg in history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": user_message})

            completion = self._groq_client.chat.completions.create(
                model=settings.groq_model,
                messages=messages,
                max_tokens=1024,
                temperature=0.7,
            )
            text = completion.choices[0].message.content.strip()
            logger.info(f"Groq response generated ({len(text)} chars)")
            return {"text": text, "provider": "groq", "error": None}
        except Exception as exc:
            logger.error(f"Groq API error: {exc}")
            return {"text": "", "provider": "groq", "error": str(exc)}
