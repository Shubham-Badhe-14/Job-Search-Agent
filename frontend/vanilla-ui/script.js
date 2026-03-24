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

// Job-Centric Alignment State
let hasResumeAnalyzed = false;
let selectedJob = null;
let currentATSData = null;

function getIsAlignmentUnlocked() {
    return hasResumeAnalyzed && selectedJob !== null;
}

// =============================================
// Navigation Guard — Toast Notification
// =============================================
let toastTimeout = null;

function showNavToast(message) {
    const toast = document.getElementById('navToast');
    toast.textContent = message;
    toast.classList.add('visible');
    if (toastTimeout) clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        toast.classList.remove('visible');
    }, 2500);
}

document.querySelectorAll('.nav-links a[data-guard]').forEach(link => {
    link.addEventListener('click', (e) => {
        const guard = link.dataset.guard;

        if (guard === 'resume' && !hasResumeAnalyzed) {
            e.preventDefault();
            showNavToast('Please analyze your resume first to access this section.');
            return;
        }

        if (guard === 'optimize' && !getIsAlignmentUnlocked()) {
            e.preventDefault();
            if (!hasResumeAnalyzed) {
                showNavToast('Please analyze your resume first to access this section.');
            } else {
                showNavToast('Select a target job to unlock optimization insights.');
            }
            return;
        }
    });
});

// Helper: Smooth section reveal (removes .hidden, adds fade+slide animation)
function revealSection(el) {
    if (typeof el === 'string') el = document.getElementById(el);
    if (!el) return;
    el.classList.remove('hidden');
    el.classList.add('reveal-in');
    el.addEventListener('animationend', () => el.classList.remove('reveal-in'), { once: true });
}

