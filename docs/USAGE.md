# Usage Guide

## Prerequisites
*   Python 3.10+ installed.
*   API Keys for Google Gemini and Adzuna.

## Setup
1.  **Configure Environment**:
    Copy `Configs/.env.example` to `.env` and fill in your keys.
    ```bash
    cp configs/.env.example .env
    ```

2.  **Install Application**:
    Run the setup script to create a virtual environment and install dependencies.
    ```bash
    ./scripts/setup_env.sh
    ```

## Running the Application

### Option 1: Run All (Recommended)
Starts both backend and frontend in a single terminal.
```bash
./scripts/run_all.sh
```

### Option 2: Run Separately
**Backend**:
```bash
./scripts/run_backend.sh
```
Docs available at `http://localhost:8000/docs`.

**Frontend**:
```bash
./scripts/run_frontend.sh
```
UI available at `http://localhost:8501`.

## Workflow
1.  **Upload Resume**: Upload your PDF resume in the sidebar.
2.  **Job Search**: Enter target role and location.
3.  **Select Job**: Choose a job from the search results.
4.  **Gap Analysis**: View missing skills.
5.  **Learning Path**: Get a customized learning plan.
