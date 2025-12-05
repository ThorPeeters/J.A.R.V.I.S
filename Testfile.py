import pyttsx3

engine = pyttsx3.init()
def list_voices():
    voices = engine.getProperty('voices')
    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name} | ID: {voice.id}")
list_voices()