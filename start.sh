#!/bin/bash

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Ejecutar la aplicación con gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT