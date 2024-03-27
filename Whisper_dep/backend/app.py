from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from whisper_integration import transcribe_audio
from audio_recording import start_recording, get_next_transcription, stop_recording  # Asegúrate de importar stop_recording
from transformers import pipeline
import os
import logging
import sys
from diarization import diarize_and_transcribe  # Asegúrate de importar la función correctamente


# Inicializa la pipeline de traducción
translators = {
    'ru-es': pipeline("translation", model="Helsinki-NLP/opus-mt-ru-es"),
    'fr-es': pipeline("translation", model="Helsinki-NLP/opus-mt-fr-es"),
    'en-es': pipeline("translation", model="Helsinki-NLP/opus-mt-en-es"),
    'de-es': pipeline("translation", model="Helsinki-NLP/opus-mt-de-es"),
    'it-es': pipeline("translation", model="Helsinki-NLP/opus-mt-it-es"),
    'ja-es': pipeline("translation", model="Helsinki-NLP/opus-mt-ja-es"),
    'pl-es': pipeline("translation", model="Helsinki-NLP/opus-mt-pl-es"),
    'ru-en': pipeline("translation", model="Helsinki-NLP/opus-mt-ru-en"),
    'zh-en': pipeline("translation", model="Helsinki-NLP/opus-mt-zh-en"),
    'fr-en': pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en"),
    'de-en': pipeline("translation", model="Helsinki-NLP/opus-mt-de-en"),
    'it-en': pipeline("translation", model="Helsinki-NLP/opus-mt-it-en"),
    'ja-en': pipeline("translation", model="Helsinki-NLP/opus-mt-ja-en"),
    'pl-en': pipeline("translation", model="Helsinki-NLP/opus-mt-pl-en"),
    'ar-en': pipeline("translation", model="Helsinki-NLP/opus-mt-ar-en"),
    'ar-es': pipeline("translation", model="Helsinki-NLP/opus-mt-ar-es"),


}

# Definir la ruta al directorio frontend
frontend_dir = os.path.abspath("../frontend")
basedir = os.path.abspath(os.path.dirname(__file__))

# Verifica si la aplicación se está ejecutando como un ejecutable de PyInstaller
if getattr(sys, 'frozen', False):
    # Si es así, utiliza la carpeta temporal establecida por PyInstaller
    template_folder = os.path.join(sys._MEIPASS, 'frontend/templates')
    static_folder = os.path.join(sys._MEIPASS, 'frontend/static')
else:
    # De lo contrario, utiliza las rutas normales
    frontend_dir = os.path.abspath("../frontend")
    template_folder = os.path.join(frontend_dir, 'templates')
    static_folder = os.path.join(frontend_dir, 'static')
app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
app_logs = []  # Esta lista almacenará los logs

class MemoryHandler(logging.Handler):
    def emit(self, record):
        # Aquí es donde añadimos el mensaje de log a la lista app_logs
        app_logs.append(self.format(record))

# Configuramos el nivel de log a DEBUG para capturar todos los mensajes
app.logger.setLevel(logging.DEBUG)

# Creamos un manejador que usa nuestra clase MemoryHandler
memory_handler = MemoryHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
memory_handler.setFormatter(formatter)

# Añadimos nuestro manejador de memoria al logger de la aplicación y al logger de werkzeug
app.logger.addHandler(memory_handler)
logging.getLogger('werkzeug').addHandler(memory_handler)

@app.route('/logs')
def logs():
    """Ruta para servir la página de logs."""
    return render_template('logs.html')

@app.route('/get_logs', methods=['GET'])
def get_logs():
    """Endpoint para obtener los logs acumulados."""
    return jsonify({"logs": app_logs})

