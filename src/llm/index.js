'use strict';

const config = require('../config');
const gemini = require('./gemini');
const groq = require('./groq');

// Round-robin state for "auto" mode
let turn = 0;

/**
 * Route a message to the appropriate LLM provider and return the reply.
 * @param {string} userMessage
 * @returns {Promise<string>}
 */
async function chat(userMessage) {
  const provider = config.llmProvider;

  if (provider === 'gemini') {
    return gemini.chat(userMessage);
  }

  if (provider === 'groq') {
    return groq.chat(userMessage);
  }

  // "auto" – round-robin between Gemini and Groq
  const useGemini = turn % 2 === 0;
  turn += 1;

  try {
    return useGemini
      ? await gemini.chat(userMessage)
      : await groq.chat(userMessage);
  } catch (primaryErr) {
    console.warn(
      `[LLM] ${useGemini ? 'Gemini' : 'Groq'} failed, falling back to ${useGemini ? 'Groq' : 'Gemini'}: ${primaryErr.message}`
    );
    // Fallback to the other provider
    return useGemini
      ? groq.chat(userMessage)
      : gemini.chat(userMessage);
  }
}

module.exports = { chat };
