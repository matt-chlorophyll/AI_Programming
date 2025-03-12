import os
import json
from typing import Dict, List, Any, Optional
from openai import OpenAI
import config

class BaseAgent:
    """Base class for all JobMaster agents."""
    
    def __init__(self, agent_type: str):
        """
        Initialize the base agent.
        
        Args:
            agent_type: The type of agent (job_search, user_info, etc.)
        """
        self.agent_type = agent_type
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.agent_config = config.AGENT_CONFIGS.get(agent_type, {})
        self.model = self.agent_config.get("model", config.DEFAULT_MODEL)
        self.temperature = self.agent_config.get("temperature", 0.3)
        self.max_tokens = self.agent_config.get("max_tokens", 1000)
        
    def get_completion(self, 
                       messages: List[Dict[str, str]], 
                       temperature: Optional[float] = None, 
                       max_tokens: Optional[int] = None) -> str:
        """
        Get a completion from the OpenAI API.
        
        Args:
            messages: List of message dictionaries
            temperature: Temperature parameter (optional)
            max_tokens: Max tokens parameter (optional)
            
        Returns:
            The completion text
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature if temperature is not None else self.temperature,
            max_tokens=max_tokens if max_tokens is not None else self.max_tokens
        )
        return response.choices[0].message.content
    
    def save_data(self, data: Dict[str, Any], file_path: str) -> None:
        """
        Save data to a JSON file.
        
        Args:
            data: Data to save
            file_path: Path to the file
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # If file exists, load and update existing data
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                existing_data = json.load(f)
                
            # Update existing data with new data
            if isinstance(existing_data, dict) and isinstance(data, dict):
                existing_data.update(data)
                data = existing_data
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load data from a JSON file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            The loaded data
        """
        if not os.path.exists(file_path):
            return {}
        
        with open(file_path, 'r') as f:
            return json.load(f)
            
    def run(self, *args, **kwargs):
        """
        Run the agent. To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the run method.") 