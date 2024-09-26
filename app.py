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


def generate_summary(transcript):
    try:
        response = model.generate_content([transcript, "Can you summarize this video transcript as a bulleted list?"])
        
        # Extract the generated text from the response
        summary = ""
        for part in response.parts:
            if hasattr(part, 'text'):
                summary += part.text
        
        return summary
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None


# Streamlit app layout
st.title("YouTube Video Summarizer")
st.write("Enter a YouTube video URL to get a summary of its content.")

video_url = st.text_input("Enter YouTube video URL (https://www.youtube.com/watch?v=...)")

if video_url:
    video_id = get_video_id(video_url)
    if video_id:
        st.write(f"Video ID: {video_id}")
        
        if st.button("Summarize Video"):
            with st.spinner("Getting transcript and summarizing the video..."):
                transcript = get_transcript(video_id)
                if transcript:
                    st.success("Transcript saved to 'transcript.txt'")
                    
                    # Generate the summary
                    summary = generate_summary(transcript)
                    if summary:
                        # Display the summary
                        st.subheader("Summary:")
                        st.write(summary)
    else:
        st.error("Invalid YouTube URL. Please enter a valid URL in the format: https://www.youtube.com/watch?v=...")