import os


class YoloDebug:
    if 'DEBUG' in os.environ:
        DEBUG = 1 if os.environ['DEBUG'] == 1 else 0