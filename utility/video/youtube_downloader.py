import yt_dlp
import tempfile
import os
import time

def download_youtube_video(url, output_path=None, max_retries=3):
    """
    Downloads a YouTube video and returns the path to the downloaded file.
    """
    for attempt in range(max_retries):
        try:
            # Create temporary file if no output path is specified
            if output_path is None:
                temp_dir = tempfile.mkdtemp()
                output_path = os.path.join(temp_dir, 'video.mp4')

            # Configure yt-dlp options
            ydl_opts = {
                'format': 'best[ext=mp4]/best',  # Best quality MP4 or best available
                'outtmpl': output_path,          # Output template
                'quiet': False,                  # Show output for debugging
                'no_warnings': False,            # Show warnings
                # Limit filesize to 100MB to avoid huge files
                'max_filesize': 100000000,
                # Additional options for better compatibility
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            }

            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # Get the actual path of the downloaded file
                output_path = ydl.prepare_filename(info)

            # Verify the file exists and has size > 0
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"Successfully downloaded video to {output_path}")
                return output_path
            else:
                raise Exception("Downloaded file is empty or does not exist")

        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
            
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                print("Failed to download video after all attempts")
                return None

        finally:
            # Clean up temporary directory if it was created and is empty
            if 'temp_dir' in locals() and os.path.exists(temp_dir):
                try:
                    os.rmdir(temp_dir)
                except:
                    pass

    return None
