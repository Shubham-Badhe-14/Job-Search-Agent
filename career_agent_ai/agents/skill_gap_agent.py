from crewai import Agent
from career_agent_ai.utils.llm_provider import get_llm

def get_skill_gap_agent():
    return Agent(
        role='Skill Gap Analyst',
        goal='Identify missing skills by comparing candidate profile against job requirements.',
        backstory="""You are a critical thinker who analyzes the gap between current capabilities 
        and desired targets. You objectively categorize skills into 'matched', 'missing', 
        and 'partial' to provide a clear picture of what is needed for the role.""",
        verbose=True,
        llm=get_llm(),
        allow_delegation=False
    )
