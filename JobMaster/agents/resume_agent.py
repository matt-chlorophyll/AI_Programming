from typing import Dict, Any, List, Optional
import json
import os
from .base_agent import BaseAgent
import config

class ResumeAgent(BaseAgent):
    """Agent for generating tailored resumes for job applications."""
    
    def __init__(self):
        super().__init__("resume")
        self.resume_data_dir = os.path.join(config.DATA_DIR, "resumes")
        os.makedirs(self.resume_data_dir, exist_ok=True)
    
    def get_resume_file_path(self, job_id: str) -> str:
        """
        Get the file path for a resume for a specific job.
        
        Args:
            job_id: ID of the job
            
        Returns:
            File path for the resume
        """
        return os.path.join(self.resume_data_dir, f"resume_{job_id}.json")
    
    def get_saved_resume(self, job_id: str) -> Dict[str, Any]:
        """
        Get a saved resume for a specific job.
        
        Args:
            job_id: ID of the job
            
        Returns:
            Dictionary containing the resume
        """
        resume_file = self.get_resume_file_path(job_id)
        return self.load_data(resume_file)
    
    def save_resume(self, job_id: str, resume: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a resume for a specific job.
        
        Args:
            job_id: ID of the job
            resume: Dictionary containing the resume
            
        Returns:
            The saved resume
        """
        resume_file = self.get_resume_file_path(job_id)
        self.save_data(resume, resume_file)
        return resume
    
    def generate_resume(self, user_profile: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a tailored resume for a specific job.
        
        Args:
            user_profile: Dictionary containing user profile
            job: Dictionary containing job details
            
        Returns:
            Dictionary containing the generated resume
        """
        # Extract relevant information from user profile
        basic_info = user_profile.get("basic_info", {})
        work_experience = user_profile.get("work_experience", [])
        education = user_profile.get("education", [])
        skills = user_profile.get("skills", [])
        projects = user_profile.get("projects", [])
        certifications = user_profile.get("certifications", [])
        
        # Extract job details
        job_title = job.get("title", "")
        job_description = job.get("description", "")
        required_skills = job.get("required_skills", [])
        
        # Construct a prompt for resume generation
        prompt = f"""
        Generate a tailored resume for a job application based on the candidate's profile and job details.
        
        Job details:
        - Title: {job_title}
        - Description: {job_description}
        - Required skills: {', '.join(required_skills) if isinstance(required_skills, list) else required_skills}
        
        Candidate profile:
        - Basic info: {json.dumps(basic_info)}
        - Work experience: {json.dumps(work_experience)}
        - Education: {json.dumps(education)}
        - Skills: {', '.join(skills)}
        - Projects: {json.dumps(projects)}
        - Certifications: {json.dumps(certifications)}
        
        Create a tailored resume that highlights the most relevant experience, skills, and qualifications for this specific job.
        The resume should include:
        1. Contact information
        2. Professional summary tailored to the job
        3. Relevant work experience (with achievements and responsibilities that match the job)
        4. Education
        5. Skills (prioritizing those that match the job requirements)
        6. Relevant projects and certifications
        
        Format the results as a JSON object with sections for each part of the resume.
        """
        
        messages = [
            {"role": "system", "content": "You are a resume writing assistant that creates tailored resumes for job applications."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            resume = json.loads(response)
            
            # Add metadata
            resume["metadata"] = {
                "job_id": job.get("id", ""),
                "job_title": job_title,
                "company": job.get("company", ""),
                "generated_timestamp": self._get_timestamp()
            }
            
            # Save the resume
            if job.get("id"):
                self.save_resume(job["id"], resume)
            
            return resume
        except json.JSONDecodeError:
            # If parsing fails, return a basic resume structure
            return {
                "error": "Failed to generate resume",
                "raw_response": response
            }
    
    def optimize_resume(self, resume: Dict[str, Any], feedback: str) -> Dict[str, Any]:
        """
        Optimize a resume based on feedback.
        
        Args:
            resume: Dictionary containing the resume
            feedback: Feedback for optimization
            
        Returns:
            Dictionary containing the optimized resume
        """
        # Construct a prompt for resume optimization
        prompt = f"""
        Optimize the following resume based on the provided feedback:
        
        Resume:
        {json.dumps(resume)}
        
        Feedback:
        {feedback}
        
        Please provide an optimized version of the resume that addresses the feedback.
        Format the results as a JSON object with the same structure as the original resume.
        """
        
        messages = [
            {"role": "system", "content": "You are a resume optimization assistant that improves resumes based on feedback."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            optimized_resume = json.loads(response)
            
            # Preserve metadata
            if "metadata" in resume:
                optimized_resume["metadata"] = resume["metadata"]
                
                # Update optimization timestamp
                optimized_resume["metadata"]["optimized_timestamp"] = self._get_timestamp()
            
            # Save the optimized resume if job_id is available
            if resume.get("metadata", {}).get("job_id"):
                self.save_resume(resume["metadata"]["job_id"], optimized_resume)
            
            return optimized_resume
        except json.JSONDecodeError:
            # If parsing fails, return the original resume
            return resume
    
    def format_resume_as_text(self, resume: Dict[str, Any]) -> str:
        """
        Format a resume as plain text.
        
        Args:
            resume: Dictionary containing the resume
            
        Returns:
            Formatted resume as text
        """
        # Construct a prompt for formatting
        prompt = f"""
        Format the following resume as plain text that could be copied into a document:
        
        Resume:
        {json.dumps(resume)}
        
        Please format it professionally with clear section headings, proper spacing, and a clean layout.
        """
        
        messages = [
            {"role": "system", "content": "You are a resume formatting assistant that converts resume data into well-formatted plain text."},
            {"role": "user", "content": prompt}
        ]
        
        return self.get_completion(messages)
    
    def _get_timestamp(self) -> str:
        """Get the current timestamp as a string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def run(self, action: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the resume agent with the specified action.
        
        Args:
            action: The action to perform (generate_resume, optimize_resume, etc.)
            data: Data required for the action
            
        Returns:
            Result of the action
        """
        if action == "generate_resume" and data and "user_profile" in data and "job" in data:
            resume = self.generate_resume(data["user_profile"], data["job"])
            return {"resume": resume}
        elif action == "get_saved_resume" and data and "job_id" in data:
            resume = self.get_saved_resume(data["job_id"])
            return {"resume": resume}
        elif action == "optimize_resume" and data and "resume" in data and "feedback" in data:
            optimized_resume = self.optimize_resume(data["resume"], data["feedback"])
            return {"resume": optimized_resume}
        elif action == "format_resume_as_text" and data and "resume" in data:
            formatted_text = self.format_resume_as_text(data["resume"])
            return {"formatted_text": formatted_text}
        else:
            return {"error": "Invalid action or missing data"} 