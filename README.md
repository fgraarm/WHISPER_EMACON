Instrucciones de Instalación
Pre-requisito: Instalación de FFmpeg

Descarga de FFmpeg:

Visita el sitio web oficial de FFmpeg.
Haz clic en el enlace "Windows builds from gyan.dev" para acceder a la página de descargas.
Selecciona y descarga "ffmpeg-git-full.7z" para la versión completa o "ffmpeg-git-essentials.7z" para la versión esencial.
Extracción de FFmpeg:

Utiliza un extractor de archivos compatible con .7z (p.ej., 7-Zip) para extraer el contenido del archivo descargado.
Agregar FFmpeg al PATH:

Navega a la subcarpeta bin dentro de la carpeta extraída y copia la ruta completa.
Añade esta ruta al PATH a través de las variables de entorno en la configuración del sistema.
Verificación de la Instalación:

Abre CMD o PowerShell y ejecuta ffmpeg -version para confirmar que FFmpeg ha sido instalado correctamente.
Configuración del Entorno para Whisper-dep:

Instalación de Dependencias:

Asegúrate de que Ffmpeg esté instalado siguiendo las instrucciones anteriores.
Coloca la carpeta Whisper-dep en el directorio deseado dentro de un entorno virtualizado (p.ej., usando Anaconda).
Instala las librerías requeridas utilizando PIP. Puedes encontrar el archivo requirements.txt dentro de /Backend para una instalación rápida.
pip install -U Flask openai-whisper sounddevice soundfile Transformers sentencepiece sacremoses pyannote.audio pyinstaller
Nota: Si encuentras conflictos de dependencias (p.ej., con noisereduce), asegúrate de instalar las librerías faltantes (librosa, matplotlib, scipy).

Instalación de Whisper:

Requiere Git en Windows: pip install git+https://github.com/openai/whisper.git
Para forzar la reinstalación sin dependencias: pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
Compilación de la Aplicación (.exe):

Ajusta los caminos según tu usuario y dominio virtual. 
Utiliza PyInstaller para compilar: pyinstaller -F --icon "C:\Users\fgraa\Desktop\EMAD-WHISPER.ico" ^ --add-data "C:\Users\fgraa.conda\envs\Whisper_DIVESTRA17JUL_BETA\Lib\site-packages\whisper;whisper" ^ --add-data "C:\Users\fgraa.conda\envs\Whisper_DIVESTRA17JUL_BETA\Lib\site-packages\lightning_fabric\version.info;lightning_fabric" ^ --add-data "frontend/templates;frontend/templates" ^ --add-data "frontend/static;frontend/static" ^ --add-data "C:\Users\fgraa.conda\envs\Whisper_DIVESTRA17JUL_BETA\Lib\site-packages\pyannote;pyannote" ^ --add-data "C:\Users\fgraa.conda\envs\Whisper_DIVESTRA17JUL_BETA\Lib\site-packages\pytorch_metric_learning;pytorch_metric_learning" ^ --add-data "C:\Users\fgraa.conda\envs\Whisper_DIVESTRA17JUL_BETA\Lib\site-packages\sklearn;sklearn" ^ --add-data "C:\Users\fgraa.conda\envs\Whisper_DIVESTRA17JUL_BETA\Lib\site-packages\asteroid_filterbanks;asteroid_filterbanks" ^ --hidden-import=pytorch_metric_learning.losses ^ --hidden-import=pytorch_metric_learning.miners ^ --hidden-import=pytorch_metric_learning.distances ^ --hidden-import=pytorch_metric_learning.reducers ^ --hidden-import=pytorch_metric_learning.utils.common_functions ^ --hidden-import=sklearn.utils._typedefs ^ --hidden-import=sklearn.utils._heap ^ --hidden-import=sklearn.utils._random ^ --hidden-import=sklearn.utils._param_validation ^ --hidden-import=whisper ^ --hidden-import=pyannote ^ --hidden-import=torchvision ^ --hidden-import=torchaudio ^ backend/app.py



Tras completar la instalación, el servidor web estará disponible en localhost:5000.
Funcionamiento General
Interfaz de Usuario (Frontend):

Proporciona controles para seleccionar el modelo de transcripción, subir archivos de audio, y más.
Script de Cliente (JavaScript):

Maneja la lógica del lado del cliente para enviar solicitudes al servidor y actualizar la interfaz con los resultados.
Servidor Backend (Flask en Python):

Procesa solicitudes de transcripción, diarización, grabación en tiempo real, y traducción.
Integración de Whisper para Transcripción (Python):

Utiliza el modelo Whisper para transcribir audio a texto.
Diarización de Hablantes (Python):

Emplea pyannote.audio para identificar quién habla en un segmento de audio.
Grabación de Audio en Tiempo Real (Python):

Maneja la grabación desde el micrófono y encola los segmentos de audio para su transcripción




