from fastapi import APIRouter, HTTPException, Body
import asyncio
from pydantic import BaseModel
from typing import Any
from backend.services.orchestrator import get_orchestrator
from backend.utils.data_manager import get_job_by_id

router = APIRouter(prefix="/skills", tags=["skills"])

class GapAnalysisRequest(BaseModel):
    resume_content: str
    job_id: str

@router.post("/gap")
async def analyze_gap(request: GapAnalysisRequest):
    """
    Analyze skill gap between provided resume content and selected job.
    """
    job = get_job_by_id(request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    try:
        orchestrator = get_orchestrator()
        # orchestrator now returns a string
        result = await asyncio.to_thread(orchestrator.analyze_skill_gap, request.resume_content, job)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/learning-path")
async def learning_path(gap_analysis: Any = Body(..., embed=True)):
    """
    Generate learning path based on gap analysis text.
    Accepts string or object (converted to string).
    """
    # Ensure gap_analysis is a string
    if not isinstance(gap_analysis, str):
        gap_analysis = str(gap_analysis)
    try:
        orchestrator = get_orchestrator()
        # orchestrator now returns a string
        result = await asyncio.to_thread(orchestrator.generate_learning_path, gap_analysis)
        return {"learning_path": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