@app.route('/diarize', methods=['POST'])
def diarize():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Aquí asumo que ya tienes un directorio de 'uploads' donde guardas los archivos
    
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)  # Crea la carpeta si no existe
    file_path = os.path.join(uploads_dir, file.filename)
    file.save(file_path)

    # Definir valores para los argumentos faltantes
    # Cambia esto por tu directorio de salida real
    audio_output_path = os.path.join(os.path.dirname(__file__), "../backend/output")
  # Cambia esto por tu directorio de salida real
    os.makedirs(audio_output_path, exist_ok=True)
    min_diarization_speakers = int(request.form.get('min_diarization_speakers', '2'))  # Establece esto según tus necesidades
    max_diarization_speakers = int(request.form.get('max_diarization_speakers', '5'))  # Establece esto según tus necesidades
    model = request.form.get('model', 'base')
    language = request.form.get('language', None)

    # Llamar a la función diarization con todos los argumentos necesarios
   

    formatted_results = diarize_and_transcribe(file_path, audio_output_path, min_diarization_speakers, max_diarization_speakers, model, language)

    # Haz lo que necesites con los resultados
    # Por ejemplo, devolver los resultados de la diarización
    return jsonify({"diarization": formatted_results})

    
@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    source_text = data['text']
    source_lang = data.get('source_lang', 'en')  # Idioma de origen, por defecto 'en'
    target_lang = data.get('target_lang', 'es')  # Idioma de destino, por defecto 'es'
    translator_key = f'{source_lang}-{target_lang}'
    translator = translators.get(translator_key, None)
    if not translator:
        return jsonify({"error": "No se encontró un modelo de traducción para el par de idiomas especificado."}), 400
    # Divide el texto en segmentos más pequeños
    segment_size = 400  # Ajusta este valor según sea necesario
    segments = [source_text[i:i+segment_size] for i in range(0, len(source_text), segment_size)]
    
    translated_segments = []
    for segment in segments:
        try:
            # Traduce cada segmento
            translation = translator(segment, src_lang=source_lang, tgt_lang=target_lang, truncation=True)[0]['translation_text']
            translated_segments.append(translation)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Combina todas las traducciones de segmentos en una respuesta
    full_translation = " ".join(translated_segments)
    return jsonify({"translation": full_translation})

@app.route('/')
def index():
    """Ruta para servir la página de inicio."""
    return render_template('index.html')

@app.route('/acerca-de')
def acerca_de():
    return render_template('acercade.html')

@app.route('/uso-herramienta')
def uso_herramienta():
    return render_template('usoherramienta.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Endpoint para transcribir archivos de audio."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    # Obtén el modelo, el idioma y la opción de salida desde el formulario
    model = request.form.get('model', 'tiny')
    language = request.form.get('language', None)
    output_option = request.form.get('outputOption', 'none')

    # Define la variable includeTimestamps basada en la opción de salida
    includeTimestamps = (output_option == 'timestamps')

    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    filename = os.path.join(uploads_dir, secure_filename(file.filename))
    file.save(filename)

    # Si la opción es diarización, llama a diarize_audio
    if output_option == 'diarization':
        speakers = diarize_and_transcribe(filename)
        os.remove(filename)  # Asegúrate de eliminar el archivo después de procesarlo
        return jsonify({"diarization": speakers})
    else:
        # Para otras opciones, incluyendo timestamps o ninguna, llama a transcribe_audio
        transcript = transcribe_audio(filename, model, language, includeTimestamps)
        os.remove(filename)  # Asegúrate de eliminar el archivo después de procesarlo
        return jsonify({"transcript": transcript})
 

@app.route('/record', methods=['POST'])
def record():
    """Endpoint para grabar y transcribir audio en tiempo real."""
    data = request.get_json()  # Obtiene los datos enviados como JSON
    model = data.get('model', 'tiny')
    language = data.get('language', None)
    
    start_recording(model, language)
    return jsonify({"message": "Recording started"}), 200


def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/get_transcription', methods=['GET'])
def get_transcription():
    """Endpoint para obtener la transcripción acumulada."""
    transcript = get_next_transcription()
    if transcript:
       return jsonify({"transcript": transcript})
    else:
       return jsonify({"message": "No new transcription available"}), 204

@app.route('/stop_record', methods=['POST'])
def stop_record():
    stop_recording()
    return jsonify({"message": "Recording stopped"}), 200

# Servir archivos estáticos para cualquier ruta no capturada por las rutas anteriores
@app.route('/<path:path>')
def static_proxy(path):
    """Servir archivos estáticos."""
    return send_from_directory(frontend_dir, path)

if __name__ == '__main__':
    print("Bienvenido(a) a la aplicación. Abra su navegador y acceda a http://127.0.0.1:5000")
    app.run(debug=False, host='127.0.0.1' , port=5000)

