# whatbot 🤖

A WhatsApp bot powered by **Google Gemini** and **Groq** (both free tiers) built with [whatsapp-web.js](https://github.com/pedroslopez/whatsapp-web.js).

## Features

- 💬 Replies to WhatsApp messages using AI
- 🔀 Supports **two free LLM providers** – Google Gemini & Groq – with automatic round-robin / fallback
- 🔒 QR-code authentication with session persistence (scan once, keep running)
- ⚙️ Configurable via a single `.env` file
- 🔤 Optional command prefix (e.g. `!bot`) and group-message toggle

---

## Project Structure

```
whatbot/
├── src/
│   ├── index.js        ← entry point
│   ├── bot.js          ← WhatsApp client & message handler
│   ├── config.js       ← reads .env and validates keys
│   └── llm/
│       ├── index.js    ← routes messages to Gemini or Groq
│       ├── gemini.js   ← Google Gemini integration
│       └── groq.js     ← Groq integration
├── .env.example        ← copy this to .env and fill your keys
├── .gitignore
├── package.json
└── README.md
```

---

## Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Node.js | ≥ 18 | https://nodejs.org |
| npm | comes with Node.js | – |
| Google Chrome / Chromium | latest | auto-installed by Puppeteer |

> **Windows users:** Puppeteer (used by whatsapp-web.js) may need Visual C++ build tools.  
> Run `npm install --global windows-build-tools` in an **Admin** PowerShell if the install fails.

---

## Get Your Free API Keys

### 1. Google Gemini
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API key**
4. Copy the key – you'll put it in `.env` as `GEMINI_API_KEY`

### 2. Groq
1. Go to [Groq Console](https://console.groq.com/keys)
2. Sign up for a free account
3. Click **Create API key**
4. Copy the key – you'll put it in `.env` as `GROQ_API_KEY`

---

## Local Setup (VSCode)

### Step 1 – Clone the repository

Open a terminal in VSCode (`Ctrl+` `` ` ``) and run:

```bash
git clone https://github.com/IITGoaPyVidya/whatbot.git
cd whatbot
```

### Step 2 – Install dependencies

```bash
npm install
```

> This also downloads a compatible Chromium browser for Puppeteer automatically.

### Step 3 – Create your `.env` file

```bash
# On Windows (PowerShell)
copy .env.example .env

# On macOS / Linux
cp .env.example .env
```

Open `.env` in VSCode and fill in your API keys:

```env
GEMINI_API_KEY=AIza...yourkey...
GROQ_API_KEY=gsk_...yourkey...

# Optional settings (defaults shown)
LLM_PROVIDER=auto          # gemini | groq | auto
GEMINI_MODEL=gemini-1.5-flash
GROQ_MODEL=llama3-8b-8192
BOT_PREFIX=!bot            # leave empty to reply to every message
RESPOND_IN_GROUPS=false
SYSTEM_PROMPT=You are a helpful WhatsApp assistant. Keep your answers short and clear.
```

### Step 4 – Start the bot

```bash
npm start
```

Or use the built-in **file watcher** (auto-restarts on code changes – great for development):

```bash
npm run dev
```

### Step 5 – Scan the QR code

A QR code will appear in your terminal. Open WhatsApp on your phone:

1. **Android**: Menu (⋮) → **Linked Devices** → **Link a Device**
2. **iPhone**: Settings → **Linked Devices** → **Link a Device**

Point your camera at the QR code. The bot will print `✅ WhatsApp client is ready!` once connected.

> The session is saved in `.wwebjs_auth/` so you **only need to scan once**.

---

## Recommended VSCode Extensions

Install these for a better development experience:

| Extension | ID |
|-----------|----|
| ESLint | `dbaeumer.vscode-eslint` |
| Prettier | `esbenp.prettier-vscode` |
| DotENV | `mikestead.dotenv` |
| GitLens | `eamodio.gitlens` |

Quick-install all at once (paste into VSCode terminal):

```bash
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension mikestead.dotenv
code --install-extension eamodio.gitlens
```

---

## Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | – | **Required** – your Google Gemini API key |
| `GROQ_API_KEY` | – | **Required** – your Groq API key |
| `LLM_PROVIDER` | `auto` | `gemini`, `groq`, or `auto` (round-robin with fallback) |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Gemini model to use |
| `GROQ_MODEL` | `llama3-8b-8192` | Groq model to use |
| `BOT_PREFIX` | *(empty)* | If set, bot only replies to messages starting with this prefix |
| `RESPOND_IN_GROUPS` | `false` | Set to `true` to enable replies in group chats |
| `SYSTEM_PROMPT` | *see .env.example* | System prompt sent to the LLM |

---

## How It Works

```
WhatsApp message
      │
      ▼
  bot.js  ──── prefix / group filter ────►  (ignored)
      │
      ▼
  llm/index.js  ──── LLM_PROVIDER=auto ────► round-robin
      │                                        │
      ├──────────► gemini.js ──► Gemini API   │
      │                                        │
      └──────────► groq.js   ──► Groq API    ◄┘
                                    │
                                    ▼
                             reply sent back
                           to WhatsApp message
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Missing required environment variable` | Make sure `.env` exists and both API keys are filled in |
| QR code appears repeatedly | Delete `.wwebjs_auth/` and scan again |
| Bot doesn't reply | Check that `BOT_PREFIX` matches what you send, or leave it empty |
| Chromium download fails | Set `PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true` and install Chrome manually |
| `Error: spawn` on Windows | Run `npm install --global windows-build-tools` as Administrator |

---

## License

MIT
