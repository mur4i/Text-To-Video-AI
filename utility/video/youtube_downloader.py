from pytube import YouTube
import tempfile
import os

def download_youtube_video(url, output_path=None):
    """
    Downloads a YouTube video and returns the path to the downloaded file.
    """
    try:
        # Create YouTube object
        yt = YouTube(url)
        
        # Get the highest resolution stream
        stream = yt.streams.get_highest_resolution()
        
        # Create temporary file if no output path is specified
        if output_path is None:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            output_path = temp_file.name
            temp_file.close()
        
        # Download the video
        stream.download(filename=output_path)
        
        return output_path
    except Exception as e:
        print(f"Error downloading YouTube video: {str(e)}")
        return None
