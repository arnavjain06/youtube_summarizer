import os
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Set up API key for Gemini
os.environ["GENAI_API_KEY"] = "AIzaSyAvyQF0MeD-TxtJb3kBCIuyAXzeCA6QURM"

# Configure Gemini API
genai.configure(api_key=os.environ["GENAI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def get_video_id(url):
    # Extract video ID from YouTube URL
    if "youtube.com/watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return None

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ""
        for entry in transcript:
            transcript_text += entry['text'] + " "
        
        # Save transcript to a file
        with open("transcript.txt", "w", encoding="utf-8") as file:
            file.write(transcript_text + "\n")
        
        return transcript_text
    except Exception as e:
        st.error(f"Error fetching transcript: {str(e)}")
        return None
