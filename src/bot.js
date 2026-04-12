'use strict';

const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const llm = require('./llm');
const config = require('./config');

/**
 * Create and configure the WhatsApp client.
 * @returns {Client}
 */
function createBot() {
  const client = new Client({
    authStrategy: new LocalAuth(), // persists session so you only scan QR once
    puppeteer: {
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    },
  });

  // ── QR code ──────────────────────────────────────────────────────
  client.on('qr', (qr) => {
    console.log('\n[Bot] Scan the QR code below with WhatsApp:\n');
    qrcode.generate(qr, { small: true });
  });

  // ── Ready ─────────────────────────────────────────────────────────
  client.on('ready', () => {
    console.log('[Bot] WhatsApp client is ready! ✅');
    console.log(`[Bot] LLM provider : ${config.llmProvider}`);
    console.log(
      `[Bot] Prefix filter : ${config.botPrefix ? `"${config.botPrefix}"` : 'none (replies to everything)'}`
    );
    console.log(
      `[Bot] Group replies : ${config.respondInGroups ? 'enabled' : 'disabled'}`
    );
  });

  // ── Authentication failure ─────────────────────────────────────────
  client.on('auth_failure', (msg) => {
    console.error('[Bot] Authentication failed:', msg);
  });

  // ── Disconnected ──────────────────────────────────────────────────
  client.on('disconnected', (reason) => {
    console.warn('[Bot] Client disconnected:', reason);
  });

  // ── Incoming messages ─────────────────────────────────────────────
  client.on('message', async (message) => {
    try {
      // Skip messages sent by the bot itself
      if (message.fromMe) return;

      const chat = await message.getChat();

      // Skip group messages if not enabled
      if (chat.isGroup && !config.respondInGroups) return;

      const body = message.body.trim();

      // Apply prefix filter
      if (config.botPrefix) {
        if (!body.toLowerCase().startsWith(config.botPrefix.toLowerCase())) {
          return;
        }
        // Strip the prefix before sending to LLM
        const userText = body.slice(config.botPrefix.length).trim();
        if (!userText) return;
        await replyWithLLM(message, userText);
      } else {
        if (!body) return;
        await replyWithLLM(message, body);
      }
    } catch (err) {
      console.error('[Bot] Error handling message:', err);
    }
  });

  return client;
}

/**
 * Ask the LLM and send the reply back to the WhatsApp message.
 * @param {import('whatsapp-web.js').Message} message
 * @param {string} userText
 */
async function replyWithLLM(message, userText) {
  console.log(`[Bot] Received: "${userText}"`);
  const reply = await llm.chat(userText);
  if (!reply) {
    console.warn('[Bot] LLM returned an empty reply – skipping send');
    return;
  }
  console.log(`[Bot] Replying: "${reply.slice(0, 80)}${reply.length > 80 ? '…' : ''}"`);
  await message.reply(reply);
}

module.exports = { createBot };
