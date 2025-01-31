FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt --break-system-packages # venv prob better in long run but that is the point of docker so...

# set root directory for project
WORKDIR /app

# copy everything into the image
COPY . .

CMD ["gunicorn", "--bind=0.0.0.0:5000","--error-logfile=-","--access-logfile=-","--log-level=Debug","app:app"]
