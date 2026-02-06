from crewai import Agent
from backend.utils.utils import get_llm

class JobAnalysisAgent:
    def __init__(self):
        self.llm = get_llm()

    def get_agent(self):
        return Agent(
            role='Job Requirements Analyst',
            goal='Analyze job descriptions to extract key skills, qualifications, and responsibilities',
            backstory="""You are a technical recruiter and job analyst. You are expert at reading 
            complex job descriptions and breaking them down into structured requirements, 
            separating hard skills, soft skills, and experience levels.""",
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )
