from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from whisper_integration import transcribe_audio
from audio_recording import start_recording, get_next_transcription
import os

# Definir la ruta al directorio frontend
frontend_dir = os.path.abspath("../frontend")

app = Flask(__name__, static_folder=frontend_dir, template_folder=frontend_dir)

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
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        uploads_dir = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        filename = os.path.join('uploads', secure_filename(file.filename))
        file.save(filename)
        
        # Llamada a la función de transcripción
        transcript = transcribe_audio(filename, model, language)
        
        return jsonify({"transcript": transcript})

@app.route('/record', methods=['POST'])
def record():
    """Endpoint para grabar y transcribir audio en tiempo real."""
    model = request.form.get('model', 'tiny')
    language = request.form.get('language', None)
    
    # Iniciar la grabación y obtener la transcripción
    transcript = start_recording(model, language)
    
    return jsonify({"transcript": transcript})

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/get_transcription', methods=['GET'])
def get_transcription():
    """Endpoint para obtener la transcripción acumulada."""
    transcript = get_next_transcription()
    return jsonify({"transcript": transcript})

# Servir archivos estáticos para cualquier ruta no capturada por las rutas anteriores
@app.route('/<path:path>')
def static_proxy(path):
    """Servir archivos estáticos."""
    return send_from_directory(frontend_dir, path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
