import sounddevice as sd
import soundfile as sf
from whisper_integration import transcribe_audio
import tempfile
import threading
import queue
import os

is_recording = False  # Interruptor para controlar la grabación
audio_files_queue = queue.Queue()  # Cola para guardar rutas de archivos de audio temporales
transcriptions_queue = queue.Queue()  # Cola para guardar las transcripciones acumuladas

def record_audio_segment(fs=44100, segment_duration=60):
    """
    Graba un segmento de audio del micrófono de corta duración.

    :param fs: Frecuencia de muestreo del audio.
    :param segment_duration: Duración de cada segmento de grabación en segundos.
    :return: NumPy array con los datos de audio grabados.
    """
    print(f"Grabando audio por {segment_duration} segundos...")
    recording = sd.rec(int(segment_duration * fs), samplerate=fs, channels=2, dtype='float64')
    sd.wait()  # Esperar hasta que la grabación termine
    return recording

def save_temp_audio(recording, fs=44100):
    """
    Guarda el segmento de audio grabado en un archivo temporal.

    :param recording: NumPy array con los datos de audio.
    :param fs: Frecuencia de muestreo del audio.
    :return: Ruta al archivo de audio temporal.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    sf.write(temp_file.name, recording, fs)
    return temp_file.name

def recording_and_transcription_thread(model, language):
    global is_recording
    while is_recording:
        recording = record_audio_segment(segment_duration=60)  # Grabar segmento
        audio_file_path = save_temp_audio(recording)
        audio_files_queue.put(audio_file_path)  # Añadir archivo a la cola

def process_audio_files_thread(model, language, transcriptions_queue):
    while is_recording or not audio_files_queue.empty():
        if not audio_files_queue.empty():
            audio_file_path = audio_files_queue.get()
            transcript = transcribe_audio(audio_file_path, model, language)
            transcriptions_queue.put(transcript)
            os.remove(audio_file_path)  # Eliminar archivo temporal

def start_recording(model, language=None):
    global is_recording
    is_recording = True
    # Imprimir el modelo y el idioma elegido para la transcripción en tiempo real
    language_msg = language if language else "no especificado"
    print(f"Iniciando grabación en tiempo real con el modelo Whisper '{model}' y el idioma '{language_msg}'...")
    # Hilo para grabar audio y añadirlo a la cola
    recording_thread = threading.Thread(target=recording_and_transcription_thread, args=(model, language))
    recording_thread.daemon = True
    recording_thread.start()
    # Hilo para procesar archivos de audio de la cola
    processing_thread = threading.Thread(target=process_audio_files_thread, args=(model, language, transcriptions_queue))
    processing_thread.daemon = True
    processing_thread.start()

def stop_recording():
    global is_recording
    is_recording = False  # Desactivar la grabación
    print("Grabación finalizada")
def get_next_transcription():
    """
    Obtiene la próxima transcripción de la cola si está disponible.

    :return: El texto transcrito más reciente o None si la cola está vacía.
    """
    return transcriptions_queue.get() if not transcriptions_queue.empty() else None

