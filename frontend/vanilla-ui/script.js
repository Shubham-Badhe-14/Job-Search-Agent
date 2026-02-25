// Initialize AOS
AOS.init({
    duration: 800,
    offset: 100,
    once: true
});

// State Management
let currentResumeContent = "";
let currentJobs = [];
let selectedJobId = null;

// Mouse Glow Effect
const cursor = document.querySelector('.cursor-glow');
document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
});

// File Upload Interaction
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('resumeInput');
const fileNameDisplay = document.getElementById('fileName');

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        fileNameDisplay.textContent = `Selected: ${e.target.files[0].name}`;
        dropZone.style.borderColor = '#6c5ce7';
    }
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        fileNameDisplay.textContent = `Selected: ${e.dataTransfer.files[0].name}`;
        dropZone.style.borderColor = '#6c5ce7';
    }
});

// API Base URL
const API_BASE_URL = 'http://localhost:8000';

// Elements
const searchForm = document.getElementById('searchForm');
const loader = document.getElementById('loader');
const resultsSection = document.getElementById('results');
const jobsGrid = document.querySelector('.jobs-grid');
const roadmapSection = document.getElementById('roadmap');
const timelineContainer = document.querySelector('.timeline');
const generatePlanBtn = document.getElementById('generatePlanBtn');

// Helper: Show Loader
function showLoader(show) {
    if (show) {
        loader.classList.remove('hidden');
        loader.scrollIntoView({ behavior: 'smooth' });
    } else {
        loader.classList.add('hidden');
    }
}

// Helper: Render Jobs
function renderJobs(jobs) {
    jobsGrid.innerHTML = '';
    jobs.forEach((job, index) => {
        // Default values if missing
        const matchScore = job.match_score || job.score || Math.floor(Math.random() * 20) + 80;
        const company = job.company_name || job.company || "Unknown Company";
        const location = job.location || "Remote";
        const title = job.title || "Job Title";
        const id = job.id || `job_${index}`; // Fallback ID
        const url = job.redirect_url || job.url || '#';

        const card = document.createElement('div');
        card.className = 'job-card glass-card';
        card.setAttribute('data-aos', 'fade-up');
        card.setAttribute('data-aos-delay', index * 100);

        // Random icon color for visual variety
        const colors = ['#6c5ce7', '#00cec9', '#fd79a8', '#ffeaa7'];
        const color = colors[index % colors.length];

        card.innerHTML = `
            <div class="match-badge">${matchScore}% Match</div>
            <div class="job-icon" style="background: ${color};"><i class="fa-solid fa-briefcase"></i></div>
            <h3>${title}</h3>
            <p class="company">${company} • ${location}</p>
            <div class="tags">
                <!-- We could parse description for tags, or mock them -->
                <span>Full Time</span>
            </div>
            <div class="card-actions">
                <button class="btn-apply" onclick="window.open('${url}', '_blank')">Apply Now</button>
                <button class="btn-details" onclick="selectJob('${id}')">Select for Plan</button>
            </div>
        `;
        jobsGrid.appendChild(card);
    });
    AOS.refresh();
}

