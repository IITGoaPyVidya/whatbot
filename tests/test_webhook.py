import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_VERIFY_TOKEN = "verify_token"  # matches default in config


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "WhatsApp AI Bot is running" in response.json()["message"]


def test_webhook_verification_success():
    response = client.get(
        "/webhook",
        params={
            "hub.mode": "subscribe",
            "hub.challenge": "test_challenge_123",
            "hub.verify_token": VALID_VERIFY_TOKEN,
        },
    )
    assert response.status_code == 200


def test_webhook_verification_invalid_token():
    response = client.get(
        "/webhook",
        params={
            "hub.mode": "subscribe",
            "hub.challenge": "test_challenge_123",
            "hub.verify_token": "wrong_token",
        },
    )
    assert response.status_code == 403


def test_webhook_post_non_whatsapp_payload():
    response = client.post(
        "/webhook",
        json={"object": "other", "entry": []},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ignored"


def test_webhook_post_valid_message():
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "from": "1234567890",
                                    "text": {"body": "Hello bot!"},
                                    "type": "text",
                                    "id": "msg_123",
                                }
                            ],
                            "contacts": [
                                {
                                    "profile": {"name": "Test User"},
                                    "wa_id": "1234567890",
                                }
                            ],
                        }
                    }
                ]
            }
        ],
    }
    with patch(
        "app.routes.webhook.process_incoming_message", new_callable=AsyncMock
    ):
        response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_webhook_post_invalid_json():
    response = client.post(
        "/webhook",
        content=b"not-json",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400
