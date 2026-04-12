import time
from typing import Optional
from app.config import get_settings
from app.utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)

# In-memory session store: {phone_number: {"history": [...], "last_active": timestamp}}
_sessions: dict = {}


def get_session_history(phone: str) -> list:
    """Return the conversation history for a given phone number."""
    _cleanup_expired_sessions()
    session = _sessions.get(phone)
    if session:
        session["last_active"] = time.time()
        return session["history"]
    return []


def append_to_session(phone: str, role: str, content: str) -> None:
    """Append a message to the session history."""
    _cleanup_expired_sessions()
    if phone not in _sessions:
        _sessions[phone] = {"history": [], "last_active": time.time()}

    _sessions[phone]["history"].append({"role": role, "content": content})
    _sessions[phone]["last_active"] = time.time()

    # Trim history if it exceeds max length
    if len(_sessions[phone]["history"]) > settings.max_history_length * 2:
        _sessions[phone]["history"] = _sessions[phone]["history"][
            -(settings.max_history_length * 2) :
        ]


def clear_session(phone: str) -> None:
    """Clear the conversation history for a phone number."""
    _sessions.pop(phone, None)


def _cleanup_expired_sessions() -> None:
    """Remove sessions that have been inactive longer than TTL."""
    now = time.time()
    expired = [
        phone
        for phone, data in _sessions.items()
        if now - data["last_active"] > settings.session_ttl
    ]
    for phone in expired:
        del _sessions[phone]
        logger.debug(f"Session expired and removed for {phone}")
