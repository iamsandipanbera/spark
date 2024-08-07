import speech_recognition as sr

def record_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)
        print("Recording... Speak now.")
        audio = recognizer.listen(source)
        print("Recording stopped.")
    
    return audio

def transcribe_audio(audio):
    recognizer = sr.Recognizer()
    
    try:
        print("Transcribing audio...")
        transcript = recognizer.recognize_google(audio)
        print("Transcript: {}".format(transcript))
    except sr.RequestError:
        print("API unavailable")
    except sr.UnknownValueError:
        print("Unable to recognize speech")

if __name__ == "__main__":
    audio = record_audio()
    transcribe_audio(audio)
