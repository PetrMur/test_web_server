FROM python:3.8-slim

ENV TZ=Europe/Moscow

RUN apt-get -y update && apt-get -y -f install git python3-pip bash mc

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 5000/tcp

ENV PORT 5000
CMD ["python", "start_application.py"]