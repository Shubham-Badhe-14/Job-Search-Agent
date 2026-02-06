from crewai import Agent
from backend.utils.utils import get_llm

class LearningPathAgent:
    def __init__(self):
        self.llm = get_llm()

    def get_agent(self):
        return Agent(
            role='Learning & Development Specialist',
            goal='Create personalized learning paths to close skill gaps',
            backstory="""You are a curriculum designer and career coach. Based on identified skill gaps, 
            you suggest resources (courses, books, projects) to help candidates acquire necessary skills 
            efficiently.""",
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )
