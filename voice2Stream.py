import os
import speech_recognition as sr
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
import pyttsx3
import time

# Set up AzureChatOpenAI

llm = AzureChatOpenAI(
    deployment_name="",
    openai_api_version="",
    openai_api_key="",
    openai_api_base="",
)

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        print("You said: " + user_input)
        return user_input
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def speak_word_by_word(text):
    engine = pyttsx3.init()

    #splitting the words
    words = text.split()

    
    for word in words:
        engine.say(word)
        engine.runAndWait()
        time.sleep(0.0001)

def handle_voice_input():
    user_input = recognize_speech()

    if user_input:
        user_message = HumanMessage(content=user_input)
        response_generator = llm.stream([user_message])

        for chunk in response_generator:
            speak_word_by_word(chunk.content.strip())
            print(chunk.content.strip(), end=' ', flush=True)

if __name__ == "__main__":
    handle_voice_input()