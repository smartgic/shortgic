FROM python:3.9

LABEL vendor=Smartgic.io \
    io.smartgic.maintainer="Gaëtan Trellu <gaetan.trellu@smartgic.io>"

RUN pip install fastapi uvicorn sqlalchemy

EXPOSE 8000

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
