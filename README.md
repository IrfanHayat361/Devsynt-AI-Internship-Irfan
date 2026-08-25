# DevSynt AI Automation Internship

**Name:** Irfan Hayat  
**Program:** DevSynt AI Automation Internship – Summer 2026  
**Repository:** https://github.com/IrfanHayat361/Devsynt-AI-Internship-Irfan

---

## Overview

This repository tracks my progress during the DevSynt Summer 2026 AI Automation Internship.
---

## Task 1: Set Up n8n and Push to GitHub ✅

### Completed
- ✅ n8n installed locally and running on `localhost:5678`
- ✅ ngrok configured with static domain: `haphazard-relight-unripe.ngrok-free.dev`
- ✅ n8n exposed to internet via static ngrok URL
- ✅ GitHub repository created and README pushed

---

# Project 2: SlotWise — AI Booking Concierge Bot

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


# Project 2 — Phase 1

A static HTML learning page summarising the LangChain and LangGraph concepts covered in this phase.

## How to run

Open `index.html` in any browser. No setup or installation is needed. Keep `index.html` and `style.css` in the same folder so the styling loads correctly.

## Files

```
project2-phase1/
├── index.html      the learning showcase page
├── style.css       styling for the page
├── README.md       this file
└── screenshots/
    └── page-preview.png    the page running in a browser
```

## What I learned

I learned that LangChain gives you reusable components — prompt templates, chains and output parsers — on top of a plain LLM API call, so prompts can be reused and replies can be returned in a structured form instead of free text. I also covered memory and tool-calling, which let an app carry context across calls and let the model choose functions to use rather than guessing an answer.

The main takeaway was the difference between a chain and an agent. A chain always follows a fixed path, while LangGraph builds the flow as a graph of nodes, edges and shared state, where conditional edges decide the route at runtime. This is the reason our upcoming orchestrator agent needs LangGraph, since it has to route incoming data to different agents depending on what it receives.
