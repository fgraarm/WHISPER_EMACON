from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from whisper_integration import transcribe_audio
from audio_recording import start_recording, get_next_transcription, stop_recording  # Asegúrate de importar stop_recording
from transformers import pipeline
import os

# Inicializa la pipeline de traducción
translators = {
    'en-es': pipeline("translation", model="Helsinki-NLP/opus-mt-en-es"),
    'ru-es': pipeline("translation", model="Helsinki-NLP/opus-mt-ru-es"),
    'fr-es': pipeline("translation", model="Helsinki-NLP/opus-mt-fr-es"),
    'es-en': pipeline("translation", model="Helsinki-NLP/opus-mt-es-en"),
    'es-ru': pipeline("translation", model="Helsinki-NLP/opus-mt-es-ru"),
    'es-fr': pipeline("translation", model="Helsinki-NLP/opus-mt-es-fr"),
    'fr-en': pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en"),
    'en-ru': pipeline("translation", model="Helsinki-NLP/opus-mt-en-ru"),
    'ru-en': pipeline("translation", model="Helsinki-NLP/opus-mt-ru-en"),
    'fr-ru': pipeline("translation", model="Helsinki-NLP/opus-mt-fr-ru")
}

# Definir la ruta al directorio frontend
frontend_dir = os.path.abspath("../frontend")

app = Flask(__name__, static_folder=frontend_dir, template_folder=frontend_dir)

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

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Endpoint para transcribir archivos de audio."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    model = request.form.get('model', 'tiny')
    language = request.form.get('language', None)
    includeTimestamps = 'includeTimestamps' in request.form and request.form['includeTimestamps'] == 'true'
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        uploads_dir = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        filename = os.path.join(uploads_dir, secure_filename(file.filename))
        file.save(filename)
        
        # Llamada a la función de transcripción
        transcript = transcribe_audio(filename, model, language, includeTimestamps)
        
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
    app.run(debug=True, port=5000)
