from flask import Flask, request, Response
from logging.config import dictConfig
from gradio_client import Client
import os

from settings import API_ROUTE_PREFIX_TTS

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

@app.route(f"{API_ROUTE_PREFIX_TTS}", methods=["POST"])
def tts():
    # Get and check the authentication token
    token = request.headers.get("Authorization")
    if not token or token != "Bearer " + os.getenv("API_TOKEN"):
        return "Unauthorized", 401

    text = request.json.get("text")
    name = request.json.get("name")
    app.logger.info(f"generating audio for {name}")
    if not text:
        return "text is required", 400
    if not name:
        return "name is required", 400
    
    if name.startswith("chattts"):
        return chattts(text, name)
    else:
        return "name is not supported", 400
    

def chattts(text, name):
    app.logger.info(f"generating audio for {name} using ChatTTS")
    token = os.getenv("HF_TOKEN")
    if not token:
        return "token not found", 400
    client = Client("jianliang00/ChatTTS", hf_token=token)
    result = client.predict(
        text=text,
        temperature=0.3,
        top_P=0.7,
        top_K=20,
        audio_seed_input=42,
        text_seed_input=42,
        refine_text_flag=True,
        api_name="/generate_audio"
    )
    app.logger.info(result)
    audio_path = result[0]

    def generate():
        with open(audio_path, "rb") as f:
            data = f.read(1024)
            while data:
                yield data
                data = f.read(1024)
    return Response(generate(), mimetype="audio/wav")
