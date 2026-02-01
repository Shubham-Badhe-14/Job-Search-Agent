from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from career_agent_ai.crews.job_search_crew import JobSearchCrew
from career_agent_ai.utils.data_store import DataStore

router = APIRouter(prefix="/jobs", tags=["Jobs"])

class JobSearchParams(BaseModel):
    role: str
    location: str
    num_results: int = 5

class JobSelection(BaseModel):
    job_id: str  # Or index, or title if ID not available
    job_data: dict # Full job data to be safe, or fetch from store

@router.post("/search")
async def search_jobs(params: JobSearchParams):
    crew = JobSearchCrew()
    try:
        results = crew.run_search(params.role, params.location, params.num_results)
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ranked")
async def rank_jobs():
    crew = JobSearchCrew()
    try:
        ranked_results = crew.run_ranking()
        # ranked_results is likely a markdown string or stringified JSON from CrewAI
        return {"status": "success", "data": ranked_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/select")
async def select_job(selection: JobSelection):
    """
    Select a job to focus on for Phase 2.
    Stores the selected job in a temporary 'selected_job.json'.
    """
    try:
        import os
        import json
        DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        SELECTED_JOB_FILE = os.path.join(DATA_DIR, 'selected_job.json')
        
        with open(SELECTED_JOB_FILE, 'w') as f:
            json.dump(selection.job_data, f, indent=2)
            
        return {"status": "success", "message": "Job selected", "job": selection.job_data.get('title')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
