# whisper_translation.py
import whisper

def translate_to_english(file_path, model_name='base', source_language=None):
    """
    Traduce el contenido de un archivo de audio al inglés usando Whisper.

    :param file_path: Ruta al archivo de audio a traducir.
    :param model_name: Modelo de Whisper a utilizar para la traducción.
    :return: Texto traducido al inglés.
    """
    print(f"Traduciendo al inglés con el modelo Whisper '{model_name}' y el idioma de origen '{source_language or 'auto-detected'}'...")
    
    # Cargar el modelo Whisper
    model = whisper.load_model(model_name)
    
    # Configurar opciones de traducción
    options = {"task": "translate"}
    if source_language:
        options["language"] = source_language
    # Realizar la traducción
    result = model.transcribe(file_path, **options)
    print("Traducción con Whisper finalizada")
    
    return result["text"]
