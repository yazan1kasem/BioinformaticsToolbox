# Bioinformatics Toolbox – Containerisierte Werkzeuge für Sequenzanalyse

## Projektbeschreibung

Die **Bioinformatics Toolbox** ist eine modular aufgebaute, containerisierte Webanwendung **(DJANGO)** zur Analyse biologischer Sequenzdaten. Sie umfasst klassische bioinformatische Methoden wie Multiple Sequence Alignment (MSA), phylogenetische Baumkonstruktion, Open Reading Frame (ORF)-Suche sowie eine webbasierte Benutzeroberfläche zur Dateiverwaltung und Visualisierung.

Diese Anwendung ist vollständig mit Docker lauffähig und unterstützt etablierte Bioinformatiktools wie **MUSCLE**, **ClustalW** und **RAxML** über offizielle BioContainer-Images.

---

## Hauptfunktionen

### 1. Multiple Sequence Alignment (MSA)

Die Toolbox bietet automatisiertes MSA durch Containerintegration von:
- `MUSCLE` (Multiple Sequence Comparison by Log-Expectation)
- `ClustalW`

```text
Ziel: Identifikation konservierter Sequenzmuster und Erstellung evolutionärer Hypothesen.
```

![image](https://github.com/user-attachments/assets/876db3ba-5612-4e86-8d53-400a713763d7)
*Abbildung: MSA-Ansicht*

---

### 2. Phylogenetischer Baum

Mit Hilfe von **RAxML** (Randomized Axelerated Maximum Likelihood) wird ein phylogenetischer Baum auf Basis der MSA-Ergebnisse generiert und grafisch ausgegeben.

![image](https://github.com/user-attachments/assets/aca199ec-6ef8-45fa-8b03-eebc6de56c4a)
*Abbildung: FASTA-Eingabe*

![phylo_tree](https://github.com/user-attachments/assets/7c54f5af-1c9f-4546-89d2-8970e2e70cc8) 

*Abbildung: Ausgabe (Phylogenetischer Baum)*

---

### 3. FASTA-Datei-Verarbeitung

- Unterstützung für individuelle FASTA-Uploads
- Dynamische Erkennung von Sequenzstruktur
- Übergabe an ORF-, MSA- oder Phylogenie-Komponenten

---

### 4. ORF-Finder

Der integrierte ORF-Finder identifiziert potenzielle proteincodierende Bereiche auf beiden DNA-Strängen und in allen sechs Leserastern. Die Ausgabe enthält Position, Länge und Sequenz.

![image](https://github.com/user-attachments/assets/f223cde4-403f-4238-ad10-09d14342af2e)
*Abbildung: ORF-FINDER Ansicht*

---

### 5. Webbasierte Benutzeroberfläche

Die App nutzt Flask + HTML-Templates zur Dateiverwaltung, Analyseauswahl und grafischen Darstellung der Ergebnisse.

---

## Containerisierte Infrastruktur

### docker-compose.yml (verbessert)

```yaml
version: '3.9'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
    depends_on:
      - muscle
      - clustalw
      - phylo

  muscle:
    image: biocontainers/muscle:v1.3.8.1551-2-deb_cv1
    stdin_open: true
    tty: true
    command: sh
    volumes:
      - ./containerfiles:/containerfiles
    restart: unless-stopped

  clustalw:
    image: biocontainers/clustalw:v2.1lgpl-6-deb_cv1
    stdin_open: true
    tty: true
    command: sh
    volumes:
      - ./containerfiles:/containerfiles
    restart: unless-stopped

  phylo:
    image: biocontainers/raxml:v8.2.12dfsg-1-deb_cv1
    stdin_open: true
    tty: true
    volumes:
      - ./containerfiles:/containerfiles
    restart: unless-stopped
```

---

## Dockerfile

```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "manage.py"]
```

---

## Projektstruktur

```
BioinformaticsToolbox/
├── msa3/                    → MSA-Funktionen
├── phylogenie/             → Baumkonstruktion
├── orf/                    → ORF-Analyse
├── templates/              → Frontend-Vorlagen
├── uploads/                → Benutzer-Uploads
├── containerfiles/         → Gemeinsame Volumes
├── docker-compose.yml      → Multi-Service Definition
├── Dockerfile              → Container-Build der App
├── manage.py               → Einstiegspunkt
├── requirements.txt        → Python-Abhängigkeiten
```

---

## Anwendung starten

```bash
git clone https://github.com/yazan1kasem/BioinformaticsToolbox.git
cd BioinformaticsToolbox
docker-compose up --build
```

Im Browser öffnen: `http://localhost:5000`

---

## Lizenz

Dieses Projekt ist ausschließlich für Forschungs- und Ausbildungszwecke bestimmt. Die kommerzielle Nutzung bedarf der vorherigen Genehmigung des Autors.
