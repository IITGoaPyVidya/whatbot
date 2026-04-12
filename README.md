# whatbot — WhatsApp AI Bot 🤖

A production-ready WhatsApp bot powered by **Google Gemini** and **Groq** LLMs, built with FastAPI. Designed to run 24/7 with proper hosting support.

---

## ✨ Features

- **Dual LLM support** — Google Gemini as primary, Groq as automatic fallback
- **Session management** — per-user conversation history (in-memory, configurable TTL)
- **Rate limiting** — protects against abuse
- **Docker ready** — one-command local development
- **Railway / Render / Heroku ready** — deploy in minutes
- **Structured logging** — easy debugging in production
- **Webhook verification** — secure Meta WhatsApp Cloud API integration

---

## 📁 Project Structure

```
whatbot/
├── app/
│   ├── main.py                # FastAPI application entry point
│   ├── config.py              # Configuration from environment variables
│   ├── routes/
│   │   ├── health.py          # GET /health  and  GET /
│   │   └── webhook.py         # GET & POST /webhook  (WhatsApp)
│   ├── services/
│   │   ├── llm.py             # Google Gemini + Groq integration
│   │   ├── whatsapp.py        # Send messages via Meta Cloud API
│   │   ├── message.py         # Orchestrates LLM + WhatsApp
│   │   └── session.py         # In-memory session / history management
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   └── utils/
│       ├── logger.py          # Structured logging
│       └── validators.py      # Input sanitization & validation
├── tests/
│   ├── test_webhook.py
│   └── test_llm.py
├── examples/
│   └── test_requests.http     # VSCode REST Client examples
├── .env.example               # Environment variable template
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Procfile                   # Heroku
├── README.md
├── DEPLOYMENT.md
├── API_DOCUMENTATION.md
└── VSCODE_SETUP.md
```

---

## 🔑 Required API Keys

| Service | Where to get | `.env` variable |
|---------|-------------|-----------------|
| Google Gemini | https://aistudio.google.com/app/apikey | `GOOGLE_API_KEY` |
| Groq | https://console.groq.com/keys | `GROQ_API_KEY` |
| WhatsApp Cloud API | https://developers.facebook.com → WhatsApp product | `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_BUSINESS_ACCOUNT_ID` |

---

## ⚡ Local Setup (VSCode)

### Prerequisites

- Python 3.9+
- Git
- [VSCode](https://code.visualstudio.com/)

### Step 1 — Clone the repository

```bash
git clone https://github.com/IITGoaPyVidya/whatbot.git
cd whatbot
```

### Step 2 — Create a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment variables

```bash
cp .env.example .env
code .env   # Opens in VSCode — fill in your API keys
```

### Step 5 — Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:

```
INFO | app.main | Starting WhatsApp AI Bot (environment: development)
INFO | uvicorn.server | Application startup complete.
```

### Step 6 — Test

```bash
# Health check
curl http://localhost:8000/health

# Webhook verification
curl "http://localhost:8000/webhook?hub.mode=subscribe&hub.challenge=test&hub.verify_token=your_webhook_verify_token"
```

---

## 🐳 Docker

### Run with Docker Compose (recommended for local dev)

```bash
docker-compose up --build
```

### Build and run manually

```bash
docker build -t whatbot .
docker run -p 8000:8000 --env-file .env whatbot
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `WHATSAPP_BUSINESS_ACCOUNT_ID` | Your Meta Business Account ID | ✅ |
| `WHATSAPP_PHONE_NUMBER_ID` | WhatsApp Phone Number ID | ✅ |
| `WHATSAPP_TOKEN` | WhatsApp Bearer Token | ✅ |
| `WHATSAPP_WEBHOOK_TOKEN` | Token you choose for webhook verification | ✅ |
| `GOOGLE_API_KEY` | Google Gemini API key | ✅ (or Groq) |
| `GROQ_API_KEY` | Groq API key | ✅ (or Gemini) |
| `GEMINI_MODEL` | Gemini model name | ❌ (default: `gemini-1.5-flash`) |
| `GROQ_MODEL` | Groq model name | ❌ (default: `llama3-8b-8192`) |
| `ENVIRONMENT` | `development` or `production` | ❌ |
| `DEBUG` | Enable debug mode & API docs | ❌ (default: `false`) |
| `LOG_LEVEL` | Logging level | ❌ (default: `INFO`) |
| `SESSION_TTL` | Session expiry in seconds | ❌ (default: `3600`) |
| `MAX_HISTORY_LENGTH` | Max messages per session | ❌ (default: `10`) |

---

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full guides on:
- Railway
- Render
- Heroku

---

## 🤖 Bot Commands

Users can type these commands in WhatsApp:

| Command | Action |
|---------|--------|
| `!help` or `help` | Show available commands |
| `!clear` or `clear history` | Clear conversation history |
| Any other text | Get an AI response |

---

## 🛠 Troubleshooting

### `ModuleNotFoundError: No module named 'app'`

Make sure you're running from the project root and your virtual environment is activated:

```bash
cd whatbot
source venv/bin/activate   # or .\venv\Scripts\Activate.ps1 on Windows
uvicorn app.main:app --reload
```

### WhatsApp webhook not connecting

1. Make sure your server is publicly accessible (use [ngrok](https://ngrok.com/) for local testing)
2. Verify your `WHATSAPP_WEBHOOK_TOKEN` matches what you enter in the Meta dashboard
3. Check server logs for verification errors

### LLM API errors

```bash
# Test Gemini API key
python -c "
import google.generativeai as genai
genai.configure(api_key='YOUR_GOOGLE_API_KEY')
model = genai.GenerativeModel('gemini-1.5-flash')
print(model.generate_content('hello').text)
"

# Test Groq API key
python -c "
from groq import Groq
client = Groq(api_key='YOUR_GROQ_API_KEY')
chat = client.chat.completions.create(model='llama3-8b-8192', messages=[{'role':'user','content':'hello'}])
print(chat.choices[0].message.content)
"
```

---

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API](https://ai.google.dev/)
- [Groq Documentation](https://console.groq.com/docs)
- [Meta WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Railway Deployment](https://docs.railway.app/)