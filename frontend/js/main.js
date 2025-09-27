document.addEventListener('DOMContentLoaded', () => {
    // DOM Element References
    const uploadForm = document.getElementById('upload-form');
    const loadingSpinner = document.getElementById('loading-spinner');
    const resultsSection = document.getElementById('results-section');
    const errorAlert = document.getElementById('error-alert');
    
    const summaryOutput = document.getElementById('summary-output');
    const gapsOutput = document.getElementById('gaps-output');
    const roadmapOutput = document.getElementById('roadmap-output');

    const getJobsBtn = document.getElementById('get-jobs-btn');
    const jobsLoadingSpinner = document.getElementById('jobs-loading-spinner');
    const jobsResults = document.getElementById('jobs-results');

    // State & Config
    let analysisData = {}; 
    const API_BASE_URL = 'https://ai-job-recommender-api.onrender.com';

    // --- Helper function to show errors ---
    const showError = (message) => {
        errorAlert.textContent = `Error: ${message}`;
        errorAlert.style.display = 'block';
    };

    // --- Handle Resume Analysis ---
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const file = document.getElementById('resume-file').files[0];
        if (!file) {
            showError("Please select a file to upload.");
            return;
        }

        // Reset UI for a new analysis
        resultsSection.classList.add('d-none');
        jobsResults.classList.add('d-none');
        errorAlert.style.display = 'none';
        loadingSpinner.style.display = 'block';
        getJobsBtn.disabled = true;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_BASE_URL}/analyze-resume/`, { method: 'POST', body: formData });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Analysis failed due to a server error.');
            }

            analysisData = await response.json();
            
            // Populate analysis results using marked.js
            summaryOutput.innerHTML = marked.parse(analysisData.summary);
            gapsOutput.innerHTML = marked.parse(analysisData.gaps);
            roadmapOutput.innerHTML = marked.parse(analysisData.roadmap);
            
            resultsSection.classList.remove('d-none');
            getJobsBtn.disabled = false;
        } catch (error) {
            showError(error.message);
        } finally {
            loadingSpinner.style.display = 'none';
        }
    });

    // --- Handle Job Fetching ---
    getJobsBtn.addEventListener('click', async () => {
        if (!analysisData.job_keywords) {
            showError("Analysis data is not available.");
            return;
        }
        
        // Reset UI for job search
        jobsResults.classList.add('d-none');
        errorAlert.style.display = 'none';
        jobsLoadingSpinner.style.display = 'block';
        getJobsBtn.disabled = true;

        try {
            const response = await fetch(`${API_BASE_URL}/fetch-jobs/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ keywords: analysisData.job_keywords }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to fetch jobs.');
            }

            const jobsData = await response.json();
            
            // --- POPULATE ALL FOUR JOB SECTIONS ---
            // Each call uses a "mapper" to normalize the data from different scrapers

            populateJobList('indeed-jobs', jobsData.indeed_jobs, (job) => ({
                title: job.title,
                company: job.company,
                location: job.location,
                url: job.url
            }));

            populateJobList('google-jobs', jobsData.google_jobs, (job) => ({
                title: job.title,
                company: job.company_name, // Note: key is 'company_name'
                location: job.location,
                url: job.url
            }));

            populateJobList('glassdoor-jobs', jobsData.glassdoor_jobs, (job) => ({
                title: job.title,
                company: job.company,
                location: job.location,
                url: job.url
            }));

            populateJobList('naukri-jobs', jobsData.naukri_jobs, (job) => ({
                title: job.title,
                company: job.companyName, // Note: key is 'companyName'
                location: job.location,
                url: job.url
            }));

            jobsResults.classList.remove('d-none');

        } catch (error) {
            showError(error.message);
        } finally {
            jobsLoadingSpinner.style.display = 'none';
            getJobsBtn.disabled = false;
        }
    });

    // --- Helper function to dynamically create and populate job lists ---
    const populateJobList = (elementId, jobs, mapper) => {
        const container = document.getElementById(elementId);
        container.innerHTML = ''; // Clear previous results

        if (!jobs || jobs.length === 0) {
            container.innerHTML = '<div class="card"><div class="card-body text-muted">No jobs found for this source.</div></div>';
            return;
        }

        jobs.forEach(jobData => {
            const job = mapper(jobData); // Use the mapper to get consistent field names
            const jobCardHTML = `
                <div class="card mb-3 job-card">
                    <div class="card-body">
                        <h5 class="card-title">${job.title || 'N/A'}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">${job.company || 'N/A'}</h6>
                        <p class="card-text small">📍 ${job.location || 'N/A'}</p>
                        <a href="${job.url}" class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer">View Job</a>
                    </div>
                </div>
            `;
            container.innerHTML += jobCardHTML;
        });
    };
});