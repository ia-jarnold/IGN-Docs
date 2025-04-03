FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    python3.12 \
    python3-pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt --break-system-packages # venv prob better in long run but that is the  point of docker so...like could package everything in venv and just put this app in requirements...I wonder if this is related to the lil gunicorn bug....basically have to refresh a bit.

# set root directory for project
WORKDIR /app

# copy everything into the image
COPY . .

CMD ["gunicorn", "--bind=0.0.0.0:5000","--timeout=500","--error-logfile=-","--access-logfile=-","--log-level=Debug","app:app"]
