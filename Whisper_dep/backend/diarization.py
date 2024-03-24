from pyannote.audio import Pipeline
import whisper
import soundfile as sf
import librosa
import io
import os
import numpy as np

auth_token = "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"

def pad_or_trim(audio, target_length):
    length = len(audio)
    if length > target_length:
        audio = audio[:target_length]
    elif length < target_length:
        pad = np.zeros(target_length - length, dtype=audio.dtype)  # Asegúrate de usar el mismo dtype
        audio = np.concatenate((audio, pad))
    return audio

def convert_to_wav(audio_input_path, target_sr=16000):
    audio, sr = librosa.load(audio_input_path, sr=target_sr)
    temp_wav_path = audio_input_path.rsplit(".", 1)[0] + "_temp.wav"
    sf.write(temp_wav_path, audio.astype(np.float32), target_sr)  # Asegúrate de convertir a float32
    return temp_wav_path

def diarize_and_transcribe(audio_input_path, audio_output_path, min_speakers=None, max_speakers=None, model_name="base", language=None):
    converted_audio_path = convert_to_wav(audio_input_path)
    
    try:
        diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=auth_token)
    except Exception as e:
        print(f"Error al cargar el pipeline de diarización: {e}")
        os.remove(converted_audio_path)
        return []
    
    diarization_result = diarization_pipeline({'uri': 'example', 'audio': converted_audio_path}, min_speakers=min_speakers, max_speakers=max_speakers)

    model = whisper.load_model(model_name)
    options = {"language": language} if language else {}
    print(f"Utilizando el modelo Whisper '{model_name}' para la diarización.")
    print(f"Idioma para la transcripción: {'Automático' if not language else language}")
    transcription_results = []

    for segment, _, speaker in diarization_result.itertracks(yield_label=True):
        start, end = segment.start, segment.end
        audio_segment, sr = librosa.load(converted_audio_path, sr=None, offset=start, duration=(end-start))
        audio_segment = librosa.resample(audio_segment, orig_sr=sr, target_sr=16000).astype(np.float32)  # Asegúrate de usar float32 aquí

        with io.BytesIO() as audio_buffer:
            sf.write(audio_buffer, audio_segment, 16000, format='WAV')
            audio_buffer.seek(0)
            audio_np, _ = sf.read(audio_buffer, dtype='float32')  # Asegúrate de leer como float32

            result = model.transcribe(audio_np, **options)
            transcript = result["text"]

            transcription_results.append({
                "speaker": speaker,
                "start": start,
                "end": end,
                "transcript": transcript
            })

    os.remove(converted_audio_path)  # Limpieza del archivo temporal

    if not os.path.exists(audio_output_path):
        os.makedirs(audio_output_path)
    output_file_path = os.path.join(audio_output_path, "transcriptions.txt")
    with open(output_file_path, "w", encoding='utf-8') as output_file:
        for result in transcription_results:
            output_file.write(f"Speaker {result['speaker']}: {result['start']}-{result['end']} -> {result['transcript']}\n")

    print(f"Resultados guardados en {output_file_path}")
    return transcription_results
