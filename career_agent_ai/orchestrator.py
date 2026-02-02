import json
import time
from crewai import Crew, Task, Process
from career_agent_ai.agents.job_discovery_agent import JobDiscoveryAgent
from career_agent_ai.agents.job_analysis_agent import JobAnalysisAgent
from career_agent_ai.agents.job_ranking_agent import JobRankingAgent
from career_agent_ai.agents.skill_gap_agent import SkillGapAgent
from career_agent_ai.agents.learning_path_agent import LearningPathAgent
from career_agent_ai.tools.job_search_tool import search_jobs
from career_agent_ai.data_manager import save_jobs
from career_agent_ai.utils import get_llm
import re

class JobSearchOrchestrator:
    def __init__(self):
        self.llm = get_llm()
        self.discovery_agent = JobDiscoveryAgent().get_agent()
        self.analysis_agent = JobAnalysisAgent().get_agent()
        self.ranking_agent = JobRankingAgent().get_agent()
        self.skill_gap_agent = SkillGapAgent().get_agent()
        self.learning_path_agent = LearningPathAgent().get_agent()

    def run_search(self, role: str, location: str, num_results: int = 5):
        # Define Tasks
        search_params = json.dumps({
            'role': role,
            'location': location,
            'num_results': num_results
        })

        search_task = Task(
            description=f"""Search for {num_results} job openings for the role '{role}' in '{location}'. 
            Use the Job Search Tool with these parameters: role='{role}', location='{location}', num_results={num_results}.
            The output must contain the full job details including IDs/URLs found by the tool.""",
            expected_output="A list of job postings with title, company, location, salary, description, and URL.",
            agent=self.discovery_agent,
            tools=[search_jobs]
        )

        analysis_task = Task(
            description="""Analyze the job listings provided by the previous task. 
            Extract key skills (hard and soft), experience levels, and any specific requirements.
            Format the output as a list of structured job objects.""",
            expected_output="Detailed analysis of each job listing with extracted skills.",
            agent=self.analysis_agent,
            context=[search_task]
        )

        ranking_task = Task(
            description=f"""Rank the analyzed jobs based on relevance to the role '{role}'.
            Provide a justification for the ranking.
            IMPORTANT: Your final output MUST be valid JSON list of objects, where each object has:
            - id (can be generated if missing, or use URL as unique key)
            - title
            - company
            - location
            - salary
            - description
            - skills (list of strings)
            - rank_reason
            Do not include markdown formatting like ```json ... ``` in the final output, just the raw JSON string if possible, 
            or ensure it is easily extractable.""",
            expected_output="A JSON list of ranked job objects.",
            agent=self.ranking_agent,
            context=[analysis_task]
        )

        crew = Crew(
            agents=[self.discovery_agent, self.analysis_agent, self.ranking_agent],
            tasks=[search_task, analysis_task, ranking_task],
            process=Process.sequential,
            verbose=True,
            manager_llm=self.llm
        )

        print("⏳ Waiting 15s to respect Rate Limits...")
        time.sleep(15)

        result = crew.kickoff()
        
        # Attempt to parse result as JSON and save
        # CrewAI output is a string. We might need to clean it.
        cleaned_result = str(result)
        
        # Robustly extract JSON block
        json_match = re.search(r'\[.*\]', cleaned_result, re.DOTALL)
        if json_match:
            cleaned_result = json_match.group(0)
        else:
            # Fallback: try removing markdown code blocks if no list found
            cleaned_result = cleaned_result.replace("```json", "").replace("```", "").strip()
        
        try:
            jobs_data = json.loads(cleaned_result)
            # Ensure they look like jobs
            if isinstance(jobs_data, list):
                # Add IDs if missing
                for i, job in enumerate(jobs_data):
                    if 'id' not in job:
                        job['id'] = f"job_{i}"
                save_jobs(jobs_data)
                return jobs_data
        except json.JSONDecodeError:
            print("Failed to parse CrewAI output as JSON. Saving raw text as description for one entry.")
            # Fallback: save one dummy job with the text
            fallback_jobs = [{
                'id': 'error_parsing',
                'title': 'Search Result (Parse Error)',
                'description': str(result),
                'company': 'N/A',
                'location': location,
                'salary': 'N/A',
                'skills': [],
                'rank_reason': 'Output was not valid JSON'
            }]
            save_jobs(fallback_jobs)
            return fallback_jobs

        return result

    def analyze_skill_gap(self, resume_content: str, job_details: dict):
        gap_task = Task(
            description=f"""Compare the candidate's resume skills against the target job requirements.
            
            Resume:
            {resume_content[:2000]}... (truncated if too long)
            
            Target Job:
            {json.dumps(job_details, indent=2)}
            
            Identify missing skills, matched skills, and strict requirements not met.
            Output must be a structured analysis.""",
            expected_output="Structured skill gap analysis.",
            agent=self.skill_gap_agent
        )
        
        crew = Crew(
            agents=[self.skill_gap_agent],
            tasks=[gap_task],
            process=Process.sequential,
            verbose=True
        )
        return crew.kickoff()

    def generate_learning_path(self, gap_analysis: str):
        path_task = Task(
            description=f"""Based on the following skill gap analysis, create a learning path.
            
            Gap Analysis:
            {gap_analysis}
            
            Suggest specific courses, documentation, or projects to bridge these gaps.
            Prioritize the most critical missing skills.""",
            expected_output="A personalized learning path with resources.",
            agent=self.learning_path_agent
        )
        
        crew = Crew(
            agents=[self.learning_path_agent],
            tasks=[path_task],
            process=Process.sequential,
            verbose=True
        )
        return crew.kickoff()
