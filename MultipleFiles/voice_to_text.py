import sounddevice as sd
import numpy as np
import speech_recognition as sr
import io
import tempfile

def transcribe_microphone(timeout=5, sample_rate=16000):
    """Capture audio from microphone and transcribe it"""
    r = sr.Recognizer()
    
    # Record audio
    with sr.Microphone(sample_rate=sample_rate) as source:
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening... Speak now!")
            audio_data = r.listen(source, timeout=timeout)
            
            # Transcribe audio
            return r.recognize_google(audio_data)
            
        except sr.WaitTimeoutError:
            return "No speech detected"
        except sr.UnknownValueError:
            return "Could not understand audio"
        except Exception as e:
            return f"Error: {str(e)}"
