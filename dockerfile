FROM python:3.11-slim

WORKDIR /app

COPY app.py /app/
# Fajl LOKACIJE.geojson NE kopiramo jer ćemo ga bindovati iz lokalnog foldera

RUN pip install --no-cache-dir fastapi uvicorn

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
