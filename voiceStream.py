# In[1]:
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
import os
from datetime import datetime
import azure.cognitiveservices.speech as speechsdk
import openai


# In[1]:
openai_api_key = os.environ['OPENAI_API_KEY'] 

def process_text_for_safety(text):
    safe_text = process_text_for_safety(text)
    print(safe_text, end=' ', flush=True)


llm = AzureChatOpenAI(
    deployment_name="",
    openai_api_version="",
    openai_api_key=openai_api_key,
    openai_api_base="",
)


# In[1]:
print(datetime.now())
def handle_input(question):

    user_message = HumanMessage(content=question)
    response_generator = llm.stream([user_message])

    
    for chunk in response_generator:
        print(chunk.content, end='', flush=True)


print(datetime.now())  
handle_input("Give me an explanation on football in 250 words")
print(datetime.now())


# In[1]:

AZURE_SPEECH_KEY = " "
AZURE_SPEECH_REGION = " "

speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY , region=AZURE_SPEECH_REGION)
speech_config.speech_recognition_language = "en-US"

audio_config = speechsdk.audio.Audioconfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config , audio_config=audio_config)

print("Speak now......")
speech_recognition_result = speech_recognizer.recognize_once_async().get()
output  = speech_recognition_result.text

response = openai.Completion.create(prompt=output , engine=llm.deployment_name)
output = response.choices[0].text

audio_config = speechsdk.audio.AudioOutputconfig(use_default_speaker=True)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config , audio_config=audio_config)

speech_sysnthesis_result = speech_synthesizer.speak_text_async(output).get()