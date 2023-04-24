FROM python:3.8-slim-buster
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8080

ENV FLASK_ENV=production
CMD ["python3", "."]