import os
import sys
import signal
import speech_recognition as sr
import pyttsx3
import requests
from datetime import datetime
import openai

# Add Snowboy path
sys.path.append('path_to_snowboy_directory')

import snowboydecoder

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Function to handle voice commands
def handle_command(command):
    tokens = command.lower().split()
    
    if "hello" in tokens:
        response = "Hello! How can I assist you today?"
        print(response)
        speak(response)
    elif "time" in tokens:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        response = f"The current time is {current_time}"
        print(response)
        speak(response)
    elif "open" in tokens and "browser" in tokens:
        webbrowser.open("http://www.google.com")
        response = "Opening your web browser."
        print(response)
        speak(response)
    elif "search" in tokens:
        search_query = ' '.join(tokens[tokens.index("search")+1:])
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        response = f"Searching for {search_query}."
        print(response)
        speak(response)
    elif "weather" in tokens:
        api_key = "191a7f3fd06e83f4cbe0b484b74ea08c"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = "Kolkata"
        complete_url = base_url + "q=" + city_name + "&appid=" + api_key
        response = requests.get(complete_url)
        weather_data = response.json()
        
        if weather_data.get("cod") != "404":
            try:
                main = weather_data["main"]
                temperature = main["temp"]
                pressure = main["pressure"]
                humidity = main["humidity"]
                weather_description = weather_data["weather"][0]["description"]
                response = (f"Temperature: {temperature}K\n"
                            f"Atmospheric pressure: {pressure} hPa\n"
                            f"Humidity: {humidity}%\n"
                            f"Weather description: {weather_description}")
            except KeyError as e:
                response = f"Key error in weather data: {e}"
        else:
            response = "City not found."

        print(response)
        speak(response)
    else:
        chatgpt_response = chat_with_gpt(command)
        print(chatgpt_response)
        speak(chatgpt_response)

# Function to transcribe speech to text
def transcribe_audio(audio):
    try:
        transcript = recognizer.recognize_google(audio)
        print(f"Transcript: {transcript}")
        return transcript
    except sr.RequestError:
        print("API unavailable")
    except sr.UnknownValueError:
        print("Unable to recognize speech")

# ChatGPT integration
openai.api_key = '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'

def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to handle detected hotword
def detected_callback():
    speak("Yes?")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    command = transcribe_audio(audio)
    if command:
        handle_command(command)

# Load Snowboy model and start detection
model = "your_hotword_model.pmdl"
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print("Listening for hotword...")

# Capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, detector.terminate)

# Start the detector
detector.start(detected_callback)
