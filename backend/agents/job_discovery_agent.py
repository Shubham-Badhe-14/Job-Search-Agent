from crewai import Agent
from backend.tools.job_search_tool import search_jobs
from backend.utils.utils import get_llm

class JobDiscoveryAgent:
    def __init__(self):
        self.llm = get_llm()

    def get_agent(self):
        return Agent(
            role='Senior Job Search Specialist',
            goal='Find the most relevant job opportunities that match the specified criteria',
            backstory="""You are an expert job search specialist with extensive experience in 
            identifying high-quality job opportunities. You excel at understanding job 
            market trends and finding the perfect matches.""",
            verbose=True,
            llm=self.llm,
            tools=[search_jobs],
            allow_delegation=False
        )