// Select Job Handler
window.selectJob = (id) => {
    selectedJobId = id;

    const job = currentJobs.find(j => j.id == id);

    if (job) {
        console.log("Selected job:", job);

        // Visual feedback on the card
        const cards = document.querySelectorAll('.job-card');
        cards.forEach(card => {
            // Reset styles
            card.style.borderColor = 'var(--glass-border)';
            card.style.transform = 'scale(1)';
        });

        // Display selection in the "Plan" section header area or near the button
        const resultsSection = document.getElementById('results');
        const centerBtnDiv = resultsSection.querySelector('.center-btn');

        // Check for existing selection message
        let msg = document.getElementById('selection-msg');
        if (!msg) {
            msg = document.createElement('div');
            msg.id = 'selection-msg';
            msg.className = 'selection-feedback glass-panel';
            msg.style.marginTop = '1.5rem';
            msg.style.textAlign = 'center';
            msg.style.border = '1px solid var(--secondary)';
            // Insert before the button container
            centerBtnDiv.parentElement.insertBefore(msg, centerBtnDiv);
        }

        msg.innerHTML = `
            <i class="fa-solid fa-check-circle" style="color: var(--secondary)"></i>
            <strong>Selected:</strong> ${job.title} at ${job.company || job.company_name}
        `;
        msg.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
};

// Handle Form Submission (Resume Upload + Search)
searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const role = searchForm.querySelector('input[placeholder="e.g. Frontend Developer"]').value;
    const location = searchForm.querySelector('input[placeholder="e.g. Remote, New York"]').value;
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload a resume first.");
        return;
    }

    showLoader(true);
    resultsSection.classList.add('hidden');
    roadmapSection.classList.add('hidden');

    try {
        // 1. Upload Resume
        const formData = new FormData();
        formData.append('file', file);

        const uploadRes = await fetch(`${API_BASE_URL}/resume/upload`, {
            method: 'POST',
            body: formData
        });

        if (!uploadRes.ok) throw new Error("Resume upload failed");
        const uploadData = await uploadRes.json();
        currentResumeContent = uploadData.parsed_content;
        console.log("Resume parsed successfully");

        // 2. Search Jobs
        const searchRes = await fetch(`${API_BASE_URL}/jobs/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                role: role,
                location: location,
                num_results: 3
            })
        });

        if (!searchRes.ok) {
            const errDetail = await searchRes.json().catch(() => ({ detail: searchRes.statusText }));
            throw new Error(`Job search failed: ${errDetail.detail || searchRes.statusText}`);
        }
        const searchData = await searchRes.json();
        currentJobs = searchData.jobs || []; // Adapt based on actual response structure

        // If jobs is a string (error message) or empty
        if (!Array.isArray(currentJobs)) {
            console.error("Unexpected jobs data:", searchData);
            currentJobs = [];
        }

        showLoader(false);
        resultsSection.classList.remove('hidden');
        renderJobs(currentJobs);
        resultsSection.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error(error);
        showLoader(false);
        alert(`Error: ${error.message}`);
    }
});

// Helper: Render Roadmap
function renderRoadmap(planText) {
    timelineContainer.innerHTML = '';

    // Safety check: ensure planText is a string
    if (typeof planText !== 'string') {
        console.warn("Expected string for planText, got:", typeof planText);
        // If it's an object with a 'raw' property (CrewOutput), try to use that
        if (planText && typeof planText === 'object' && planText.raw) {
            planText = planText.raw;
        } else {
            planText = String(planText || '');
        }
    }

    // Simple parsing of the plan text: assume lines or blocks
    // Ideally the backend returns structured JSON.
    // If it's markdown, we might need a parser.
    // For now, let's treat paragraphs as items.

    const items = planText.split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0 && (line.startsWith('-') || line.startsWith('*') || /^[0-9]+\./.test(line)));

    // If no list items found, just show the whole text in one block
    const planItems = items.length > 0 ? items : [planText];

    planItems.forEach((item, index) => {
        const side = index % 2 === 0 ? 'left' : 'right';
        const div = document.createElement('div');
        div.className = `timeline-item ${side}`;
        div.setAttribute('data-aos', side === 'left' ? 'fade-right' : 'fade-left');

        div.innerHTML = `
            <div class="content glass-card">
                <h3>Step ${index + 1}</h3>
                <p>${item
                .replace(/^(\*\*|__)?(Step\s+\d+[:\.]?|Module\s+\d+[:\.]?)(\*\*|__)?\s*/i, '') // Remove "Step 1:", "**Step 01**"
                .replace(/^(\*\*|__)?\s*\d+[\.\)]\s*(\*\*|__)?\s*/, '') // Remove "1.", "01.", "**1.**"
                .replace(/^[-*]\s*/, '') // Remove "- ", "* "
                .trim()
            }</p>
                <span class="status">Action Item</span>
            </div>
        `;
        timelineContainer.appendChild(div);
    });
    AOS.refresh();
}

// Generate Plan Handler
generatePlanBtn.addEventListener('click', async () => {
    if (!currentResumeContent) {
        alert("No resume content found. Please search again.");
        return;
    }

    // Use selected job or default to first one
    const jobToAnalyze = selectedJobId ? currentJobs.find(j => j.id == selectedJobId) : currentJobs[0];

    if (!jobToAnalyze) {
        alert("No job selected or available to analyze.");
        return;
    }

    generatePlanBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Generating...';

    try {
        // 1. Gap Analysis
        // Note: The backend expects 'job_id', but if the ID is from Adzuna (external), 
        // the backend might not have it in its DB unless we stored it.
        // However, looking at 'jobs.py', 'select_job' uses 'get_job_by_id'.
        // Check 'skills.py': analyze_gap uses get_job_by_id(request.job_id).
        // This implies the job must be in our local "database" (JSON file?).
        // If 'orchestrator.run_search' saves jobs to the local DB, we are good.
        // If not, we might fail here. 
        // Let's assume the backend handles it or we send the ID we got from search.

        const gapRes = await fetch(`${API_BASE_URL}/skills/gap`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                resume_content: currentResumeContent,
                job_id: String(jobToAnalyze.id) // Ensure ID is string
            })
        });

        if (!gapRes.ok) {
            const errDetail = await gapRes.json().catch(() => ({ detail: gapRes.statusText }));
            throw new Error(`Gap analysis failed: ${errDetail.detail || gapRes.statusText}`);
        }
        const gapData = await gapRes.json();

        // 2. Learning Path
        const pathRes = await fetch(`${API_BASE_URL}/skills/learning-path`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                gap_analysis: gapData.result
            })
        });

        if (!pathRes.ok) {
            const errDetail = await pathRes.json().catch(() => ({ detail: pathRes.statusText }));
            throw new Error(`Learning path generation failed: ${errDetail.detail || pathRes.statusText}`);
        }
        const pathData = await pathRes.json();

        generatePlanBtn.innerHTML = 'Generate Learning Roadmap <i class="fa-solid fa-wand-magic-sparkles"></i>';
        roadmapSection.classList.remove('hidden');
        renderRoadmap(pathData.learning_path);
        roadmapSection.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error(error);
        generatePlanBtn.innerHTML = 'Generate Learning Roadmap <i class="fa-solid fa-wand-magic-sparkles"></i>';

        // Show detailed error message if available
        let errorMsg = error.message;
        if (errorMsg.includes("Job search failed") || errorMsg === "Gap analysis failed" || errorMsg === "Learning path generation failed") {
            errorMsg += ". Please check the console for details.";
        }
        alert(`Error: ${errorMsg}`);
    }
});
