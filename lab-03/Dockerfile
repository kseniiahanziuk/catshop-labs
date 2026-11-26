FROM python:3.12-slim-bookworm

RUN useradd --uid 10001 app && mkdir /data && chown app /data

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV PYTHONUNBUFFERED=1 COUNTER_FILE=/data/visits.txt PORT=8080

USER 10001

EXPOSE 8080

CMD ["python", "app.py"]
