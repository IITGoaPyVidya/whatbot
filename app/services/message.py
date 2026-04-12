from app.services.llm import LLMService
from app.services.session import get_session_history, append_to_session
from app.services.whatsapp import send_whatsapp_message
from app.utils.validators import sanitize_message
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

_llm_service = LLMService()

HELP_TEXT = (
    "👋 *WhatsApp AI Bot*\n\n"
    "I'm powered by Google Gemini and Groq LLMs.\n\n"
    "Commands:\n"
    "• *!help* — Show this message\n"
    "• *!clear* — Clear conversation history\n\n"
    "Just type any message and I'll respond!"
)


async def process_incoming_message(sender: str, message_text: str) -> None:
    """
    Process an incoming WhatsApp text message and send a reply.

    Args:
        sender: The sender's phone number
        message_text: The incoming text message
    """
    text = sanitize_message(message_text)
    logger.info(f"Processing message from {sender}: {text[:60]}{'...' if len(text) > 60 else ''}")

    # Handle commands
    if text.lower() in ("!help", "/help", "help"):
        await send_whatsapp_message(sender, HELP_TEXT)
        return

    if text.lower() in ("!clear", "/clear", "clear history"):
        from app.services.session import clear_session
        clear_session(sender)
        await send_whatsapp_message(sender, "✅ Your conversation history has been cleared.")
        return

    # Get session history and generate LLM response
    history = get_session_history(sender)
    result = _llm_service.get_response(text, history)

    reply = result["text"]
    provider = result["provider"]
    logger.info(f"LLM provider used: {provider}")

    # Persist messages to session
    append_to_session(sender, "user", text)
    append_to_session(sender, "assistant", reply)

    # Send reply
    await send_whatsapp_message(sender, reply)
