from crewai import Crew, Task, Process
from backend.agents.job_discovery_agent import get_job_discovery_agent
from backend.agents.job_analysis_agent import get_job_analysis_agent
from backend.agents.job_ranking_agent import get_job_ranking_agent
from backend.utils.data_store import DataStore
import json

class JobSearchCrew:
    def __init__(self):
        self.discovery_agent = get_job_discovery_agent()
        self.analysis_agent = get_job_analysis_agent()
        self.ranking_agent = get_job_ranking_agent()

    def run_search(self, role: str, location: str, num_results: int = 5):
        search_params = json.dumps({
            'role': role,
            'location': location,
            'num_results': num_results
        })

        search_task = Task(
            description=f"""Search for current job openings for the '{role}' role in '{location}'. 
            Use the Job Search tool. Find at least {num_results} relevant positions.
            Input parameters: {search_params}
            IMPORTANT: Return ONLY the raw JSON output from the tool. Do not add markdown or extra text.""",
            expected_output="A JSON list of job objects.",
            agent=self.discovery_agent
        )

        crew = Crew(
            agents=[self.discovery_agent],
            tasks=[search_task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        # CrewAI result is usually a string. We try to parse it or just save it.
        # Since the tool returns JSON string, the agent might pass it through.
        # Ideally, we want to parse it.
        try:
            # Clean up potential markdown code blocks
            clean_result = str(result).replace("```json", "").replace("```", "").strip()
            jobs = json.loads(clean_result)
            DataStore.save_jobs(jobs)
            return jobs
        except Exception as e:
            print(f"Error parsing search results: {e}. Raw: {str(result)}")
            # Fallback: if it's just text, maybe try to extract json or just return raw
            return {"raw_output": str(result), "error": str(e)}

    def run_ranking(self):
        jobs = DataStore.get_jobs()
        if not jobs:
            return {"error": "No jobs found to rank. Run search first."}
        
        jobs_str = json.dumps(jobs, indent=2)
        
        analysis_task = Task(
            description=f"""Analyze the following job listings. 
            For each job, extract the required skills (Core, Preferred, Bonus).
            Jobs Data: {jobs_str}""",
            expected_output="Structured analysis of skills for each job.",
            agent=self.analysis_agent
        )
        
        ranking_task = Task(
            description="""Rank the analyzed jobs based on clarity of requirements and general quality.
            Since we don't have a candidate profile yet, rank by 'Skill Density' (how well defined the role is).
            Return the Top 5 jobs as a JSON list with their analysis.""",
            expected_output="JSON list of ranked jobs.",
            agent=self.ranking_agent,
            context=[analysis_task]  # Depends on analysis
        )

        crew = Crew(
            agents=[self.analysis_agent, self.ranking_agent],
            tasks=[analysis_task, ranking_task],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        return str(result)
