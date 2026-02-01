from fastapi import FastAPI
from career_agent_ai.api import jobs, resume, skills
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

app = FastAPI(
    title="CareerAgent AI (Local MVP)",
    description="Agentic AI system for Job Search and Skill Gap Analysis",
    version="1.0.0"
)

# Include Routers
app.include_router(jobs.router)
app.include_router(resume.router)
app.include_router(skills.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to CareerAgent AI API",
        "endpoints": {
            "search_jobs": "/jobs/search",
            "rank_jobs": "/jobs/ranked",
            "select_job": "/jobs/select",
            "upload_resume": "/resume/upload",
            "analyze_gap": "/skills/gap"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
