import os
import json
import requests
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

@tool("Job Search Tool")
def search_jobs(role: str, location: str, num_results: int = 5) -> str:
    """
    Search for job listings using the Adzuna API.
    
    Args:
        role: The job role to search for (e.g., "Data Scientist").
        location: The location to search in (e.g., "New York").
        num_results: Number of results to return (default 5).
    
    Returns:
        Formatted string of job listings or error message.
    """
    # Check if required environment variables are loaded
    required_vars = ['ADZUNA_APP_ID', 'ADZUNA_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        error_msg = "❌ Missing required environment variables in .env file:\n"
        for var in missing_vars:
            error_msg += f"   - {var}\n"
        return error_msg
    
    # No need to parse JSON anymore, arguments are passed directly
    if not role or not location:
            return "Error: 'role' and 'location' are required fields."

    app_id = os.getenv('ADZUNA_APP_ID')
    api_key = os.getenv('ADZUNA_API_KEY')
    
    base_url = "http://api.adzuna.com/v1/api/jobs"
    # Country code could be parametrized if needed, defaulting to 'us' as per original script
    # Original script used 'us', sticking to that but could be 'gb', etc.
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
        raw_jobs = [] # To be used if we want structured data later, but tool returns string
        
        for job in jobs_data.get('results', []):
            job_details = {
                'id': job.get('id'), # Useful for selection later
                'title': job.get('title', 'N/A'),
                'company': job.get('company', {}).get('display_name', 'N/A'),
                'location': job.get('location', {}).get('display_name', 'N/A'),
                'salary': str(job.get('salary_min', 'Not specified')), # Convert to string to avoid format issues
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
