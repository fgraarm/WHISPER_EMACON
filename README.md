Esta es la version 1 de la herramienta WHISPER para el EMACON, esta herramienta deberia ser capaz de importar archivos de audio o grabar en tiempo real y devolver la transcripcion al usuario
Ademas cuenta con una serie de modelos de lenguaje de Huggingface que permiten traducir la transcripcion, se pueden añadir mas
Si no se tiene GPU es recomendable no utilizar más allá de medium para archivos importados.

INSTRUCCIONES INSTALACION:

Ffmpeg debe estar instalado
Colocar la carpeta Whisper-dep (whisper depurado) donde se desee
en un entorno virtualizado con anaconda por ejemplo instalar las siguientes librerias , todas con PIP
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

pip install –U pyinstaller, para compilar la aplicación en .exe
Desde raíz: pyinstaller -F --add-data "C:\Users\fgraa\.conda\envs\Whisperdepurado\Lib\site-packages\whisper;whisper" --add-data "frontend/templates;frontend/templates" --add-data "frontend/static;frontend/static" backend/app.py
Se debe ajustar la ubicacion de la liberia de whisper instalada.

El ejecutable se lleva whisper y todas las librerias necesarias, ya no hace falta el entorno virtual.

PROXIMAS ACTUALIZACIONES: DIARIZACION, ELIMINACION RUIDO....