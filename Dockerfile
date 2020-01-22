# Simple Docker image for Silvereye WPS demo

FROM python:3.7.6

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive

### WPS demo content ###

ADD . /etc/silvereye

WORKDIR /etc/silvereye

RUN pip install -e .
RUN python setup.py develop

RUN mkdir /pywps-log

CMD ["pserve", "development.ini", "--reload"]
