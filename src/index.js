'use strict';

require('dotenv').config();
const config = require('./config');
const { createBot } = require('./bot');

// Validate required environment variables before starting
try {
  config.validate();
} catch (err) {
  console.error(`[Startup] Configuration error: ${err.message}`);
  console.error('[Startup] Copy .env.example to .env and fill in your API keys.');
  process.exit(1);
}

const client = createBot();

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n[Startup] Shutting down...');
  await client.destroy();
  process.exit(0);
});

client.initialize();
