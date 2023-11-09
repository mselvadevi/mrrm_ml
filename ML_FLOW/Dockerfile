FROM python:3.7-slim-buster


WORKDIR /mlflow/

COPY requirements.txt .
#RUN apt-get upgrade
#RUN pip install --no-cache-dir -r requirements.txt && \
#  rm requirements.txt

RUN apt-get update 
RUN  apt-get install -y software-properties-common lsb-release 
RUN  apt-get clean all 
RUN  wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null

#RUN apt-add-repository "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main"
RUN apt-get update 
RUN apt-get install -y build-essential libsnappy-dev libbrotli-dev libssl-dev zlib1g-dev liblz4-dev libzstd-dev libre2-dev  libbz2-dev 
RUN apt-get install -y cmake


RUN python -m pip install mlflow 
#RUN python -m  pip install --no-cache-dir -r requirements.txt 
EXPOSE 5000

ENV BACKEND_URI sqlite:////mlflow/mlflow.db
ENV ARTIFACT_ROOT /mlflow/artifacts

CMD mlflow server --backend-store-uri ${BACKEND_URI} --default-artifact-root ${ARTIFACT_ROOT} --host 0.0.0.0 --port 5000