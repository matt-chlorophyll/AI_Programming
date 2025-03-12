import yt_dlp
import whisper
import os
from datetime import datetime
from tqdm import tqdm

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
        temp_audio_path = os.path.join(self.working_dir, 'temp_audio.mp3')
        
        # Create progress bar for download
        progress_bar = None
        
        def download_progress_hook(d):
            nonlocal progress_bar
            if d['status'] == 'downloading':
                if progress_bar is None:
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    progress_bar = tqdm(
                        total=total,
                        unit='B',
                        unit_scale=True,
                        desc="Downloading audio"
                    )
                downloaded = d.get('downloaded_bytes', 0)
                progress_bar.update(downloaded - progress_bar.n)
            elif d['status'] == 'finished' and progress_bar is not None:
                progress_bar.close()

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.working_dir, 'temp_audio.%(ext)s'),
            'ffmpeg_location': 'C:\\FFmpeg\\bin\\ffmpeg.exe',
            'progress_hooks': [download_progress_hook],
            'quiet': True  # Suppress yt-dlp's output
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
            if not os.path.exists(audio_path):
                print(f"Audio file not found at: {audio_path}")
                return None
            
            audio_path = os.path.abspath(audio_path)
            
            # Create a progress bar for transcription
            with tqdm(total=100, desc="Transcribing audio") as pbar:
                def progress_callback(progress):
                    pbar.update(int(progress * 100) - pbar.n)
                
                # Transcribe the audio with GPU settings
                result = self.model.transcribe(
                    audio_path,
                    fp16=False if self.device == "cpu" else True,
                    progress_callback=progress_callback
                )
            
            # Create filename with timestamp using absolute path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(x for x in video_title if x.isalnum() or x in (' ', '-', '_'))
            filename = os.path.join(self.output_dir, f"{timestamp}_{safe_title}.txt")
            
            # Save the transcript with a progress bar
            print("Saving transcript...")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Title: {video_title}\n")
                f.write(f"Transcription Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("\nTranscript:\n")
                f.write(result["text"])
            
            # Clean up the temporary audio file
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            return filename
            
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return None

    def process_video(self, youtube_url):
        """Process a YouTube video: download audio and transcribe"""
        print(f"\nProcessing video: {youtube_url}")
        audio_path, video_title = self.download_audio(youtube_url)
        
        if audio_path and video_title:
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