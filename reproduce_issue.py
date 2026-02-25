import requests
import json
import os
import sys

# Configuration
BASE_URL = "http://localhost:8000"

def test_full_flow():
    print("🚀 Starting Backend Verification...")

    # 1. Resume Upload (Mock)
    # We need a file. Let's create a dummy one.
    with open("dummy_resume.pdf", "wb") as f:
        f.write(b"%PDF-1.4 dummy content")
    
    print("\n1. Uploading Resume...")
    files = {'file': open('dummy_resume.pdf', 'rb')}
    try:
        res = requests.post(f"{BASE_URL}/resume/upload", files=files)
        if res.status_code != 200:
            print(f"❌ Upload Failed: {res.text}")
            return
        data = res.json()
        resume_content = data['parsed_content']
        print(f"✅ Upload Success. Content length: {len(resume_content)}")
    except Exception as e:
        print(f"❌ Upload Exception: {e}")
        return

    # 2. Job Search
    print("\n2. Searching Jobs (Bangalore)...")
    payload = {
        "role": "Python Developer",
        "location": "Bangalore",
        "num_results": 2
    }
    try:
        res = requests.post(f"{BASE_URL}/jobs/search", json=payload)
        if res.status_code != 200:
            print(f"❌ Search Failed: {res.text}")
            return
        data = res.json()
        jobs = data['jobs']
        print(f"✅ Search Success. Found {len(jobs)} jobs.")
        
        if not jobs:
            print("❌ No jobs found to test with.")
            return
            
        job_id = jobs[0]['id']
        print(f"👉 Selected Job ID: {job_id}")
    except Exception as e:
        print(f"❌ Search Exception: {e}")
        return

    # 3. Gap Analysis
    print(f"\n3. Gap Analysis for Job {job_id}...")
    gap_payload = {
        "resume_content": "I am a Python developer with 5 years experience in FastAPI and React.",
        "job_id": str(job_id)
    }
    try:
        res = requests.post(f"{BASE_URL}/skills/gap", json=gap_payload)
        if res.status_code != 200:
            print(f"❌ Gap Analysis Failed: {res.text}")
            return
        data = res.json()
        gap_result = data['result']
        print(f"✅ Gap Analysis Success. Result type: {type(gap_result)}")
        print(f"Result snippet: {str(gap_result)[:50]}...")
    except Exception as e:
        print(f"❌ Gap Analysis Exception: {e}")
        return

    # 4. Learning Path
    print(f"\n4. Learning Path Generation...")
    # Test with string
    path_payload = {
        "gap_analysis": str(gap_result)
    }
    try:
        res = requests.post(f"{BASE_URL}/skills/learning-path", json=path_payload)
        if res.status_code != 200:
            print(f"❌ Learning Path Failed: {res.text}")
            return
        data = res.json()
        print(f"✅ Learning Path Success. Result length: {len(data['learning_path'])}")
    except Exception as e:
        print(f"❌ Learning Path Exception: {e}")
        return

    print("\n✨ ALL SYSTEM CHECKS PASSED ✨")
    
    # Clean up
    if os.path.exists("dummy_resume.pdf"):
        os.remove("dummy_resume.pdf")

if __name__ == "__main__":
    test_full_flow()
