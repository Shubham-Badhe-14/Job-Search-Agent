# CareerAgent AI - Architecture

## Overview
CareerAgent AI is a multi-agent system designed to automate job searching and career development. It uses a robust backend API and a Streamlit frontend.

## System Architecture

### Phases
1.  **Phase 1: Job Search & Ranking** (Resume-agnostic)
    *   **Job Discovery Agent**: Queries Adzuna API for roles.
    *   **Job Ranking Agent**: Evaluates and ranks jobs.
    *   **Job Analysis Agent**: Extracts skills and requirements.

2.  **Phase 2: Skill Gap & Learning Path** (Resume-personalized)
    *   **Resume Parsing Agent**: Extracts data from PDF resumes.
    *   **Skill Gap Agent**: Compares user skills vs. job requirements.
    *   **Learning Path Agent**: Generates a study plan.

### Components
*   **Backend (`backend/`)**:
    *   Built with **FastAPI**.
    *   Exposes endpoints for search, select, upload, and analysis.
    *   Manages CrewAI agents and tools.
*   **Frontend (`frontend/`)**:
    *   Built with **Streamlit**.
    *   Provides an interactive UI for the workflow.
*   **Data (`backend/data/`)**:
    *   JSON-based local storage for jobs and temporary resume data.

## Tech Stack
*   **Language**: Python 3.10+
*   **Orchestration**: CrewAI, LangChain
*   **LLM**: Google Gemini 2.0 Flash Lite (via `langchain-google-genai`)
*   **API**: FastAPI, Uvicorn
*   **UI**: Streamlit
*   **Tools**: Adzuna API, pdfplumber
