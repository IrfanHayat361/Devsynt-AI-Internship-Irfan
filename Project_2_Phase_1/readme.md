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
    └── Working_Page.png    the page running in a browser
```

## What I learned

I learned that LangChain gives you reusable components — prompt templates, chains and output parsers — on top of a plain LLM API call, so prompts can be reused and replies can be returned in a structured form instead of free text. I also covered memory and tool-calling, which let an app carry context across calls and let the model choose functions to use rather than guessing an answer.

The main takeaway was the difference between a chain and an agent. A chain always follows a fixed path, while LangGraph builds the flow as a graph of nodes, edges and shared state, where conditional edges decide the route at runtime. This is the reason our upcoming orchestrator agent needs LangGraph, since it has to route incoming data to different agents depending on what it receives.

