# CareerAgent AI (Local MVP)

A modular, API-driven multi-agent system for personalized job search and career development.

## 🚀 Features

### Phase 1: AI-Powered Job Search
- **Job Discovery**: Fetches jobs via Adzuna API.
- **Job Analysis**: Extracts required skills from descriptions.
- **Job Ranking**: Ranks jobs by relevance and quality.

### Phase 2: Resume & Skills Engine
- **Resume Parsing**: Extracts structured data from PDF resumes using `pdfplumber`.
- **Skill Gap Analysis**: Compares candidate skills vs. job requirements.
- **Learning Path Generation**: personalized roadmap to bridge skill gaps.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Shubham-Badhe-14/Job-Search-Agent.git
    cd Job-Search-Agent
    ```

2.  **Set up Virtual Environment**:
    ```bash
    python3 -m venv agent_env
    source agent_env/bin/activate
    pip install -r requirements.txt
    pip install pytest httpx  # For testing
    ```

3.  **Configure Environment**:
    Create a `.env` file with your API keys:
    ```ini
    GOOGLE_API_KEY=AIz...
    ADZUNA_APP_ID=...
    ADZUNA_API_KEY=...
    ```

## 🏃 Usage

### Start the API
```bash
uvicorn career_agent_ai.app:app --reload
```
The API will be available at `http://127.0.0.1:8000`.
Check the interactive docs at `http://127.0.0.1:8000/docs`.

### API Endpoints

- **Job Search**:
    - `POST /jobs/search`: Trigger agentic search.
    - `GET /jobs/ranked`: Retrieve ranked jobs.
    - `POST /jobs/select`: Select a job for skill analysis.

- **Career Development**:
    - `POST /resume/upload`: Upload PDF resume.
    - `POST /skills/gap`: Analyze skill gap for selected job.
    - `POST /skills/learning-path`: Generate learning path.

## 🧪 Testing

Run unit tests:
```bash
python -m pytest career_agent_ai/tests/
```

## 📂 Project Structure

```
career_agent_ai/
├── agents/             # CrewAI Agents (Discovery, Analysis, Ranking, Skills, Learning)
├── tools/              # Tools (Adzuna Search, Resume Parser)
├── api/                # FastAPI Routers
├── data/               # Local JSON storage
├── tests/              # Unit and integration tests
├── app.py              # Application entry point
├── orchestrator.py     # Agent workflow orchestration
└── utils.py            # Shared utilities
```
