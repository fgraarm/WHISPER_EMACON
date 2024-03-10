from flask import Flask, request, jsonify, send_from_directory
import werkzeug
from app.whisper_integration import process_audio, process_audio_real_time  # Asegúrate de que esta importación sea correcta basada en tu estructura de carpetas

app = Flask(__name__, static_folder='../frontend/public', static_url_path='')

@app.route('/')
def serve_root():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and werkzeug.utils.secure_filename(file.filename):
        model_name = request.form.get('model', 'base')  # Default model is 'base'
        language = request.form.get('language', '')  # Language could be empty, auto-detection
        transcription = process_audio(file, model_name, language)
        return jsonify({"transcription": transcription})

@app.route('/realtimerecording', methods=['POST'])
def real_time_recording():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        model_name = request.form.get('model', 'base')  # Default model is 'base'
        language = request.form.get('language', '')  # Language could be empty, auto-detection
        transcription = process_audio_real_time(file, model_name, language)
        return jsonify({"transcription": transcription})

if __name__ == '__main__':
    app.run(debug=True)

