import os
import requests
import io

# voicerss.org Text to Speech API
API_URL = f"http://api.voicerss.org/?key={os.environ.get('API_KEY_TTS')}&hl=en-us&c=MP3&src="

async def get_audio(text):
    req = requests.get(API_URL + text)

    return io.BytesIO(req.content)