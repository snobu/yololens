FROM nvidia/cuda:8.0-cudnn7-devel-ubuntu16.04

RUN apt update -qq && \
    apt install -qqy software-properties-common && \
    add-apt-repository ppa:jonathonf/python-3.6 && \
    apt update -qq && \
    apt install -qqy python3.6 python3.6-dev curl git nginx

RUN curl -Os https://bootstrap.pypa.io/get-pip.py && \
    python3.6 get-pip.py

RUN pip3.6 install setuptools colorama simplejson falcon gunicorn

RUN git clone --depth 1 https://github.com/snobu/azure-documentdb-python && \
    cd azure-documentdb-python && python3.6 -m easy_install .

RUN mkdir -p /app
RUN mkdir -p /app/frontend/results /app/frontend/uploads

COPY api/ /app/api
COPY api/data/ /app/data
COPY api/libdarknet/ /app/api/libdarknet
COPY frontend/ /app/frontend
# COPY frontend-vnext/dist /app/frontend-vnext
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
ENTRYPOINT ["/bin/sh", "/app/bootstrap.sh"]

EXPOSE 80
