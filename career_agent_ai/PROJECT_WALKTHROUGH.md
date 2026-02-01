# CareerAgent AI (Local MVP) - Project Walkthrough

## Overview
I have successfully refactored the monolithic `job_search.py` into a modular, API-first system called **CareerAgent AI**. 
The system is designed with a clear separation of concerns:
1.  **Phase 1**: Job Search & Ranking (Resume-agnostic).
2.  **Phase 2**: Skill Gap & Learning Path (Resume-personalized).

## Directory Structure
The project is now organized in `career_agent_ai/`:
- **`agents/`**: Contains specialized agents (`JobDiscovery`, `JobAnalysis`, `ResumeParsing`, etc.).
- **`crews/`**: Manages multi-agent workflows (`JobSearchCrew`, `SkillGapCrew`).
- **`tools/`**: Reusable tools (`resume_parser.py`, `job_search_tool.py`).
- **`api/`**: FastAPI routers exposing the functionality.
- **`data/`**: JSON-based local storage.
- **`tests/`**: Unit tests.

## Key Changes
- **Modularization**: Converted the single script into specialized modules.
- **API-First**: Replaced CLI interaction with a REST API (`app.py`).
- **Two-Phase Flow**: 
    - Job Search runs independently first.
    - Resume analysis is triggered *only* after selecting a target job.
- **Testing**: Added unit tests for the resume parser and validation logic.

## How to Run
1.  **Install Dependencies**:
    ```bash
    pip install crewai langchain langchain-openai langchain-google-genai fastapi uvicorn requests python-dotenv PyPDF2 pdfplumber
    ```

2.  **Start the Server**:
    ```bash
    python career_agent_ai/app.py
    ```

3.  **Use the API**:
    Open your browser to `http://127.0.0.1:8000/docs`.
    - **Search**: POST `/jobs/search`
    - **Select**: POST `/jobs/select`
    - **Upload Resume**: POST `/resume/upload`
    - **Get Gap Analysis**: GET `/skills/gap`

## Verification
I have added unit tests in `career_agent_ai/tests/`. Run them with:
```bash
python -m unittest discover career_agent_ai/tests
```
