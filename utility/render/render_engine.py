import time
import os
import tempfile
import zipfile
import platform
import subprocess
from moviepy.editor import (AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip)
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
import requests
from utility.video.youtube_downloader import download_youtube_video

def download_file(url, filename):
    with open(filename, 'wb') as f:
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        f.write(response.content)

def search_program(program_name):
    try: 
        search_cmd = "where" if platform.system() == "Windows" else "which"
        return subprocess.check_output([search_cmd, program_name]).decode().strip()
    except subprocess.CalledProcessError:
        return None

def get_program_path(program_name):
    program_path = search_program(program_name)
    return program_path

def get_output_media(audio_file_path, timed_captions, background_video_data, video_server):
    OUTPUT_FILE_NAME = "rendered_video.mp4"
    magick_path = get_program_path("magick")
    print(magick_path)
    if magick_path:
        os.environ['IMAGEMAGICK_BINARY'] = magick_path
    else:
        os.environ['IMAGEMAGICK_BINARY'] = '/usr/bin/convert'
    
    visual_clips = []
    
    for (t1, t2), video_url in background_video_data:
        try:
            # Se for um vídeo do YouTube
            if "youtube.com" in video_url or "youtu.be" in video_url:
                video_filename = download_youtube_video(video_url)
                if video_filename is None:
                    raise Exception("Failed to download YouTube video")
                
                print(f"Loading video clip from {video_filename}")
                # Create VideoFileClip from the downloaded file
                video_clip = VideoFileClip(video_filename)
                
                # Se o vídeo for menor que o tempo necessário, fazemos loop
                total_duration = t2 - t1
                if total_duration > video_clip.duration:
                    video_clip = video_clip.loop(duration=total_duration)
                    
                video_clip = video_clip.set_start(t1).set_end(t2)
                
                # Depois de criar o clip, podemos remover o arquivo
                try:
                    os.remove(video_filename)
                except Exception as e:
                    print(f"Warning: Could not remove temporary file {video_filename}: {str(e)}")
            else:
                # Download do vídeo do Pexels
                video_filename = tempfile.NamedTemporaryFile(delete=False).name
                download_file(video_url, video_filename)
                video_clip = VideoFileClip(video_filename)
                video_clip = video_clip.set_start(t1).set_end(t2)
            
            if video_clip is not None:
                visual_clips.append(video_clip)
            else:
                raise Exception("Failed to create video clip")
                
        except Exception as e:
            print(f"Error processing video segment {t1}-{t2}: {str(e)}")
            # Se falhar um segmento, tentamos continuar com os outros
            continue
    
    audio_clips = []
    audio_file_clip = AudioFileClip(audio_file_path)
    audio_clips.append(audio_file_clip)

    for (t1, t2), text in timed_captions:
        text_clip = TextClip(txt=text, fontsize=100, font="FreeSans-Bold", color="white", stroke_width=3, stroke_color="black", method="label")
        text_clip = text_clip.set_start(t1)
        text_clip = text_clip.set_end(t2)
        text_clip = text_clip.set_position(["center", 800])
        visual_clips.append(text_clip)

    video = CompositeVideoClip(visual_clips)
    
    if audio_clips:
        audio = CompositeAudioClip(audio_clips)
        video.duration = audio.duration
        video.audio = audio

    video.write_videofile(OUTPUT_FILE_NAME, codec='libx264', audio_codec='aac', fps=25, preset='veryfast')
    
    # Clean up downloaded files
    for (t1, t2), video_url in background_video_data:
        video_filename = tempfile.NamedTemporaryFile(delete=False).name
        os.remove(video_filename)

    return OUTPUT_FILE_NAME
