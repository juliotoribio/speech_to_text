import os
import subprocess

def convert_to_wav(input_path):
    """Convertir a WAV usando FFmpeg."""
    output_path = input_path.rsplit(".", 1)[0] + ".wav"
    try:
        subprocess.run(
            ["ffmpeg", "-i", input_path, "-ar", "16000", "-ac", "1", output_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return output_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error al convertir el archivo: {e.stderr.decode()}")

def clean_files(*paths):
    """Eliminar archivos temporales."""
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

            