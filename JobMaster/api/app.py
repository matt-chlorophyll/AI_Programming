from fastapi import FastAPI, HTTPException, Body, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
import sys
import os
import json

# Add parent directory to path to import from main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import JobMaster
from models.user import UserProfile, BasicInfo, WorkExperience, Education, Project, Certification
from models.job import Job, JobSearch, JobMatch

app = FastAPI(
    title="JobMaster API",
    description="API for the JobMaster job search and application assistant",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create JobMaster instance
job_master = JobMaster()

# Dependency to get JobMaster instance
def get_job_master():
    return job_master

# User Information Endpoints
@app.get("/user", response_model=Dict[str, Any], tags=["User Information"])
async def get_user_info(job_master: JobMaster = Depends(get_job_master)):
    """Get the user's profile information."""
    return job_master.manage_user_info("get_user_info")

@app.post("/user/basic-info", response_model=Dict[str, Any], tags=["User Information"])
async def update_basic_info(basic_info: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Update the user's basic information."""
    return job_master.manage_user_info("collect_basic_info", basic_info)

@app.post("/user/work-experience", response_model=Dict[str, Any], tags=["User Information"])
async def add_work_experience(experience: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Add a work experience entry to the user's profile."""
    return job_master.manage_user_info("add_work_experience", experience)

@app.post("/user/education", response_model=Dict[str, Any], tags=["User Information"])
async def add_education(education: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Add an education entry to the user's profile."""
    return job_master.manage_user_info("add_education", education)

@app.post("/user/skills", response_model=Dict[str, Any], tags=["User Information"])
async def add_skills(skills: Dict[str, List[str]] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Add skills to the user's profile."""
    return job_master.manage_user_info("add_skills", skills)

@app.post("/user/projects", response_model=Dict[str, Any], tags=["User Information"])
async def add_project(project: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Add a project to the user's profile."""
    return job_master.manage_user_info("add_projects", project)

@app.post("/user/certifications", response_model=Dict[str, Any], tags=["User Information"])
async def add_certification(certification: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Add a certification to the user's profile."""
    return job_master.manage_user_info("add_certifications", certification)

@app.get("/user/profile-completeness", response_model=Dict[str, Any], tags=["User Information"])
async def analyze_profile_completeness(job_master: JobMaster = Depends(get_job_master)):
    """Analyze the completeness of the user's profile."""
    return job_master.manage_user_info("analyze_profile_completeness")

# Job Search Endpoints
@app.post("/jobs/search", response_model=Dict[str, Any], tags=["Job Search"])
async def search_jobs(search_params: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Search for jobs based on the provided parameters."""
    return job_master.search_jobs("search_jobs", search_params)

@app.get("/jobs/saved", response_model=Dict[str, Any], tags=["Job Search"])
async def get_saved_jobs(job_master: JobMaster = Depends(get_job_master)):
    """Get the list of saved jobs."""
    return job_master.search_jobs("get_saved_jobs")

@app.post("/jobs/save", response_model=Dict[str, Any], tags=["Job Search"])
async def save_job(job: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Save a job to the saved jobs list."""
    return job_master.search_jobs("save_job", job)

@app.delete("/jobs/{job_id}", response_model=Dict[str, Any], tags=["Job Search"])
async def remove_saved_job(job_id: str, job_master: JobMaster = Depends(get_job_master)):
    """Remove a job from the saved jobs list."""
    return job_master.search_jobs("remove_saved_job", {"job_id": job_id})

@app.post("/jobs/analyze-match", response_model=Dict[str, Any], tags=["Job Search"])
async def analyze_job_match(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Analyze how well a job matches the user's profile."""
    return job_master.search_jobs("analyze_job_match", data)

# Resume Endpoints
@app.post("/resume/generate", response_model=Dict[str, Any], tags=["Resume"])
async def generate_resume(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Generate a tailored resume for a specific job."""
    return job_master.manage_resume("generate_resume", data)

@app.get("/resume/{job_id}", response_model=Dict[str, Any], tags=["Resume"])
async def get_saved_resume(job_id: str, job_master: JobMaster = Depends(get_job_master)):
    """Get a saved resume for a specific job."""
    return job_master.manage_resume("get_saved_resume", {"job_id": job_id})

@app.post("/resume/optimize", response_model=Dict[str, Any], tags=["Resume"])
async def optimize_resume(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Optimize a resume based on feedback."""
    return job_master.manage_resume("optimize_resume", data)

@app.post("/resume/format", response_model=Dict[str, Any], tags=["Resume"])
async def format_resume_as_text(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Format a resume as plain text."""
    return job_master.manage_resume("format_resume_as_text", data)

# Cover Letter Endpoints
@app.post("/cover-letter/generate", response_model=Dict[str, Any], tags=["Cover Letter"])
async def generate_cover_letter(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Generate a tailored cover letter for a specific job."""
    return job_master.manage_cover_letter("generate_cover_letter", data)

@app.get("/cover-letter/{job_id}", response_model=Dict[str, Any], tags=["Cover Letter"])
async def get_saved_cover_letter(job_id: str, job_master: JobMaster = Depends(get_job_master)):
    """Get a saved cover letter for a specific job."""
    return job_master.manage_cover_letter("get_saved_cover_letter", {"job_id": job_id})

@app.post("/cover-letter/optimize", response_model=Dict[str, Any], tags=["Cover Letter"])
async def optimize_cover_letter(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Optimize a cover letter based on feedback."""
    return job_master.manage_cover_letter("optimize_cover_letter", data)

@app.post("/cover-letter/format", response_model=Dict[str, Any], tags=["Cover Letter"])
async def format_cover_letter_as_text(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Format a cover letter as plain text."""
    return job_master.manage_cover_letter("format_cover_letter_as_text", data)

# Interview Preparation Endpoints
@app.post("/interview/common-questions", response_model=Dict[str, Any], tags=["Interview Preparation"])
async def generate_common_questions(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Generate common interview questions for a specific job."""
    return job_master.prepare_for_interview("generate_common_questions", data)

@app.post("/interview/technical-questions", response_model=Dict[str, Any], tags=["Interview Preparation"])
async def generate_technical_questions(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Generate technical interview questions for a specific job."""
    return job_master.prepare_for_interview("generate_technical_questions", data)

@app.post("/interview/company-research", response_model=Dict[str, Any], tags=["Interview Preparation"])
async def generate_company_research(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Generate company research for interview preparation."""
    return job_master.prepare_for_interview("generate_company_research", data)

@app.post("/interview/tips", response_model=Dict[str, Any], tags=["Interview Preparation"])
async def generate_interview_tips(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Generate general interview tips for a specific job."""
    return job_master.prepare_for_interview("generate_interview_tips", data)

@app.get("/interview/{job_id}", response_model=Dict[str, Any], tags=["Interview Preparation"])
async def get_saved_interview_prep(job_id: str, job_master: JobMaster = Depends(get_job_master)):
    """Get saved interview preparation for a specific job."""
    return job_master.prepare_for_interview("get_saved_interview_prep", {"job_id": job_id})

@app.post("/interview/evaluate-answer", response_model=Dict[str, Any], tags=["Interview Preparation"])
async def evaluate_practice_answer(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Evaluate a practice answer for an interview question."""
    return job_master.prepare_for_interview("evaluate_practice_answer", data)

# Networking Endpoints
@app.post("/networking/connection-message", response_model=Dict[str, Any], tags=["Networking"])
async def generate_connection_message(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Generate a connection message for a professional contact."""
    return job_master.manage_networking("generate_connection_message", data)

@app.post("/networking/coffee-chat-topics", response_model=Dict[str, Any], tags=["Networking"])
async def generate_coffee_chat_topics(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Generate topics for a coffee chat or informational interview."""
    return job_master.manage_networking("generate_coffee_chat_topics", data)

@app.post("/networking/follow-up-message", response_model=Dict[str, Any], tags=["Networking"])
async def generate_follow_up_message(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Generate a follow-up message after a networking meeting."""
    return job_master.manage_networking("generate_follow_up_message", data)

@app.post("/networking/analyze-profile", response_model=Dict[str, Any], tags=["Networking"])
async def analyze_contact_profile(data: Dict[str, Any] = Body(...), job_master: JobMaster = Depends(get_job_master)):
    """Analyze a contact's profile to identify networking opportunities."""
    return job_master.manage_networking("analyze_contact_profile", data)

@app.get("/networking/{contact_id}", response_model=Dict[str, Any], tags=["Networking"])
async def get_saved_networking_info(contact_id: str, job_master: JobMaster = Depends(get_job_master)):
    """Get saved networking information for a specific contact."""
    return job_master.manage_networking("get_saved_networking_info", {"contact_id": contact_id})

# Complete Job Application Package
@app.get("/application-package/{job_id}", response_model=Dict[str, Any], tags=["Application Package"])
async def generate_job_application_package(job_id: str, job_master: JobMaster = Depends(get_job_master)):
    """Generate a complete job application package for a specific job."""
    return job_master.generate_job_application_package(job_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 