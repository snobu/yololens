# YoloLens

## A Python wrapper over Darknet Yolo v3

![screenshot](screenshot.png)

* Frontend lovingly stolen from Sarah Drasner (https://codepen.io/sdras/pen/dZOdpv), [object File] bug included.
* Code contributions into frontend by [Radu Matei](https://github.com/radu-matei).
* Branding by [Bojan Vrhovnik](https://github.com/bojanv)
* Uses the [Yolo v3](https://pjreddie.com/darknet/yolo/) model with default weights

Docker Hub: https://hub.docker.com/r/adcaline/yololens/

Builds with GPU support (CUDA 8.0, Tesla M60 and higher, could work on K80 as well).
GPU nodes in AKS can't yet do CUDA 9.0+ (stale/stable? drivers).
