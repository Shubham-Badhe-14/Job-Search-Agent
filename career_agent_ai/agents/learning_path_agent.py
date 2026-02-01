from crewai import Agent
from career_agent_ai.utils.llm_provider import get_llm

def get_learning_path_agent():
    return Agent(
        role='Learning Strategy Advisor',
        goal='Create personalized learning paths to close skill gaps.',
        backstory="""You are an experienced educator and career coach. You design step-by-step 
        learning roadmaps that are practical and achievable. You recommend specific resources 
        and timeline estimates to help candidates upskill effectively.""",
        verbose=True,
        llm=get_llm(),
        allow_delegation=False
    )
