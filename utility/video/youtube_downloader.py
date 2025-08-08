import yt_dlp
import tempfile
import os

def download_youtube_video(url, output_path=None):
    """
    Downloads a YouTube video and returns the path to the downloaded file.
    """
    try:
        # Create temporary file if no output path is specified
        if output_path is None:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            output_path = temp_file.name
            temp_file.close()

        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best[ext=mp4]',  # Best quality MP4
            'outtmpl': output_path,     # Output template
            'quiet': True,              # Less output
            'no_warnings': True,        # No warnings
        }

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return output_path
    except Exception as e:
        print(f"Error downloading YouTube video: {str(e)}")
        return None
