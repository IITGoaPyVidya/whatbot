'use strict';

const Groq = require('groq-sdk');
const config = require('../config');

let client;

function getClient() {
  if (!client) {
    if (!config.groq.apiKey) {
      throw new Error('GROQ_API_KEY is not set');
    }
    client = new Groq({ apiKey: config.groq.apiKey });
  }
  return client;
}

/**
 * Send a message to Groq and return the text response.
 * @param {string} userMessage
 * @returns {Promise<string>}
 */
async function chat(userMessage) {
  const groq = getClient();

  const completion = await groq.chat.completions.create({
    model: config.groq.model,
    messages: [
      { role: 'system', content: config.systemPrompt },
      { role: 'user', content: userMessage },
    ],
  });

  const content = completion.choices[0]?.message?.content;
  if (!content) {
    console.warn('[Groq] Received an empty response from the API');
    return '';
  }
  return content;
}

module.exports = { chat };
