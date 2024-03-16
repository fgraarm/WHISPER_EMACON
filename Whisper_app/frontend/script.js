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
        document.getElementById('recording-gif').style.display = 'block'; // Mostrar el GIF de grabación

    
    toggleRecordingButtons(true); // Ocultar el botón de grabar y mostrar el de detener
     // Capturar el modelo y el lenguaje seleccionados
    const model = document.getElementById('model-select').value;
    const language = document.getElementById('language-input').value; // Correcto según tu HTML


    // Preparar el cuerpo de la solicitud
    const requestBody = {
        model: model,
        language: language
    };
     fetch('/record', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // Asegurándose de que el servidor sabe que estás enviando JSON
        },
        body: JSON.stringify(requestBody) // Convertir los datos del formulario a JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(() => {
        setLoading(false); // Ocultar GIF de carga
        recordingInterval = setInterval(fetchTranscription, 20000); // Cada 20 segundos
    })
    .catch(error => {
       document.getElementById('recording-gif').style.display = 'none'; // Asegúrate de ocultar el GIF si hay un error
        toggleRecordingButtons(false);
        console.error('Error:', error);
    });
});

document.getElementById('stop-btn').addEventListener('click', function() {
        document.getElementById('recording-gif').style.display = 'none'; // Ocultar el GIF de grabación
    toggleRecordingButtons(false); // Mostrar el botón de grabar y ocultar el de detener
    clearInterval(recordingInterval); // Detener el intervalo de solicitud de transcripciones
    fetch('/stop_record', { method: 'POST' })  // Asegúrate de que este es el endpoint correcto
    .then(response => {
        console.log('Recording stopped successfully');
    })
    .catch(error => console.error('Error al detener la grabación:', error));
});
document.getElementById('translate-btn').addEventListener('click', function() {
    const transcription = document.getElementById('transcription-result').textContent;
    const sourceLang = document.getElementById('source-lang-select').value; // Asumiendo que tienes este selector
    const targetLang = document.getElementById('target-lang-select').value;
    
    fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            text: transcription,
            source_lang: sourceLang, // Envía el idioma de origen
            target_lang: targetLang,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Asegúrate de acceder a la propiedad correcta de la respuesta JSON para obtener el texto traducido
        document.getElementById('translation-result').textContent = data.translation; // Ajustado para usar data.translation
    })
    .catch(error => console.error('Error:', error));
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
