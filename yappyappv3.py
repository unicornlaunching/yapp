import streamlit as st
from pytube3 import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os

def get_transcript(video_url):
    if 'youtu.be' in video_url:
        video_id = video_url.split('.be/')[1]
        video_id = video_id.split('?')[0]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
    else:
        video_id = video_url.split('watch?v=')[1]

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        st.write('Error retrieving transcript: ', str(e))
        return None

    texts = [d.get('text') for d in transcript]
    return " ".join(texts)

def download_clip(video_url):
    if 'youtu.be' in video_url:
        video_id = video_url.split('.be/')[1]
        video_id = video_id.split('?')[0]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

    # Download video
    yt = YouTube(video_url)
    stream = yt.streams.first()
    stream.download(filename="temp")

    # Cut first 10 seconds
    ffmpeg_extract_subclip("temp.mp4", 0, 10, targetname="clip.mp4")

    # Remove the temp file
    if os.path.exists("temp.mp4"):
        os.remove("temp.mp4")

st.title('YouTube Transcript Extraction')

video_url = st.text_input("Enter a Youtube video URL: ")

if st.button('Get Transcript'):
    if video_url:
        result = get_transcript(video_url)
        if result:
            st.write(result)
    else:
        st.write("Please enter a valid URL")

if st.button('Download 10-second Clip'):
    if video_url:
        download_clip(video_url)
        st.write("Download Completed. Check the app's directory for 'clip.mp4'")
    else:
        st.write("Please enter a valid URL")
