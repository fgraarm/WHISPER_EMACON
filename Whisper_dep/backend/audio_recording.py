import sounddevice as sd
import soundfile as sf
from whisper_integration import transcribe_audio
import tempfile
import threading
import queue
import os

audio_files_queue = queue.Queue()
transcriptions_queue = queue.Queue()
is_recording = False

def record_audio_segment(fs=44100, segment_duration=5):
    print("Grabando segmento de audio...")
    recording = sd.rec(int(segment_duration * fs), samplerate=fs, channels=2, dtype='float64')
    sd.wait()
    return recording

def save_temp_audio(recording, fs=44100):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav', dir='uploads')
    sf.write(temp_file.name, recording, fs)
    return temp_file.name

def recording_thread(model, language):
    while is_recording:
        recording = record_audio_segment()
        audio_file_path = save_temp_audio(recording)
        audio_files_queue.put(audio_file_path)

def process_audio_files_thread(model, language):
    while is_recording or not audio_files_queue.empty():
        if not audio_files_queue.empty():
            audio_file_path = audio_files_queue.get()
            transcript = transcribe_audio(audio_file_path, model, language)
            transcriptions_queue.put(transcript)
            os.remove(audio_file_path)

def start_recording(model, language=None):
    global is_recording
    is_recording = True
    threading.Thread(target=recording_thread, args=(model, language), daemon=True).start()
    threading.Thread(target=process_audio_files_thread, args=(model, language), daemon=True).start()
    print(f"Iniciando grabación en tiempo real con el modelo '{model}' y el idioma '{language or 'no especificado'}'...")

def stop_recording():
    global is_recording
    is_recording = False
    print("Grabación finalizada")

def get_next_transcription():
    return transcriptions_queue.get() if not transcriptions_queue.empty() else None