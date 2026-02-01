from crewai import Agent
from career_agent_ai.utils.llm_provider import get_llm

def get_job_ranking_agent():
    return Agent(
        role='Job Ranking Specialist',
        goal='Rank job opportunities based on skill density and relevance to the search criteria.',
        backstory="""You are a rational and objective specialist who ranks options based on quantifiable data. 
        You evaluate how well a job description matches the standard requirements for the role 
        and identify the highest quality opportunities.""",
        verbose=True,
        llm=get_llm(),
        allow_delegation=False
    )
