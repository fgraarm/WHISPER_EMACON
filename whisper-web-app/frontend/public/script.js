let mediaRecorder;
let isRecording = false;

function showProcessingState(message) {
    document.getElementById('status').innerText = message;
}

function processAudioSegment(audioBlob) {
    const formData = new FormData();
    formData.append('file', audioBlob);
    formData.append('model', document.getElementById('model-select').value);
    formData.append('language', document.getElementById('language-input').value);

    fetch('/realtimerecording', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('transcription').innerText += data.transcription + " ";
    })
    .catch(error => {
        console.error('Error:', error);
        showProcessingState('Error al procesar la grabación en tiempo real.');
    });
}

document.getElementById('upload-button').addEventListener('click', function() {
    const audioFile = document.getElementById('audio-file').files[0];
    if (!audioFile) {
        showProcessingState('Por favor, selecciona un archivo de audio.');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', audioFile);
    formData.append('model', document.getElementById('model-select').value);
    formData.append('language', document.getElementById('language-input').value);
    
    showProcessingState('Cargando y procesando audio...');
    
    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        showProcessingState('Transcripción completada.');
        document.getElementById('transcription').innerText = data.transcription;
    })
    .catch(error => {
        console.error('Error:', error);
        showProcessingState('Error al procesar el audio.');
    });
});

document.getElementById('record-button').addEventListener('click', function() {
    if (isRecording) {
        return; // Prevent starting a new recording if already recording
    }
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            isRecording = true;
            showProcessingState('Grabando...');
            
            mediaRecorder.addEventListener('dataavailable', event => {
                if (event.data.size > 0 && isRecording) {
                    processAudioSegment(event.data);
                }
            });

            mediaRecorder.start(15000); // Start recording, and generate audio chunks every 15 seconds
            
            document.getElementById('stop-button').disabled = false;
        })
        .catch(error => {
            console.error("Error accessing the microphone", error);
            showProcessingState('Error al acceder al micrófono.');
        });
});

document.getElementById('stop-button').addEventListener('click', function() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        isRecording = false;
        document.getElementById('stop-button').disabled = true;
        showProcessingState('Deteniendo grabación...');
    }
});
