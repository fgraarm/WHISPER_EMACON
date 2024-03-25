Esta es la version 1 de la herramienta WHISPER para el EMACON, esta herramienta deberia ser capaz de importar archivos de audio o grabar en tiempo real y devolver la transcripcion al usuario
Ademas cuenta con una serie de modelos de lenguaje de Huggingface que permiten traducir la transcripcion, se pueden añadir mas
Si no se tiene GPU es recomendable no utilizar más allá de medium para archivos importados.

INSTRUCCIONES INSTALACION:

Ffmpeg debe estar instalado (VER INSTRUCCIONES ABAJO)

Colocar la carpeta Whisper-dep (whisper depurado) donde se desee
en un entorno virtualizado con anaconda por ejemplo instalar las siguientes librerias , todas con PIP
El archivo requirements.txt está disponible dentro de /Backend para la instalacion rapida de las librerias necesarias
si se hace paso por paso
0. pip install -U Flask
1. pip install -U openai-whisper  
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
noisereduce 3.0.0 requires librosa, which is not installed.
noisereduce 3.0.0 requires matplotlib, which is not installed.
noisereduce 3.0.0 requires scipy, which is not installed.
4. pip install git+https://github.com/openai/whisper.git  (Requiere instalar previamente Git en windows)
5. pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
6. pip install -U sounddevice 
7. pip install –U soundfile
8. pip install -U Transformers
9. pip install -U sentencepiece
10. pip install –U sacremoses
11. pip install -U pyannote.audio  DIARIZACION

pip install –U pyinstaller, para compilar la aplicación en .exe
Desde raíz:////AJUSTAR SEGUN USUARIO Y NOMBRE DE DOMINIO VIRTUAL//// pyinstaller -F --icon "C:\Users\fgraa\Desktop\emad_whisper_jR8_icon.ico" --add-data "C:\Users\fgraa\.conda\envs\Whisperdepurado_20240325\Lib\site-packages\whisper;whisper" --add-data "C:\Users\fgraa\.conda\envs\Whisperdepurado_20240325\Lib\site-packages\lightning_fabric\version.info;lightning_fabric" --add-data "frontend/templates;frontend/templates" --add-data "frontend/static;frontend/static" --add-data "C:\Users\fgraa\.conda\envs\Whisperdepurado_20240325\Lib\site-packages\pyannote;pyannote" --add-data "C:\Users\fgraa\.conda\envs\Whisperdepurado_20240325\Lib\site-packages\pytorch_metric_learning;pytorch_metric_learning" --add-data "C:\Users\fgraa\.conda\envs\Whisperdepurado_20240325\Lib\site-packages\sklearn;sklearn" --add-data "C:\Users\fgraa\.conda\envs\Whisperdepurado_20240325\Lib\site-packages\asteroid_filterbanks;asteroid_filterbanks” backend/app.py




Se debe ajustar la ubicacion de la liberia de whisper instalada. en mi caso use conda

El ejecutable se lleva whisper y todas las librerias necesarias, ya no hace falta el entorno virtual.

EL SERVIDOR WEB SE LEVANTA AL POCO TIEMPO EN LOCALHOST:5000

FUNCIONAMIENTO GENERAL
1. Interfaz de Usuario (Frontend)
La interfaz de usuario, definida en usoherramienta.html, proporciona controles para:

Seleccionar un modelo de transcripción y especificar un idioma (opcional).
Subir archivos de audio para la transcripción.
Iniciar y detener la grabación de audio en tiempo real.
Traducir el texto transcrito a otro idioma.
2. Script de Cliente (JavaScript)
El archivo script.js maneja la lógica del lado del cliente, incluyendo:

Mostrar y ocultar elementos de la interfaz durante la carga, la grabación, y la traducción.
Enviar solicitudes al servidor para transcribir audio, iniciar/detener grabaciones, y traducir texto.
Actualizar la interfaz con los resultados de transcripciones, diarizaciones, y traducciones.
3. Servidor Backend (Flask en Python)
El archivo app.py define un servidor Flask que maneja las solicitudes del cliente, incluyendo:

