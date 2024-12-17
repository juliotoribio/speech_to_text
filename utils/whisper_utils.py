import whisper

# Cargar el modelo de Whisper
model = whisper.load_model("base")

def transcribe_audio(file_path):
    """Transcribir audio con Whisper."""
    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        raise Exception(f"Error al transcribir el archivo: {str(e)}")