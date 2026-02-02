import streamlit as st
import requests
import json
import os

# Configuration
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="CareerAgent AI", page_icon="🚀", layout="wide")

st.title("🚀 CareerAgent AI (Testing Interface)")

# Session State Initialization
if 'resume_content' not in st.session_state:
    st.session_state.resume_content = None
if 'jobs' not in st.session_state:
    st.session_state.jobs = []
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = None
if 'gap_analysis' not in st.session_state:
    st.session_state.gap_analysis = None
if 'learning_path' not in st.session_state:
    st.session_state.learning_path = None

# Sidebar - Progress
st.sidebar.header("Workflow Progress")
steps = {
    "1. Resume": st.session_state.resume_content is not None,
    "2. Search": len(st.session_state.jobs) > 0,
    "3. Select": st.session_state.selected_job is not None,
    "4. Gap Analysis": st.session_state.gap_analysis is not None,
    "5. Plan": st.session_state.learning_path is not None
}

for step, done in steps.items():
    if done:
        st.sidebar.success(step)
    else:
        st.sidebar.warning(step)

# --- Step 1: Upload Resume ---
st.header("1. Upload Resume")
uploaded_file = st.file_uploader("Upload your data-science-resume.pdf", type="pdf")

if uploaded_file:
    if st.button("Process Resume"):
        with st.spinner("Parsing resume..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            try:
                response = requests.post(f"{API_URL}/resume/upload", files=files)
                if response.status_code == 200:
                    data = response.json()
                    # The tool parses it and returns "✅ Resume parsed successfully!\n\nResume Content:\n..."
                    # We might want to clean it up or just store it.
                    content = data.get("parsed_content", "")
                    if isinstance(content, str):
                        st.session_state.resume_content = content
                        st.success("Resume parsed successfully!")
                        with st.expander("View Parsed Content"):
                            st.text(content[:1000] + "...")
                    else:
                        st.error("Unexpected response format")
                else:
                    st.error(f"Failed to upload: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

# --- Step 2: Job Search ---
st.header("2. Job Search")
col1, col2, col3 = st.columns(3)
with col1:
    role = st.text_input("Target Role", "Data Scientist")
with col2:
    location = st.text_input("Location", "New York")
with col3:
    num_results = st.number_input("Number of Jobs", min_value=1, max_value=10, value=3)

if st.button("Search Jobs"):
    with st.spinner("Searching and analyzing jobs (this may take a minute)..."):
        try:
            payload = {"role": role, "location": location, "num_results": num_results}
            response = requests.post(f"{API_URL}/jobs/search", json=payload)
            if response.status_code == 200:
                data = response.json()
                st.session_state.jobs = data.get("jobs", [])
                st.success(f"Found {len(st.session_state.jobs)} jobs!")
            else:
                st.error(f"Search failed: {response.text}")
        except Exception as e:
            st.error(f"Connection Error: {e}")

# --- Step 3: Select Job ---
if st.session_state.jobs:
    st.header("3. Select Job")
    
    # Create valid options for selectbox
    job_options = {f"{j.get('title', 'N/A')} at {j.get('company', 'N/A')}": j for j in st.session_state.jobs}
    
    selected_option = st.selectbox("Choose a job to analyze:", list(job_options.keys()))
    
    if selected_option:
        job = job_options[selected_option]
        with st.expander("Job Details", expanded=True):
            st.markdown(f"**Title:** {job.get('title')}")
            st.markdown(f"**Company:** {job.get('company')}")
            st.markdown(f"**Location:** {job.get('location')}")
            st.markdown(f"**Description:**\n{job.get('description')}")
            st.markdown(f"**URL:** [Link]({job.get('url')})")
        
        if st.button("Select This Job"):
            st.session_state.selected_job = job
            st.success("Job selected!")

# --- Step 4: Gap Analysis ---
if st.session_state.selected_job and st.session_state.resume_content:
    st.header("4. Skill Gap Analysis")
    if st.button("Analyze Skill Gaps"):
        with st.spinner("Analyzing skill gaps against selected job..."):
            try:
                payload = {
                    "resume_content": st.session_state.resume_content,
                    "job_id": str(st.session_state.selected_job.get("id", "unknown")) 
                }
                # Note: job_id is just for logging/reference in this simple MVP flow or if we stored it
                # The Orchestrator actually needs job details if it's not looking up by ID from a DB.
                # However, our /skills/gap endpoint expects 'job_id' and looks it up.
                # We saved jobs to jobs.json during search, so get_job_by_id should work IF id matches.
                
                response = requests.post(f"{API_URL}/skills/gap", json=payload)
                if response.status_code == 200:
                    result = response.json().get("result")
                    
                    # Extract raw text if it's a dict
                    if isinstance(result, dict) and "raw" in result:
                        result = result["raw"]
                        
                    st.session_state.gap_analysis = result
                    st.success("Analysis complete!")
                else:
                    st.error(f"Analysis failed: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

    if st.session_state.gap_analysis:
        st.markdown("### 📊 Analysis Results")
        st.markdown(st.session_state.gap_analysis)

# --- Step 5: Learning Path ---
if st.session_state.gap_analysis:
    st.header("5. Personalized Learning Path")
    if st.button("Generate Learning Path"):
        with st.spinner("Generating learning path..."):
            try:
                # The API expects just the gap analysis string wrapped in JSON
                payload = {"gap_analysis": str(st.session_state.gap_analysis)}
                response = requests.post(f"{API_URL}/skills/learning-path", json=payload)
                
                if response.status_code == 200:
                    path = response.json().get("learning_path")
                    
                    # Extract raw text if it's a dict
                    if isinstance(path, dict) and "raw" in path:
                        path = path["raw"]
                        
                    st.session_state.learning_path = path
                    st.success("Plan generated!")
                else:
                    st.error(f"Generation failed: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

    if st.session_state.learning_path:
        st.markdown("### 🎓 Your Learning Plan")
        st.markdown(st.session_state.learning_path)
