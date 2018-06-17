#FROM nvidia/cuda:9.2-cudnn7-devel-ubuntu16.04
FROM nvidia/cuda:8.0-cudnn7-devel-ubuntu16.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev curl git

RUN mkdir -p /app
RUN mkdir -p /app/frontend/results /app/frontend/uploads

COPY api/ /app/api
COPY api/data/ /app/data
COPY api/libdarknet/ /app/api/libdarknet
COPY frontend/ /app/frontend

COPY LICENSE /app/
COPY Makefile.patch /app/

RUN git clone --depth 1 https://github.com/pjreddie/darknet
WORKDIR darknet
RUN patch -p1 Makefile < /app/Makefile.patch

RUN  make && \
    echo '______ libdarknet ______' && \
    echo 'ldd: ' && \
    du -sh libdarknet.so && \
    ldd libdarknet.so && \
    echo '________________________' && \
    cp -v libdarknet.so /app/api/libdarknet/

RUN pip3 install setuptools colorama simplejson gunicorn

RUN git clone --depth 1 https://github.com/snobu/falcon
WORKDIR falcon
RUN python3 setup.py install

RUN echo Downloading weights.. && curl -s -o /app/api/libdarknet/yolov3.weights \
    http://yololens.blob.core.windows.net/weights/yolov3.weights

WORKDIR /app/api
CMD gunicorn app:api -b 0.0.0.0 2>&1

EXPOSE 8000
