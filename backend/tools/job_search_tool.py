import os
import json
import requests
from dotenv import load_dotenv
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

load_dotenv()

class JobSearchToolInput(BaseModel):
    """Input parameters for the Job Search Tool."""
    role: str = Field(..., description="The job role to search for (e.g., 'Data Scientist').")
    location: str = Field(..., description="The location to search in (e.g., 'New York').")
    num_results: int = Field(5, description="Number of results to return (default 5).")

class JobSearchTool(BaseTool):
    name: str = "Job Search Tool"
    description: str = "Search for job listings using the Adzuna API."
    args_schema: Type[BaseModel] = JobSearchToolInput

    def _run(self, role: str, location: str, num_results: int = 5) -> str:
        """
        Search for job listings using the Adzuna API.
        """
        # Check if required environment variables are loaded
        required_vars = ['ADZUNA_APP_ID', 'ADZUNA_API_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            error_msg = "❌ Missing required environment variables in .env file:\n"
            for var in missing_vars:
                error_msg += f"   - {var}\n"
            return error_msg
        
        if not role or not location:
                return "Error: 'role' and 'location' are required fields."

        app_id = os.getenv('ADZUNA_APP_ID')
        api_key = os.getenv('ADZUNA_API_KEY')
        
        base_url = "http://api.adzuna.com/v1/api/jobs"
        country = 'us' 
        url = f"{base_url}/{country}/search/1"
        
        params = {
            'app_id': app_id,
            'app_key': api_key,
            'results_per_page': num_results,
            'what': role,
            'where': location,
            'content-type': 'application/json'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            jobs_data = response.json()

            job_listings = []
            
            for job in jobs_data.get('results', []):
                job_details = {
                    'id': job.get('id'), 
                    'title': job.get('title', 'N/A'),
                    'company': job.get('company', {}).get('display_name', 'N/A'),
                    'location': job.get('location', {}).get('display_name', 'N/A'),
                    'salary': str(job.get('salary_min', 'Not specified')), 
                    'description': job.get('description', '')[:300] + '...' if job.get('description') else 'No description',
                    'url': job.get('redirect_url', 'N/A')
                }
                
                formatted_job = f"""
Title: {job_details['title']}
Company: {job_details['company']}
Location: {job_details['location']}
Salary: {job_details['salary']}
Description: {job_details['description']}
URL: {job_details['url']}
---"""
                job_listings.append(formatted_job)
            
            if not job_listings:
                 return "No jobs found for the specified criteria."
                 
            return '\n'.join(job_listings)
            
        except requests.exceptions.HTTPError as err:
            return f"HTTP Error: {err}"
        except requests.exceptions.RequestException as e:
            return f"Request Error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"

# Export an instance of the tool
search_jobs = JobSearchTool()
