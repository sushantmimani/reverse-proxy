FROM python:2.7
ADD . reverse_proxy
WORKDIR reverse_proxy
RUN pip install --user -r requirements.txt
