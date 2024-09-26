import os
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Set up API key for Gemini
os.environ["GENAI_API_KEY"] = "AIzaSyAvyQF0MeD-TxtJb3kBCIuyAXzeCA6QURM"

# Configure Gemini API
genai.configure(api_key=os.environ["GENAI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

