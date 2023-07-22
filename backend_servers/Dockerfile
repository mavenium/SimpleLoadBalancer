FROM python:3.9
LABEL MAINTAINER = "Mahdi Namaki | mavenium@gmail.com"

ENV PYTHONUNBUFFERD 1

RUN mkdir /app
WORKDIR /app
COPY src/app.py /app/app.py

ADD ./requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --upgrade -r requirements.txt

CMD ["python", "/app/app.py"]