# start.sh
# Script para iniciar la aplicación Flask con Gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT