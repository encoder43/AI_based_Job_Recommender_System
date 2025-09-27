import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.helper import extract_text_from_pdf, ask_groq
# Import all new job fetching functions
from src.job_api import fetch_indeed_jobs, fetch_google_jobs, fetch_glassdoor_jobs, fetch_naukri_jobs

app = FastAPI(title="AI Job Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to the AI Job Recommender API!"}

@app.post("/analyze-resume/")
async def analyze_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
    try:
        pdf_bytes = await file.read()
        resume_text = extract_text_from_pdf(pdf_bytes)
        if not resume_text or len(resume_text) < 100:
            raise HTTPException(status_code=400, detail="Could not extract sufficient text from the PDF.")
        
        summary_prompt = f"Summarize this resume highlighting the skills, education, and experience: \n\n{resume_text}"
        gaps_prompt = f"Analyze this resume and highlight missing skills, certifications, and experiences needed for better job opportunities: \n\n{resume_text}"
        roadmap_prompt = f"Based on this resume, suggest a future roadmap to improve this person's career prospects (Skills to learn, certifications, industry exposure): \n\n{resume_text}"
        
        summary_task = asyncio.to_thread(ask_groq, summary_prompt, 500)
        gaps_task = asyncio.to_thread(ask_groq, gaps_prompt, 400)
        roadmap_task = asyncio.to_thread(ask_groq, roadmap_prompt, 400)
        
        summary, gaps, roadmap = await asyncio.gather(summary_task, gaps_task, roadmap_task)
        keywords_prompt = f"Based on this resume summary, what is the single most relevant job title to search for? Give only the job title and nothing else.\n\nSummary: {summary}"
        job_keywords = ask_groq(keywords_prompt, 100)
        
        return {"summary": summary, "gaps": gaps, "roadmap": roadmap, "job_keywords": job_keywords.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

class JobKeywords(BaseModel):
    keywords: str

@app.post("/fetch-jobs/")
async def get_jobs(request: JobKeywords):
    try:
        keywords = request.keywords

        # --- THIS IS THE NEW LINE ---
        # Extract the first job title from the comma-separated list
        primary_keyword = keywords.split(',')[0].strip()
        
        # Create concurrent tasks using the SINGLE, primary keyword
        indeed_task = asyncio.to_thread(fetch_indeed_jobs, primary_keyword)
        google_task = asyncio.to_thread(fetch_google_jobs, primary_keyword)
        glassdoor_task = asyncio.to_thread(fetch_glassdoor_jobs, primary_keyword)
        naukri_task = asyncio.to_thread(fetch_naukri_jobs, primary_keyword) # Also using primary keyword for consistency
        
        # The rest of the function remains the same...
        results = await asyncio.gather(
            indeed_task,
            google_task,
            glassdoor_task,
            naukri_task,
            return_exceptions=True
        )
        
        indeed_jobs = results[0] if not isinstance(results[0], Exception) else []
        google_jobs = results[1] if not isinstance(results[1], Exception) else []
        glassdoor_jobs = results[2] if not isinstance(results[2], Exception) else []
        naukri_jobs = results[3] if not isinstance(results[3], Exception) else []
        
        return {
            "indeed_jobs": indeed_jobs,
            "google_jobs": google_jobs,
            "glassdoor_jobs": glassdoor_jobs,
            "naukri_jobs": naukri_jobs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch jobs: {str(e)}")
# To run the server: uvicorn main:app --reload