import os


class YoloDebug:
    DEBUG = 0
    if 'DEBUG' in os.environ:
        if os.environ['DEBUG'] == 1: DEBUG = 1