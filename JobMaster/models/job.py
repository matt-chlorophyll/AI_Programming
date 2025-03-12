from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Job(BaseModel):
    """Job information."""
    id: str
    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None
    salary_range: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    education_requirements: Optional[str] = None
    url: Optional[str] = None
    date_posted: Optional[str] = None
    application_deadline: Optional[str] = None
    remote: Optional[bool] = None
    benefits: Optional[List[str]] = None
    company_description: Optional[str] = None
    search_timestamp: Optional[str] = None
    search_query: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "job123",
                "title": "Senior Software Engineer",
                "company": "Tech Company",
                "location": "New York, NY",
                "description": "We are looking for a Senior Software Engineer to join our team...",
                "required_skills": ["Python", "AWS", "Docker"],
                "preferred_skills": ["Kubernetes", "CI/CD", "React"],
                "salary_range": "$120,000 - $150,000",
                "job_type": "Full-time",
                "experience_level": "5+ years",
                "education_requirements": "Bachelor's degree in Computer Science or related field",
                "url": "https://example.com/jobs/123",
                "date_posted": "2023-05-15",
                "remote": True,
                "benefits": ["Health insurance", "401(k)", "Flexible work hours"]
            }
        }

class JobSearch(BaseModel):
    """Job search parameters."""
    job_title: str
    location: Optional[str] = None
    keywords: Optional[List[str]] = None
    experience_level: Optional[str] = None
    job_type: Optional[str] = None
    remote: Optional[bool] = None
    salary_min: Optional[int] = None
    date_posted: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_title": "Software Engineer",
                "location": "New York, NY",
                "keywords": ["Python", "AWS", "React"],
                "experience_level": "Mid-level",
                "job_type": "Full-time",
                "remote": True,
                "salary_min": 100000,
                "date_posted": "last_week"
            }
        }

class JobMatch(BaseModel):
    """Job match analysis."""
    match_percentage: float
    matching_skills: List[str]
    missing_skills: List[str]
    relevant_experience: List[str]
    recommendations: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "match_percentage": 85,
                "matching_skills": ["Python", "AWS", "JavaScript"],
                "missing_skills": ["Kubernetes", "GraphQL"],
                "relevant_experience": [
                    "3 years of experience with Python development",
                    "Experience with AWS cloud services"
                ],
                "recommendations": [
                    "Highlight your AWS experience in your resume",
                    "Consider taking a Kubernetes course to fill skill gap"
                ]
            }
        } 