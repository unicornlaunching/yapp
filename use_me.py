import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

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

    # Filter only the transcribed text
    texts = [d.get('text') for d in transcript]
    return " ".join(texts)

st.title('YouTube Transcript Extraction')

video_url = st.text_input("Enter a Youtube video URL: ")

if st.button('Get Transcript'):
    if video_url:
        result = get_transcript(video_url)
        if result:
            st.write(result)
    else:
        st.write("Please enter a valid URL")