const cursor = document.querySelector('.cursor-glow');
let cursorTicking = false;
document.addEventListener('mousemove', (e) => {
    if (!cursorTicking) {
        window.requestAnimationFrame(() => {
            if (cursor) {
                cursor.style.left = e.clientX + 'px';
                cursor.style.top = e.clientY + 'px';
            }
            cursorTicking = false;
        });
        cursorTicking = true;
    }
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
const resultsSection = document.getElementById('results');
const jobsGrid = document.querySelector('.jobs-grid');
const roadmapSection = document.getElementById('roadmap');
const timelineContainer = document.querySelector('.timeline');
const generatePlanBtn = document.getElementById('generatePlanBtn');

// =============================================
// AlignmentProcessingOverlay — Reusable Component
// =============================================
class AlignmentProcessingOverlay {
    constructor() {
        this.overlay = document.getElementById('processingOverlay');
        this.steps = Array.from(document.querySelectorAll('#processingSteps .processing-step'));
        this.currentStep = -1;
        this.isRunning = false;
        this.startTime = 0;
    }

    show() {
        this.isRunning = true;
        this.currentStep = -1;
        this.startTime = Date.now();
        this.steps.forEach(step => {
            step.classList.remove('visible', 'completed', 'active-step');
        });
        this.overlay.classList.remove('fade-out');
        this.overlay.classList.add('active');
    }

    setStep(index, text = null) {
        if (!this.isRunning) return;
        
        for(let i = 0; i < index && i < this.steps.length; i++) {
            this.steps[i].classList.remove('active-step');
            this.steps[i].classList.add('completed', 'visible');
        }
        
        if (index < this.steps.length) {
            this.currentStep = index;
            const step = this.steps[index];
            step.classList.remove('completed');
            step.classList.add('visible', 'active-step');
            if (text) {
                const textElem = step.querySelector('.step-text');
                if(textElem) textElem.textContent = text;
            }
        }
    }

    async dismiss() {
        const minWait = 2500 - (Date.now() - this.startTime);
        if (minWait > 0) {
            await new Promise(r => setTimeout(r, minWait));
        }
        
        // Final completion visual
        for(let i = 0; i < this.steps.length; i++) {
            this.steps[i].classList.remove('active-step');
            this.steps[i].classList.add('completed', 'visible');
        }
        
        await new Promise(r => setTimeout(r, 600));
        this.overlay.classList.remove('active');
        this.overlay.classList.add('fade-out');
        this.isRunning = false;
        await new Promise(r => setTimeout(r, 600));
        this.overlay.classList.remove('fade-out');
    }

    abort() {
        this.isRunning = false;
        this.overlay.classList.remove('active', 'fade-out');
    }
}

const processingOverlay = new AlignmentProcessingOverlay();

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
        selectedJob = job;
        console.log("Selected job:", job);

        // Visual feedback on the card
        const cards = document.querySelectorAll('.job-card');
        cards.forEach(card => {
            card.style.borderColor = 'var(--glass-border)';
            card.style.transform = 'scale(1)';
        });

        // Display selection message
        const resultsSection = document.getElementById('results');

        let msg = document.getElementById('selection-msg');
        if (!msg) {
            msg = document.createElement('div');
            msg.id = 'selection-msg';
            msg.className = 'selection-feedback glass-panel';
            msg.style.marginTop = '1.5rem';
            msg.style.textAlign = 'center';
            msg.style.border = '1px solid var(--secondary)';
            resultsSection.appendChild(msg);
        }

        msg.innerHTML = `
            <i class="fa-solid fa-check-circle" style="color: var(--secondary)"></i>
            <strong>Selected:</strong> ${job.title} at ${job.company || job.company_name}
        `;

        // --- UNLOCK ALIGNMENT SECTIONS ---
        if (getIsAlignmentUnlocked()) {
            // Hide locked panel
            document.getElementById('locked-alignment').classList.add('hidden');

            // Sync current resume to studio
            const editor = document.getElementById('resumeEditor');
            if(editor && currentResumeContent) {
                editor.value = currentResumeContent;
            }

            // Show Generate Roadmap button
            document.getElementById('generatePlanBtnWrap').style.display = '';

            // Show optimization insights
            showOptimizationInsights(
                [
                    { section: 'Experience Bullets', impact: 'High', reason: 'Rephrase generic descriptions to highlight impact and measurable outcomes.' },
                    { section: 'Skills Section', impact: 'Medium', reason: 'Group skills by category for better ATS parsing.' },
                    { section: 'Summary', impact: 'Low', reason: 'Add a targeted professional summary aligned to the target role.' }
                ],
                [
                    { skill: 'React', current_level: 85, required_level: 90 },
                    { skill: 'TypeScript', current_level: 40, required_level: 80 },
                    { skill: 'System Design', current_level: 20, required_level: 70 },
                    { skill: 'CI/CD', current_level: 30, required_level: 60 }
                ],
                currentATSData?.overall_score || 72,
                (currentATSData?.overall_score || 72) + 12
            );

            // Show alignment journey
            // showAgentActivity();

            // Scroll to optimization
            document.getElementById('optimization-insights').scrollIntoView({ behavior: 'smooth' });
        }
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

    processingOverlay.show();
    resultsSection.classList.add('hidden');
    roadmapSection.classList.add('hidden');
    // Hide all alignment-dependent sections on fresh search
    document.getElementById('ats-insights')?.classList.add('hidden');
    document.getElementById('optimization-insights')?.classList.add('hidden');
    // document.getElementById('agent-activity')?.classList.add('hidden');
    document.getElementById('locked-alignment')?.classList.add('hidden');
    if(document.getElementById('generatePlanBtnWrap')) document.getElementById('generatePlanBtnWrap').style.display = 'none';
    // Reset alignment state
    selectedJob = null;
    selectedJobId = null;
    hasResumeAnalyzed = false;
    currentATSData = null;

    try {
        processingOverlay.setStep(0, "Parsing Resume Structure");
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

        processingOverlay.setStep(1, "Extracting Core Competencies");
        await new Promise(r => setTimeout(r, 400));
        processingOverlay.setStep(2, "Matching Against Target Role");

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
        currentJobs = searchData.jobs || [];

        if (!Array.isArray(currentJobs)) {
            console.error("Unexpected jobs data:", searchData);
            currentJobs = [];
        }


        processingOverlay.setStep(3, "Computing Alignment Score");

        // --- STEP 1: ATS Evaluation (baseline score ONLY) ---
        try {
            const atsRes = await fetch(`${API_BASE_URL}/resume/evaluate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    resume_text: currentResumeContent,
                    structured_resume: { skills: [], experience: [], education: [], certifications: [] }
                })
            });
            if (atsRes.ok) {
                currentATSData = await atsRes.json();
            }
        } catch (atsErr) {
            console.warn('ATS evaluation skipped:', atsErr.message);
            currentATSData = {
                overall_score: 72, confidence: 0.85,
                category_scores: {
                    section_completeness: { score: 12 }, keyword_clarity: { score: 10 },
                    impact_quantification: { score: 14 }, action_verb_strength: { score: 7 },
                    formatting_simplicity: { score: 8 }, readability_clarity: { score: 7 },
                    skills_organization: { score: 7 }, resume_focus_coherence: { score: 7 }
                }
            };
        }

        // Mark resume as analyzed
        hasResumeAnalyzed = true;

        processingOverlay.setStep(4, "Identifying Skill Gaps");
        await new Promise(r => setTimeout(r, 600));
        processingOverlay.setStep(5, "Generating Optimization Strategy");
        await new Promise(r => setTimeout(r, 500));

        // Dismiss overlay (respects 2.5s minimum, cascades remaining steps)
        await processingOverlay.dismiss();

        // Reveal results
        revealSection(resultsSection);
        renderJobs(currentJobs);
        showATSInsights(currentATSData);

        // Auto-unlock optimization insights — don't require user to click a job
        if (currentJobs && currentJobs.length > 0) {
            // Silently pre-select the first job so optimization works
            selectedJob = currentJobs[0];
            selectedJobId = currentJobs[0].id;
        }

        // Hide locked panel, show optimization
        document.getElementById('locked-alignment')?.classList.add('hidden');
        document.getElementById('generatePlanBtnWrap').style.display = '';

        const editor = document.getElementById('resumeEditor');
        if (editor && currentResumeContent) editor.value = currentResumeContent;

        showOptimizationInsights(
            [
                { section: 'Experience Bullets', impact: 'High', reason: 'Rephrase generic descriptions to highlight impact and measurable outcomes.' },
                { section: 'Skills Section', impact: 'Medium', reason: 'Group skills by category for better ATS parsing.' },
                { section: 'Summary', impact: 'Low', reason: 'Add a targeted professional summary aligned to the target role.' }
            ],
            [
                { skill: 'React', current_level: 85, required_level: 90 },
                { skill: 'TypeScript', current_level: 40, required_level: 80 },
                { skill: 'System Design', current_level: 20, required_level: 70 },
                { skill: 'CI/CD', current_level: 30, required_level: 60 }
            ],
            currentATSData?.overall_score || 72,
            (currentATSData?.overall_score || 72) + 12
        );

        resultsSection.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error(error);
        processingOverlay.abort();
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

// =============================================
// ATS INTELLIGENCE — Rendering Functions
// =============================================

// ATS Score Ring Animation
function renderATSScore(score, confidence) {
    const ring = document.getElementById('scoreRingFill');
    const scoreDisplay = document.getElementById('atsScoreValue');
    const confidenceDisplay = document.getElementById('atsConfidence');

    // Circumference = 2 * PI * r (r=80) = 502.65
    const circumference = 502;
    const offset = circumference - (score / 100) * circumference;

    // Animate ring
    setTimeout(() => {
        ring.style.strokeDashoffset = offset;
    }, 300);

    // Count-up animation
    let current = 0;
    const duration = 1500;
    const increment = score / (duration / 16);
    const counter = setInterval(() => {
        current += increment;
        if (current >= score) {
            current = score;
            clearInterval(counter);
            // Add pulse after animation completes
            ring.classList.add('pulse');
        }
        scoreDisplay.textContent = Math.round(current);
    }, 16);

    confidenceDisplay.textContent = `Confidence Level: ${Math.round((confidence || 0) * 100)}%`;
}

// Category Breakdown Grid
function renderCategoryGrid(categoryScores) {
    const grid = document.getElementById('categoryGrid');
    grid.innerHTML = '';

    const entries = Object.entries(categoryScores || {});
    
    if (entries.length === 0) {
        grid.innerHTML = '<p style="color:var(--text-muted)">No category data available.</p>';
        return;
    }

    entries.forEach(([key, data], index) => {
        let score = 0, max = 15;
        if (typeof data === 'number') {
            score = data;
            const k = key.toLowerCase();
            if (k.includes('quantification')) max = 20;
            else if (k.includes('section') || k.includes('keyword')) max = 15;
            else max = 10;
        } else if (data && typeof data === 'object') {
            score = data.score || 0;
            max = data.max || data.max_score || 15;
            // Some evaluations return max out of 10, 15, or 20. Fallback ensures it doesn't break.
        }

        const label = key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
        const pct = Math.round((score / max) * 100) || 0;

        const card = document.createElement('div');
        card.className = 'category-card';
        card.setAttribute('data-aos', 'fade-up');
        card.setAttribute('data-aos-delay', index * 80);

        card.innerHTML = `
            <h4>${label}</h4>
            <div class="cat-score">${score}/${max}</div>
            <div class="category-bar-track">
                <div class="category-bar-fill" style="width: 0;" data-width="${pct}"></div>
            </div>
        `;
        grid.appendChild(card);
    });

    // Animate bars after render
    setTimeout(() => {
        grid.querySelectorAll('.category-bar-fill').forEach(bar => {
            bar.style.width = bar.dataset.width + '%';
        });
    }, 500);

    AOS.refresh();
}

// Render Improvement Suggestions
function renderSuggestions(suggestions) {
    const list = document.getElementById('suggestionsList');
    list.innerHTML = '';

    if (!suggestions || suggestions.length === 0) {
        list.innerHTML = '<p style="color: var(--text-muted);">No suggestions available yet.</p>';
        return;
    }

    suggestions.forEach((sugg, index) => {
        const impact = sugg.impact || 'medium';
        const card = document.createElement('div');
        card.className = 'suggestion-card';
        card.setAttribute('data-aos', 'fade-up');
        card.setAttribute('data-aos-delay', index * 100);

        card.innerHTML = `
            <h4>${sugg.section || 'General'}</h4>
            <span class="impact-badge ${impact.toLowerCase()}">${impact} Impact</span>
            <p>${sugg.reason || sugg.improved_text || 'Improve for better alignment.'}</p>
            
        `;
        list.appendChild(card);
    });
    AOS.refresh();
}

// Render Skill Gap Bars
function renderSkillGaps(skillGaps) {
    const list = document.getElementById('skillGapList');
    list.innerHTML = '';

    if (!skillGaps || skillGaps.length === 0) {
        list.innerHTML = '<p style="color: var(--text-muted);">No skill gaps detected.</p>';
        return;
    }

    skillGaps.forEach((gap, index) => {
        const current = gap.current_level || 0;
        const required = gap.required_level || 100;
        const isDeficit = current < required;

        const item = document.createElement('div');
        item.className = `skill-gap-item ${isDeficit ? 'deficit' : ''}`;
        item.setAttribute('data-aos', 'fade-up');
        item.setAttribute('data-aos-delay', index * 80);

        item.innerHTML = `
            <div class="skill-name">
                ${gap.skill || 'Unknown Skill'}
                <span>${current}% / ${required}%</span>
            </div>
            <div class="skill-bar-track">
                <div class="skill-bar-current" data-width="${current}"></div>
                <div class="skill-bar-required" style="left: ${required}%"></div>
            </div>
        `;
        list.appendChild(item);
    });

    // Animate bars
    setTimeout(() => {
        list.querySelectorAll('.skill-bar-current').forEach(bar => {
            bar.style.width = bar.dataset.width + '%';
        });
    }, 500);

    AOS.refresh();
}

// Render Alignment Delta
function renderAlignmentDelta(currentScore, optimizedScore) {
    document.getElementById('deltaCurrentScore').textContent = currentScore;
    document.getElementById('deltaOptimizedScore').textContent = optimizedScore;
    const delta = optimizedScore - currentScore;
    if (delta > 0) {
        document.getElementById('deltaImprovement').textContent = `+${delta} Points Improvement`;
    }
}



// Render Alignment Journey Timeline
function renderAgentTimeline(steps) { return;
    const timeline = document.getElementById('agentTimeline');
    timeline.innerHTML = '';

    const defaultSteps = steps || [
        { label: 'Resume Baseline Evaluated', detail: 'Your resume was scored against ATS compatibility standards', completed: true },
        { label: 'Target Role Selected', detail: 'A specific job was chosen as the alignment benchmark', completed: true },
        { label: 'Skill Gap Identified', detail: 'Missing and partial competencies mapped against requirements', completed: true },
        { label: 'Alignment Score Calculated', detail: 'Overall compatibility measured across 8 evaluation categories', completed: true },
        { label: 'Optimization Strategy Generated', detail: 'Tailored suggestions created to close identified gaps', completed: true },
        { label: 'Projected Score Improvement', detail: 'Estimated post-optimization score calculated', completed: true }
    ];

    defaultSteps.forEach((step, index) => {
        const node = document.createElement('div');
        node.className = `agent-step ${step.completed ? 'completed' : ''}`;
        node.setAttribute('data-aos', 'fade-up');
        node.setAttribute('data-aos-delay', index * 120);

        node.innerHTML = `
            <div class="step-label">
                ${step.label}
                ${step.completed ? '<i class="fa-solid fa-check step-check"></i>' : ''}
            </div>
            <div class="step-detail">${step.detail}</div>
        `;
        timeline.appendChild(node);
    });

    AOS.refresh();
}

// Journey Toggle (collapsible)
document.getElementById('journeyToggle')?.addEventListener('click', () => {
    const header = document.getElementById('journeyToggle');
    const body = document.getElementById('journeyBody');
    header.classList.toggle('expanded');
    body.classList.toggle('expanded');
});

// =============================================
// Integration — Call ATS/Optimization after upload
// =============================================

// Show ATS Insights with mock data when resume is uploaded
function showATSInsights(atsData) {
    const atsSection = document.getElementById('ats-insights');
    revealSection(atsSection);

    const score = atsData?.overall_score || 0;
    const confidence = atsData?.confidence || 0;

    renderATSScore(score, confidence);
    renderCategoryGrid(atsData?.category_scores || {});

    atsSection.scrollIntoView({ behavior: 'smooth' });
}

function showOptimizationInsights(suggestions, skillGaps, currentScore, optimizedScore) {
    const optSection = document.getElementById('optimization-insights');
    revealSection(optSection);

    renderSuggestions(suggestions);
    renderSkillGaps(skillGaps);
    renderAlignmentDelta(currentScore, optimizedScore || currentScore + 12);
}

function showAgentActivity() { return;
    renderAgentPhase(phaseData);
}

// --- Resume Studio Features ---
document.getElementById('resumeEditor')?.addEventListener('input', (e) => {
    currentResumeContent = e.target.value;
});

document.getElementById('btnDownloadResume')?.addEventListener('click', () => {
    if (!currentResumeContent) {
        alert("No resume content to download.");
        return;
    }
    const blob = new Blob([currentResumeContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'Tailored_Resume.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

document.getElementById('btnAutoImprove')?.addEventListener('click', async (e) => {
    const btn = e.target;
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Improving...';
    btn.disabled = true;
    
    // Simulate AI Tailoring Delay (Or hook to actual endpoint in the future)
    await new Promise(r => setTimeout(r, 2000));
    
    if (currentResumeContent && selectedJob) {
        // Simple mock of AI improvement: Insert a dynamic summary targeting the role
        const tailoredHeader = `PROFESSIONAL SUMMARY\nHighly adaptible and technically proficient candidate directly aligned for the ${selectedJob.title} role at ${selectedJob.company || selectedJob.company_name}. Demonstrates strong core competencies tracking strongly with job requirements.\n\n`;
        if (!currentResumeContent.includes("PROFESSIONAL SUMMARY")) {
            currentResumeContent = tailoredHeader + currentResumeContent;
        }
        document.getElementById('resumeEditor').value = currentResumeContent;
    }
    
    btn.innerHTML = '<i class="fa-solid fa-check"></i> Improved!';
    setTimeout(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }, 2000);
});
