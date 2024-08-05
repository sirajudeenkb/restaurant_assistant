import pyttsx3

def play_text_to_speech(text, rate=200, voice="english"):
    engine = pyttsx3.init()
    
    # Set properties
    engine.setProperty('rate', rate)  # Speed of speech
    voices = engine.getProperty('voices')
    for v in voices:
        if voice.lower() in v.name.lower():
            engine.setProperty('voice', v.id)
            break

    # Play the speech
    engine.say(text)
    engine.runAndWait()

def tts_wrapper(text, rate=200, voice="english"):
    play_text_to_speech(text, rate, voice)