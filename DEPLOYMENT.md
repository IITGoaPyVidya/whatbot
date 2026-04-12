# Deployment Guide

This guide covers deploying the WhatsApp AI Bot to Railway, Render, and Heroku.

---

## 🚂 Railway (Recommended)

Railway is the simplest option — it auto-deploys from GitHub and provides a managed HTTPS URL.

### Steps

1. **Create account** at https://railway.app (free tier available)

2. **New project → Deploy from GitHub repo**
   - Authorize Railway to access `IITGoaPyVidya/whatbot`
   - Select the repository

3. **Add environment variables** in the Railway dashboard:
   ```
   WHATSAPP_BUSINESS_ACCOUNT_ID=xxx
   WHATSAPP_PHONE_NUMBER_ID=xxx
   WHATSAPP_TOKEN=xxx
   WHATSAPP_WEBHOOK_TOKEN=xxx
   GOOGLE_API_KEY=xxx
   GROQ_API_KEY=xxx
   ENVIRONMENT=production
   DEBUG=false
   PORT=8000
   ```

4. **Get your public URL** — Railway shows it after deployment, e.g.  
   `https://whatbot-production-xxxx.up.railway.app`

5. **Configure the WhatsApp Webhook** in the Meta Developers Dashboard:
   - Webhook URL: `https://whatbot-production-xxxx.up.railway.app/webhook`
   - Verify Token: the value of `WHATSAPP_WEBHOOK_TOKEN`
   - Subscribe to the `messages` field

---

## 🎨 Render

1. Create account at https://render.com

2. **New → Web Service → Connect GitHub**
   - Select `IITGoaPyVidya/whatbot`

3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3

4. Add environment variables in the Render dashboard (same as Railway above)

5. Deploy and note your public URL (e.g., `https://whatbot.onrender.com`)

6. Configure WhatsApp webhook with the Render URL

> **Note**: Render free tier spins down after inactivity. Use a paid plan or a ping service (e.g., UptimeRobot) for 24/7 uptime.

---

## 🟣 Heroku

### Prerequisites

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli
heroku login
```

### Deploy

```bash
# Create app
heroku create your-whatbot-name

# Set environment variables
heroku config:set \
  WHATSAPP_BUSINESS_ACCOUNT_ID=xxx \
  WHATSAPP_PHONE_NUMBER_ID=xxx \
  WHATSAPP_TOKEN=xxx \
  WHATSAPP_WEBHOOK_TOKEN=xxx \
  GOOGLE_API_KEY=xxx \
  GROQ_API_KEY=xxx \
  ENVIRONMENT=production \
  DEBUG=false

# Deploy
git push heroku main

# Open app
heroku open
```

Your webhook URL will be: `https://your-whatbot-name.herokuapp.com/webhook`

---

## 🔒 Configure WhatsApp Webhook (all platforms)

1. Go to [Meta Developers Dashboard](https://developers.facebook.com/)
2. Select your app → **WhatsApp** → **Configuration**
3. Under **Webhook**:
   - Click **Edit**
   - **Callback URL**: `https://<your-public-url>/webhook`
   - **Verify Token**: value of `WHATSAPP_WEBHOOK_TOKEN` from your `.env`
   - Click **Verify and Save**
4. Under **Webhook Fields**, subscribe to **messages**

---

## 📡 Exposing Localhost for Testing

Use [ngrok](https://ngrok.com/) to create a temporary public URL:

```bash
# Install ngrok, then:
ngrok http 8000
```

Copy the `https://xxxx.ngrok.io` URL and use it as your webhook URL in Meta's dashboard.

---

## 🔄 Keeping the Service Running (24/7)

| Platform | Auto-restart | Free tier uptime |
|----------|-------------|-----------------|
| Railway  | ✅ Yes       | 500 hrs/month   |
| Render   | ✅ Yes       | Spins down on free |
| Heroku   | ✅ Yes       | Paid plans only  |

For guaranteed 24/7 uptime, use **Railway** (paid) or any VPS (DigitalOcean, AWS EC2).
