# 🤖 Whatbot — WhatsApp AI Bot

A WhatsApp bot that replies to messages using **Google Gemini** (primary) and **Groq** (automatic fallback), both on free API tiers.

---

## Features

- 📱 Connects to WhatsApp via QR code scan — no paid WhatsApp Business API needed
- 🧠 Uses Google Gemini (`gemini-1.5-flash`) as the primary LLM
- 🔄 Automatically falls back to Groq (`llama-3.3-70b-versatile`) if Gemini fails
- 💾 Saves your WhatsApp session so you only need to scan the QR once
- ⚙️ Fully configurable via environment variables

---

## Project Structure

```
whatbot/
├── src/
│   ├── bot.js       # WhatsApp client — listens for messages, sends replies
│   ├── llm.js       # LLM abstraction — Gemini with Groq fallback
│   └── config.js    # Loads & validates environment variables
├── .env.example     # Template for your secrets (copy to .env)
├── .gitignore
├── package.json
└── .github/
    └── workflows/
        └── ci.yml   # GitHub Actions CI workflow
```

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Node.js | ≥ 18 | https://nodejs.org |
| npm | comes with Node | — |
| Google Chrome / Chromium | any recent | installed automatically by Puppeteer |

You also need **two free API keys**:

- **Google Gemini** → https://aistudio.google.com/app/apikey
- **Groq** → https://console.groq.com/keys

---

## Local Setup (VSCode)

### 1 — Clone the repository

```bash
git clone https://github.com/IITGoaPyVidya/whatbot.git
cd whatbot
```

### 2 — Open in VSCode

```bash
code .
```

Install the recommended VSCode extension for Node.js development when prompted, or manually:

- **ESLint** (`dbaeumer.vscode-eslint`)
- **DotENV** (`mikestead.dotenv`) — syntax highlighting for `.env` files

### 3 — Install dependencies

Open the integrated terminal in VSCode (`Ctrl+`` ` `` ` or `View → Terminal`) and run:

```bash
npm install
```

> This installs `whatsapp-web.js`, `@google/generative-ai`, `groq-sdk`, and other packages.  
> Puppeteer will also download a Chromium binary (~170 MB) automatically on first install.

### 4 — Configure your API keys

```bash
# Copy the example file
cp .env.example .env
```

Then open `.env` in VSCode and fill in your keys:

```env
GEMINI_API_KEY=your_actual_gemini_key
GROQ_API_KEY=your_actual_groq_key
```

> ⚠️ **Never commit `.env`** — it is already in `.gitignore`.

### 5 — Run the bot

```bash
npm start
```

Or, for auto-restart on file changes during development:

```bash
npm run dev
```

On first run you will see a **QR code** in the terminal:

```
📱 Scan the QR code below with WhatsApp to log in:

█▀▀▀▀▀█  ▀▀ ▀ ▀ █▀▀▀▀▀█
...
```

1. Open **WhatsApp** on your phone
2. Go to **Settings → Linked Devices → Link a Device**
3. Scan the QR code

After scanning, the bot prints:

```
✅ Authenticated successfully. Session saved for future use.
🤖 Whatbot is ready and listening for messages!
```

From now on, any DM sent to your WhatsApp number will receive an AI reply. The session is saved in `.wwebjs_auth/` so you **won't need to scan the QR again** on restarts.

### 6 — Stop the bot

Press `Ctrl+C` in the terminal. The bot shuts down gracefully.

---

## Configuration Reference

All settings are controlled via environment variables in `.env`:

| Variable | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | *(required)* | Google Gemini API key |
| `GROQ_API_KEY` | *(required)* | Groq API key |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Gemini model name |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Groq model name |
| `SYSTEM_PROMPT` | *(see config.js)* | Personality prompt for the bot |
| `MAX_TOKENS` | `512` | Max tokens per LLM response |

---

## How LLM Fallback Works

```
Incoming WhatsApp message
        │
        ▼
  Ask Gemini (primary)
        │
   ┌────┴────┐
 success   failure
   │           │
   ▼           ▼
 Reply     Ask Groq (fallback)
                │
           ┌────┴────┐
         success   failure
           │           │
           ▼           ▼
         Reply    "Sorry, try again" message
```

---

## FAQ

**Q: Do I need a WhatsApp Business account?**  
No. The bot works with any regular WhatsApp account by linking it as a device.

**Q: Will my WhatsApp get banned?**  
Unofficial bots carry a small risk of rate-limiting or temporary bans if they send spam. Use responsibly and avoid bulk messaging.

**Q: The QR code expires before I scan it.**  
It refreshes automatically — a new QR will appear in the terminal. Just scan the fresh one.

**Q: How do I run this on a server (Linux VPS)?**  
Install Node.js 20+, copy the repo, add your `.env`, then run:
```bash
npm install
npm start
```
For persistent operation, use `pm2`:
```bash
npm install -g pm2
pm2 start src/bot.js --name whatbot
pm2 save
```

---

## License

MIT