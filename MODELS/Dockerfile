FROM nvidia/cuda:12.1.0-base-ubuntu20.04
RUN apt update 
RUN apt-get install -y python3 python3-pip
WORKDIR usr/src/KPO
COPY requirements.txt .
#RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U spacy[cuda121]
RUN python3 -m spacy download en_core_web_trf


COPY . .


#EXPOSE 8000
#CMD gunicorn -w 4 -b 0.0.0.0:8000 wsgi:server
