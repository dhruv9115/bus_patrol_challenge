#Deriving the latest base image
FROM python:3.9-slim-buster

EXPOSE 80

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY server/server.py /app
RUN python -m pip install -r requirements.txt
CMD ["python", "server.py"]
