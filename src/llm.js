import { GoogleGenerativeAI } from "@google/generative-ai";
import Groq from "groq-sdk";
import { config } from "./config.js";

const geminiClient = new GoogleGenerativeAI(config.geminiApiKey);
const groqClient = new Groq({ apiKey: config.groqApiKey });

/**
 * Ask Google Gemini for a reply.
 * @param {string} userMessage
 * @returns {Promise<string>}
 */
async function askGemini(userMessage) {
  const model = geminiClient.getGenerativeModel({
    model: config.geminiModel,
    systemInstruction: config.systemPrompt,
  });

  const result = await model.generateContent({
    contents: [{ role: "user", parts: [{ text: userMessage }] }],
    generationConfig: { maxOutputTokens: config.maxTokens },
  });

  return result.response.text();
}

/**
 * Ask Groq for a reply.
 * @param {string} userMessage
 * @returns {Promise<string>}
 */
async function askGroq(userMessage) {
  const completion = await groqClient.chat.completions.create({
    model: config.groqModel,
    messages: [
      { role: "system", content: config.systemPrompt },
      { role: "user", content: userMessage },
    ],
    max_tokens: config.maxTokens,
  });

  return completion.choices[0].message.content;
}

/**
 * Get an LLM reply. Tries Gemini first; falls back to Groq on error.
 * @param {string} userMessage
 * @returns {Promise<string>}
 */
export async function getLLMReply(userMessage) {
  try {
    const reply = await askGemini(userMessage);
    console.log("[LLM] Used Gemini");
    return reply;
  } catch (geminiError) {
    console.warn("[LLM] Gemini failed, falling back to Groq:", geminiError.message);
    try {
      const reply = await askGroq(userMessage);
      console.log("[LLM] Used Groq (fallback)");
      return reply;
    } catch (groqError) {
      console.error("[LLM] Both providers failed:", groqError.message);
      return "Sorry, I'm having trouble reaching my AI backend right now. Please try again in a moment.";
    }
  }
}
