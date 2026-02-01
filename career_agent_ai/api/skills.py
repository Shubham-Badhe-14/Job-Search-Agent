from fastapi import APIRouter, HTTPException
from career_agent_ai.crews.skill_gap_crew import SkillGapCrew
import os
import json

router = APIRouter(prefix="/skills", tags=["Skills"])

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
SELECTED_JOB_FILE = os.path.join(DATA_DIR, 'selected_job.json')
RESUME_PATH = os.path.join(DATA_DIR, 'current_resume.pdf')

@router.get("/gap")
async def analyze_gap():
    """
    Trigger Skill Gap Analysis + Learning Path for the selected job.
    """
    if not os.path.exists(SELECTED_JOB_FILE):
        raise HTTPException(status_code=400, detail="No job selected. Please select a job first.")
    
    if not os.path.exists(RESUME_PATH):
        raise HTTPException(status_code=400, detail="No resume found. Please upload a resume first.")
        
    try:
        with open(SELECTED_JOB_FILE, 'r') as f:
            job_data = json.load(f)
            
        # Job description is likely in 'description' field
        job_description = job_data.get('description', '')
        if not job_description:
             # If just title, we might have a problem, but let's pass what we have
             job_description = str(job_data)

        crew = SkillGapCrew()
        result = crew.analyze_gap(job_description, RESUME_PATH)
        
        return {"status": "success", "data": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/learning-path")
async def get_learning_path():
    # In our current Flow, /gap returns everything including learning path.
    # We could separate them, but CrewAI runs them in sequence.
    # We'll just point to /gap for now or implement a separate Crew run if needed.
    return {"status": "info", "message": "Please use /skills/gap to generate the full analysis including learning path."}
