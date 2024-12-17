import os

# Configuración de la carpeta de grabaciones
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'recordings')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)