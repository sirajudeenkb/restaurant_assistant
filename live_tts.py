import requests
from pydub import AudioSegment
from pydub.playback import play
import io

class ElevenLabsTTS:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
        self.voices = {
            "rachel": "21m00Tcm4TlvDq8ikWAM",
            "antoni": "ErXwobaYiN019PkySvjV",
            "elli": "MF3mGyEYCl7XYWbV9V6O",
            "josh": "TxGEqnHWrfWFTfGW9XjX",
            "arnold": "VR6AewLTigWG4xSOukaG",
            "adam": "pNInz6obpgDQGcFmaJgB",
            "sam": "yoZ06aMxZJJ28mfd3POQ",
            "bella": "EXAVITQu4vr4xnSDxMaL"
        }

    def play_text_to_speech(self, text, voice="antoni", stability=1.5, similarity_boost=0.5):
        voice_id = self.voices.get(voice.lower(), self.voices["antoni"])

        url = f"{self.base_url}/text-to-speech/{voice_id}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            audio = AudioSegment.from_mp3(io.BytesIO(response.content))
            play(audio)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

def tts_wrapper(text, voice="antoni", stability=0.5, similarity_boost=0.5):
    api_key = ""  # Replace with your actual API key
    tts = ElevenLabsTTS(api_key)
    tts.play_text_to_speech(text, voice, stability, similarity_boost)

# Usage example:
# tts_wrapper("Hello, this is a test using ElevenLabs API.", voice="rachel")