from pyannote.audio import Pipeline
import whisper
import soundfile as sf
import librosa
import io
import os
import numpy as np

auth_token = "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"

def pad_or_trim(audio, target_length):
    # Ajusta el tamaño del audio al objetivo especificado.
    length = len(audio)
    if length > target_length:
        audio = audio[:target_length]
    elif length < target_length:
        pad = np.zeros(target_length - length, dtype=audio.dtype)
        audio = np.concatenate((audio, pad))
    return audio

def convert_to_wav(audio_input_path, target_sr=16000):
    # Convierte el archivo de entrada a WAV con la tasa de muestreo objetivo.
    audio, sr = librosa.load(audio_input_path, sr=target_sr)
    temp_wav_path = audio_input_path.rsplit(".", 1)[0] + "_temp.wav"
    sf.write(temp_wav_path, audio.astype(np.float32), target_sr)
    return temp_wav_path

def format_transcription(speaker, start, end, transcript, previous_speakers):
    # Formatea la transcripción según los requisitos.
    speaker_id = speaker.replace("SPEAKER_", "")
    speaker_prefix = f"SPEAKER_{speaker_id}" if speaker_id not in previous_speakers else speaker_id
    formatted_start = "{:.2f}".format(start)
    formatted_end = "{:.2f}".format(end)
    formatted_line = f"{speaker_prefix}: {formatted_start}-{formatted_end} -> {transcript.strip()}"
    previous_speakers.add(speaker_id)
    return formatted_line

def diarize_and_transcribe(audio_input_path, audio_output_path, min_speakers=None, max_speakers=None, model_name="base", language=None):
    # Realiza la diarización y la transcripción del archivo de audio.
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
    
    previous_speakers = set()
    transcription_results_json = []
    for segment, _, speaker in diarization_result.itertracks(yield_label=True):
        start, end = segment.start, segment.end
        audio_segment, sr = librosa.load(converted_audio_path, sr=None, offset=start, duration=(end-start))
        audio_segment = librosa.resample(audio_segment, orig_sr=sr, target_sr=16000).astype(np.float32)

        with io.BytesIO() as audio_buffer:
            sf.write(audio_buffer, audio_segment, 16000, format='WAV')
            audio_buffer.seek(0)
            audio_np, _ = sf.read(audio_buffer, dtype='float32')

            result = model.transcribe(audio_np, **options)
            transcript = result["text"]

            # Aquí aplicamos el formateo necesario antes de agregarlo a los resultados
            speaker_id = speaker.replace("SPEAKER_", "")
            speaker_prefix = speaker_id if speaker_id in previous_speakers else f"SPEAKER_{speaker_id}"
            previous_speakers.add(speaker_id)
            
            formatted_start = "{:.2f}".format(start)
            formatted_end = "{:.2f}".format(end)
           
            transcription_results_json.append({
            "start": formatted_start,
            "end": formatted_end,
            "speaker": speaker_prefix,
            "transcript": transcript
        })
            
    os.remove(converted_audio_path)  # Limpia el archivo temporal

    # En lugar de simplemente imprimir los resultados, los devolvemos para su uso posterior
    return transcription_results_json
