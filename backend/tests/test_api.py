from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from backend.app import app
from backend.services.orchestrator import JobSearchOrchestrator

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to CareerAgent AI API. Visit /docs for documentation."}

@patch('backend.routes.jobs.orchestrator')
def test_search_jobs(mock_orchestrator):
    # Mock the return value of the orchestrator
    mock_results = [{
        "id": "job_1",
        "title": "Software Engineer",
        "company": "Tech Corp",
        "location": "Remote",
        "salary": "120k",
        "description": "Great job",
        "url": "http://example.com"
    }]
    mock_orchestrator.run_search.return_value = mock_results

    response = client.post("/jobs/search", json={"role": "Software Engineer", "location": "Remote"})
    
    assert response.status_code == 200
    assert response.json()["jobs"][0]["title"] == "Software Engineer"
    mock_orchestrator.run_search.assert_called_once_with("Software Engineer", "Remote", 5)

@patch('backend.routes.jobs.load_jobs')
def test_get_ranked_jobs(mock_load_jobs):
    mock_load_jobs.return_value = [{"id": "job_1", "title": "SE"}]
    response = client.get("/jobs/ranked")
    assert response.status_code == 200
    assert response.json()["jobs"][0]["title"] == "SE"

@patch('backend.routes.jobs.get_job_by_id')
def test_select_job_found(mock_get_job):
    mock_get_job.return_value = {"id": "job_1", "title": "SE"}
    response = client.post("/jobs/select", json={"job_id": "job_1"})
    assert response.status_code == 200
    assert response.json()["job"]["id"] == "job_1"

@patch('backend.routes.jobs.get_job_by_id')
def test_select_job_not_found(mock_get_job):
    mock_get_job.return_value = None
    response = client.post("/jobs/select", json={"job_id": "non_existent"})
    assert response.status_code == 404
