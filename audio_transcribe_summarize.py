#audio_transcribe_summarize.py

#CPLT71

"""
Basic offline audio transcription and LLM summarization demo for WSL2.
- Records audio from your PC mic (via WSL2)
- Transcribes audio to text using Whisper (offline)
- Summarizes transcript with local LLM (Ollama/Mistral)
"""

# 1. Install dependencies (run these in WSL2 terminal):
# pip install sounddevice scipy openai-whisper requests
# sudo apt-get install -y portaudio19-dev ffmpeg

import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import requests
import os

# --- Check available audio devices ---
def list_audio_devices():
    print("Available audio devices:")
    print(sd.query_devices())
    return sd.query_devices()

# --- Step 1: Record audio from mic ---
def record_audio(filename="output.wav", duration=10, fs=16000):
    print(f"Recording {duration} seconds of audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, recording)
    print(f"Recording saved as {filename}")
    return filename

# --- Step 2: Transcribe with Whisper (offline) ---
def transcribe_audio(filename, model_size="base"):
    print(f"Transcribing {filename} with Whisper ({model_size})...")
    model = whisper.load_model(model_size)
    result = model.transcribe(filename)
    print("Transcript:", result["text"])
    return result["text"]

# --- Step 3: Summarize with local LLM (Ollama/Mistral) ---
def summarize_with_ollama(text, word_count=50):
    prompt = f"Summarize the following in about {word_count} words:\n\n{text}"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt},
        stream=True
    )
    summary = ""
    for line in response.iter_lines():
        if line:
            try:
                import json
                data = json.loads(line.decode("utf-8"))
                summary += data.get("response", "")
            except Exception:
                continue
    print("Summary:", summary)
    return summary
#audio_transcribe_summarize.py
#CPLT73
if __name__ == "__main__":
    # Check available audio devices
    devices = list_audio_devices()
    
    # Check if we have any audio devices
    if len(devices) == 0:
        print("No audio devices found. This is common in WSL2.")
        print("Options:")
        print("1. Use an existing audio file")
        print("2. Record audio on Windows and copy to WSL")
        print("3. Use WSL2 with audio support (requires additional setup)")
        
        # For demonstration, let's check if there's an existing audio file
        test_files = ["test.wav", "sample.wav", "audio.wav", "recording.wav"]
        found_file = None
        for file in test_files:
            if os.path.exists(file):
                found_file = file
                break
        
        if found_file:
            print(f"Found existing audio file: {found_file}")
            transcript = transcribe_audio(found_file)
            summarize_with_ollama(transcript, word_count=50)
        else:
            print("No existing audio files found. Please:")
            print("1. Record audio on Windows and save as 'test.wav' in this directory, or")
            print("2. Set up WSL2 with audio support")
            print("\nFor WSL2 audio setup, you need:")
            print("- WSL2 with GUI support")
            print("- PulseAudio or ALSA configuration")
            print("- Windows audio forwarding to WSL2")
    else:
        # Record audio if devices are available
        wav_file = record_audio(duration=10)
        # Transcribe
        transcript = transcribe_audio(wav_file)
        # Summarize
        summarize_with_ollama(transcript, word_count=50)
