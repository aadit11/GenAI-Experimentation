from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
import pyttsx3
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# Set up AzureChatOpenAI

llm = AzureChatOpenAI(
    deployment_name="",
    openai_api_version="",
    openai_api_key="",
    openai_api_base="",
)

def get_text_input():
    user_input = input("Enter your text: ")
    return user_input

def speak(text, save_path="temp.wav"):
    engine = pyttsx3.init()
    engine.save_to_file(text, save_path)
    engine.runAndWait()

def handle_text_input():
    user_input = get_text_input()

    if user_input:
        user_message = HumanMessage(content=user_input)
        response_generator = llm.stream([user_message])

        response_text = ""
        for chunk in response_generator:
            response_text += " " + chunk.content.strip()

        print(response_text)
        if response_text:
            speak(response_text)

def create_video_with_audio(image_path, audio_path, output_path="output_video.mp4"):
    image = ImageClip(image_path, duration=1)  # Duration can be adjusted as needed
    audio = AudioFileClip(audio_path)

    # Set the audio for the image clip
    image = image.set_audio(audio)

    # Write the final video with audio
    image.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)

if __name__ == "__main__":
    handle_text_input()  # Collect text input
    audio_path = "temp.wav"  # Replace with the actual path to your temp audio file
    image_path = "input_image.png"  # Replace with the actual path to your input image
    create_video_with_audio(image_path, audio_path)  # Create the output video
