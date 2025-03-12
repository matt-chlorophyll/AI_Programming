from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

from .linkedin_scraper import LinkedInScraper
from .chat_manager import ChatManager

app = FastAPI(title="Toffee AI")

class ProfileRequest(BaseModel):
    linkedin_url: str
    student_interests: str
    preferred_meeting_type: str  # "coffee" or "online"

class ChatResponse(BaseModel):
    message_draft: str
    questions: List[str]
    tips: List[str]

@app.post("/analyze", response_model=ChatResponse)
async def analyze_profile(request: ProfileRequest):
    try:
        # Initialize components
        scraper = LinkedInScraper()
        chat_manager = ChatManager()

        # Extract LinkedIn profile data
        profile_data = await scraper.extract_profile(request.linkedin_url)

        # Generate personalized content
        message = chat_manager.draft_message(
            profile_data,
            request.student_interests,
            request.preferred_meeting_type
        )
        
        questions = chat_manager.generate_questions(
            profile_data,
            request.student_interests
        )
        
        tips = chat_manager.generate_tips(
            profile_data,
            request.preferred_meeting_type
        )

        return ChatResponse(
            message_draft=message,
            questions=questions,
            tips=tips
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 