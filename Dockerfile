FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    pip install --upgrade pip setuptools && \
    apt-get install -y git && \
    apt-get install -y nginx

# We copy this file first to leverage docker cache

WORKDIR /

COPY . /ogcpywps

# Install OgcService
RUN git clone https://github.com/fderue/ogcservice.git
RUN pip install ./ogcservice

# Install pywps
RUN git clone -b ogc-TIE6 https://github.com/crim-ca/pywps.git

RUN pip install -r /pywps/requirements.txt
RUN pip install /pywps


RUN pip install -e /ogcpywps 
RUN mkdir -p /var/ogc/pywps /var/ogc/pywps/outputs /var/ogc/pywps/tmp

COPY ogcpywps.conf /etc/nginx/conf.d/ogcpywps.conf

CMD ["bash", "-c", "nginx && gunicorn -b 127.0.0.1:28095 --paste /ogcpywps/production.ini"]