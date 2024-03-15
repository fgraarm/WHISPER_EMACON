import sounddevice as sd
import soundfile as sf
import numpy as np
from whisper_integration import transcribe_audio
import tempfile
import threading
import queue

# Cola para guardar las transcripciones acumuladas
transcriptions_queue = queue.Queue()

def record_audio(duration=20, fs=44100):
    """
    Graba un segmento de audio del micrófono.

    :param duration: Duración de la grabación en segundos.
    :param fs: Frecuencia de muestreo del audio.
    :return: NumPy array con los datos de audio grabados.
    """
    print(f"Grabando audio por {duration} segundos...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
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

def recording_and_transcription_thread(model, language, transcriptions_queue):
    """
    Función que se ejecutará en un hilo separado para grabar y transcribir audio.
    
    :param model: Modelo de Whisper a utilizar para la transcripción.
    :param language: Idioma del audio, si se conoce.
    :param transcriptions_queue: Cola para poner las transcripciones.
    """
    while True:
        recording = record_audio()
        audio_file_path = save_temp_audio(recording)
        transcript = transcribe_audio(audio_file_path, model, language)
        transcriptions_queue.put(transcript)

def start_recording(model, language=None):
    """
    Inicia el proceso de grabación de audio y transcripción en intervalos.

    :param model: Modelo de Whisper a utilizar para la transcripción.
    :param language: Idioma del audio, si se conoce.
    """
    # Iniciar la grabación y transcripción en un hilo separado
    thread = threading.Thread(target=recording_and_transcription_thread, args=(model, language, transcriptions_queue))
    thread.daemon = True  # Esto asegura que el hilo se cierre cuando el programa principal finalice
    thread.start()

def get_next_transcription():
    """
    Obtiene la próxima transcripción de la cola si está disponible.

    :return: El texto transcrito más reciente o None si la cola está vacía.
    """
    return transcriptions_queue.get() if not transcriptions_queue.empty() else None

if __name__ == "__main__":
    # Esto es solo para fines de demostración
    print("Iniciando la grabación y transcripción de prueba...")
    start_recording('tiny')

