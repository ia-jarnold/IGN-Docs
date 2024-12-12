FROM python:3.12

# set root directory for project
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# copy everything into the image
COPY . .

# build docs using containers env..this is the only place to build source from webservice exposes a route and volume to maintain this.
#RUN cd docs && \
#    make html

CMD ["gunicorn", "-b 0.0.0.0:5000", "app:app"]
