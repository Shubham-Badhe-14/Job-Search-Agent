import json
import os
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
JOBS_FILE = os.path.join(DATA_DIR, 'jobs.json')
RESUME_FILE = os.path.join(DATA_DIR, 'resumes.json')

class DataStore:
    @staticmethod
    def _ensure_dir():
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

    @staticmethod
    def save_jobs(jobs: List[Dict[str, Any]]):
        DataStore._ensure_dir()
        with open(JOBS_FILE, 'w') as f:
            json.dump(jobs, f, indent=2)

    @staticmethod
    def get_jobs() -> List[Dict[str, Any]]:
        if not os.path.exists(JOBS_FILE):
            return []
        with open(JOBS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    @staticmethod
    def save_resume(data: Dict[str, Any]):
        DataStore._ensure_dir()
        with open(RESUME_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def get_resume() -> Dict[str, Any]:
        if not os.path.exists(RESUME_FILE):
            return {}
        with open(RESUME_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
