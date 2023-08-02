import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3
import subprocess

import pyaudio
import audioop
import wave

def record_until_silence(output_filename, threshold=1000, chunk_size=1024, sample_format=pyaudio.paInt16, channels=1, rate=44100):
    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    frames = []
    silence_detected = False

    timer = 0
    while not silence_detected:
        data = stream.read(chunk_size)
        rms = audioop.rms(data, 2)  # width=2 for format=paInt16

        if rms < threshold:
            if timer > 100:
                silence_detected = True
            frames.append(data)
        else:
            frames.append(data)
            timer = 0
        timer += 1

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save audio data to .wav file
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def text_to_speech(text, filename):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()

def mp3_to_wav(mp3_path, filename="./audio/output.wav"):
    command = f"ffmpeg -i ./audio/input.mp3 {filename}"
    process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    return filename

def transcribe_audio(audio_file_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text

def listen():
    threshold=1000
    chunk_size=1024
    sample_format=pyaudio.paInt16
    channels=1
    rate=44100
    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    silence_detected = True

    while silence_detected:
        data = stream.read(chunk_size)
        rms = audioop.rms(data, 2)  # width=2 for format=paInt16

        if rms > threshold:
            silence_detected = False
    
    return 


# # Transcribe the audio file
def get_user_input():
    print("listening")
    listen()
    print("Recording, speak now...")
    record_until_silence("./audio/output.wav")
    transcript = transcribe_audio("./audio/output.wav")
    return transcript