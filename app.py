import os
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from pydantic import BaseModel, ValidationError

# Set up API key for Gemini
os.environ["GENAI_API_KEY"] = "AIzaSyBkOs7KXMExBd4VHpPNG7eneK5OzENQvLM"

# Configure Gemini API
genai.configure(api_key=os.environ["GENAI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

class VideoInfo(BaseModel):
    url: str

class Transcript(BaseModel):
    text: str

class Summary(BaseModel):
    bullet_points: list[str]

def get_video_id(video_info: VideoInfo):
    if "youtube.com/watch?v=" in video_info.url:
        return video_info.url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in video_info.url:
        return video_info.url.split("youtu.be/")[1].split("?")[0]
    else:
        return None

def get_transcript(video_info: VideoInfo) -> Transcript:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(get_video_id(video_info))
        transcript_text = ""
        for entry in transcript:
            transcript_text += entry['text'] + "\n"
        
        with open("transcript.txt", "w", encoding="utf-8") as file:
            file.write(transcript_text + "\n")
        
        return Transcript(text=transcript_text)
    except Exception as e:
        st.error(f"Error fetching transcript: {str(e)}")
        return None


def generate_summary(transcript: Transcript) -> Summary:
    try:
        response = model.generate_content([transcript.text, "Can you summarize this video transcript as a bulleted list?"])
        
        summary_text = ""
        for part in response.parts:
            if hasattr(part, 'text'):
                summary_text += part.text
        
        summary_points = summary_text.split("\n")
        return Summary(bullet_points=summary_points)
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None


# Streamlit app layout
st.title("YouTube Video Summarizer")
st.write("Enter a YouTube video URL to get a summary of its content.")

video_url = st.text_input("Enter YouTube video URL (https://www.youtube.com/watch?v=...)")

if video_url:
    try:
        video_info = VideoInfo(url=video_url)
        video_id = get_video_id(video_info)
        if video_id:
            st.write(f"Video ID: {video_id}")
            
            if st.button("Summarize Video"):
                with st.spinner("Getting transcript and summarizing the video..."):
                    transcript = get_transcript(video_info)
                    if transcript:
                        st.success("Transcript saved to 'transcript.txt'")
                        
                        # Generate the summary
                        summary = generate_summary(transcript)
                        if summary:
                            # Display the summary
                            st.subheader("Summary:")
                            for line in summary.bullet_points:
                                st.write(f"- {line}")
        else:
            st.error("Invalid YouTube URL. Please enter a valid URL in the format: https://www.youtube.com/watch?v=...")
    except ValidationError as e:
        st.error(f"Invalid URL: {str(e)}")