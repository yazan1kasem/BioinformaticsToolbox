# funktioniert... manchmal
FROM python:3.9

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

#   Port 8081 wird für die Anwendung freigegeben, weil 8000 nicht funktionieren will
EXPOSE 8082

#   python -m uvicorn main:app --reload --port 8081 zum Starten der Anwendung, weil unicorn nicht im PATH ist
#   fastapi run app/main.py --port 8081
CMD ["fastapi", "run", "app/main.py", "--port", "8082"]
