from typing import Dict, Any, List, Optional
import json
import os
import requests
from bs4 import BeautifulSoup
from .base_agent import BaseAgent
import config

class JobSearchAgent(BaseAgent):
    """Agent for searching and finding relevant job opportunities."""
    
    def __init__(self):
        super().__init__("job_search")
        self.job_data_file = config.JOB_DATA_FILE
    
    def get_saved_jobs(self) -> List[Dict[str, Any]]:
        """
        Get the list of saved jobs.
        
        Returns:
            List of saved job dictionaries
        """
        data = self.load_data(self.job_data_file)
        return data.get("saved_jobs", [])
    
    def save_job(self, job: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Save a job to the saved jobs list.
        
        Args:
            job: Dictionary containing job details
            
        Returns:
            Updated list of saved jobs
        """
        data = self.load_data(self.job_data_file)
        saved_jobs = data.get("saved_jobs", [])
        
        # Check if job already exists (by URL or ID)
        job_exists = False
        for existing_job in saved_jobs:
            if (existing_job.get("url") and existing_job["url"] == job.get("url")) or \
               (existing_job.get("id") and existing_job["id"] == job.get("id")):
                job_exists = True
                break
        
        # Add job if it doesn't exist
        if not job_exists:
            saved_jobs.append(job)
            data["saved_jobs"] = saved_jobs
            self.save_data(data, self.job_data_file)
        
        return saved_jobs
    
    def remove_saved_job(self, job_id: str) -> List[Dict[str, Any]]:
        """
        Remove a job from the saved jobs list.
        
        Args:
            job_id: ID of the job to remove
            
        Returns:
            Updated list of saved jobs
        """
        data = self.load_data(self.job_data_file)
        saved_jobs = data.get("saved_jobs", [])
        
        # Remove job with matching ID
        saved_jobs = [job for job in saved_jobs if job.get("id") != job_id]
        
        data["saved_jobs"] = saved_jobs
        self.save_data(data, self.job_data_file)
        
        return saved_jobs
    
    def search_jobs(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search for jobs based on the provided query.
        
        Args:
            query: Dictionary containing search parameters
            
        Returns:
            List of job results
        """
        # Construct a prompt for the job search
        job_title = query.get("job_title", "")
        location = query.get("location", "")
        keywords = query.get("keywords", [])
        experience_level = query.get("experience_level", "")
        
        print(f"Searching for jobs with: title={job_title}, location={location}, keywords={keywords}, experience={experience_level}")
        
        prompt = f"""
        Generate 5 realistic job postings for a {job_title} position
        {f'in {location}' if location else ''}
        {f'with keywords: {", ".join(keywords)}' if keywords else ''}
        {f'at {experience_level} level' if experience_level else ''}.
        
        For each job, include:
        1. Job title
        2. Company name
        3. Location
        4. Job description (summary)
        5. Required skills
        6. Salary range (if applicable)
        7. A fictional but realistic job ID
        8. A fictional but realistic URL
        
        Format the results as a JSON array of job objects.
        """
        
        messages = [
            {"role": "system", "content": "You are a job search assistant that generates realistic job postings based on search criteria."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            print("Sending request to OpenAI API...")
            response = self.get_completion(messages)
            print(f"Received response: {response[:100]}...") # Print first 100 chars of response
            
            # Try to parse the response as JSON
            jobs = json.loads(response)
            print(f"Successfully parsed JSON with {len(jobs)} jobs")
            
            # Add a timestamp and search query to each job
            for job in jobs:
                job["search_timestamp"] = self._get_timestamp()
                job["search_query"] = query
            
            return jobs
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Raw response: {response}")
            return []
        except Exception as e:
            print(f"Error in search_jobs: {e}")
            return []
    
    def analyze_job_match(self, job: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze how well a job matches the user's profile.
        
        Args:
            job: Dictionary containing job details
            user_profile: Dictionary containing user profile
            
        Returns:
            Dictionary containing match analysis
        """
        # Extract relevant information from user profile
        user_skills = user_profile.get("skills", [])
        user_experiences = user_profile.get("work_experience", [])
        user_education = user_profile.get("education", [])
        
        # Extract job requirements
        job_skills = job.get("required_skills", [])
        job_description = job.get("description", "")
        
        # Construct a prompt for the analysis
        prompt = f"""
        Analyze how well the candidate's profile matches the job requirements.
        
        Job details:
        - Title: {job.get('title', '')}
        - Description: {job_description}
        - Required skills: {', '.join(job_skills) if isinstance(job_skills, list) else job_skills}
        
        Candidate profile:
        - Skills: {', '.join(user_skills)}
        - Work experience: {json.dumps(user_experiences)}
        - Education: {json.dumps(user_education)}
        
        Provide an analysis with the following:
        1. Overall match percentage (0-100)
        2. Matching skills
        3. Missing skills
        4. Relevant experience
        5. Recommendations for the candidate
        
        Format the results as a JSON object.
        """
        
        messages = [
            {"role": "system", "content": "You are a job match analyzer that evaluates how well a candidate's profile matches job requirements."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            analysis = json.loads(response)
            return analysis
        except json.JSONDecodeError:
            # If parsing fails, return a basic analysis
            return {
                "match_percentage": 0,
                "matching_skills": [],
                "missing_skills": [],
                "relevant_experience": [],
                "recommendations": ["Unable to analyze job match. Please try again."]
            }
    
    def _get_timestamp(self) -> str:
        """Get the current timestamp as a string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def run(self, action: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the job search agent with the specified action.
        
        Args:
            action: The action to perform (search_jobs, save_job, etc.)
            data: Data required for the action
            
        Returns:
            Result of the action
        """
        if action == "search_jobs" and data:
            return {"jobs": self.search_jobs(data)}
        elif action == "get_saved_jobs":
            return {"saved_jobs": self.get_saved_jobs()}
        elif action == "save_job" and data:
            return {"saved_jobs": self.save_job(data)}
        elif action == "remove_saved_job" and data and "job_id" in data:
            return {"saved_jobs": self.remove_saved_job(data["job_id"])}
        elif action == "analyze_job_match" and data and "job" in data and "user_profile" in data:
            return {"match_analysis": self.analyze_job_match(data["job"], data["user_profile"])}
        else:
            return {"error": "Invalid action or missing data"} 