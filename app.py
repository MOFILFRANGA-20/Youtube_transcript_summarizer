import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Load .env
load_dotenv()

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("AIzaSyCflGxx4jtTyIzzO1B3eVssjZsTgSO0YqQ"))
model = genai.GenerativeModel("gemini-2.0-flash")

def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t['text'] for t in transcript])
    except:
        return None

def summarize_text(text):
    prompt = f"Summarize this YouTube video transcript:\n{text}"
    response = model.generate_content(prompt)
    return response.text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['youtube_url']
        video_id = extract_video_id(url)
        transcript = get_transcript(video_id)
        if transcript:
            summary = summarize_text(transcript)
            return render_template("summarize.html", summary=summary)
        else:
            return render_template("index.html", error="Transcript not found.")
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
