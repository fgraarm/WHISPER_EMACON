let mediaRecorder;
let audioChunks = [];

function showProcessingState(message) {
    document.getElementById('status').innerText = message;
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
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            showProcessingState('Grabando...');
            
            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });
            
            mediaRecorder.addEventListener('stop', () => {
                showProcessingState('Procesando grabación...');
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('file', audioBlob, 'recording.wav');
                formData.append('model', document.getElementById('model-select').value);
                formData.append('language', document.getElementById('language-input').value);
                
                fetch('/upload', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    showProcessingState('Transcripción de la grabación completada.');
                    document.getElementById('transcription').innerText = data.transcription;
                })
                .catch(error => {
                    console.error('Error:', error);
                    showProcessingState('Error al procesar la grabación.');
                });
            });
            
            mediaRecorder.start();
            document.getElementById('stop-button').disabled = false;
        })
        .catch(error => {
            console.error("Error accessing the microphone", error);
            showProcessingState('Error al acceder al micrófono.');
        });
});

document.getElementById('stop-button').addEventListener('click', function() {
    mediaRecorder.stop();
    document.getElementById('stop-button').disabled = true;
    showProcessingState('Deteniendo grabación...');
});

// Agrega un listener para el nuevo botón de detener procesamiento
document.getElementById('stop-processing-button').addEventListener('click', function() {
    // Detiene la grabación si está en curso
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
    }
    
    // Detiene el procesamiento de la transcripción si está en curso
    showProcessingState('Procesamiento detenido.');
});


