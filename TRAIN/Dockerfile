FROM nvidia/cuda:12.1.0-base-ubuntu20.04
RUN apt update 
RUN apt-get install -y python3 python3-pip
RUN apt-get update 
RUN apt-get upgrade -y 
RUN apt-get install -y git
WORKDIR usr/src/TRAIN
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
