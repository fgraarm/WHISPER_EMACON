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
        # Crea un archivo temporal y cierra el descriptor de archivo para permitir su re-apertura en Windows
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        tmpfile.close()
        
        # Exporta el segmento de audio al archivo temporal
        segment.export(tmpfile.name, format="wav")
        
        # Carga y transcribe el audio utilizando la función proporcionada por Whisper
        audio = whisper.load_audio(tmpfile.name)
        result = model.transcribe(audio, language=language if language else None)
        transcriptions.append(result['text'])
        
        # Limpia y elimina el archivo temporal
        os.remove(tmpfile.name)
        
    return " ".join(transcriptions)

def process_audio(file_stream, model_name="base", language=""):
    """Procesa el archivo de audio: segmentación, transcripción y devuelve el texto concatenado."""
    model = load_model(model_name)
    audio_segments = segment_audio(file_stream)
    transcription = transcribe_audio_segments(model, audio_segments, language)
    return transcription
