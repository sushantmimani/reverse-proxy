FROM python:2.7
ADD . reverse-proxy
WORKDIR reverse-proxy
RUN pip install --user -r requirements.txt
