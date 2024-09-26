# YouTube Video Summarizer

This Streamlit web app allows users to input a YouTube video URL, retrieve its transcript, and generate a summary using Google's Gemini API.

## Features

- Extracts video transcripts using the `youtube-transcript-api`.
- Summarizes the transcript using Google's Gemini Generative Model.
- Saves the video transcript to a `transcript.txt` file.
- Easy-to-use interface for summarizing YouTube video content.

## Requirements

- Python 3.7+
- Streamlit
- `google-generativeai`
- `youtube-transcript-api`

## Installation

1. Clone the repository or download the code:

2. Install the required Python packages:

    pip install -r requirements.txt


3. Set up the Gemini API key:

    Replace `"Add your Gemini API key"` with your actual API key.

4. Run the app using Streamlit:
    ```bash
    streamlit run app.py
    ```

## Usage

1. Open the app in your browser at `http://localhost:8501`.
2. Enter a valid YouTube video URL (e.g., `https://www.youtube.com/watch?v=...`).
3. Click on the **Summarize Video** button.
4. View the generated summary and save the transcript to a file.

## Example

```bash
Video ID: dQw4w9WgXcQ
Transcript saved to 'transcript.txt'
Summary:
- Bulleted summary of the transcript here...
