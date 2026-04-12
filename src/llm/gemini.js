'use strict';

const { GoogleGenerativeAI } = require('@google/generative-ai');
const config = require('../config');

let client;

function getClient() {
  if (!client) {
    if (!config.gemini.apiKey) {
      throw new Error('GEMINI_API_KEY is not set');
    }
    client = new GoogleGenerativeAI(config.gemini.apiKey);
  }
  return client;
}

/**
 * Send a message to Google Gemini and return the text response.
 * @param {string} userMessage
 * @returns {Promise<string>}
 */
async function chat(userMessage) {
  const genAI = getClient();
  const model = genAI.getGenerativeModel({
    model: config.gemini.model,
    systemInstruction: config.systemPrompt,
  });

  const result = await model.generateContent(userMessage);
  const response = result.response;
  if (!response) {
    throw new Error('Gemini returned an undefined response object');
  }
  return response.text();
}

module.exports = { chat };
