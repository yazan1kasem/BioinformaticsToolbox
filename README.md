# Bioinformatics Toolbox – Containerisierte Werkzeuge für Sequenzanalyse

## Projektbeschreibung

Die **Bioinformatics Toolbox** ist eine containerisierte Anwendung zur Analyse biologischer Sequenzdaten. Sie vereint klassische bioinformatische Methoden wie Multiple Sequence Alignment (MSA), phylogenetische Baumgenerierung und FASTA-Verarbeitung in einer modularen Struktur. Die Anwendung nutzt Python, ist Docker-kompatibel und über eine Weboberfläche zugänglich.

Dieses Projekt wurde für Ausbildungs- und Forschungszwecke entwickelt und kann lokal oder serverseitig bereitgestellt werden.

---

## Hauptfunktionen

### 1. Multiple Sequence Alignment (MSA)
Die Toolbox ermöglicht das Einlesen mehrerer FASTA-Sequenzen und führt ein MSA durch. Ziel ist es, evolutionäre Verwandtschaften, konservierte Regionen und Mutationen zu analysieren.

### 2. Phylogenetischer Baum
Basierend auf den Alignments wird ein phylogenetischer Baum erzeugt. Die Darstellung erfolgt als Grafik, die die evolutionäre Nähe visualisiert.

### 3. FASTA-Datei-Verarbeitung
Benutzer können eigene FASTA-Dateien hochladen. Das System erkennt und extrahiert Sequenzinformationen automatisch und stellt diese zur weiteren Analyse bereit.

### 4. Webbasierte Benutzeroberfläche
Eine einfache HTML-basierte GUI (über Flask Templates) ermöglicht Uploads, Auswahl von Funktionen und Visualisierung der Ergebnisse.

### 5. Ordnerstruktur mit Uploads
Im Upload-Verzeichnis werden Benutzerdateien abgelegt, geparst und je nach Funktion in den Analysefluss eingebunden.

---

## Docker & Containerstruktur

Das gesamte Projekt ist dockerisiert. Die `docker-compose.yml` orchestriert die Umgebung und startet den Webserver sowie alle notwendigen Services.

### docker-compose.yml

```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
```

### Dockerfile

```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "manage.py"]
```

- **`build: .`** – verwendet den lokalen Ordner zum Bauen des Containers
- **`volumes`** – ermöglicht Änderungen am Code ohne Rebuild
- **`FLASK_ENV=development`** – sorgt für automatisches Neuladen
- **`manage.py`** – zentraler Einstiegspunkt zum Start der Webanwendung

---

## Projektstruktur

```
BioinformaticsToolbox/
├── msa3/                      → MSA-Logik
├── phylogenetischen Baums/   → Phylogenie-Funktionen
├── sequencetools/            → FASTA-Verarbeitung
├── uploads/                  → Benutzerdateien
├── templates/                → HTML-Templates
├── containerfiles/           → Docker- und Build-Dateien
├── db.sqlite3                → Lokale Datenbank
├── docker-compose.yml        → Multi-Service-Konfiguration
├── Dockerfile                → Container-Builddefinition
├── manage.py                 → Haupt-Entry-Point (Flask App)
├── requirements.txt          → Python-Abhängigkeiten
```

---

## Ausführung

1. Repository klonen  
   ```bash
   git clone https://github.com/yazan1kasem/BioinformaticsToolbox.git
   cd BioinformaticsToolbox
   ```

2. Anwendung mit Docker starten  
   ```bash
   docker-compose up --build
   ```

3. Webanwendung aufrufen  
   ```
   http://localhost:5000
   ```

---

## Lizenz

Dieses Projekt ist für Bildungs- und Forschungszwecke lizenziert. Für die kommerzielle Nutzung ist die Zustimmung des Autors erforderlich.
