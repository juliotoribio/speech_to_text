from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER
from utils.file_utils import convert_to_wav, clean_files
from utils.whisper_utils import transcribe_audio
import os
import logging

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)

# Inicialización de Flask
app = Flask(__name__)

# Verificar que UPLOAD_FOLDER exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    logging.info(f"Directorio {UPLOAD_FOLDER} creado.")

@app.route("/")
def index():
    """Renderiza la página principal."""
    return render_template("index.html")

@app.route("/upload-recording", methods=["POST"])
def upload_recording():
    """Procesa los archivos grabados desde el navegador."""
    file = request.files.get("audio")
    if not file:
        logging.error("No se envió ningún archivo.")
        return jsonify({"error": "No se envió ningún archivo"}), 400

    # Guardar el archivo temporalmente
    input_path = os.path.join(UPLOAD_FOLDER, "recording.webm")
    try:
        file.save(input_path)
        logging.info(f"Archivo guardado temporalmente en {input_path}")

        # Convertir a WAV y transcribir
        output_path = convert_to_wav(input_path)
        logging.info(f"Archivo convertido a WAV: {output_path}")

        text = transcribe_audio(output_path)
        logging.info("Transcripción completada.")

        return jsonify({"text": text})
    except Exception as e:
        logging.error(f"Error procesando grabación: {str(e)}")
        return jsonify({"error": f"Error procesando grabación: {str(e)}"}), 500
    finally:
        # Limpieza de archivos temporales
        if os.path.exists(input_path):
            os.remove(input_path)
            logging.info(f"Archivo temporal eliminado: {input_path}")
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)
            logging.info(f"Archivo convertido eliminado: {output_path}")

@app.route("/upload-file", methods=["POST"])
def upload_file():
    """Procesa archivos subidos como MP3, WAV, etc."""
    file = request.files.get("file")
    if not file:
        logging.error("No se envió ningún archivo.")
        return jsonify({"error": "No se envió ningún archivo"}), 400

    # Validar extensiones permitidas
    extension = file.filename.rsplit(".", 1)[-1].lower()
    if extension not in {"mp3", "wav", "m4a", "flac"}:
        logging.error("Formato no soportado.")
        return jsonify({"error": "Formato no soportado"}), 400

    # Guardar el archivo temporalmente
    input_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    try:
        file.save(input_path)
        logging.info(f"Archivo guardado temporalmente en {input_path}")

        # Convertir a WAV si es necesario y transcribir
        output_path = input_path
        if extension != "wav":
            output_path = convert_to_wav(input_path)
            logging.info(f"Archivo convertido a WAV: {output_path}")

        text = transcribe_audio(output_path)
        logging.info("Transcripción completada.")

        return jsonify({"text": text})
    except Exception as e:
        logging.error(f"Error procesando archivo: {str(e)}")
        return jsonify({"error": f"Error procesando archivo: {str(e)}"}), 500
    finally:
        # Limpieza de archivos temporales
        if os.path.exists(input_path):
            os.remove(input_path)
            logging.info(f"Archivo temporal eliminado: {input_path}")
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)
            logging.info(f"Archivo convertido eliminado: {output_path}")

if __name__ == "__main__":
    app.run(debug=True)