from crewai import Agent
from career_agent_ai.utils import get_llm

class SkillGapAgent:
    def __init__(self):
        self.llm = get_llm()

    def get_agent(self):
        return Agent(
            role='Skills Gap Analyst',
            goal='Compare candidate resume skills against job requirements to identify missing skills',
            backstory="""You are an expert in skill assessment. You receive a candidate's profile 
            and a target job description. Your job is to meticulously identify what skills the 
            candidate lacks versus what is required.""",
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )
