import yt_dlp
import whisper
import os
from datetime import datetime

class YoutubeTranscriber:
    def __init__(self, model_size="base"):
        """
        Initialize the transcriber with specified whisper model size
        model_size options: "tiny", "base", "small", "medium", "large"
        """
        # Check if CUDA is available
        import torch
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Add FFmpeg to system PATH if it's not already there
        ffmpeg_path = "C:\\FFmpeg\\bin"
        if ffmpeg_path not in os.environ["PATH"]:
            os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]
        
        self.model = whisper.load_model(model_size).to(self.device)
        
        # Set up working directory and output directory with absolute paths
        self.working_dir = os.path.abspath(os.path.dirname(__file__))
        self.output_dir = os.path.join(self.working_dir, "transcripts")
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def download_audio(self, youtube_url):
        """Download audio from YouTube video"""
        # Create full path for temporary audio file
        temp_audio_path = os.path.join(self.working_dir, 'temp_audio.mp3')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.working_dir, 'temp_audio.%(ext)s'),
            'ffmpeg_location': 'C:\\FFmpeg\\bin\\ffmpeg.exe'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(youtube_url, download=True)
                return temp_audio_path, info.get('title', 'Untitled')
            except Exception as e:
                print(f"Error downloading video: {str(e)}")
                return None, None

    def transcribe_audio(self, audio_path, video_title):
        """Transcribe the audio file using Whisper"""
        try:
            # Add file check with absolute path
            if not os.path.exists(audio_path):
                print(f"Audio file not found at: {audio_path}")
                return None
            
            # Convert audio path to absolute path
            audio_path = os.path.abspath(audio_path)
            print(f"Starting transcription of file: {audio_path}")
            
            # Transcribe the audio with GPU settings
            result = self.model.transcribe(
                audio_path,
                fp16=False if self.device == "cpu" else True
            )
            
            # Create filename with timestamp using absolute path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(x for x in video_title if x.isalnum() or x in (' ', '-', '_'))
            filename = os.path.join(self.output_dir, f"{timestamp}_{safe_title}.txt")
            
            # Save the transcript
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Title: {video_title}\n")
                f.write(f"Transcription Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("\nTranscript:\n")
                f.write(result["text"])
            
            # Clean up the temporary audio file only after successful transcription
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            return filename
            
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            import traceback
            print(traceback.format_exc())  # This will print the full error trace
            return None

    def process_video(self, youtube_url):
        """Process a YouTube video: download audio and transcribe"""
        print("Downloading audio...")
        audio_path, video_title = self.download_audio(youtube_url)

        if audio_path and video_title:
            print("Transcribing audio (this may take a while)...")
            transcript_path = self.transcribe_audio(audio_path, video_title)
            
            if transcript_path:
                print(f"\nTranscription completed! Saved to: {transcript_path}")
                return transcript_path
        
        return None

# Example usage
if __name__ == "__main__":
    url = input("Enter the YouTube video URL: ")
    transcriber = YoutubeTranscriber(model_size="small")  # You can change model size here
    transcriber.process_video(url) 