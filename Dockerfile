FROM nvidia/cuda:8.0-cudnn7-devel-ubuntu16.04

RUN apt update -qq && \
    apt install -qqy python3 python3-pip python3-dev curl git nginx && \
    pip3 install setuptools colorama simplejson falcon gunicorn

RUN mkdir -p /app
RUN mkdir -p /app/frontend/results /app/frontend/uploads

COPY api/ /app/api
COPY api/data/ /app/data
COPY api/libdarknet/ /app/api/libdarknet
COPY frontend/ /app/frontend
COPY bootstrap.sh /app/
COPY LICENSE /app/
COPY Makefile.patch /app/
COPY nginx.conf /app/

RUN git clone --depth 1 https://github.com/pjreddie/darknet
WORKDIR darknet
RUN patch -p1 Makefile < /app/Makefile.patch && \
    echo '\n\nCompiling Darknet53 (Yolov3) with CUDA...\n' && \
    make && \
    echo '______ libdarknet (with CUDA) ______' && \
    echo 'ldd: ' && \
    du -sh libdarknet.so && \
    ldd libdarknet.so && \
    echo '____________________________________' && \
    cp -v libdarknet.so /app/api/libdarknet/

WORKDIR /app/api
CMD /app/bootstrap.sh

EXPOSE 80