FROM python:3.10

WORKDIR usr/src/web_client
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
#EXPOSE 8000
#CMD gunicorn -w 4 -b 0.0.0.0:8000 wsgi:server
