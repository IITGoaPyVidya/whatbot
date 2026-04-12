import re


def is_valid_phone_number(phone: str) -> bool:
    """Validate E.164 phone number format."""
    return bool(re.match(r"^\+?[1-9]\d{7,14}$", phone))


def sanitize_message(text: str, max_length: int = 4096) -> str:
    """Sanitize and truncate incoming message text."""
    if not text:
        return ""
    text = text.strip()
    if len(text) > max_length:
        text = text[:max_length]
    return text


def is_valid_whatsapp_payload(payload: dict) -> bool:
    """Check that a webhook payload looks like a WhatsApp message."""
    return (
        isinstance(payload, dict)
        and payload.get("object") == "whatsapp_business_account"
        and isinstance(payload.get("entry"), list)
    )
