# Dockerfile für Django
FROM python:3.9-slim

# Arbeitsverzeichnis setzen
WORKDIR /code

# Abhängigkeiten installieren
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Projektdateien kopieren
COPY . /code/

# Entwicklungsserver starten
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
