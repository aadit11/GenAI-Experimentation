from gtts import gTTS
from moviepy.editor import AudioFileClip, concatenate_videoclips, CompositeVideoClip, ImageClip
import matplotlib.pyplot as plt
import os

# Parameters
text_to_speak = """Hello my name is Aadit. I am a final year student. I am studying Computer Science"""
words_per_slide = 10
output_video_filename = 'text_slide_video.mp4'
output_audio_filename = 'text_slide_audio.mp3'
background_image = 'input_image1.png'  # Path to your background image

def text_to_audio_and_frames(text, words_per_slide):
    tts = gTTS(text)
    tts.save(output_audio_filename)
    audio = AudioFileClip(output_audio_filename)

    words = text.split()
    number_of_slides = len(words) // words_per_slide + (len(words) % words_per_slide > 0)
    clips = []
    durations = []

    for i in range(number_of_slides):
        slide_text = ' '.join(words[i*words_per_slide:(i+1)*words_per_slide])
        fig, ax = plt.subplots()
        plt.text(0.5, 0.5, slide_text, fontsize=12, ha='center')
        plt.axis('off')
        plt.savefig(f'slide_{i}.png')
        plt.close(fig)

        start_time = i * (audio.duration / number_of_slides)
        end_time = (i + 1) * (audio.duration / number_of_slides)
        duration = end_time - start_time
        durations.append(duration)
        
        # Create a moviepy ImageClip
        frame_clip = ImageClip(f'slide_{i}.png').set_duration(duration)
        clips.append(frame_clip)

    return concatenate_videoclips(clips), audio, durations

def create_video_with_audio(frames, audio, durations):
    for i, clip in enumerate(frames.clips):
        clip.duration = durations[i]
    
    bg_clip = ImageClip(background_image).resize(frames.size).set_duration(frames.duration)  # Resize background image to fit the frame
    
    final_video = CompositeVideoClip([bg_clip] + frames.clips)
    
    final_video = final_video.set_audio(audio)
    
    final_video.write_videofile(output_video_filename, fps=24)  # Adjust fps if needed

frames, audio, durations = text_to_audio_and_frames(text_to_speak, words_per_slide)
create_video_with_audio(frames, audio, durations)

for i in range(len(frames.clips)):
    os.remove(f"slide_{i}.png")

os.remove(output_audio_filename)

print(f"Video created: {output_video_filename}")
