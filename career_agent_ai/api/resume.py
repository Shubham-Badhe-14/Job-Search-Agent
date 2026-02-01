from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
import os
import pdfplumber
import PyPDF2
from career_agent_ai.utils.data_store import DataStore

router = APIRouter(prefix="/resume", tags=["Resume"])

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
RESUME_PATH = os.path.join(DATA_DIR, 'current_resume.pdf')

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume PDF.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    try:
        with open(RESUME_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Optional: Parse immediately to verify
        text = _parse_resume_text(RESUME_PATH)
        if not text:
             return {"status": "warning", "message": "Resume uploaded but text extraction failed/empty."}
             
        # Store text or structured data if we want. For now just file.
        DataStore.save_resume({"path": RESUME_PATH, "extracted_preview": text[:200] + "..."})

        return {"status": "success", "message": "Resume uploaded successfully", "path": RESUME_PATH}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _parse_resume_text(file_path):
    # Quick check helper reusing logic from tool
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                t = page.extract_text()
                if t: text += t + "\n"
            if text.strip(): return text.strip()
    except:
        pass
    return None
