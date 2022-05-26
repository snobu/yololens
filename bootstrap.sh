#!/bin/bash

WEIGHTS=/mnt/weights/yolov3.weights

if [ ! -f $WEIGHTS ]; then
   echo "File $WEIGHTS not found. Downloading from blob storage..."
   curl -Ss -o $WEIGHTS \
        https://yololens.blob.core.windows.net/weights/yolov3.weights
fi

ln -vsf /mnt/weights/yolov3.weights /app/api/libdarknet/yolov3.weights

echo Staring nginx and gunicorn...
nginx -c /app/nginx.conf && gunicorn app:api -b 127.0.0.1
