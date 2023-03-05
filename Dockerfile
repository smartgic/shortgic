FROM python:3.11-alpine

LABEL vendor="smartgic.io"
LABEL source="https://github.com/smartgic/mqtt-client"
LABEL authors="Gaëtan Trellu <gaetan.trellu@smartgic.io>"
LABEL title="Smart'Gic shortener URL"
LABEL description="Simple URL shortener using FastAPI, SQLAlchemy and SQLite"

RUN addgroup -g 1000 shortgic && \
    adduser --shell /sbin/nologin --disabled-password \
    --uid 1000 --ingroup shortgic shortgic && \
    mkdir -m 700 /db && \
    chown shortgic:shortgic /db

USER shortgic

ENV PATH="$PATH:/home/shortgic/.local/bin"

COPY --chown=shortgic:shortgic requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=shortgic:shortgic app/ /app

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
