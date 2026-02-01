# CareerAgent AI (Local MVP)

A comprehensive, local-first AI-powered job search and career development system. Orignally based on a monolithic script, this project has been refactored into a modular, API-driven architecture using CrewAI, LangChain, and FastAPI.

## Architecture

The system is divided into two distinct phases:

### Phase 1: AI-Powered Job Search
- **Goal**: Find and rank relevant job opportunities.
- **Agents**:
    - `Job Discovery Agent`: Fetches jobs via Adzuna API.
    - `Job Analysis Agent`: Extracts required skills from descriptions.
    - `Job Ranking Agent`: Ranks jobs by quality and relevance.
- **Flow**: Search -> Analyze -> Rank -> Select

### Phase 2: Resume & Skills Engine
- **Goal**: Personalized skill gap analysis and learning path.
- **Trigger**: Activated *only* after a user selects a job from Phase 1.
- **Agents**:
    - `Resume Parsing Agent`: Extracts structured data from PDF resumes.
    - `Skill Gap Agent`: Compares resume skills vs. selected job requirements.
    - `Learning Path Agent`: Generates a personalized learning roadmap.
- **Flow**: Upload Resume -> Select Job -> Gap Analysis -> Learning Path

## Project Structure

```
career_agent_ai/
├── agents/             # Agent definitions (Role, Goal, Backstory)
├── tools/              # Tools (Job Search, Resume Parser)
├── crews/              # Orchestration logic (JobSearchCrew, SkillGapCrew)
├── api/                # FastAPI routers
├── data/               # Local JSON storage
├── tests/              # Unit tests
├── utils/              # Helper utilities
└── app.py              # Main API entry point
```

## Setup & Usage

1. **Prerequisites**
   - Python 3.9+
   - API Keys: `ADZUNA_APP_ID`, `ADZUNA_API_KEY`, `OPENAI_API_KEY` (or `GOOGLE_API_KEY`).

2. **Installation**
   ```bash
   pip install crewai langchain langchain-openai langchain-google-genai fastapi uvicorn requests python-dotenv PyPDF2 pdfplumber
   ```

3. **Environment Variables**
   Create a `.env` file in the root:
   ```
   OPENAI_API_KEY=sk-...
   ADZUNA_APP_ID=...
   ADZUNA_API_KEY=...
   # Optional
   GOOGLE_API_KEY=...
   ```

4. **Running the API**
   ```bash
   python career_agent_ai/app.py
   ```
   The API will start at `http://127.0.0.1:8000`.

5. **API Documentation**
   Visit `http://127.0.0.1:8000/docs` to interact with the API endpoints.

## API Workflow

1. **Search Jobs**: `POST /jobs/search` with `{ "role": "Data Scientist", "location": "New York" }`.
2. **View Ranked**: `GET /jobs/ranked` to see analyzed results.
3. **Select Job**: `POST /jobs/select` with the chosen job details.
4. **Upload Resume**: `POST /resume/upload` with a PDF file.
5. **Analyze Gap**: `GET /skills/gap` to receive the gap analysis and learning path.
