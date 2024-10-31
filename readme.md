# YouTube Video Translator

This project is a Flask-based web application designed to translate YouTube videos from English to various Indian languages. It automates the process of fetching video transcripts, translating the text, generating audio from the translated text, and stitching the audio back into the video.

## Features

- **Transcript Generation**: Fetches the transcript of a YouTube video using the YouTube Transcript API.
- **Language Translation**: Translates the transcript text into the target Indian language using the Translate Agent API by LyZR.
- **Audio Generation**: Converts the translated text into audio using the AI4Bharat Text-to-Speech API.
- **Stitching Audio and Video**: Combines the original video with the generated audio using `ffmpeg`.

## Supported Languages

The application supports translation into the following Indian languages:

1. Malayalam
2. Telugu
3. Tamil
4. Kannada
5. Gujarati
6. Marathi
7. Rajasthani
8. Punjabi
9. Bengali
10. Odia
11. Assamese
12. Hindi
13. Bodo
14. Manipuri
15. English

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/youtube-video-translator.git
    cd youtube-video-translator
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables for the APIs (YouTube Transcript API, LyZR Translate Agent API, AI4Bharat Text-to-Speech API).

## Usage

1. Run the Flask application:
    ```sh
    flask run
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Enter the YouTube URL and select the target language for translation.

4. Click the "Submit" button to start the translation process.

5. Once the process is complete, you will see links to the original and processed videos.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

