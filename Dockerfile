FROM python:3.10

WORKDIR usr/src/TCP_SERVER
COPY NLP_requirements.txt .
#RUN python3 -m pip install --upgrade pip
RUN pip install -r NLP_requirements.txt
RUN python3 -m spacy download en_core_web_trf
COPY . .

#EXPOSE 8000
#CMD gunicorn -w 4 -b 0.0.0.0:8000 wsgi:server
