FROM python:2.7
#RUN git clone https://github.com/sushantmimani/reverse-proxy.git
ADD . reverse-proxy
WORKDIR reverse-proxy
RUN pip install --user -r requirements.txt
