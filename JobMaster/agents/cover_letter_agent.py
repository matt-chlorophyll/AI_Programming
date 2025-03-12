from typing import Dict, Any, List, Optional
import json
import os
from .base_agent import BaseAgent
import config

class CoverLetterAgent(BaseAgent):
    """Agent for generating tailored cover letters for job applications."""
    
    def __init__(self):
        super().__init__("cover_letter")
        self.cover_letter_data_dir = os.path.join(config.DATA_DIR, "cover_letters")
        os.makedirs(self.cover_letter_data_dir, exist_ok=True)
    
    def get_cover_letter_file_path(self, job_id: str) -> str:
        """
        Get the file path for a cover letter for a specific job.
        
        Args:
            job_id: ID of the job
            
        Returns:
            File path for the cover letter
        """
        return os.path.join(self.cover_letter_data_dir, f"cover_letter_{job_id}.json")
    
    def get_saved_cover_letter(self, job_id: str) -> Dict[str, Any]:
        """
        Get a saved cover letter for a specific job.
        
        Args:
            job_id: ID of the job
            
        Returns:
            Dictionary containing the cover letter
        """
        cover_letter_file = self.get_cover_letter_file_path(job_id)
        return self.load_data(cover_letter_file)
    
    def save_cover_letter(self, job_id: str, cover_letter: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a cover letter for a specific job.
        
        Args:
            job_id: ID of the job
            cover_letter: Dictionary containing the cover letter
            
        Returns:
            The saved cover letter
        """
        cover_letter_file = self.get_cover_letter_file_path(job_id)
        self.save_data(cover_letter, cover_letter_file)
        return cover_letter
    
    def generate_cover_letter(self, user_profile: Dict[str, Any], job: Dict[str, Any], resume: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a tailored cover letter for a specific job.
        
        Args:
            user_profile: Dictionary containing user profile
            job: Dictionary containing job details
            resume: Optional dictionary containing the resume
            
        Returns:
            Dictionary containing the generated cover letter
        """
        # Extract relevant information from user profile
        basic_info = user_profile.get("basic_info", {})
        work_experience = user_profile.get("work_experience", [])
        skills = user_profile.get("skills", [])
        
        # Extract job details
        job_title = job.get("title", "")
        company_name = job.get("company", "")
        job_description = job.get("description", "")
        required_skills = job.get("required_skills", [])
        
        # Construct a prompt for cover letter generation
        prompt = f"""
        Generate a tailored cover letter for a job application based on the candidate's profile and job details.
        
        Job details:
        - Title: {job_title}
        - Company: {company_name}
        - Description: {job_description}
        - Required skills: {', '.join(required_skills) if isinstance(required_skills, list) else required_skills}
        
        Candidate profile:
        - Name: {basic_info.get('name', '')}
        - Contact: {basic_info.get('email', '')}, {basic_info.get('phone', '')}
        - Relevant work experience: {json.dumps(work_experience[:2]) if work_experience else ''}
        - Skills: {', '.join(skills[:10]) if skills else ''}
        
        Create a professional, compelling cover letter that:
        1. Addresses the hiring manager or company appropriately
        2. Expresses interest in the specific role and company
        3. Highlights 2-3 most relevant experiences or skills that match the job requirements
        4. Explains why the candidate is a good fit for the role
        5. Includes a call to action and professional closing
        
        The cover letter should be concise (about 300-400 words) and tailored specifically to this job and company.
        Format the results as a JSON object with 'greeting', 'introduction', 'body', 'closing', and 'full_text' fields.
        """
        
        messages = [
            {"role": "system", "content": "You are a cover letter writing assistant that creates tailored cover letters for job applications."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            cover_letter = json.loads(response)
            
            # Add metadata
            cover_letter["metadata"] = {
                "job_id": job.get("id", ""),
                "job_title": job_title,
                "company": company_name,
                "generated_timestamp": self._get_timestamp()
            }
            
            # Save the cover letter
            if job.get("id"):
                self.save_cover_letter(job["id"], cover_letter)
            
            return cover_letter
        except json.JSONDecodeError:
            # If parsing fails, return a basic cover letter structure
            return {
                "error": "Failed to generate cover letter",
                "raw_response": response
            }
    
    def optimize_cover_letter(self, cover_letter: Dict[str, Any], feedback: str) -> Dict[str, Any]:
        """
        Optimize a cover letter based on feedback.
        
        Args:
            cover_letter: Dictionary containing the cover letter
            feedback: Feedback for optimization
            
        Returns:
            Dictionary containing the optimized cover letter
        """
        # Construct a prompt for cover letter optimization
        prompt = f"""
        Optimize the following cover letter based on the provided feedback:
        
        Cover Letter:
        {json.dumps(cover_letter)}
        
        Feedback:
        {feedback}
        
        Please provide an optimized version of the cover letter that addresses the feedback.
        Format the results as a JSON object with the same structure as the original cover letter.
        """
        
        messages = [
            {"role": "system", "content": "You are a cover letter optimization assistant that improves cover letters based on feedback."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            optimized_cover_letter = json.loads(response)
            
            # Preserve metadata
            if "metadata" in cover_letter:
                optimized_cover_letter["metadata"] = cover_letter["metadata"]
                
                # Update optimization timestamp
                optimized_cover_letter["metadata"]["optimized_timestamp"] = self._get_timestamp()
            
            # Save the optimized cover letter if job_id is available
            if cover_letter.get("metadata", {}).get("job_id"):
                self.save_cover_letter(cover_letter["metadata"]["job_id"], optimized_cover_letter)
            
            return optimized_cover_letter
        except json.JSONDecodeError:
            # If parsing fails, return the original cover letter
            return cover_letter
    
    def format_cover_letter_as_text(self, cover_letter: Dict[str, Any]) -> str:
        """
        Format a cover letter as plain text.
        
        Args:
            cover_letter: Dictionary containing the cover letter
            
        Returns:
            Formatted cover letter as text
        """
        # If the cover letter already has a full_text field, return it
        if "full_text" in cover_letter and cover_letter["full_text"]:
            return cover_letter["full_text"]
        
        # Otherwise, construct a prompt for formatting
        prompt = f"""
        Format the following cover letter as plain text that could be copied into a document:
        
        Cover Letter:
        {json.dumps(cover_letter)}
        
        Please format it professionally with proper spacing and a clean layout.
        """
        
        messages = [
            {"role": "system", "content": "You are a cover letter formatting assistant that converts cover letter data into well-formatted plain text."},
            {"role": "user", "content": prompt}
        ]
        
        return self.get_completion(messages)
    
    def _get_timestamp(self) -> str:
        """Get the current timestamp as a string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def run(self, action: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the cover letter agent with the specified action.
        
        Args:
            action: The action to perform (generate_cover_letter, optimize_cover_letter, etc.)
            data: Data required for the action
            
        Returns:
            Result of the action
        """
        if action == "generate_cover_letter" and data and "user_profile" in data and "job" in data:
            resume = data.get("resume")
            cover_letter = self.generate_cover_letter(data["user_profile"], data["job"], resume)
            return {"cover_letter": cover_letter}
        elif action == "get_saved_cover_letter" and data and "job_id" in data:
            cover_letter = self.get_saved_cover_letter(data["job_id"])
            return {"cover_letter": cover_letter}
        elif action == "optimize_cover_letter" and data and "cover_letter" in data and "feedback" in data:
            optimized_cover_letter = self.optimize_cover_letter(data["cover_letter"], data["feedback"])
            return {"cover_letter": optimized_cover_letter}
        elif action == "format_cover_letter_as_text" and data and "cover_letter" in data:
            formatted_text = self.format_cover_letter_as_text(data["cover_letter"])
            return {"formatted_text": formatted_text}
        else:
            return {"error": "Invalid action or missing data"} 