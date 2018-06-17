import sys, os
import darknet as dn
import simplejson as json

def detect(filename, outfile):
    print('detect() has been called.')
    result = dn.detect(net, meta, filename, outfile)
    return json.dumps(result)

# Init GPU (if support compiled in libdarknet) and load model
dn.set_gpu(0)
net = dn.load_net(b"libdarknet/yolov3.cfg", b"libdarknet/yolov3.weights", 0)
meta = dn.load_meta(b"libdarknet/coco.data")
