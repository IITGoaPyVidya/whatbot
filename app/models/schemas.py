from typing import Optional, List
from pydantic import BaseModel, Field


# ---- Incoming WhatsApp payload models ----

class TextBody(BaseModel):
    body: str


class Message(BaseModel):
    id: str
    from_number: str = Field(alias="from")
    type: str
    text: Optional[TextBody] = None
    timestamp: Optional[str] = None

    model_config = {"populate_by_name": True}


class Contact(BaseModel):
    profile: Optional[dict] = None
    wa_id: str


class Value(BaseModel):
    messaging_product: Optional[str] = None
    messages: Optional[List[Message]] = None
    contacts: Optional[List[Contact]] = None
    statuses: Optional[List[dict]] = None


class Change(BaseModel):
    value: Value
    field: Optional[str] = None


class Entry(BaseModel):
    id: Optional[str] = None
    changes: List[Change]


class WebhookPayload(BaseModel):
    object: str
    entry: List[Entry]


# ---- Health check ----

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str = "1.0.0"


# ---- LLM response ----

class LLMResponse(BaseModel):
    text: str
    provider: str
    error: Optional[str] = None
