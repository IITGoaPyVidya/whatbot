import pkg from "whatsapp-web.js";
import qrcode from "qrcode-terminal";
import { getLLMReply } from "./llm.js";

const { Client, LocalAuth } = pkg;

const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: {
    // Run headless in server/CI; set to false if you want to see the browser window
    headless: true,
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
    ],
  },
});

// Display QR code in terminal for first-time login
client.on("qr", (qr) => {
  console.log("\n📱 Scan the QR code below with WhatsApp to log in:\n");
  qrcode.generate(qr, { small: true });
});

client.on("authenticated", () => {
  console.log("✅ Authenticated successfully. Session saved for future use.");
});

client.on("auth_failure", (msg) => {
  console.error("❌ Authentication failed:", msg);
  process.exit(1);
});

client.on("ready", () => {
  console.log("🤖 Whatbot is ready and listening for messages!");
});

// Handle incoming messages
client.on("message", async (message) => {
  // Ignore group messages and status broadcasts
  if (message.isGroupMsg || message.from === "status@broadcast") return;

  const userText = message.body.trim();
  if (!userText) return;

  console.log(`[MSG] From ${message.from}: ${userText}`);

  try {
    const reply = await getLLMReply(userText);
    await message.reply(reply);
    console.log(`[REPLY] Sent to ${message.from}`);
  } catch (err) {
    console.error("[ERROR] Failed to send reply:", err.message);
  }
});

client.on("disconnected", (reason) => {
  console.warn("⚠️  Client disconnected:", reason);
  process.exit(0);
});

// Graceful shutdown
process.on("SIGINT", async () => {
  console.log("\n🛑 Shutting down whatbot...");
  await client.destroy();
  process.exit(0);
});

client.initialize();
