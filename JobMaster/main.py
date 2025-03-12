import os
import json
from typing import Dict, Any, List, Optional
import config
from agents import (
    UserInfoAgent,
    JobSearchAgent,
    ResumeAgent,
    CoverLetterAgent,
    InterviewPrepAgent,
    NetworkingAgent
)

class JobMaster:
    """Main class for the JobMaster application."""
    
    def __init__(self):
        """Initialize the JobMaster application."""
        # Initialize agents
        self.user_info_agent = UserInfoAgent()
        self.job_search_agent = JobSearchAgent()
        self.resume_agent = ResumeAgent()
        self.cover_letter_agent = CoverLetterAgent()
        self.interview_prep_agent = InterviewPrepAgent()
        self.networking_agent = NetworkingAgent()
        
        # Create data directory if it doesn't exist
        os.makedirs(config.DATA_DIR, exist_ok=True)
    
    def manage_user_info(self, action: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Manage user information.
        
        Args:
            action: The action to perform
            data: Data required for the action
            
        Returns:
            Result of the action
        """
        return self.user_info_agent.run(action, data)
    
    def search_jobs(self, action: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for jobs.
        
        Args:
            action: The action to perform
            data: Data required for the action
            
        Returns:
            Result of the action
        """
        return self.job_search_agent.run(action, data)
    
    def manage_resume(self, action: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Manage resumes.
        
        Args:
            action: The action to perform
            data: Data required for the action
            
        Returns:
            Result of the action
        """
        return self.resume_agent.run(action, data)
    
    def manage_cover_letter(self, action: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Manage cover letters.
        
        Args:
            action: The action to perform
            data: Data required for the action
            
        Returns:
            Result of the action
        """
        return self.cover_letter_agent.run(action, data)
    
    def prepare_for_interview(self, action: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Prepare for interviews.
        
        Args:
            action: The action to perform
            data: Data required for the action
            
        Returns:
            Result of the action
        """
        return self.interview_prep_agent.run(action, data)
    
    def manage_networking(self, action: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Manage networking.
        
        Args:
            action: The action to perform
            data: Data required for the action
            
        Returns:
            Result of the action
        """
        return self.networking_agent.run(action, data)
    
    def generate_job_application_package(self, job_id: str) -> Dict[str, Any]:
        """
        Generate a complete job application package for a specific job.
        
        Args:
            job_id: ID of the job
            
        Returns:
            Dictionary containing the job application package
        """
        # Get user profile
        user_profile = self.user_info_agent.get_user_info()
        
        # Get job details
        saved_jobs = self.job_search_agent.get_saved_jobs()
        job = next((j for j in saved_jobs if j.get("id") == job_id), None)
        
        if not job:
            return {"error": f"Job with ID {job_id} not found"}
        
        # Generate resume
        resume_result = self.resume_agent.run("generate_resume", {
            "user_profile": user_profile,
            "job": job
        })
        
        # Generate cover letter
        cover_letter_result = self.cover_letter_agent.run("generate_cover_letter", {
            "user_profile": user_profile,
            "job": job,
            "resume": resume_result.get("resume")
        })
        
        # Generate interview preparation
        interview_prep_result = self.interview_prep_agent.run("generate_common_questions", {
            "user_profile": user_profile,
            "job": job
        })
        
        technical_questions_result = self.interview_prep_agent.run("generate_technical_questions", {
            "user_profile": user_profile,
            "job": job
        })
        
        company_research_result = self.interview_prep_agent.run("generate_company_research", {
            "job": job
        })
        
        # Analyze job match
        job_match_result = self.job_search_agent.run("analyze_job_match", {
            "job": job,
            "user_profile": user_profile
        })
        
        # Return the complete package
        return {
            "job": job,
            "resume": resume_result.get("resume"),
            "cover_letter": cover_letter_result.get("cover_letter"),
            "interview_prep": {
                "common_questions": interview_prep_result.get("common_questions"),
                "technical_questions": technical_questions_result.get("technical_questions"),
                "company_research": company_research_result.get("company_research")
            },
            "job_match": job_match_result.get("match_analysis")
        }

def main():
    """Main function to run the JobMaster application."""
    job_master = JobMaster()
    
    # Example usage
    print("JobMaster initialized!")
    print("Use the JobMaster class to interact with the application.")
    
    # Example: Add basic user information
    # job_master.manage_user_info("collect_basic_info", {
    #     "name": "John Doe",
    #     "email": "john.doe@example.com",
    #     "phone": "123-456-7890"
    # })
    
    # Example: Search for jobs
    # job_master.search_jobs("search_jobs", {
    #     "job_title": "Software Engineer",
    #     "location": "New York, NY",
    #     "keywords": ["Python", "Machine Learning"]
    # })

if __name__ == "__main__":
    main() 