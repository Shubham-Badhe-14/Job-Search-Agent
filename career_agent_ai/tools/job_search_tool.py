import json
import os
import requests
from dotenv import load_dotenv
from crewai.tools import tool

load_dotenv()

@tool("Job Search Tool")
def search_jobs(input_json: str) -> str:
    """
    Search for job listings using the Adzuna API.
    
    Args:
        input_json: JSON string with schema {'role': '<role>', 'location': '<location>', 'num_results': <number>}
    
    Returns:
        JSON string of job listings or error message
    """
    try:
        # Check if required environment variables are loaded
        required_vars = ['ADZUNA_APP_ID', 'ADZUNA_API_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            return json.dumps({"error": f"Missing environment variables: {missing_vars}"})
        
        input_data = json.loads(input_json)
        role = input_data['role']
        location = input_data['location']
        num_results = input_data.get('num_results', 5)
    except (json.JSONDecodeError, KeyError) as e:
        return json.dumps({"error": "Invalid input format. Expected JSON with 'role', 'location', 'num_results'."})

    app_id = os.getenv('ADZUNA_APP_ID')
    api_key = os.getenv('ADZUNA_API_KEY')
    
    base_url = "http://api.adzuna.com/v1/api/jobs"
    url = f"{base_url}/us/search/1"
    
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
                'id': job.get('id', 'N/A'),
                'title': job.get('title', 'N/A'),
                'company': job.get('company', {}).get('display_name', 'N/A'),
                'location': job.get('location', {}).get('display_name', 'N/A'),
                'salary_min': job.get('salary_min', 'Not specified'),
                'salary_max': job.get('salary_max', 'Not specified'),
                'description': job.get('description', ''),
                'url': job.get('redirect_url', 'N/A')
            }
            job_listings.append(job_details)
        
        return json.dumps(job_listings)
        
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"API Request Error: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"})
