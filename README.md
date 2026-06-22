# CS Expert Agent 🧠

An agentic AI system that answers Computer Science questions across core subjects — built with LangGraph, Groq, and Wikipedia.

---

## Subjects Covered

OS · DBMS · Computer Architecture · Microprocessors · ML · Soft Computing · Computer Vision · Network Security · Computer Networks · DSA · OOP · System Design · Compiler Design · Software Engineering · Distributed Systems · Cloud Computing · Web Development · DevOps · Programming Fundamentals · Theory of Computation

---

## How it works

The agent breaks every question into 4 stages:

```
Question
   ↓
[Classifier]   → detects the subject via keyword scoring, falls back to LLM if needed
   ↓
[Retriever]    → fetches relevant context from Wikipedia (no API key needed)
   ↓
[Reasoner]     → synthesizes context + model knowledge into a structured answer
   ↓
[Follow-ups]   → suggests 3 questions to explore next
```

## Project Structure

```
cs-agent/
├── agent/
│   ├── state.py                # AgentState schema
│   ├── llm.py                  # Groq client
│   ├── subjects.py             # subject data and keywords
│   ├── graph.py                # graph wiring and entry point
│   ├── tools/
│   │   └── wikipedia_tool.py   # Wikipedia retrieval
│   └── nodes/
│       ├── classifier.py       # NODE 1
│       ├── retriever.py        # NODE 2
│       ├── reasoner.py         # NODE 3
│       └── followups.py        # NODE 4
├── ui/
│   └── app.py                  # Streamlit frontend
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

Get a free Groq API key at [console.groq.com](https://console.groq.com) — no credit card needed.

```bash
python -m streamlit run ui/app.py
```

Paste your key in the sidebar and ask any CS question.

---

## Stack

| Component | Tool |
|---|---|
| Agent orchestration | LangGraph |
| LLM | Groq — Llama 3.3 70B (free tier) |
| Retrieval | Wikipedia REST API (free, no key) |
| UI | Streamlit |