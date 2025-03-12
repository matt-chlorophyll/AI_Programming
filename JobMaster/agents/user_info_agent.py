from typing import Dict, Any, List, Optional
import json
import os
from .base_agent import BaseAgent
import config

class UserInfoAgent(BaseAgent):
    """Agent for managing user information for job applications."""
    
    def __init__(self):
        super().__init__("user_info")
        self.user_data_file = config.USER_DATA_FILE
        
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get the stored user information.
        
        Returns:
            Dictionary containing user information
        """
        return self.load_data(self.user_data_file)
    
    def save_user_info(self, user_info: Dict[str, Any]) -> None:
        """
        Save user information.
        
        Args:
            user_info: Dictionary containing user information
        """
        self.save_data(user_info, self.user_data_file)
    
    def collect_basic_info(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect basic user information.
        
        Args:
            user_input: Dictionary containing user input
            
        Returns:
            Dictionary containing processed basic information
        """
        # Get existing user data
        user_data = self.get_user_info()
        
        # Update with new information
        basic_info = {
            "name": user_input.get("name", user_data.get("name", "")),
            "email": user_input.get("email", user_data.get("email", "")),
            "phone": user_input.get("phone", user_data.get("phone", "")),
            "location": user_input.get("location", user_data.get("location", "")),
            "linkedin": user_input.get("linkedin", user_data.get("linkedin", "")),
            "github": user_input.get("github", user_data.get("github", "")),
            "portfolio": user_input.get("portfolio", user_data.get("portfolio", "")),
        }
        
        # Update user data
        user_data.update({"basic_info": basic_info})
        self.save_user_info(user_data)
        
        return basic_info
    
    def add_work_experience(self, experience: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Add a work experience entry.
        
        Args:
            experience: Dictionary containing work experience details
            
        Returns:
            Updated list of work experiences
        """
        user_data = self.get_user_info()
        work_experiences = user_data.get("work_experience", [])
        
        # Add new experience
        work_experiences.append(experience)
        
        # Update user data
        user_data["work_experience"] = work_experiences
        self.save_user_info(user_data)
        
        return work_experiences
    
    def add_education(self, education: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Add an education entry.
        
        Args:
            education: Dictionary containing education details
            
        Returns:
            Updated list of education entries
        """
        user_data = self.get_user_info()
        education_entries = user_data.get("education", [])
        
        # Add new education entry
        education_entries.append(education)
        
        # Update user data
        user_data["education"] = education_entries
        self.save_user_info(user_data)
        
        return education_entries
    
    def add_skills(self, skills: List[str]) -> List[str]:
        """
        Add skills to the user profile.
        
        Args:
            skills: List of skills to add
            
        Returns:
            Updated list of skills
        """
        user_data = self.get_user_info()
        existing_skills = user_data.get("skills", [])
        
        # Add new skills (avoid duplicates)
        updated_skills = list(set(existing_skills + skills))
        
        # Update user data
        user_data["skills"] = updated_skills
        self.save_user_info(user_data)
        
        return updated_skills
    
    def add_projects(self, project: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Add a project to the user profile.
        
        Args:
            project: Dictionary containing project details
            
        Returns:
            Updated list of projects
        """
        user_data = self.get_user_info()
        projects = user_data.get("projects", [])
        
        # Add new project
        projects.append(project)
        
        # Update user data
        user_data["projects"] = projects
        self.save_user_info(user_data)
        
        return projects
    
    def add_certifications(self, certification: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Add a certification to the user profile.
        
        Args:
            certification: Dictionary containing certification details
            
        Returns:
            Updated list of certifications
        """
        user_data = self.get_user_info()
        certifications = user_data.get("certifications", [])
        
        # Add new certification
        certifications.append(certification)
        
        # Update user data
        user_data["certifications"] = certifications
        self.save_user_info(user_data)
        
        return certifications
    
    def analyze_profile_completeness(self) -> Dict[str, Any]:
        """
        Analyze the completeness of the user profile.
        
        Returns:
            Dictionary containing analysis results
        """
        user_data = self.get_user_info()
        
        # Check for required sections
        has_basic_info = "basic_info" in user_data and all([
            user_data["basic_info"].get("name"),
            user_data["basic_info"].get("email"),
            user_data["basic_info"].get("phone")
        ])
        
        has_work_experience = "work_experience" in user_data and len(user_data["work_experience"]) > 0
        has_education = "education" in user_data and len(user_data["education"]) > 0
        has_skills = "skills" in user_data and len(user_data["skills"]) > 0
        
        # Calculate completeness percentage
        sections = ["basic_info", "work_experience", "education", "skills", "projects", "certifications"]
        completed_sections = sum(1 for section in sections if section in user_data and user_data[section])
        completeness_percentage = (completed_sections / len(sections)) * 100
        
        return {
            "completeness_percentage": completeness_percentage,
            "has_basic_info": has_basic_info,
            "has_work_experience": has_work_experience,
            "has_education": has_education,
            "has_skills": has_skills,
            "missing_sections": [section for section in sections if section not in user_data or not user_data[section]]
        }
    
    def run(self, action: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the user information agent with the specified action.
        
        Args:
            action: The action to perform (collect_basic_info, add_work_experience, etc.)
            data: Data required for the action
            
        Returns:
            Result of the action
        """
        if action == "get_user_info":
            return self.get_user_info()
        elif action == "collect_basic_info" and data:
            return self.collect_basic_info(data)
        elif action == "add_work_experience" and data:
            return {"work_experience": self.add_work_experience(data)}
        elif action == "add_education" and data:
            return {"education": self.add_education(data)}
        elif action == "add_skills" and data and "skills" in data:
            return {"skills": self.add_skills(data["skills"])}
        elif action == "add_projects" and data:
            return {"projects": self.add_projects(data)}
        elif action == "add_certifications" and data:
            return {"certifications": self.add_certifications(data)}
        elif action == "analyze_profile_completeness":
            return self.analyze_profile_completeness()
        else:
            return {"error": "Invalid action or missing data"} 