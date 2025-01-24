FROM python:3.12

# set root directory for project
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# copy everything into the image
COPY . .

CMD ["gunicorn", "--bind=0.0.0.0:5000","--error-logfile=-","--access-logfile=-","--log-level=Debug","app:app"]
