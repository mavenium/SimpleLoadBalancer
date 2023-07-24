FROM python:3.9
LABEL MAINTAINER = "Mahdi Namaki | mavenium@gmail.com"

ENV PYTHONUNBUFFERD 1

RUN mkdir /app
WORKDIR /app
COPY ../src/main.py /app

CMD ["python", "/app/main.py"]