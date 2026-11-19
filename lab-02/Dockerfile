FROM python:3.12-bookworm AS build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.12-slim-bookworm

RUN useradd --uid 10001 app \
 && mkdir /data \
 && chown app /data

COPY --from=build /opt/venv /opt/venv

WORKDIR /app
COPY app.py .

ENV PATH="/opt/venv/bin:$PATH" PYTHONUNBUFFERED=1 COUNTER_FILE=/data/visits.txt

USER 10001

EXPOSE 8080

CMD ["python", "app.py"]
