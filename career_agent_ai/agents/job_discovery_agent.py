from crewai import Agent
from career_agent_ai.tools.job_search_tool import search_jobs
from career_agent_ai.utils.llm_provider import get_llm

def get_job_discovery_agent():
    return Agent(
        role='Senior Job Discovery Specialist',
        goal='Find the most relevant job opportunities based on the user\'s criteria.',
        backstory="""You are an expert job search specialist with extensive experience in 
        identifying high-quality job opportunities from various sources. 
        You are precise and focused on finding the latest and most relevant openings.""",
        verbose=True,
        llm=get_llm(),
        allow_delegation=False,
        tools=[search_jobs]
    )
