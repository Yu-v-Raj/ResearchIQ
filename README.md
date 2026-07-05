<div align="center">

# 🧠 ResearchIQ

### Intelligent Multi-Agent AI Research Platform

ResearchIQ is an AI-powered multi-agent research assistant that automates web research using specialized AI agents for searching, reading, writing, and critiquing.

---

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=for-the-badge&logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-Agent-green?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-MultiAgent-orange?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Llama3.3-purple?style=for-the-badge)

</div>

---

# 📖 Overview

ResearchIQ is a modular **Multi-Agent AI Research Platform** designed to automate the complete research workflow.

Unlike traditional AI assistants that rely on a single prompt, ResearchIQ divides the task into multiple specialized AI agents. Each agent performs a dedicated responsibility—from discovering relevant information to producing a refined research report.

The project demonstrates modern concepts in **Agentic AI**, **LLM orchestration**, **tool calling**, **web intelligence**, and **scalable AI system design**.

---

# 🚀 Motivation

Large Language Models are powerful, but a single model often struggles to perform complex research reliably.

ResearchIQ solves this problem by decomposing research into specialized AI agents.

Each agent focuses on one responsibility, producing higher-quality and more maintainable results while keeping the architecture modular and extensible.

---

# ✨ Current Features

### 🔍 Search Agent

- Intelligent web search
- Retrieves relevant websites
- Uses Tavily Search API
- Filters relevant search results

---

### 📄 Reader Agent

- Reads webpages
- Scrapes article content
- Removes noisy HTML
- Extracts meaningful information

---

### ✍️ Writer Agent

- Creates structured research reports
- Organizes information logically
- Produces human-readable summaries

---

### 🧠 Critic Agent

- Reviews generated reports
- Identifies weak sections
- Suggests improvements

---

### ⚡ Research Progress Tracking

- Live progress updates
- Pipeline status visualization
- Success & error notifications
- Research completion indicator

---

### 🎨 Modern User Interface

- Responsive Streamlit UI
- Clean dashboard
- Dark theme
- User-friendly workflow

---

# 🏗 Multi-Agent Architecture

```
                    User Query
                         │
                         ▼
                  Search Agent
                         │
                         ▼
                  Reader Agent
                         │
                         ▼
                  Writer Agent
                         │
                         ▼
                  Critic Agent
                         │
                         ▼
                  Final Research Report
```

---

# 🔄 Research Workflow

```
User enters research topic
        │
        ▼
Search relevant sources
        │
        ▼
Scrape webpages
        │
        ▼
Generate research report
        │
        ▼
Critique report quality
        │
        ▼
Display final report
```

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Frontend | Streamlit |
| AI Framework | LangChain |
| Agent Framework | LangGraph |
| LLM | Groq (Llama-3.3-70B) |
| Search API | Tavily |
| Web Scraping | BeautifulSoup |
| Environment | python-dotenv |

---

# 📂 Project Structure

```
ResearchIQ/

├── app.py
├── agents.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── README.md
├── .gitignore
└── assets/
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/Yu-v-Raj/ResearchIQ.git
```

Go into the project

```bash
cd ResearchIQ
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```
GROQ_API_KEY=YOUR_GROQ_API_KEY
TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

---

# ▶ Running

```bash
streamlit run app.py
```

---

# 📸 Screenshots

> Screenshots will be added as development progresses.

---

# 🎯 Project Goals

ResearchIQ aims to explore modern Agentic AI systems through modular AI agents that collaborate to perform complex research tasks.

The project emphasizes:

- Agent orchestration
- Modular architecture
- LLM workflows
- Prompt engineering
- Scalable AI systems
- Production-ready software practices

---

# 🗺 Development Roadmap

## ✅ Phase 1 (Completed)

- Multi-Agent Architecture
- Search Agent
- Reader Agent
- Writer Agent
- Critic Agent
- Modern Streamlit UI
- Live Progress Tracking
- Git Version Control
- GitHub Repository

---

## 🚧 Phase 2 (In Progress)

- Research History
- PDF Export
- Markdown Export
- Copy Report
- Research Statistics
- Token Usage Dashboard

---

## 🔜 Phase 3

- Source Credibility Analysis
- Automatic Citations
- DOCX Export
- Report Templates
- Duplicate Source Detection

---

## 🔜 Phase 4

- Planner Agent
- Reflection Loop
- Follow-up Chat
- Multi-step Research Planning

---

## 🔜 Phase 5

- Retrieval-Augmented Generation (RAG)
- PDF Upload
- ChromaDB / FAISS
- Semantic Search
- Conversational Memory

---

## 🔜 Phase 6

- Authentication
- Google Login
- User Dashboard
- Saved Reports
- Cloud Database

---

## 🔜 Phase 7

- FastAPI Backend
- Docker Support
- CI/CD Pipeline
- Unit Testing
- GitHub Actions
- Cloud Deployment

---

# 🚀 Future Enhancements

ResearchIQ is being developed toward a production-grade AI research platform.

Planned capabilities include:

- Multi-LLM support (GPT, Claude, Gemini, Groq, DeepSeek)
- Planner Agent
- Reflection Agent
- Retrieval-Augmented Generation (RAG)
- Document Intelligence
- Voice Input
- Speech Output
- Interactive Charts
- Timeline Generation
- Mind Maps
- Source Credibility Ranking
- REST API
- Docker Deployment
- Kubernetes Support
- Redis Caching
- PostgreSQL
- LangSmith Observability
- Authentication
- Analytics Dashboard
- Plugin System

---

# 💡 Skills Demonstrated

- Python Development
- Agentic AI
- Multi-Agent Systems
- LangChain
- LangGraph
- Prompt Engineering
- LLM Tool Calling
- Web Scraping
- AI Workflow Design
- Modular Software Architecture
- API Integration
- Software Engineering Best Practices

---

# 📄 License

This project is licensed under the MIT License.

---

<div align="center">

### ⭐ If you like this project, consider giving it a star.

Built with ❤️ by **Yuvraj Sharma**

</div>
