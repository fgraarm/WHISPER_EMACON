import whisper
from pydub import AudioSegment
import tempfile
import os

def load_model(model_name="base"):
    """Carga el modelo de Whisper especificado."""
    model = whisper.load_model(model_name)
    return model

def segment_audio(audio_file, segment_duration=30000):
    """Segmenta el archivo de audio en bloques de duración especificada (en milisegundos)."""
    sound = AudioSegment.from_file(audio_file)
    length = len(sound)
    return [sound[i:i + segment_duration] for i in range(0, length, segment_duration)]

def transcribe_audio_segments(model, audio_segments, language=""):
    """Transcribe los segmentos de audio utilizando Whisper."""
    transcriptions = []
    for segment in audio_segments:
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        tmpfile.close()
        segment.export(tmpfile.name, format="wav")
        audio = whisper.load_audio(tmpfile.name)
        result = model.transcribe(audio, language=language if language else None)
        transcriptions.append(result['text'])
        os.remove(tmpfile.name)
    return " ".join(transcriptions)

def process_audio(file_stream, model_name="base", language=""):
    """Procesa el archivo de audio: segmentación, transcripción y devuelve el texto concatenado."""
    model = load_model(model_name)
    audio_segments = segment_audio(file_stream)
    transcription = transcribe_audio_segments(model, audio_segments, language)
    return transcription

def transcribe_audio_real_time(model, audio_file, language=""):
    """Transcribe el audio en tiempo real sin segmentación."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile:
            audio_file.save(tmpfile.name)
            # Asegúrate de que el puntero de lectura esté posicionado al principio del archivo
            tmpfile.seek(0)
            audio = whisper.load_audio(tmpfile.name)
            result = model.transcribe(audio, language=language if language else None)
            return result['text']
    except Exception as e:
        # Maneja cualquier excepción que pueda ocurrir
        print(f"Error al transcribir audio en tiempo real: {e}")
        return None

def process_audio_real_time(file_stream, model_name="base", language=""):
    """Procesa el archivo de audio en tiempo real sin segmentación."""
    model = load_model(model_name)
    transcription = transcribe_audio_real_time(model, file_stream, language)
    return transcription
