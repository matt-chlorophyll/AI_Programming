from typing import Dict, Any, List, Optional
import json
import os
from .base_agent import BaseAgent
import config

class NetworkingAgent(BaseAgent):
    """Agent for helping users with professional networking."""
    
    def __init__(self):
        super().__init__("networking")
        self.networking_data_dir = os.path.join(config.DATA_DIR, "networking")
        os.makedirs(self.networking_data_dir, exist_ok=True)
    
    def get_networking_file_path(self, contact_id: str) -> str:
        """
        Get the file path for networking information for a specific contact.
        
        Args:
            contact_id: ID of the contact
            
        Returns:
            File path for the networking information
        """
        return os.path.join(self.networking_data_dir, f"networking_{contact_id}.json")
    
    def get_saved_networking_info(self, contact_id: str) -> Dict[str, Any]:
        """
        Get saved networking information for a specific contact.
        
        Args:
            contact_id: ID of the contact
            
        Returns:
            Dictionary containing the networking information
        """
        networking_file = self.get_networking_file_path(contact_id)
        return self.load_data(networking_file)
    
    def save_networking_info(self, contact_id: str, networking_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save networking information for a specific contact.
        
        Args:
            contact_id: ID of the contact
            networking_info: Dictionary containing the networking information
            
        Returns:
            The saved networking information
        """
        networking_file = self.get_networking_file_path(contact_id)
        self.save_data(networking_info, networking_file)
        return networking_info
    
    def generate_connection_message(self, user_profile: Dict[str, Any], contact_info: Dict[str, Any], job: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate a connection message for a professional contact.
        
        Args:
            user_profile: Dictionary containing user profile
            contact_info: Dictionary containing contact information
            job: Optional dictionary containing job details
            
        Returns:
            Dictionary containing the generated connection message
        """
        # Extract user information
        user_name = user_profile.get("basic_info", {}).get("name", "")
        user_title = user_profile.get("basic_info", {}).get("title", "")
        user_experience = user_profile.get("work_experience", [])
        
        # Extract contact information
        contact_name = contact_info.get("name", "")
        contact_title = contact_info.get("title", "")
        contact_company = contact_info.get("company", "")
        
        # Extract job information if available
        job_title = job.get("title", "") if job else ""
        job_company = job.get("company", "") if job else ""
        
        # Determine the connection context
        connection_context = ""
        if job:
            connection_context = f"I'm interested in the {job_title} position at {job_company}"
        else:
            connection_context = f"I'm interested in connecting with professionals in the {contact_info.get('industry', 'industry')}"
        
        # Construct a prompt for generating a connection message
        prompt = f"""
        Generate a professional LinkedIn connection message from {user_name} to {contact_name}.
        
        About the sender ({user_name}):
        - Current/recent title: {user_title}
        - Experience: {json.dumps(user_experience[:1]) if user_experience else ''}
        
        About the recipient ({contact_name}):
        - Title: {contact_title}
        - Company: {contact_company}
        
        Connection context:
        {connection_context}
        
        The message should:
        1. Be professional and concise (under 300 characters for LinkedIn)
        2. Mention a specific reason for connecting
        3. Reference a shared interest, background, or the specific job if applicable
        4. Be personalized to the recipient
        5. Have a clear but non-demanding call to action
        
        Generate three different versions of the message with different approaches:
        1. Direct approach (mentioning the job or professional interest clearly)
        2. Mutual connection or interest approach (focusing on shared background or interests)
        3. Value-offering approach (offering something of value to the recipient)
        
        Format the results as a JSON object with the three message versions.
        """
        
        messages = [
            {"role": "system", "content": "You are a networking assistant that creates professional connection messages."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            connection_messages = json.loads(response)
            
            # Generate a contact ID if not provided
            contact_id = contact_info.get("id", self._generate_id(contact_name))
            
            # Save the connection messages
            networking_info = self.get_saved_networking_info(contact_id)
            networking_info["contact_info"] = contact_info
            networking_info["connection_messages"] = connection_messages
            networking_info["metadata"] = {
                "contact_id": contact_id,
                "job_id": job.get("id", "") if job else "",
                "generated_timestamp": self._get_timestamp()
            }
            self.save_networking_info(contact_id, networking_info)
            
            return connection_messages
        except json.JSONDecodeError:
            # If parsing fails, return a basic structure
            return {
                "error": "Failed to generate connection messages",
                "raw_response": response
            }
    
    def generate_coffee_chat_topics(self, user_profile: Dict[str, Any], contact_info: Dict[str, Any], job: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate topics for a coffee chat or informational interview.
        
        Args:
            user_profile: Dictionary containing user profile
            contact_info: Dictionary containing contact information
            job: Optional dictionary containing job details
            
        Returns:
            Dictionary containing the generated coffee chat topics
        """
        # Extract contact information
        contact_name = contact_info.get("name", "")
        contact_title = contact_info.get("title", "")
        contact_company = contact_info.get("company", "")
        contact_industry = contact_info.get("industry", "")
        
        # Determine the context
        context = ""
        if job:
            context = f"The user is interested in the {job.get('title', '')} position at {job.get('company', '')}"
        else:
            context = f"The user is interested in learning more about careers in {contact_industry}"
        
        # Construct a prompt for generating coffee chat topics
        prompt = f"""
        Generate topics and questions for a coffee chat or informational interview with {contact_name}, who is a {contact_title} at {contact_company}.
        
        Context:
        {context}
        
        Generate the following:
        
        1. Introduction topics (3-4 items):
           - Professional icebreakers
           - Establishing rapport
        
        2. Career path questions (4-5 items):
           - Questions about their career journey
           - How they got to their current position
        
        3. Industry/company insights (4-5 items):
           - Questions about the industry trends
           - Questions about the company culture and environment
        
        4. Role-specific questions (4-5 items):
           - Questions about their day-to-day responsibilities
           - Skills and qualifications important for success
        
        5. Advice-seeking questions (3-4 items):
           - Career development advice
           - Industry-specific advice
        
        6. Follow-up and next steps (2-3 items):
           - Professional ways to continue the relationship
           - Appropriate next steps
        
        For each topic or question, provide:
        - The question or topic
        - Why this is valuable to discuss
        - Potential follow-up questions
        
        Format the results as a JSON object with sections for each category of topics.
        """
        
        messages = [
            {"role": "system", "content": "You are a networking assistant that creates topics and questions for professional coffee chats and informational interviews."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            coffee_chat_topics = json.loads(response)
            
            # Generate a contact ID if not provided
            contact_id = contact_info.get("id", self._generate_id(contact_name))
            
            # Save the coffee chat topics
            networking_info = self.get_saved_networking_info(contact_id)
            networking_info["contact_info"] = contact_info
            networking_info["coffee_chat_topics"] = coffee_chat_topics
            
            # Update metadata if it doesn't exist
            if "metadata" not in networking_info:
                networking_info["metadata"] = {
                    "contact_id": contact_id,
                    "job_id": job.get("id", "") if job else "",
                    "generated_timestamp": self._get_timestamp()
                }
            
            self.save_networking_info(contact_id, networking_info)
            
            return coffee_chat_topics
        except json.JSONDecodeError:
            # If parsing fails, return a basic structure
            return {
                "error": "Failed to generate coffee chat topics",
                "raw_response": response
            }
    
    def generate_follow_up_message(self, user_profile: Dict[str, Any], contact_info: Dict[str, Any], meeting_notes: str) -> Dict[str, Any]:
        """
        Generate a follow-up message after a networking meeting.
        
        Args:
            user_profile: Dictionary containing user profile
            contact_info: Dictionary containing contact information
            meeting_notes: Notes from the meeting
            
        Returns:
            Dictionary containing the generated follow-up message
        """
        # Extract user information
        user_name = user_profile.get("basic_info", {}).get("name", "")
        
        # Extract contact information
        contact_name = contact_info.get("name", "")
        
        # Construct a prompt for generating a follow-up message
        prompt = f"""
        Generate a professional follow-up email from {user_name} to {contact_name} after a networking meeting or coffee chat.
        
        Meeting notes:
        {meeting_notes}
        
        The follow-up email should:
        1. Express gratitude for the meeting
        2. Reference specific points discussed during the meeting
        3. Include any promised follow-up items
        4. Suggest next steps or future communication
        5. End with a professional closing
        
        Generate two versions of the follow-up email:
        1. A standard thank you and follow-up
        2. A more detailed follow-up that includes specific action items
        
        Format the results as a JSON object with the two email versions.
        """
        
        messages = [
            {"role": "system", "content": "You are a networking assistant that creates professional follow-up messages after networking meetings."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            follow_up_messages = json.loads(response)
            
            # Generate a contact ID if not provided
            contact_id = contact_info.get("id", self._generate_id(contact_name))
            
            # Save the follow-up messages
            networking_info = self.get_saved_networking_info(contact_id)
            networking_info["contact_info"] = contact_info
            networking_info["follow_up_messages"] = follow_up_messages
            networking_info["meeting_notes"] = meeting_notes
            
            # Update metadata if it doesn't exist
            if "metadata" not in networking_info:
                networking_info["metadata"] = {
                    "contact_id": contact_id,
                    "generated_timestamp": self._get_timestamp()
                }
            
            self.save_networking_info(contact_id, networking_info)
            
            return follow_up_messages
        except json.JSONDecodeError:
            # If parsing fails, return a basic structure
            return {
                "error": "Failed to generate follow-up messages",
                "raw_response": response
            }
    
    def analyze_contact_profile(self, contact_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a contact's profile to identify networking opportunities.
        
        Args:
            contact_info: Dictionary containing contact information
            
        Returns:
            Dictionary containing the profile analysis
        """
        # Extract contact information
        contact_name = contact_info.get("name", "")
        contact_title = contact_info.get("title", "")
        contact_company = contact_info.get("company", "")
        contact_industry = contact_info.get("industry", "")
        contact_background = contact_info.get("background", "")
        
        # Construct a prompt for analyzing the profile
        prompt = f"""
        Analyze the following professional's profile to identify networking opportunities:
        
        Name: {contact_name}
        Title: {contact_title}
        Company: {contact_company}
        Industry: {contact_industry}
        Background: {contact_background}
        
        Provide an analysis that includes:
        1. Key insights about the professional's background and experience
        2. Potential conversation starters or common interests
        3. How this contact might be valuable for career development
        4. Recommended approach for initial outreach
        5. Potential mutual connections or organizations to reference
        
        Format the results as a JSON object with sections for each part of the analysis.
        """
        
        messages = [
            {"role": "system", "content": "You are a networking assistant that analyzes professional profiles to identify networking opportunities."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.get_completion(messages)
        
        try:
            # Try to parse the response as JSON
            profile_analysis = json.loads(response)
            
            # Generate a contact ID if not provided
            contact_id = contact_info.get("id", self._generate_id(contact_name))
            
            # Save the profile analysis
            networking_info = self.get_saved_networking_info(contact_id)
            networking_info["contact_info"] = contact_info
            networking_info["profile_analysis"] = profile_analysis
            
            # Update metadata if it doesn't exist
            if "metadata" not in networking_info:
                networking_info["metadata"] = {
                    "contact_id": contact_id,
                    "generated_timestamp": self._get_timestamp()
                }
            
            self.save_networking_info(contact_id, networking_info)
            
            return profile_analysis
        except json.JSONDecodeError:
            # If parsing fails, return a basic structure
            return {
                "error": "Failed to analyze profile",
                "raw_response": response
            }
    
    def _generate_id(self, name: str) -> str:
        """Generate a simple ID from a name."""
        import hashlib
        import time
        
        # Create a hash of the name and current time
        hash_input = f"{name}_{time.time()}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:10]
    
    def _get_timestamp(self) -> str:
        """Get the current timestamp as a string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def run(self, action: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the networking agent with the specified action.
        
        Args:
            action: The action to perform (generate_connection_message, generate_coffee_chat_topics, etc.)
            data: Data required for the action
            
        Returns:
            Result of the action
        """
        if action == "generate_connection_message" and data and "user_profile" in data and "contact_info" in data:
            job = data.get("job")
            messages = self.generate_connection_message(data["user_profile"], data["contact_info"], job)
            return {"connection_messages": messages}
        elif action == "generate_coffee_chat_topics" and data and "user_profile" in data and "contact_info" in data:
            job = data.get("job")
            topics = self.generate_coffee_chat_topics(data["user_profile"], data["contact_info"], job)
            return {"coffee_chat_topics": topics}
        elif action == "generate_follow_up_message" and data and "user_profile" in data and "contact_info" in data and "meeting_notes" in data:
            messages = self.generate_follow_up_message(data["user_profile"], data["contact_info"], data["meeting_notes"])
            return {"follow_up_messages": messages}
        elif action == "analyze_contact_profile" and data and "contact_info" in data:
            analysis = self.analyze_contact_profile(data["contact_info"])
            return {"profile_analysis": analysis}
        elif action == "get_saved_networking_info" and data and "contact_id" in data:
            networking_info = self.get_saved_networking_info(data["contact_id"])
            return {"networking_info": networking_info}
        else:
            return {"error": "Invalid action or missing data"} 