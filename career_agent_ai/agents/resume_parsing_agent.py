from crewai import Agent
from career_agent_ai.tools.resume_parser import parse_resume
from career_agent_ai.utils.llm_provider import get_llm

def get_resume_parsing_agent():
    return Agent(
        role='Resume Parsing Specialist',
        goal='Extract and structure information from candidate resumes.',
        backstory="""You are an expert at parsing unstructured resume data into structured formats. 
        You identify key skills, work experience, education, and achievements from PDF text. 
        You are detail-oriented and ensure no critical information is missed.""",
        verbose=True,
        llm=get_llm(),
        allow_delegation=False,
        tools=[parse_resume]
    )
