function setLoading(isLoading) {
    document.getElementById('loading').style.display = isLoading ? 'block' : 'none';
}

// Función para actualizar el estado de los botones de grabación y detener
function toggleRecordingButtons(isRecording) {
    document.getElementById('record-btn').style.display = isRecording ? 'none' : 'block';
    document.getElementById('stop-btn').style.display = isRecording ? 'block' : 'none';
}

document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    setLoading(true); // Mostrar GIF de carga
    const formData = new FormData();
    formData.append('file', document.getElementById('audio-file').files[0]);
    formData.append('model', document.getElementById('model-select').value);
    formData.append('language', document.getElementById('language-input').value);

    fetch('/transcribe', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        setLoading(false); // Ocultar GIF de carga
        document.getElementById('transcription-result').textContent = data.transcript;
    })
    .catch(error => {
        setLoading(false); // Ocultar GIF de carga en caso de error
        console.error('Error:', error);
    });
});

let recordingInterval;

document.getElementById('record-btn').addEventListener('click', function() {
    setLoading(true); // Mostrar GIF de carga
    toggleRecordingButtons(true); // Ocultar el botón de grabar y mostrar el de detener
    fetch('/record', { method: 'POST' })
    .then(() => {
        setLoading(false); // Ocultar GIF de carga
        recordingInterval = setInterval(fetchTranscription, 20000); // Cada 20 segundos
    })
    .catch(error => {
        setLoading(false); // Ocultar GIF de carga en caso de error
        toggleRecordingButtons(false);
        console.error('Error:', error);
    });
});

document.getElementById('stop-btn').addEventListener('click', function() {
    setLoading(false); // Ocultar GIF de carga
    toggleRecordingButtons(false); // Mostrar el botón de grabar y ocultar el de detener
    clearInterval(recordingInterval); // Detener el intervalo de solicitud de transcripciones
    // Aquí se debe implementar la lógica para detener la grabación en el backend
    fetch('/stop_record', { method: 'POST' })
    .catch(error => console.error('Error al detener la grabación:', error));
});

function fetchTranscription() {
    fetch('/get_transcription')
    .then(response => response.json())
    .then(data => {
        if (data.transcript) {
            let currentText = document.getElementById('transcription-result').textContent;
            document.getElementById('transcription-result').textContent = currentText + data.transcript;
        }
    })
    .catch(error => console.error('Error:', error));
}
