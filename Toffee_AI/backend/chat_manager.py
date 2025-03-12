from typing import List, Dict
import openai
from .prompts.templates import MESSAGE_TEMPLATE, QUESTIONS_TEMPLATE, TIPS_TEMPLATE

class ChatManager:
    def __init__(self):
        # Initialize OpenAI client
        self.client = openai.OpenAI()  # Make sure to set OPENAI_API_KEY in environment variables

    def draft_message(
        self,
        profile_data: Dict,
        student_interests: str,
        meeting_type: str
    ) -> str:
        prompt = MESSAGE_TEMPLATE.format(
            name=profile_data["name"],
            role=profile_data["role"],
            company=profile_data["company"],
            interests=student_interests,
            meeting_type=meeting_type
        )
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you prefer
            messages=[
                {"role": "system", "content": "You are a professional career advisor helping students draft LinkedIn messages."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    def generate_questions(
        self,
        profile_data: Dict,
        student_interests: str
    ) -> List[str]:
        prompt = QUESTIONS_TEMPLATE.format(
            role=profile_data["role"],
            company=profile_data["company"],
            experience=profile_data["experience"],
            interests=student_interests
        )
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career advisor helping students prepare for networking meetings."},
                {"role": "user", "content": prompt}
            ]
        )
        questions = [q.strip() for q in response.choices[0].message.content.split("\n") if q.strip()]
        return questions[:5]  # Return top 5 questions

    def generate_tips(
        self,
        profile_data: Dict,
        meeting_type: str
    ) -> List[str]:
        prompt = TIPS_TEMPLATE.format(
            role=profile_data["role"],
            company=profile_data["company"],
            meeting_type=meeting_type
        )
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career advisor helping students prepare for professional meetings."},
                {"role": "user", "content": prompt}
            ]
        )
        tips = [tip.strip() for tip in response.choices[0].message.content.split("\n") if tip.strip()]
        return tips 