# JobMaster

JobMaster is an AI-powered job search and application assistant that uses specialized agents to help users find, apply for, and prepare for job opportunities.

## Features

- **Job Search Agent**: Searches for relevant job opportunities based on user preferences
- **User Information Management Agent**: Stores and manages user information for job applications
- **Resume Writing Agent**: Generates tailored resumes for specific job applications
- **Cover Letter Writing Agent**: Creates customized cover letters for job applications
- **Interview Preparation Agent**: Helps users prepare for job interviews
- **Networking Agent**: Assists with professional networking and communication

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```
   python main.py
   ```

## Project Structure

- `main.py`: Entry point for the application
- `config.py`: Configuration settings
- `agents/`: Contains all agent implementations
- `models/`: Data models and schemas
- `utils/`: Utility functions
- `data/`: Data storage
- `api/`: API endpoints

## License

MIT 