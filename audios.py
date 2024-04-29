import keyboard
import pyaudio
from faster_whisper import WhisperModel
import wave
import time
import pyttsx3
import os


audio_save_path = './audios/audio.wav'


def listen(audio_save_path = audio_save_path):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    frames = []
    print("Listening... Press space to stop")
    while not keyboard.is_pressed('space'):
        data = stream.read(1024)
        frames.append(data)
    
    print('Stopping...')
        
    start = time.time()
    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(audio_save_path, 'wb') as sound_file:
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(16000)
        sound_file.writeframes(b''.join(frames))
    end = time.time()
    # print("Speech to audio file in: ", end-start)



def transcribe(audio_file_path = audio_save_path):
    model = WhisperModel("tiny.en")

    start = time.time()
    segments, _ = model.transcribe(audio_file_path, beam_size=5, word_timestamps=True)
    transcribed_text = ''.join(segment.text for segment in segments)
    end = time.time()
    # print("Audio Transcribed in: ", end-start)
    os.remove(audio_file_path)
    print(transcribed_text)
    return transcribed_text


def speak(transcribed_text):
    
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty(rate, 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
                
    start = time.time()
    print("Model: ", transcribed_text)
    engine.say(transcribed_text)
    engine.runAndWait()
    end = time.time()
    
    # print("Text to speech in: ", end-start)

