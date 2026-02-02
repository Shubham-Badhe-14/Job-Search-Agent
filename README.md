# 🚀 CareerAgent AI

A robust, multi-agent AI system designed to automate job searching, skill gap analysis, and personalized career development planning. Powered by **Google Gemini 2.0 Flash Lite** and **CrewAI**.

![Status: Stable](https://img.shields.io/badge/Status-Stable-green)
![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI: Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)

## ✨ Key Features

### 🤖 Intelligent Agents (Phase 2)
*   **Job Discovery Agent**: Intelligently queries the Adzuna API to find relevant roles.
*   **Job Ranking Specialist**: Evaluates and ranks jobs based on description quality and relevance.
*   **Skills Gap Analyst**: Extracts skills from your uploaded PDF resume and compares them against target job requirements.
*   **Learning Path Curator**: Generates personalized study plans (courses, docs, projects) to bridge identified gaps.

### 🛡️ "Antigravity" Resilience
*   **Smart Rate Limiting**: Features a custom exponential backoff system to gracefully handle API rate limits (429 errors).
*   **Gemini Lite Optimization**: Tuned to use the efficient `gemini-flash-lite-latest` model for high availability.

### 💻 Interfaces
*   **Backend**: High-performance **FastAPI** server with documented endpoints.
*   **Frontend**: Interactive **Streamlit** dashboard for easy testing and visualization.

---

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Shubham-Badhe-14/Job-Search-Agent.git
    cd Job-Search-Agent
    ```

2.  **Setup Environment**:
    We provided helper scripts to make this easy.
    ```bash
    # This will create the 'agent_env' virtual environment and install dependencies
    ./run_backend.sh
    # (Press Ctrl+C after it starts to exit)
    ```
    *Alternatively, manually:*
    ```bash
    python3 -m venv agent_env
    source agent_env/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure Keys**:
    Create a `.env` file in the root directory:
    ```ini
    GOOGLE_API_KEY=your_gemini_key_here
    ADZUNA_APP_ID=your_adzuna_app_id
    ADZUNA_API_KEY=your_adzuna_api_key
    ```

---

## 🚀 Usage

We call it the **"Two-Terminal"** setup.

### 1. Start the Brain (Backend) 🧠
Open your first terminal and run:
```bash
./run_backend.sh
```
*   API Docs will be at: `http://localhost:8000/docs`

### 2. Start the Interface (Frontend) 💻
Open a **second terminal** and run:
```bash
./run_frontend.sh
```
*   This will automatically open the UI in your browser at `http://localhost:8501`.

---

## 🧪 Workflow Validation

1.  **Upload Resume**: Drag & Drop your PDF resume in the sidebar.
2.  **Search Jobs**: Enter a query (e.g., "Data Scientist" in "New York").
3.  **Select Job**: Choose a promising result from the list.
4.  **Gap Analysis**: Click "Analyze Skill Gaps" to see what you're missing.
5.  **Learning Plan**: Generate a roadmap to get hired!

---

## 📂 Project Structure

```
career_agent_ai/
├── agents/             # CrewAI Agent Definitions
├── tools/              # Custom Tools (Adzuna, PDF Parser)
├── api/                # FastAPI Route Handlers
├── data/               # Local JSON Data Store
│   └── resumes/        # (Ignored by Git for privacy)
├── app.py              # Backend Entry Point
├── orchestrator.py     # Agent Workflow Logic
└── utils.py            # LLM Configuration & Retry Logic
```

## 🔐 Privacy Note
This repository is configured to **ignore** all PDF files in the `data/resumes/` directory. Your personal data stays on your local machine.
