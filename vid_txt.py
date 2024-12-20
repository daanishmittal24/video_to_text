import streamlit as st
import moviepy.editor as mp
import os
import speech_recognition as sr
import re

st.title("Video to Text Converter")

uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "mkv", "avi", "mov"])

audio_folder = "audio"
transcribed_text_path = os.path.join(audio_folder, "transcribed_text.txt")

os.makedirs(audio_folder, exist_ok=True)

def sanitize_filename(filename):
    sanitized = filename.replace(" ", "_")
    return sanitized

def extract_audio(video_file):
    video_clip = None
    try:
        video_path = os.path.join(audio_folder, sanitize_filename(video_file.name))
        with open(video_path, "wb") as f:
            f.write(video_file.getbuffer())
        video_clip = mp.VideoFileClip(video_path)
        audio_filename = sanitize_filename(f"{os.path.splitext(video_file.name)[0]}.wav")
        audio_path = os.path.join(audio_folder, audio_filename)
        video_clip.audio.write_audiofile(audio_path)
        video_clip.close()
        return audio_path
    except Exception as e:
        if video_clip:
            video_clip.close()
        st.error(f"Error extracting audio: {e}")
        return None

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
        return ""

if uploaded_video:
    st.write("Processing video...")

    with st.spinner("Extracting audio and transcribing..."):
        audio_path = extract_audio(uploaded_video)

        if audio_path:
            text = transcribe_audio(audio_path)

            if text:
                st.success("Audio transcribed successfully!")
                st.subheader("Transcribed Text")
                st.write(text)

                text += "\n\nMade with ❤️ by Daanish Mittal"

                with open(transcribed_text_path, "w", encoding="utf-8") as file:
                    file.write(text)

                with open(transcribed_text_path, "r", encoding="utf-8") as text_file:
                    st.download_button(
                        label="Download Transcribed Text",
                        data=text_file,
                        file_name="transcribed_text.txt",
                        mime="text/plain"
                    )

            if os.path.exists(audio_path):
                os.remove(audio_path)
            if os.path.exists(os.path.join(audio_folder, sanitize_filename(uploaded_video.name))):
                os.remove(os.path.join(audio_folder, sanitize_filename(uploaded_video.name)))

st.markdown(
    """
    <br><br>
    <h5 style='text-align: center;'>Made with ❤️ by <a href='https://github.com/daanishmittal24' target='_blank'>Daanish Mittal</a></h5>
    """, unsafe_allow_html=True
)

