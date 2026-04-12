'use strict';

const dotenv = require('dotenv');
dotenv.config();

function requireEnv(name) {
  const val = process.env[name];
  if (!val) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return val;
}

module.exports = {
  gemini: {
    apiKey: process.env.GEMINI_API_KEY || '',
    model: process.env.GEMINI_MODEL || 'gemini-1.5-flash',
  },
  groq: {
    apiKey: process.env.GROQ_API_KEY || '',
    model: process.env.GROQ_MODEL || 'llama3-8b-8192',
  },
  llmProvider: process.env.LLM_PROVIDER || 'auto',
  botPrefix: process.env.BOT_PREFIX || '',
  respondInGroups: process.env.RESPOND_IN_GROUPS === 'true',
  systemPrompt:
    process.env.SYSTEM_PROMPT ||
    'You are a helpful WhatsApp assistant. Keep your answers short and clear.',

  /** Validate that at least one LLM key is present */
  validate() {
    const provider = this.llmProvider;
    if (provider === 'gemini' || provider === 'auto') {
      requireEnv('GEMINI_API_KEY');
    }
    if (provider === 'groq' || provider === 'auto') {
      requireEnv('GROQ_API_KEY');
    }
  },
};
