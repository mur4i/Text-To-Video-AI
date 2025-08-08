from openai import OpenAI
import os
import edge_tts
import json
import asyncio
import whisper_timestamped as whisper
from utility.script.script_generator import generate_script
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a video from a topic.")
    parser.add_argument("topic", type=str, help="The topic for the video")
    parser.add_argument("--youtube", type=str, help="YouTube video URL to use as background", default=None)
    parser.add_argument("--video-server", type=str, choices=["pexel", "youtube"], default="pexel", help="Video source to use")

    args = parser.parse_args()
    SAMPLE_TOPIC = args.topic
    SAMPLE_FILE_NAME = "audio_tts.wav"
    VIDEO_SERVER = args.video_server
    YOUTUBE_URL = args.youtube

    if VIDEO_SERVER == "youtube" and not YOUTUBE_URL:
        parser.error("--youtube URL is required when using youtube video server")

    response = generate_script(SAMPLE_TOPIC)
    print("script: {}".format(response))

    asyncio.run(generate_audio(response, SAMPLE_FILE_NAME))

    timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
    print(timed_captions)

    search_terms = getVideoSearchQueriesTimed(response, timed_captions)
    print(search_terms)

    background_video_urls = None
    
    # Se estamos usando YouTube, não precisamos dos search_terms
    if VIDEO_SERVER == "youtube" and YOUTUBE_URL:
        # Calculamos o tempo total do vídeo a partir das legendas
        total_start = min(t1 for (t1, t2), _ in timed_captions)
        total_end = max(t2 for (t1, t2), _ in timed_captions)
        background_video_urls = [[[total_start, total_end], YOUTUBE_URL]]
    # Caso contrário, usamos o processo normal do Pexels
    elif search_terms is not None:
        background_video_urls = generate_video_url(search_terms, VIDEO_SERVER, YOUTUBE_URL)
        print(background_video_urls)
        # Só faz o merge se não for YouTube
        background_video_urls = merge_empty_intervals(background_video_urls)
    else:
        print("No background video")

    if background_video_urls is not None:
        video = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
        print(video)
    else:
        print("No video")
