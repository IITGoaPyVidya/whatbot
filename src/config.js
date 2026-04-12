import "dotenv/config";

function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

export const config = {
  geminiApiKey: requireEnv("GEMINI_API_KEY"),
  groqApiKey: requireEnv("GROQ_API_KEY"),

  // Which Gemini model to use (free tier supports gemini-1.5-flash)
  geminiModel: process.env.GEMINI_MODEL || "gemini-1.5-flash",

  // Which Groq model to use (free tier supports llama-3.3-70b-versatile)
  groqModel: process.env.GROQ_MODEL || "llama-3.3-70b-versatile",

  // System prompt sent to the LLM on every message
  systemPrompt:
    process.env.SYSTEM_PROMPT ||
    "You are a helpful and friendly WhatsApp assistant. Keep responses concise and conversational.",

  // Max tokens in LLM response
  maxTokens: parseInt(process.env.MAX_TOKENS || "512", 10),
};
