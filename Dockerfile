FROM python:3.7        ##Create base image
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y python && pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app