from crewai import Agent
from backend.utils.utils import get_llm

class JobRankingAgent:
    def __init__(self):
        self.llm = get_llm()

    def get_agent(self):
        return Agent(
            role='Job Evaluation & Ranking Specialist',
            goal='Evaluate and rank job opportunities based on relevance and quality',
            backstory="""You are a career strategist. Your job is to assess a list of 
            job opportunities and rank them. You consider factors like role clarity, 
            company reputation (inferred), and alignment with the search criteria.""",
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )
