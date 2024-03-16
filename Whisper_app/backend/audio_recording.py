import sounddevice as sd
import soundfile as sf
from whisper_integration import transcribe_audio
import tempfile
import threading
import queue

is_recording = False  # Nuevo interruptor para controlar la grabación
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
    global is_recording
    while is_recording:  # Usa is_recording para controlar el bucle
        recording = record_audio()
        audio_file_path = save_temp_audio(recording)
        transcript = transcribe_audio(audio_file_path, model, language)
        transcriptions_queue.put(transcript)

def start_recording(model, language=None):
    global is_recording
    is_recording = True  # Activar la grabación
    thread = threading.Thread(target=recording_and_transcription_thread, args=(model, language, transcriptions_queue))
    thread.daemon = True
    thread.start()
def stop_recording():
    global is_recording
    is_recording = False  # Desactivar la grabación

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

