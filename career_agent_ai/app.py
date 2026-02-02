from fastapi import FastAPI
from career_agent_ai.api import jobs, resume, skills

app = FastAPI(
    title="CareerAgent AI",
    description="A multi-agent system for job search and career development.",
    version="0.1.0"
)

app.include_router(jobs.router)
app.include_router(resume.router)
app.include_router(skills.router)

@app.get("/")
async def root():
    return {"message": "Welcome to CareerAgent AI API. Visit /docs for documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
