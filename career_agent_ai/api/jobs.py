from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from career_agent_ai.orchestrator import JobSearchOrchestrator
from career_agent_ai.data_manager import load_jobs, get_job_by_id

router = APIRouter(prefix="/jobs", tags=["jobs"])
orchestrator = JobSearchOrchestrator()

class JobSearchRequest(BaseModel):
    role: str
    location: str
    num_results: Optional[int] = 5

class JobSelectRequest(BaseModel):
    job_id: str

@router.post("/search")
async def search_jobs_endpoint(request: JobSearchRequest):
    """
    Trigger a specialized job search agent workflow.
    """
    try:
        results = orchestrator.run_search(request.role, request.location, request.num_results)
        return {"status": "success", "jobs": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ranked")
async def get_ranked_jobs():
    """
    Get the list of currently stored (ranked) jobs.
    """
    jobs = load_jobs()
    return {"jobs": jobs}

@router.post("/select")
async def select_job(request: JobSelectRequest):
    """
    Select a job for further analysis (Phase 2).
    """
    job = get_job_by_id(request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Store selection? For now just return it to confirm.
    # In Phase 2 we might store 'selected_job.json'
    return {"status": "selected", "job": job}
