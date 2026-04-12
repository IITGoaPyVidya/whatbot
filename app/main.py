from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import get_settings
from app.routes import health, webhook
from app.utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting WhatsApp AI Bot (environment: {settings.environment})")
    yield
    logger.info("Shutting down WhatsApp AI Bot")


app = FastAPI(
    title="WhatsApp AI Bot",
    description=(
        "A production-ready WhatsApp bot that integrates with "
        "Google Gemini and Groq LLMs."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(webhook.router)
