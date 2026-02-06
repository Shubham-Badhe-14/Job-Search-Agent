import json
import os
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
JOBS_FILE = os.path.join(DATA_DIR, "jobs.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_jobs(jobs: List[Dict[str, Any]]):
    ensure_data_dir()
    with open(JOBS_FILE, 'w') as f:
        json.dump(jobs, f, indent=2)

def load_jobs() -> List[Dict[str, Any]]:
    ensure_data_dir()
    if not os.path.exists(JOBS_FILE):
        return []
    try:
        with open(JOBS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def get_job_by_id(job_id: str) -> Dict[str, Any]:
    jobs = load_jobs()
    for job in jobs:
        if str(job.get('id')) == str(job_id):
            return job
    return None
