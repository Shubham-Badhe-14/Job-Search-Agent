from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from career_agent_ai.tools.resume_parser import parse_resume

router = APIRouter(prefix="/resume", tags=["resume"])

RESUME_DIR = "career_agent_ai/data/resumes"

if not os.path.exists(RESUME_DIR):
    os.makedirs(RESUME_DIR)

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume PDF and extract its text content.
    """
    file_location = f"{RESUME_DIR}/{file.filename}"
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

    # Use the tool to parse it
    # note: parse_resume is a langchain tool, we need to call its func or invoke it.
    # checking tool definition: it has `parse_resume` function decorated with @tool.
    # We can call it directly if logic is straightforward or use .run()
    
    # Since I defined `parse_resume` as a function decorated with @tool, I can call it.
    # However, LangChain tools usually return string.
    try:
        # The tool expects a string file_path argument if invoked via agent, 
        # but if called as function, we pass arguments.
        # Let's check the tool definition again. It takes `file_path`.
        result = parse_resume.invoke({"file_path": file_location})
        
        # Save parsed content for later use?
        # Ideally we store it in session or return it to client.
        return {"status": "success", "filename": file.filename, "parsed_content": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {e}")
