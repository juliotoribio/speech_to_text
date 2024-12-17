#!/bin/bash
pip install gunicorn  # Fuerza instalación por si falla
gunicorn app:app --bind 0.0.0.0:$PORT