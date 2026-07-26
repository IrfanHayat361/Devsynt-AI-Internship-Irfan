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

## Task 2: WhatsApp Bot - Phase 1 ✅

### Niche Chosen
**Dental Clinic Booking Bot** — A bilingual WhatsApp bot that helps patients book appointments at a dental clinic.

### Key Features

#### 1. **Bilingual Support (English & Arabic)**
- Bot automatically detects language from incoming messages
- Arabic script detection triggers Arabic responses
- Mid-conversation language switching is supported
- All messages exist in both languages

#### 2. **Conversation States**
- **State 0:** Language Detection (automatic, no message)
- **State 1:** Greeting & Intent (Book appointment or Ask question?)
- **State 2:** Service Selection (Checkup, Cleaning, Whitening)
- **State 3:** Timing Preference (Tomorrow, 2-3 days, next week, specific date)
- **State 4:** Available Slots (Mock calendar slots for chosen date)
- **State 5:** Booking Confirmation (Summary with service, date, time)

#### 3. **Human Handoff**
The bot escalates to a human agent for:
- Medical questions or health concerns
- Complaints or disputes
- Pricing negotiations
- Anything off-script requiring judgment

**Why This Matters:** Medical queries need professional oversight. Complaints need empathy. Pricing needs negotiation. The handoff state is what makes this a professional solution, not a toy chatbot.

#### 4. **Nudge System (Appointment Reminders)**
- **+1h Nudge:** Free-form reminder message (within 24h WhatsApp window)
- **+24h Nudge:** Template message (requires Meta approval — noted for production)
- **+72h Final Nudge:** Template message (requires Meta approval — noted for production)
- **Lost Lead:** If no response after +72h, mark as lost

### Webhook Setup & Testing

**Webhook Created:**
- URL: `http://localhost:5678/webhook-test/whatsapp-incoming`
- Method: POST
- Status: ✅ Tested and working

**Testing Method:**
- Used Postman to send mock WhatsApp messages to the webhook
- Received 200 OK responses
- n8n execution log shows messages received successfully

### Project Files Structure

devsynt-ai-internship-irfan/
├── README.md (this file)
└── task2-whatsapp-phase1/
├── assets/
│ ├── flow-diagram.png (Conversation flow visualization)
│ ├── webhook-test-postman.png (Postman 200 OK response)
│ └── webhook-execution-log.png (n8n receiving message)
├── messages.md (All bot messages EN + AR)
└── workflow.json (Exported n8n workflow)