Transcripción y Diarización: Recibe archivos de audio, los procesa utilizando los módulos whisper_integration.py y diarization.py, y devuelve los resultados al cliente.
Grabación en Tiempo Real: Inicia y detiene la grabación de audio mediante audio_recording.py, transcribe el audio grabado, y permite consultar las transcripciones acumuladas.
Traducción: Utiliza una pipeline de Hugging Face Transformers para traducir texto entre idiomas soportados.
4. Integración de Whisper para Transcripción (Python)
El archivo whisper_integration.py utiliza el modelo Whisper de OpenAI para transcribir audio a texto. Puede configurarse con diferentes modelos (tiny, base, etc.) y admite la especificación de un idioma.

5. Diarización de Hablantes (Python)
diarization.py emplea la biblioteca pyannote.audio para la diarización, es decir, identificar cuándo y quién habla en un segmento de audio. Posteriormente, utiliza Whisper para transcribir los segmentos identificados por hablante.

6. Grabación de Audio en Tiempo Real (Python)
audio_recording.py maneja la grabación de audio desde el micrófono utilizando sounddevice, guarda los segmentos de audio temporalmente y los encola para su transcripción. También proporciona la funcionalidad para iniciar y detener la grabación, y para recuperar las transcripciones acumuladas.

Flujo de Trabajo General
Inicio de la Aplicación: El usuario interactúa con la interfaz web para subir archivos de audio, iniciar la grabación en tiempo real, o introducir texto para traducir.
Procesamiento del Servidor: Las solicitudes son enviadas al servidor Flask, donde son procesadas según el tipo de solicitud (transcripción, diarización, grabación en tiempo real, traducción).
Respuesta al Cliente: Los resultados del procesamiento (transcripciones, diarizaciones, traducciones) son enviados de vuelta al cliente y mostrados en la interfaz.
Este sistema integrado permite una interacción fluida entre el usuario y las capacid

INSTRUCCIONES INSTALACION FFMPEG: 
Paso 1: Descargar FFmpeg
Ve al sitio web oficial de FFmpeg.
Haz clic en el enlace de "Windows builds from gyan.dev" para ir a la página de descargas.
Selecciona una versión para descargar. Por lo general, encontrarás una sección llamada "git" que contiene las últimas versiones. Haz clic en el enlace que dice "ffmpeg-git-full.7z" o "ffmpeg-git-essentials.7z". La versión "full" incluye todas las características, mientras que "essentials" tiene menos dependencias y podría ser suficiente para la mayoría de los usuarios.
Guarda el archivo .7z en tu computadora.
Paso 2: Extraer FFmpeg
Necesitarás un extractor de archivos que pueda manejar archivos .7z. Si no tienes uno, puedes descargar 7-Zip de forma gratuita.
Una vez que tengas un extractor de archivos, haz clic derecho en el archivo .7z que descargaste y selecciona "Extraer aquí" o "Extraer a ffmpeg-git-full/" (el nombre exacto puede variar dependiendo del archivo que hayas descargado).
Se creará una nueva carpeta que contiene FFmpeg.
Paso 3: Agregar FFmpeg al PATH
Abre la carpeta extraída y encuentra la subcarpeta bin. Dentro de esta carpeta, verás los ejecutables de FFmpeg, incluyendo ffmpeg.exe.
Haz clic en la barra de direcciones del Explorador de Windows y copia la ruta completa a la carpeta bin.
Abre el menú de Inicio, escribe "variables de entorno" y selecciona la opción "Editar las variables de entorno del sistema" o "Editar las variables de entorno para tu cuenta".
En la ventana del Sistema (o en la ventana de Propiedades del Sistema, dependiendo de tu versión de Windows), haz clic en "Variables de entorno...".
Bajo "Variables del sistema" (para todos los usuarios) o "Variables de usuario" (solo para tu usuario), busca la variable Path y selecciónala.
Haz clic en "Editar...".
En la ventana de edición, haz clic en "Nuevo" y pega la ruta a la carpeta bin de FFmpeg que copiaste antes.
Haz clic en "Aceptar" en todas las ventanas para cerrarlas y aplicar los cambios.
Paso 4: Verificar la Instalación
Abre una nueva ventana de la línea de comandos (CMD) o PowerShell.
Escribe ffmpeg -version y presiona Enter. Si ves la versión de FFmpeg y la configuración de compilación, la instalación fue exitosa y FFmpeg está correctamente añadido al PATH

