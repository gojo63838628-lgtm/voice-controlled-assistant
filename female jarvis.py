import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import pyjokes
from datetime import datetime
import subprocess
import os
import random

def speak(text):
    print(f"JARVIS: {text}")
    tts = gTTS(text=text, lang='en')
    filename = f"voice_{random.randint(1,100000)}.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Speech service is unavailable.")
            return ""
        except sr.WaitTimeoutError:
            speak("No command detected.")
            return ""

def open_youtube():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    try:
        subprocess.Popen([edge_path, "https://www.youtube.com"])
        speak("Opening YouTube now.")
    except Exception as e:
        speak("Failed to open YouTube.")
        print(e)

def handle_command(command):
    if any(phrase in command for phrase in ["time", "what's the time", "tell me the time"]):
        current_time = datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {current_time}")

    elif "joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "open youtube" in command:
        open_youtube()

    elif "exit" in command or "quit" in command or "goodbye" in command:
        speak("Goodbye, Harshit!")
        return False

    else:
        speak("I'm not sure how to respond to that yet.")
    return True

def jarvis():
    speak("Hello Harshit, I am your assistant.")
    active = True
    while active:
        command = listen()
        if command:
            active = handle_command(command)

jarvis()