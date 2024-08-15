import pyaudio
import wave
import os
import numpy as np
from faster_whisper import WhisperModel
from rag.voice_assistant import AiVoiceAssistant
from live_tts import tts_wrapper 

# Define color constants
NEON_BLUE = "\033[94m"
NEON_GREEN = "\033[92m"
RESET_COLOR = "\033[0m"

NGROK_URL = "https://enhanced-quietly-fowl.ngrok-free.app/"  # Replace with your actual ngrok URL, run Ollama on cloud 

ai_assistant = AiVoiceAssistant(NGROK_URL)

def is_speech(data, threshold):
    audio_data = np.frombuffer(data, np.int16)
    return np.abs(audio_data).mean() > threshold

def record_until_silence(p, stream, file_path, silence_duration=2, threshold=300):
    frames = []
    silent_chunks = 0
    max_silent_chunks = int(silence_duration * 16000 / 1024)

    while True:
        data = stream.read(1024)
        frames.append(data)

        if is_speech(data, threshold):
            silent_chunks = 0  # Reset silent chunk count if speech is detected
        else:
            silent_chunks += 1

        if silent_chunks > max_silent_chunks:
            break

    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))

def transcribe_chunk(model, file_path):
    segments, _ = model.transcribe(file_path)
    return " ".join([segment.text for segment in segments])

def main():
    print("Initializing model...")
    model_size = "medium.en"
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    print("Model initialized successfully.")

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    print("Audio stream opened.")
    print("-"*15)

    silence_duration = 2  # Duration in seconds to consider as silence to stop recording

    try:
        while True:
            chunk_file = "temp_chunk.wav"
            print("Listening for speech...")

            while True:
                data = stream.read(1024)
                if is_speech(data, threshold=500):
                    print("Speech detected, recording...")
                    record_until_silence(p, stream, chunk_file, silence_duration=silence_duration)
                    break

            print("Transcribing...")
            transcription = transcribe_chunk(model, chunk_file)
            os.remove(chunk_file)
            print("Customer: " + NEON_BLUE + transcription + RESET_COLOR)

            # Process customer input and get response from AI assistant
            output = ai_assistant.interact_with_llm(transcription)
            if output:
                output = output.lstrip()
                print("Processing...")
                tts_wrapper(output)
                print("AI Assistant: " + NEON_GREEN + output + RESET_COLOR)
                print("-"*15)

    except KeyboardInterrupt:
        print("Stopping....")
    
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()