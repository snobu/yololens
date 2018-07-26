FROM nvidia/cuda:8.0-cudnn7-devel-ubuntu16.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev curl git nginx && \
    pip3 install --upgrade pip && \
    pip3 install setuptools colorama simplejson falcon gunicorn

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
RUN patch -p1 Makefile < /app/Makefile.patch && \
    make && \
    echo '______ libdarknet (with CUDA) ______' && \
    echo 'ldd: ' && \
    du -sh libdarknet.so && \
    ldd libdarknet.so && \
    echo '____________________________________' && \
    cp -v libdarknet.so /app/api/libdarknet/

RUN echo Downloading weights.. && curl -s -o /app/api/libdarknet/yolov3.weights \
    http://yololens.blob.core.windows.net/weights/yolov3.weights

WORKDIR /app/api
CMD $(ls /mnt/weights/yolov3.weights || curl -s -o /mnt/weights/yolov3.weights \
        http://yololens.blob.core.windows.net/weights/yolov3.weights) && \
        nginx -c /app/nginx.conf && gunicorn app:api -b 127.0.0.1

EXPOSE 80