import asyncio

from fastapi import APIRouter, HTTPException, Query, Request, BackgroundTasks
from app.config import get_settings
from app.services.message import process_incoming_message
from app.utils.logger import setup_logger
from app.utils.validators import is_valid_whatsapp_payload

router = APIRouter()
settings = get_settings()
logger = setup_logger(__name__)


@router.get("/webhook", tags=["WhatsApp"])
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    """
    Webhook verification endpoint required by Meta WhatsApp Cloud API.
    Meta sends a GET request with a challenge that must be echoed back.
    """
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_webhook_token:
        logger.info("Webhook verified successfully")
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(content=hub_challenge)

    logger.warning("Webhook verification failed — invalid token or mode")
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook", tags=["WhatsApp"])
async def receive_message(request: Request, background_tasks: BackgroundTasks):
    """
    Receive and process incoming WhatsApp messages.
    Messages are processed in the background so Meta receives a 200 quickly.
    """
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    if not is_valid_whatsapp_payload(payload):
        logger.warning("Received non-WhatsApp payload, ignoring")
        return {"status": "ignored"}

    logger.debug(f"Webhook payload received: {payload}")

    # Extract and process messages
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messages = value.get("messages", [])
            for msg in messages:
                msg_type = msg.get("type")
                sender = msg.get("from")

                if msg_type == "text" and sender:
                    text_body = msg.get("text", {}).get("body", "")
                    if text_body:
                        background_tasks.add_task(
                            process_incoming_message, sender, text_body
                        )
                else:
                    logger.info(f"Unsupported message type '{msg_type}' from {sender}, skipping")

    return {"status": "ok"}
