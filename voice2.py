import os
import speech_recognition as sr
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
import pyttsx3

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

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def handle_voice_input():
    user_input = recognize_speech()

    if user_input:
        user_message = HumanMessage(content=user_input)
        response_generator = llm.stream([user_message])

        response_text = ""
        for chunk in response_generator:
            response_text += " " + chunk.content.strip()

        print(response_text)
        if response_text:
            speak(response_text)


if __name__ == "__main__":
    handle_voice_input()
