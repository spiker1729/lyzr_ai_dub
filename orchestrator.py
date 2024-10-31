# -*- coding: utf-8 -*-

import requests
import json
import base64
import subprocess
from flask import Flask, request, render_template, url_for
from youtube_transcript_api import YouTubeTranscriptApi
from download import YouTubeVideoDownloader

app = Flask(__name__)

def fetch_transcript(video_id):
    # Fetch the transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Initialize variables
    total_text = ""
    first_start = None
    total_duration = 0

    # Iterate through the transcript
    for entry in transcript:
        if first_start is None:
            first_start = entry['start']
        
        total_duration += entry['duration']
        if total_duration > 120:
            break
        
        total_text += entry['text'] + " "

    # Output the results
    transcript_text = total_text.strip()
    start_time = first_start

    return transcript_text, start_time

def translate_text(text, target_language):
    url = "https://agent.api.lyzr.app/v2/chat/"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "lyzr-4sEJb7BuVX0QRHD8vY1RM9nP"
    }
    
    data = {
        "user_id": "pradumn.sde@gmail.com",
        "agent_id": "6722f7ac61f92e3cfee9c64b",
        "session_id": "5d27c131-9154-489a-9eda-0603321ae5f4",
        "message": f'translate in {target_language}: "{text}"'
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses

        # Print entire response for debugging
        # print("Full Response JSON:", response.json())

        # Extract the translated text from the response
        translated_text = response.json().get('response', None)
        if translated_text is None:
            print("Translation failed or returned empty response.")
            return None
        
        return translated_text

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError as ve:
        print(f"Error in translation: {ve}")
        return None

def generate_audio(transcript_text, target_language, output_file='output.wav'):
    url = 'https://demo-api.models.ai4bharat.org/inference/tts'

    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://models.ai4bharat.org',
        'priority': 'u=1, i',
        'referer': 'https://models.ai4bharat.org/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36'
    }

    payload = {
        "controlConfig": {"dataTracking": True},
        "input": [{"source": transcript_text}],
        "config": {"gender": "male", "language": {"sourceLanguage": target_language}}
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    response_json = response.json()
    print(response_json)
    audio_content = response_json['audio'][0]['audioContent']

    # Decode the base64 encoded audio content
    audio_data = base64.b64decode(audio_content)

    # Write the decoded audio content to a file
    with open(output_file, 'wb') as audio_file:
        audio_file.write(audio_data)

    print(f"Audio file saved as {output_file}")
    return output_file

def stitch_audio_video(video_file, audio_file, start_time, output_file='final_output.mp4'):
    """Stitch the audio file with the video file using ffmpeg, adding a delay to the audio based on the start time."""
    try:
        command = [
            "ffmpeg",
            "-i", video_file,
            "-itsoffset", str(start_time),
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            output_file
        ]
        subprocess.run(command, check=True)
        print(f"Final video with audio saved as: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error stitching audio and video: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    youtube_url = request.form['youtube_url']
    target_language = request.form['target_language']

    # Extract video ID from YouTube URL
    video_id = youtube_url.split('v=')[-1]

    # Download and trim the video
    downloader = YouTubeVideoDownloader(youtube_url)
    video_path, video_title = downloader.download_and_trim()
    if video_path:
        print(f"Trimmed video file saved at: {video_path}")
        print(f"Video title: {video_title}\n")
    
    # Fetch the transcript
    transcript_text, start_time = fetch_transcript(video_id)
    print(f"Transcript: {transcript_text}")
    print(f"Start time: {start_time}")

    # Translate the transcript
    translated_text = translate_text(transcript_text, target_language)
    print(f"Translated text: {translated_text}")

    # Generate the audio file from the translated transcript
    audio_file = generate_audio(translated_text, target_language)
    print(f"Generated audio file: {audio_file}")

    # Stitch the audio file with the trimmed video, adding the delay
    final_output_file = f"{video_title}_final.mp4"
    stitch_audio_video(video_path, audio_file, start_time, final_output_file)

    # Redirect to the index page with the video URLs
    return render_template('index.html', original_url=youtube_url, dubbed_url=url_for('static', filename=final_output_file))

if __name__ == "__main__":
    app.run(debug=True)