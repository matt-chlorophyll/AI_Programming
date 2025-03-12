from typing import Dict, Any, List, Optional
import json
import os
from .base_agent import BaseAgent
import config

class InterviewPrepAgent(BaseAgent):
    """Agent for helping users prepare for job interviews."""
    
    def __init__(self):
        super().__init__("interview_prep")
        self.interview_prep_data_dir = os.path.join(config.DATA_DIR, "interview_prep")
        os.makedirs(self.interview_prep_data_dir, exist_ok=True)
    
    def get_interview_prep_file_path(self, job_id: str) -> str:
        """
        Get the file path for interview preparation for a specific job.
        
        Args:
            job_id: ID of the job
            
        Returns:
            File path for the interview preparation
        """
        return os.path.join(self.interview_prep_data_dir, f"interview_prep_{job_id}.json")
    
    def get_saved_interview_prep(self, job_id: str) -> Dict[str, Any]:
        """
        Get saved interview preparation for a specific job.
        
        Args:
            job_id: ID of the job
            
        Returns:
            Dictionary containing the interview preparation
        """
        interview_prep_file = self.get_interview_prep_file_path(job_id)
        return self.load_data(interview_prep_file)
    
    def save_interview_prep(self, job_id: str, interview_prep: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save interview preparation for a specific job.
        
        Args:
            job_id: ID of the job
            interview_prep: Dictionary containing the interview preparation
            
        Returns:
            The saved interview preparation
        """
        interview_prep_file = self.get_interview_prep_file_path(job_id)
        self.save_data(interview_prep, interview_prep_file)
        return interview_prep
    
    def generate_common_questions(self, user_profile: Dict[str, Any], job: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate common interview questions for a specific job.
        
        Args:
            user_profile: Dictionary containing user profile
            job: Dictionary containing job details
            
        Returns:
            List of dictionaries containing questions and suggested answers
        """
        # Extract job details
        job_title = job.get("title", "")
        company_name = job.get("company", "")
        job_description = job.get("description", "")
        required_skills = job.get("required_skills", [])
        
        # Extract relevant user information
        skills = user_profile.get("skills", [])
        work_experience = user_profile.get("work_experience", [])
        
        # Construct a prompt for generating common questions
        prompt = f"""
        Generate 10 common interview questions for a {job_title} position at {company_name}, along with suggested answers based on the candidate's profile.
        
        Job details:
        - Title: {job_title}
        - Company: {company_name}
        - Description: {job_description}
        - Required skills: {', '.join(required_skills) if isinstance(required_skills, list) else required_skills}
        
        Candidate profile:
        - Skills: {', '.join(skills)}
        - Work experience: {json.dumps(work_experience)}
        
        For each question, provide:
        1. The question
        2. Why this question might be asked
        3. A suggested answer based on the candidate's profile
        4. Tips for delivering a strong response
        
        Include a mix of:
        - Technical questions related to the required skills
        - Behavioral questions
        - Situational questions
        - Questions about the candidate's experience
        - Questions about the company or role
        
        Format the results as a JSON array of question objects.
        """
        
        messages = [
            {"role": "system", "content": "You are an interview preparation assistant that generates common interview questions and suggested answers."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            questions = json.loads(response)
            
            # Save the questions if job_id is available
            if job.get("id"):
                interview_prep = self.get_saved_interview_prep(job["id"])
                interview_prep["common_questions"] = questions
                interview_prep["metadata"] = {
                    "job_id": job.get("id", ""),
                    "job_title": job_title,
                    "company": company_name,
                    "generated_timestamp": self._get_timestamp()
                }
                self.save_interview_prep(job["id"], interview_prep)
            
            return questions
        except json.JSONDecodeError:
            # If parsing fails, return an empty list
            return []
    
    def generate_technical_questions(self, user_profile: Dict[str, Any], job: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate technical interview questions for a specific job.
        
        Args:
            user_profile: Dictionary containing user profile
            job: Dictionary containing job details
            
        Returns:
            List of dictionaries containing technical questions and suggested answers
        """
        # Extract job details
        job_title = job.get("title", "")
        job_description = job.get("description", "")
        required_skills = job.get("required_skills", [])
        
        # Extract relevant user information
        skills = user_profile.get("skills", [])
        
        # Construct a prompt for generating technical questions
        prompt = f"""
        Generate 8 technical interview questions for a {job_title} position, along with suggested answers.
        
        Job details:
        - Title: {job_title}
        - Description: {job_description}
        - Required skills: {', '.join(required_skills) if isinstance(required_skills, list) else required_skills}
        
        Candidate skills:
        {', '.join(skills)}
        
        For each question, provide:
        1. The technical question
        2. Why this question is relevant to the role
        3. A suggested answer that demonstrates technical knowledge
        4. Follow-up questions the interviewer might ask
        
        Focus on technical questions that assess the candidate's knowledge of:
        - Technical skills required for the role
        - Problem-solving abilities
        - Technical concepts and methodologies
        
        Format the results as a JSON array of question objects.
        """
        
        messages = [
            {"role": "system", "content": "You are an interview preparation assistant that generates technical interview questions and suggested answers."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            questions = json.loads(response)
            
            # Save the questions if job_id is available
            if job.get("id"):
                interview_prep = self.get_saved_interview_prep(job["id"])
                interview_prep["technical_questions"] = questions
                
                # Update metadata if it doesn't exist
                if "metadata" not in interview_prep:
                    interview_prep["metadata"] = {
                        "job_id": job.get("id", ""),
                        "job_title": job_title,
                        "company": job.get("company", ""),
                        "generated_timestamp": self._get_timestamp()
                    }
                
                self.save_interview_prep(job["id"], interview_prep)
            
            return questions
        except json.JSONDecodeError:
            # If parsing fails, return an empty list
            return []
    
    def generate_company_research(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate company research for interview preparation.
        
        Args:
            job: Dictionary containing job details
            
        Returns:
            Dictionary containing company research
        """
        # Extract job details
        company_name = job.get("company", "")
        
        # Construct a prompt for generating company research
        prompt = f"""
        Generate comprehensive company research for {company_name} that would be useful for a job interview.
        
        Include:
        1. Company overview (history, mission, values)
        2. Products or services
        3. Recent news or developments
        4. Company culture
        5. Key competitors
        6. Potential interview questions about the company
        7. Good questions for the candidate to ask about the company
        
        Format the results as a JSON object with sections for each category of information.
        """
        
        messages = [
            {"role": "system", "content": "You are an interview preparation assistant that generates company research for job interviews."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            company_research = json.loads(response)
            
            # Save the company research if job_id is available
            if job.get("id"):
                interview_prep = self.get_saved_interview_prep(job["id"])
                interview_prep["company_research"] = company_research
                
                # Update metadata if it doesn't exist
                if "metadata" not in interview_prep:
                    interview_prep["metadata"] = {
                        "job_id": job.get("id", ""),
                        "job_title": job.get("title", ""),
                        "company": company_name,
                        "generated_timestamp": self._get_timestamp()
                    }
                
                self.save_interview_prep(job["id"], interview_prep)
            
            return company_research
        except json.JSONDecodeError:
            # If parsing fails, return a basic structure
            return {
                "error": "Failed to generate company research",
                "raw_response": response
            }
    
    def generate_interview_tips(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate general interview tips for a specific job.
        
        Args:
            job: Dictionary containing job details
            
        Returns:
            Dictionary containing interview tips
        """
        # Extract job details
        job_title = job.get("title", "")
        company_name = job.get("company", "")
        
        # Construct a prompt for generating interview tips
        prompt = f"""
        Generate comprehensive interview tips for a {job_title} position at {company_name}.
        
        Include:
        1. Before the interview (preparation, research, what to bring)
        2. During the interview (body language, communication tips, handling difficult questions)
        3. After the interview (follow-up, thank you notes)
        4. Common mistakes to avoid
        5. Industry-specific interview tips for this role
        6. Remote/video interview tips (if applicable)
        
        Format the results as a JSON object with sections for each category of tips.
        """
        
        messages = [
            {"role": "system", "content": "You are an interview preparation assistant that generates interview tips for job candidates."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            interview_tips = json.loads(response)
            
            # Save the interview tips if job_id is available
            if job.get("id"):
                interview_prep = self.get_saved_interview_prep(job["id"])
                interview_prep["interview_tips"] = interview_tips
                
                # Update metadata if it doesn't exist
                if "metadata" not in interview_prep:
                    interview_prep["metadata"] = {
                        "job_id": job.get("id", ""),
                        "job_title": job_title,
                        "company": company_name,
                        "generated_timestamp": self._get_timestamp()
                    }
                
                self.save_interview_prep(job["id"], interview_prep)
            
            return interview_tips
        except json.JSONDecodeError:
            # If parsing fails, return a basic structure
            return {
                "error": "Failed to generate interview tips",
                "raw_response": response
            }
    
    def evaluate_practice_answer(self, question: str, answer: str, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a practice answer for an interview question.
        
        Args:
            question: The interview question
            answer: The user's practice answer
            job: Dictionary containing job details
            
        Returns:
            Dictionary containing evaluation and feedback
        """
        # Extract job details
        job_title = job.get("title", "")
        
        # Construct a prompt for evaluating the answer
        prompt = f"""
        Evaluate the following practice answer for a {job_title} interview question:
        
        Question: {question}
        
        Answer: {answer}
        
        Provide a detailed evaluation including:
        1. Overall rating (1-10)
        2. Strengths of the answer
        3. Areas for improvement
        4. Specific suggestions to make the answer stronger
        5. Alternative approaches or points to consider
        
        Format the results as a JSON object with sections for each part of the evaluation.
        """
        
        messages = [
            {"role": "system", "content": "You are an interview coach that evaluates practice answers and provides constructive feedback."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            evaluation = json.loads(response)
            return evaluation
        except json.JSONDecodeError:
            # If parsing fails, return a basic structure
            return {
                "error": "Failed to evaluate practice answer",
                "raw_response": response
            }
    
    def _get_timestamp(self) -> str:
        """Get the current timestamp as a string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def run(self, action: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the interview preparation agent with the specified action.
        
        Args:
            action: The action to perform (generate_common_questions, evaluate_practice_answer, etc.)
            data: Data required for the action
            
        Returns:
            Result of the action
        """
        if action == "generate_common_questions" and data and "user_profile" in data and "job" in data:
            questions = self.generate_common_questions(data["user_profile"], data["job"])
            return {"common_questions": questions}
        elif action == "generate_technical_questions" and data and "user_profile" in data and "job" in data:
            questions = self.generate_technical_questions(data["user_profile"], data["job"])
            return {"technical_questions": questions}
        elif action == "generate_company_research" and data and "job" in data:
            research = self.generate_company_research(data["job"])
            return {"company_research": research}
        elif action == "generate_interview_tips" and data and "job" in data:
            tips = self.generate_interview_tips(data["job"])
            return {"interview_tips": tips}
        elif action == "get_saved_interview_prep" and data and "job_id" in data:
            prep = self.get_saved_interview_prep(data["job_id"])
            return {"interview_prep": prep}
        elif action == "evaluate_practice_answer" and data and "question" in data and "answer" in data and "job" in data:
            evaluation = self.evaluate_practice_answer(data["question"], data["answer"], data["job"])
            return {"evaluation": evaluation}
        else:
            return {"error": "Invalid action or missing data"} 