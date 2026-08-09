# Project 1: SlotWise — AI Booking Concierge Bot

A conversational Telegram bot built in n8n that helps customers book a restaurant table through a short, natural chat, powered by Groq's LLM.

## Niche
Restaurant table booking 

## How It Works

The bot guides a customer through the full booking flow in one AI Agent, using its system prompt and conversation memory:

1. **Greeting** — greets the customer and asks whether they want to book a table or ask a question
2. **Service / Occasion** — asks the occasion and party size
3. **Timing** — asks preferred day and rough time
4. **Slot Offer** — offers 3 fixed slots (6:00 PM, 7:30 PM, 9:00 PM)
5. **Confirmation** — confirms the booking with a summary (party size, day, time)
6. **Handoff** — if the customer negotiates pricing, complains, or goes off-script, the bot replies "Let me connect you with our team — someone will be with you shortly" instead of improvising

## Workflow Structure

Telegram Trigger → AI Agent → Send a text message
├── Groq Chat Model (llama-3.1-8b-instant)
└── Simple Memory (keyed per Telegram chat ID)


- **Telegram Trigger** — receives incoming messages
- **AI Agent** — holds the full booking flow in its system prompt; handles greeting, service, timing, slots, confirmation, and handoff
- **Groq Chat Model** — the LLM (llama-3.1-8b-instant) driving the conversation
- **Simple Memory** — remembers each user's conversation, keyed by their Telegram chat ID, so the bot moves through the steps across messages
- **Send a text message** — sends the bot's reply back to the user on Telegram

## Tech Stack
- n8n (locally hosted, exposed via ngrok static domain)
- Telegram Bot API (bot created via @BotFather)
- Groq API (free tier) for the LLM

## Files
- `SlotWise-Bot-v2.json` — exported n8n workflow
- `Telegram-bot-workflow-SS.png` — screenshot of the workflow canvas

## Setup
1. Import `SlotWise-Bot-v2.json` into n8n
2. Add your own credentials in n8n:
   - Telegram account (bot token from @BotFather)
   - Groq account (API key from console.groq.com)
3. Activate the workflow so the Telegram trigger listens for messages

## Notes
Credentials are not included in the workflow file — add your own Telegram bot token and Groq API key in n8n's credentials manager after importing.
