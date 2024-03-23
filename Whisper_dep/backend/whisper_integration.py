import whisper

def transcribe_audio(file_path, model_name='tiny', language=None, includeTimestamps=False):
    """
    Transcribe el archivo de audio al texto utilizando el modelo Whisper especificado.

    :param file_path: Ruta al archivo de audio a transcribir.
    :param model_name: El nombre del modelo Whisper a utilizar (tiny, base, small, medium, large).
    :param language: El idioma del audio, si se conoce.
    :return: Texto transcrito del audio.
    """
    language_msg = language if language else "no especificado"
    print(f"Transcribiendo con el modelo Whisper '{model_name}' y el idioma '{language_msg}'...")
    
    # Cargar el modelo Whisper
    model = whisper.load_model(model_name)
    
    # Configurar opciones de transcripción basadas en si se proporcionó el idioma
    options = {"language": language} if language else {}
    
    # Realizar la transcripción
    result = model.transcribe(file_path, **options)
    print("Transcripción con Whisper finalizada")
    if includeTimestamps:
        # Procesar la salida para incluir timestamps
        # La siguiente es una forma simplificada y necesitarás ajustarla según tus necesidades específicas
        segments = result['segments']
        transcript_with_timestamps = ""
        for segment in segments:
            start = segment['start']
            end = segment['end']
            text = segment['text']
            transcript_with_timestamps += f"[{start}-{end}] {text}\n"
        return transcript_with_timestamps
    else:
        # Devolver solo el texto transcrito si no se solicitan timestamps
        return result["text"]


