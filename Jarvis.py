import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import json
import os
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        recognizer.pause_threshold = 1.5
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return ""

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)
    speak(f"I will remember that your {key.replace('_', ' ')} is {value}.")

def recall(key):
    memory = load_memory()
    return memory.get(key, None)

#client = OpenAI(api_key = "ADD API KEY HERE")

def chat_with_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("GPT Error:", e)
        return "Sorry, I had trouble thinking about that."


def run_jarvis():
    speak("Hello, I am JARVIS. How can I help you?")
    while True:
        command = listen()
        if 'time' in command:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {now}")

        elif 'open google' in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif 'open notes' in command:
            speak("Opening Notes")
            os.system("open -a Notes")

        elif 'remember that my name is' in command:
            name = command.split("remember that my name is")[-1].strip()
            remember("name", name)
        elif 'what is my name' in command:
            name = recall("name")
            if name:
                speak(f"Your name is {name}.")
            else:
                speak("I don't know your name yet.")
        elif 'remember that my favorite color is' in command:
            color = command.split("remember that my favorite color is")[-1].strip()
            remember("favorite_color", color)
        elif 'what is my favorite color' in command:
            color = recall("favorite_color")
            if color:
                speak(f"Your favorite color is {color}.")
            else:
                speak("I don't know your favorite color yet.")

        elif 'stop' in command or 'goodbye' in command:
            speak("Goodbye, sir.")
            break
        else:
            response = chat_with_gpt(command)
            speak(response)


# Run the assistant
run_jarvis()
