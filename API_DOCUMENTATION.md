# API Documentation

Base URL (local): `http://localhost:8000`

Interactive docs (when `DEBUG=true`): `http://localhost:8000/docs`

---

## Endpoints

### `GET /`

Returns basic info about the running service.

**Response:**
```json
{
  "message": "WhatsApp AI Bot is running",
  "docs": "/docs",
  "health": "/health",
  "environment": "development"
}
```

---

### `GET /health`

Health check endpoint. Use this with your uptime monitor.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2026-04-12T11:00:00+00:00",
  "version": "1.0.0"
}
```

---

### `GET /webhook`

WhatsApp webhook verification. Called by Meta once when you configure the webhook.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `hub.mode` | string | Must be `subscribe` |
| `hub.challenge` | string | Challenge string from Meta |
| `hub.verify_token` | string | Must match `WHATSAPP_WEBHOOK_TOKEN` |

**Success Response (200):**

Returns the integer value of `hub.challenge`.

**Failure Response (403):**
```json
{"detail": "Verification failed"}
```

---

### `POST /webhook`

Receives incoming WhatsApp messages. Called by Meta for every message event.

**Request Body:** WhatsApp Cloud API webhook payload (JSON)

**Example:**
```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "changes": [
        {
          "value": {
            "messages": [
              {
                "from": "9876543210",
                "id": "wamid.xxx",
                "timestamp": "1700000000",
                "text": { "body": "Hello!" },
                "type": "text"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

**Response (200):**
```json
{"status": "ok"}
```

Non-WhatsApp payloads return:
```json
{"status": "ignored"}
```

---

## Bot Commands (via WhatsApp message text)

| Command | Response |
|---------|----------|
| `!help` | Shows help message with available commands |
| `!clear` | Clears conversation history for that user |
| Any other text | AI-generated response from Gemini or Groq |
