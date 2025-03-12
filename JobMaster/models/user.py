from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import date

class BasicInfo(BaseModel):
    """Basic user information."""
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None

class WorkExperience(BaseModel):
    """Work experience information."""
    company: str
    title: str
    location: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    current: bool = False
    description: Optional[str] = None
    achievements: Optional[List[str]] = None
    skills_used: Optional[List[str]] = None

class Education(BaseModel):
    """Education information."""
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    current: bool = False
    gpa: Optional[float] = None
    achievements: Optional[List[str]] = None
    courses: Optional[List[str]] = None

class Project(BaseModel):
    """Project information."""
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    skills_used: Optional[List[str]] = None
    achievements: Optional[List[str]] = None

class Certification(BaseModel):
    """Certification information."""
    name: str
    issuer: str
    date_obtained: Optional[str] = None
    expiration_date: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None

class UserProfile(BaseModel):
    """Complete user profile."""
    basic_info: BasicInfo
    work_experience: Optional[List[WorkExperience]] = []
    education: Optional[List[Education]] = []
    skills: Optional[List[str]] = []
    projects: Optional[List[Project]] = []
    certifications: Optional[List[Certification]] = []
    languages: Optional[List[Dict[str, str]]] = []
    interests: Optional[List[str]] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "basic_info": {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "phone": "123-456-7890",
                    "location": "New York, NY",
                    "linkedin": "linkedin.com/in/johndoe",
                    "github": "github.com/johndoe",
                    "portfolio": "johndoe.com",
                    "title": "Software Engineer",
                    "summary": "Experienced software engineer with a passion for building scalable applications."
                },
                "work_experience": [
                    {
                        "company": "Tech Company",
                        "title": "Senior Software Engineer",
                        "location": "New York, NY",
                        "start_date": "2020-01",
                        "end_date": None,
                        "current": True,
                        "description": "Leading development of cloud-based applications.",
                        "achievements": [
                            "Reduced system latency by 30%",
                            "Implemented CI/CD pipeline"
                        ],
                        "skills_used": ["Python", "AWS", "Docker"]
                    }
                ],
                "education": [
                    {
                        "institution": "University of Technology",
                        "degree": "Bachelor of Science",
                        "field_of_study": "Computer Science",
                        "location": "Boston, MA",
                        "start_date": "2012-09",
                        "end_date": "2016-05",
                        "gpa": 3.8
                    }
                ],
                "skills": ["Python", "JavaScript", "AWS", "Docker", "React", "Node.js"],
                "projects": [
                    {
                        "name": "Personal Website",
                        "description": "Responsive personal website built with React",
                        "url": "johndoe.com",
                        "skills_used": ["React", "CSS", "JavaScript"]
                    }
                ],
                "certifications": [
                    {
                        "name": "AWS Certified Solutions Architect",
                        "issuer": "Amazon Web Services",
                        "date_obtained": "2019-06",
                        "url": "credential-url"
                    }
                ]
            }
        } 