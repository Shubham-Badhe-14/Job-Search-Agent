from crewai import Crew, Task, Process
from career_agent_ai.agents.resume_parsing_agent import get_resume_parsing_agent
from career_agent_ai.agents.skill_gap_agent import get_skill_gap_agent
from career_agent_ai.agents.learning_path_agent import get_learning_path_agent
from career_agent_ai.utils.data_store import DataStore
import json

class SkillGapCrew:
    def __init__(self):
        self.resume_agent = get_resume_parsing_agent()
        self.gap_agent = get_skill_gap_agent()
        self.learning_agent = get_learning_path_agent()

    def analyze_gap(self, job_description: str, resume_path: str = None):
        # 1. Parse Resume Task (if needed, or just context)
        # We assume we need to parse it fresh or load it.
        # But if resume_path is provided, we parse.
        
        tasks_list = []
        
        parse_task = None
        if resume_path:
            parse_task = Task(
                description=f"Parse the resume at: {resume_path}. Extract skills, experience, and education.",
                expected_output="Structured text or JSON of the resume.",
                agent=self.resume_agent
            )
            tasks_list.append(parse_task)
        else:
            # Maybe load from store? For now assume it's passed or parsed.
            pass

        # 2. Gap Analysis
        gap_task = Task(
            description=f"""Analyze the skill gap.
            
            Target Job Description:
            {job_description}
            
            Compare against the candidate's resume (provided in context or previous task).
            Identify:
            - Matched Skills
            - Missing Skills
            - Partial skills (matches but needs improvement)
            - Match Percentage (0-100)
            """,
            expected_output="Detailed skill gap analysis.",
            agent=self.gap_agent,
            context=[parse_task] if parse_task else [] # If parse task exists, use its output
        )
        tasks_list.append(gap_task)

        # 3. Learning Path
        learning_task = Task(
            description="""Based on the identified Missing and Partial skills, create a personalized learning path.
            - List specific topics to learn.
            - Order them logically (foundational to advanced).
            - Suggest types of projects to build.
            """,
            expected_output="Step-by-step learning path.",
            agent=self.learning_agent,
            context=[gap_task]
        )
        tasks_list.append(learning_task)

        crew = Crew(
            agents=[self.resume_agent, self.gap_agent, self.learning_agent],
            tasks=tasks_list,
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        return str(result)
