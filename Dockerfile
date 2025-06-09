# Usa una base leggera con Python
FROM python:3.11-slim

# Imposta la working directory
WORKDIR /app

# Copia tutti i file del progetto (escludi venv e __pycache__)
COPY . .

# Installa Flask e dipendenze
RUN pip install --upgrade pip && pip install flask

# Espone la porta Flask
EXPOSE 5000

# Avvia l'app
CMD ["python", "app.py"]
