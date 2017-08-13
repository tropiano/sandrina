FROM ubuntu:16.04
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r web/requirements.txt
ENTRYPOINT ["python"]
CMD ["web/app.py"]