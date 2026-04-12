import httpx
from app.config import get_settings
from app.utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)

WHATSAPP_API_URL = (
    "https://graph.facebook.com/v19.0/{phone_number_id}/messages"
)


async def send_whatsapp_message(to: str, text: str) -> dict:
    """
    Send a text message via the WhatsApp Cloud API.

    Args:
        to: Recipient's phone number (E.164 format without '+')
        text: Message text to send

    Returns:
        Response JSON from Meta API
    """
    url = WHATSAPP_API_URL.format(
        phone_number_id=settings.whatsapp_phone_number_id
    )
    headers = {
        "Authorization": f"Bearer {settings.whatsapp_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": text},
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Message sent to {to}: {data.get('messages', [{}])[0].get('id', 'unknown')}")
            return data
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"WhatsApp API HTTP error: {exc.response.status_code} - {exc.response.text}"
            )
            raise
        except Exception as exc:
            logger.error(f"WhatsApp API error: {exc}")
            raise
