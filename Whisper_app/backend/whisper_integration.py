import whisper

def transcribe_audio(file_path, model_name='tiny', language=None):
    """
    Transcribe el archivo de audio al texto utilizando el modelo Whisper especificado.

    :param file_path: Ruta al archivo de audio a transcribir.
    :param model_name: El nombre del modelo Whisper a utilizar (tiny, base, small, medium, large).
    :param language: El idioma del audio, si se conoce.
    :return: Texto transcrito del audio.
    """
    # Cargar el modelo Whisper
    model = whisper.load_model(model_name)
    
    # Configurar opciones de transcripción basadas en si se proporcionó el idioma
    options = {"language": language} if language else {}
    
    # Realizar la transcripción
    result = model.transcribe(file_path, **options)
    
    return result["text"]

if __name__ == "__main__":
    # Este bloque es solo para fines de prueba
    print(transcribe_audio("path/to/your/audio/file.wav", model_name='tiny'))
