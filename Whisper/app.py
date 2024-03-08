from pydub import AudioSegment
from flask import Flask, request, jsonify, render_template, current_app
import whisper
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Directorio temporal para guardar archivos cargados
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegúrate de que el directorio existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Cargar el modelo de Whisper de forma global para eficiencia
modelo_whisper = whisper.load_model("base")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Segmentar y procesar el audio
    audio = AudioSegment.from_file(file_path)
    segment_duration_ms = 30 * 1000  # 30 segundos en milisegundos
    full_transcription = ""

    for i in range(0, len(audio), segment_duration_ms):
        segment = audio[i:i+segment_duration_ms]
        segment_file_path = f"{file_path}_segment_{i//segment_duration_ms}.wav"
        segment.export(segment_file_path, format="wav")
        
        segment_audio = whisper.load_audio(segment_file_path)
        segment_audio = whisper.pad_or_trim(segment_audio)
        result = modelo_whisper.transcribe(segment_audio)
        full_transcription += " " + result["text"]

        # Opcional: eliminar el archivo de segmento después de transcribirlo
        os.remove(segment_file_path)

    # Opcional: eliminar el archivo original después de procesarlo
    os.remove(file_path)

    return jsonify({"text": full_transcription.strip()})

@app.route('/transcribe_realtime', methods=['POST'])
def transcribe_realtime():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        segment_audio = whisper.load_audio(file_path)
        segment_audio = whisper.pad_or_trim(segment_audio)
        result = modelo_whisper.transcribe(segment_audio)
        
        os.remove(file_path)  # Eliminar el archivo de segmento después de transcribirlo
        
        return jsonify({"text": result["text"]})
    else:
        return "No file received", 400

if __name__ == '__main__':
    app.run(debug=True)

